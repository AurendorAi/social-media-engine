"""Bounded public HTTPS reads. No credentials, cookies, proxies or private-network fetches."""
import http.client
import ipaddress
import json
import socket
import ssl
import time
from urllib.parse import urlsplit, urljoin, parse_qsl

from engine import EngineError, require

USER_AGENT = "SocialMediaEngine/2.1 (https://github.com/AurendorAi/social-media-engine)"


def public_url(url):
    require(isinstance(url, str) and 0 < len(url) <= 4096, "Use an explicit public HTTPS URL.")
    require(not any(ord(c) < 33 or ord(c) == 127 for c in url) and "\\" not in url, "Invalid URL characters.")
    try:
        parts = urlsplit(url)
        require(parts.scheme == "https" and parts.hostname and parts.port in (None, 443), "Only public HTTPS on port 443 is supported.")
        require(not parts.username and not parts.password and not parts.fragment, "URLs must not contain credentials or fragments.")
        sensitive = {"token", "access_token", "api_key", "apikey", "key", "signature", "sig", "x-amz-signature", "x-amz-credential", "x-goog-signature", "x-goog-credential"}
        require(not any(k.lower() in sensitive for k, _ in parse_qsl(parts.query)), "Use a stable public URL without authentication parameters; import authorized downloads locally.")
        host = parts.hostname.encode("idna").decode("ascii")
        require(host != "localhost" and not host.endswith((".localhost", ".local", ".internal")), "Private network URLs are not allowed.")
        return parts, host
    except (ValueError, UnicodeError) as exc:
        raise EngineError("Invalid HTTPS URL.") from exc


def public_addresses(host):
    try:
        addresses = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
    except OSError as exc:
        raise EngineError("Resource host could not be resolved.") from exc
    require(bool(addresses), "Resource host has no addresses.")
    for _, _, _, _, address in addresses:
        ip = ipaddress.ip_address(address[0])
        require(ip.is_global and not ip.is_multicast and not ip.is_reserved and not ip.is_unspecified,
                "Resource URL resolves to a non-public address.")
        if getattr(ip, "ipv4_mapped", None):
            require(ip.ipv4_mapped.is_global, "Resource URL resolves to a non-public address.")
    return addresses


class PublicConnection(http.client.HTTPSConnection):
    def connect(self):
        # Connect only to the exact IP addresses checked above: no DNS-rebinding gap.
        addresses = public_addresses(self.host)
        last = None
        for family, kind, proto, _, address in addresses[:4]:
            sock = socket.socket(family, kind, proto)
            try:
                sock.settimeout(self.timeout)
                sock.connect(address)
                self.sock = self._context.wrap_socket(sock, server_hostname=self.host)
                return
            except OSError as exc:
                last = exc
                sock.close()
        raise EngineError("Could not connect securely to the resource host.") from last


def fetch(url, max_bytes=20 * 1024 * 1024):
    deadline = time.monotonic() + 45
    for _ in range(5):
        require(time.monotonic() < deadline, "Resource download exceeded its time limit.")
        parts, host = public_url(url)
        connection = PublicConnection(host, timeout=8, context=ssl.create_default_context())
        try:
            target = parts.path or "/"
            if parts.query:
                target += "?" + parts.query
            connection.request("GET", target, headers={"User-Agent": USER_AGENT, "Accept-Encoding": "identity", "Accept": "*/*"})
            response = connection.getresponse()
            if response.status in (301, 302, 303, 307, 308):
                location = response.getheader("Location")
                require(location, "Redirect has no destination.")
                url = urljoin(url, location)
                continue
            require(response.status == 200, f"Resource service returned HTTP {response.status}. Try another source or use the host browser; no automatic retry was made.")
            length = response.getheader("Content-Length")
            require(length is None or 0 <= int(length) <= max_bytes, "Resource exceeds the download size limit.")
            require(response.getheader("Content-Encoding", "identity").lower() in ("", "identity"), "Compressed HTTP responses are not supported.")
            chunks, size = [], 0
            while True:
                require(time.monotonic() < deadline, "Resource download exceeded its time limit.")
                chunk = response.read(min(65536, max_bytes + 1 - size))
                if not chunk:
                    break
                size += len(chunk)
                require(size <= max_bytes, "Resource exceeds the download size limit.")
                chunks.append(chunk)
            require(size > 0, "Resource is empty.")
            if length is not None:
                require(size == int(length), "Resource download was incomplete.")
            return b"".join(chunks), response.getheader("Content-Type", "").split(";")[0].lower(), url
        except EngineError:
            raise
        except (OSError, ValueError, http.client.HTTPException) as exc:
            raise EngineError("Resource request failed or returned an incomplete response. Try the original source in your browser.") from exc
        finally:
            connection.close()
    raise EngineError("Resource exceeded the redirect limit.")


def fetch_json(url):
    raw, mime, _ = fetch(url, max_bytes=4 * 1024 * 1024)
    try:
        value = json.loads(raw)
        require(isinstance(value, dict), "Resource API must return a JSON object.")
        return value
    except (ValueError, UnicodeError) as exc:
        raise EngineError("Resource API did not return valid JSON.") from exc
