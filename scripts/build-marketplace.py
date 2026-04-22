#!/usr/bin/env python3
"""
build-marketplace.py

Scan plugins/*/.claude-plugin/plugin.json and regenerate marketplace.json
with entries pointing to each plugin via relative path.

Preserves top-level marketplace metadata (name, owner, description) and
overwrites only the `plugins` array.

Usage:
  python3 build-marketplace.py [marketplace-repo-root]

Default: runs against the repo root containing the script's parent scripts/ dir.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path


def build(repo_root: Path) -> dict:
    marketplace_file = repo_root / ".claude-plugin" / "marketplace.json"
    if not marketplace_file.exists():
        sys.stderr.write(f"ERROR: marketplace.json not found at {marketplace_file}\n")
        sys.exit(1)

    with open(marketplace_file) as f:
        marketplace = json.load(f)

    plugins_dir = repo_root / "plugins"
    if not plugins_dir.exists():
        sys.stderr.write(f"WARN: plugins/ dir not found at {plugins_dir} — empty marketplace\n")
        marketplace["plugins"] = []
    else:
        entries = []
        for plugin_dir in sorted(plugins_dir.iterdir()):
            if not plugin_dir.is_dir():
                continue
            if plugin_dir.name.startswith("."):
                continue
            manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
            if not manifest_path.exists():
                sys.stderr.write(f"WARN: skipping {plugin_dir.name} — no plugin.json\n")
                continue
            with open(manifest_path) as f:
                manifest = json.load(f)

            entry = {
                "name": manifest.get("name", plugin_dir.name),
                "source": f"./plugins/{plugin_dir.name}",
                "description": manifest.get("description", ""),
                "version": manifest.get("version", "0.0.1"),
                "author": manifest.get("author", {}),
            }
            if manifest.get("keywords"):
                entry["keywords"] = manifest["keywords"]
            if manifest.get("homepage"):
                entry["homepage"] = manifest["homepage"]
            entries.append(entry)
        marketplace["plugins"] = entries

    with open(marketplace_file, "w") as f:
        json.dump(marketplace, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"✓ marketplace.json rebuilt — {len(marketplace['plugins'])} plugin(s)")
    for p in marketplace["plugins"]:
        print(f"  - {p['name']} @ {p['version']}  [{p['source']}]")
    return marketplace


def main():
    repo_root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 \
        else Path(__file__).resolve().parent.parent
    build(repo_root)


if __name__ == "__main__":
    main()
