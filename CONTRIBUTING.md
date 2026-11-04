# Contributing assets

Submit a pull request with a manifest, editable source (local or versioned HTTPS),
license, attribution, provenance, compatibility, byte size and SHA-256. Include
creation and validation evidence. Submit only content you can redistribute under
the declared license; reference imagery needs its own permission. Accepted asset
licenses initially are CC BY 4.0 and CC0. New first-party assets use CC BY 4.0.

Third-party authors retain copyright. Retain credit when adapting content, link
the license and identify changes. Do not include extracted game files, proprietary
packs, credentials or builds. Script/test/workflow contributions use MIT; content,
metadata and documentation use their declared Creative Commons license.

Keep sources compact and generated exports external. Publisher-owned Releases
avoid centralizing everyone's downloads in our account. See [storage](docs/storage.md)
and the [manifest contract](docs/format.md).

```sh
python3 tools/catalog.py build
python3 tools/catalog.py validate
python3 -m unittest discover -s tests -v
```

Maintainers review provenance, licensing, compatibility and presentation before
merging. Automation validates metadata/local integrity, not artistic quality,
ownership, malware absence or remote availability. CI has read-only permissions
and does not publish content or consume paid APIs.
