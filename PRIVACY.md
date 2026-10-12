# Privacy

Social Media Engine has no built-in telemetry, central account, or automatic upload.
The local runtime stores brand answers, assets, content, reviews, feedback, metrics and
audit records in the user's selected working folder. Data is not encrypted by this
plugin. Protect the device, filesystem permissions and backups.

The dashboard listens on loopback only. Its random token is a local session capability,
not a multi-user authentication system. Keep its URL private. Stop the server when done.

The AI host and any deliberately used external providers have their own data policies.
Authorized creative tools may receive brand references/prompts; an authorized Postiz
send uploads selected assets and captions. Reading accounts/posts also contacts Postiz.
Environment credentials are not written into the brand database. Do not enter secrets
in brand answers or feedback; automated detection is limited, not a secret-scanner guarantee.

To remove local data, stop all plugin processes and delete the chosen workspace's
`.social-media-engine/` after backing up anything needed. This does not delete provider
uploads, scheduled/public posts, host chat history, or external service records.
Use those services' controls separately.

Privacy questions: mohammedj@aurendor.io.

## Resource discovery

Explicit resource searches send the search words and normal network metadata to the
selected library service. Met search also fetches matching public object records.
Resource downloads contact the selected public file host and validated redirects.
The built-in downloader sends no API keys, cookies or brand profile. Do not put private
campaign details in queries or signed/account-specific URLs in provenance.
Candidate metadata, licence evidence and downloaded files stay in the selected local
brand workspace. Host browser/search and creative services have their own data policies.
No discovery or download runs on plugin installation.
