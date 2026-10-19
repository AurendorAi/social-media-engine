"""Build a minimal, deterministic plugin ZIP. Never include the repository wholesale."""
from pathlib import Path
import hashlib
import json
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/social-media-engine"
ALLOWED_TOP = {"plugin.json", ".codex-plugin", ".claude-plugin", "skills", "scripts", "assets", "README.md", "LICENSE"}
ALLOWED_SUFFIXES = {".json", ".md", ".py", ".js", ".css", ".html", ".png", ".svg"}
FORBIDDEN = [b"/Users/", b"Content OS", b"/home/ubuntu", b"POSTIZ_API_KEY=sk-"]


def source_files():
    files = []
    for path in sorted(PLUGIN.rglob("*")):
        rel = path.relative_to(PLUGIN)
        if "__pycache__" in rel.parts or path.suffix in {".pyc", ".pyo"}:
            continue
        if path.is_symlink():
            raise ValueError("Release input must not contain symlinks: " + str(rel))
        if path.is_dir():
            continue
        if rel.parts[0] not in ALLOWED_TOP or (path.suffix not in ALLOWED_SUFFIXES and path.name != "LICENSE"):
            raise ValueError("Unexpected release input: " + str(rel))
        data = path.read_bytes()
        if any(marker in data for marker in FORBIDDEN):
            raise ValueError("Private path or legacy product name in: " + str(rel))
        if len(data) > 5 * 1024 * 1024:
            raise ValueError("Unexpected large runtime file: " + str(rel))
        files.append((rel.as_posix(), data))
    return files


def validate_marketplaces(name, version):
    """A valid ZIP is not installable by name if repository discovery is stale."""
    for relative, host in ((".agents/plugins/marketplace.json", "Codex"),
                           (".claude-plugin/marketplace.json", "Claude")):
        marketplace = json.loads((ROOT / relative).read_text(encoding="utf-8"))
        entries = [entry for entry in marketplace.get("plugins", [])
                   if entry.get("name") == name]
        if len(entries) != 1:
            raise ValueError(host + " marketplace must contain exactly one matching plugin")
        entry = entries[0]
        source = entry.get("source")
        if host == "Codex":
            if not isinstance(source, dict) or source.get("source") != "local":
                raise ValueError("Codex marketplace must use the local packaged source")
            source = source.get("path")
        if not isinstance(source, str) or not source.startswith("./"):
            raise ValueError(host + " marketplace source must be repository-relative")
        if (ROOT / source).resolve() != PLUGIN.resolve():
            raise ValueError(host + " marketplace source disagrees with packaged plugin")
        if "version" in entry and entry["version"] != version:
            raise ValueError(host + " marketplace version disagrees with plugin")


def build():
    codex = json.loads((PLUGIN / ".codex-plugin/plugin.json").read_text())
    claude = json.loads((PLUGIN / ".claude-plugin/plugin.json").read_text())
    version = codex["version"]
    portable = json.loads((PLUGIN / "plugin.json").read_text())
    if portable["name"] != codex["name"] or portable["version"] != version:
        raise ValueError("Portable manifest disagrees")
    if codex["name"] != PLUGIN.name or claude["name"] != PLUGIN.name or claude["version"] != version:
        raise ValueError("Plugin manifests disagree")
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise ValueError("Invalid version")
    validate_marketplaces(codex["name"], version)
    files = source_files()
    names = {name for name, _ in files}
    required = {"plugin.json", "README.md", ".codex-plugin/plugin.json", ".claude-plugin/plugin.json",
                "skills/social-media-engine/SKILL.md", "scripts/sme.py",
                "scripts/engine.py", "scripts/creative_memory.py", "scripts/providers.py", "scripts/dashboard.py",
                "scripts/resources.py", "scripts/resource_http.py", "assets/resource-libraries.json",
                "scripts/style_catalog.py", "assets/style-catalog.json",
                "skills/social-media-engine/references/image-acquisition.md",
                "skills/social-media-engine/references/resource-sourcing.md",
                "assets/dashboard.html", "assets/dashboard.js", "assets/dashboard.css", "LICENSE"}
    if not required <= names:
        raise ValueError("Missing required plugin files: " + str(required - names))
    target = ROOT / "dist"
    target.mkdir(exist_ok=True)
    archive = target / ("social-media-engine-" + version + ".zip")
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
        for name, data in files:
            info = zipfile.ZipInfo(name, (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, data)
    checksum = hashlib.sha256(archive.read_bytes()).hexdigest()
    (target / "SHA256SUMS").write_text(checksum + "  " + archive.name + "\n")
    print(json.dumps({"archive": str(archive), "bytes": archive.stat().st_size,
                      "files": len(files), "sha256": checksum}, indent=2))
    return archive


if __name__ == "__main__":
    build()
