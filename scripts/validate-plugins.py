#!/usr/bin/env python3
"""
validate-plugins.py

Validate every plugin under plugins/* against the Claude Code plugin spec
and the marketplace.json schema.

Checks:
  - Each plugin has .claude-plugin/plugin.json
  - plugin.json has required fields (name, version)
  - name matches directory name
  - No commands/, agents/, skills/, hooks/ inside .claude-plugin/ (common mistake)
  - If skills/ exists, each subdir has SKILL.md
  - If agents/ exists, each .md has frontmatter
  - If commands/ exists, each .md has frontmatter
  - marketplace.json references match plugins/ directories

Usage:
  python3 validate-plugins.py [marketplace-repo-root]

Exit codes:
  0 — all checks passed
  1 — validation errors found
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path


PLUGIN_NAME_RE = re.compile(r"^[a-z][a-z0-9-]*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(-[\w.]+)?(\+[\w.]+)?$")


class Validator:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def err(self, msg: str):
        self.errors.append(msg)

    def warn(self, msg: str):
        self.warnings.append(msg)

    def validate_plugin(self, plugin_dir: Path):
        name = plugin_dir.name
        prefix = f"[{name}]"

        manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
        if not manifest_path.exists():
            self.err(f"{prefix} missing .claude-plugin/plugin.json")
            return

        try:
            with open(manifest_path) as f:
                manifest = json.load(f)
        except json.JSONDecodeError as e:
            self.err(f"{prefix} invalid JSON in plugin.json: {e}")
            return

        m_name = manifest.get("name")
        if not m_name:
            self.err(f"{prefix} plugin.json missing 'name'")
        elif m_name != name:
            self.err(f"{prefix} plugin.json name '{m_name}' != directory name '{name}'")
        elif not PLUGIN_NAME_RE.match(m_name):
            self.err(f"{prefix} plugin name '{m_name}' must be kebab-case (lowercase + hyphens)")

        version = manifest.get("version")
        if not version:
            self.err(f"{prefix} plugin.json missing 'version'")
        elif not SEMVER_RE.match(str(version)):
            self.warn(f"{prefix} version '{version}' is not strict semver")

        if not manifest.get("description"):
            self.warn(f"{prefix} plugin.json missing 'description'")

        # Common mistake: commands/agents/skills/hooks inside .claude-plugin/
        claude_plugin_dir = plugin_dir / ".claude-plugin"
        for bad_sub in ["commands", "agents", "skills", "hooks"]:
            if (claude_plugin_dir / bad_sub).exists():
                self.err(
                    f"{prefix} '{bad_sub}/' is inside .claude-plugin/ — "
                    f"must be at plugin root"
                )

        # Check skills/ structure
        skills_dir = plugin_dir / "skills"
        if skills_dir.exists():
            for skill_sub in skills_dir.iterdir():
                if not skill_sub.is_dir():
                    self.warn(f"{prefix} skills/{skill_sub.name} is not a directory")
                    continue
                skill_md = skill_sub / "SKILL.md"
                if not skill_md.exists():
                    self.err(f"{prefix} skills/{skill_sub.name}/SKILL.md missing")

        # Check agents/ have frontmatter
        agents_dir = plugin_dir / "agents"
        if agents_dir.exists():
            for agent_md in agents_dir.glob("*.md"):
                with open(agent_md) as f:
                    content = f.read()
                if not content.startswith("---\n"):
                    self.warn(f"{prefix} agents/{agent_md.name} has no YAML frontmatter")

        # Check commands/ have frontmatter
        commands_dir = plugin_dir / "commands"
        if commands_dir.exists():
            for cmd_md in commands_dir.glob("*.md"):
                with open(cmd_md) as f:
                    content = f.read()
                if not content.startswith("---\n"):
                    self.warn(f"{prefix} commands/{cmd_md.name} has no YAML frontmatter")

    def validate_marketplace(self):
        mp_path = self.repo_root / ".claude-plugin" / "marketplace.json"
        if not mp_path.exists():
            self.err("marketplace.json missing at .claude-plugin/marketplace.json")
            return

        try:
            with open(mp_path) as f:
                mp = json.load(f)
        except json.JSONDecodeError as e:
            self.err(f"marketplace.json invalid JSON: {e}")
            return

        for required in ("name", "owner", "plugins"):
            if required not in mp:
                self.err(f"marketplace.json missing required field '{required}'")

        if "owner" in mp and "name" not in mp.get("owner", {}):
            self.err("marketplace.json owner.name is required")

        # Every referenced plugin must exist
        plugin_dirs = set()
        plugins_root = self.repo_root / "plugins"
        if plugins_root.exists():
            plugin_dirs = {d.name for d in plugins_root.iterdir()
                           if d.is_dir() and not d.name.startswith(".")}

        for p in mp.get("plugins", []):
            src = p.get("source", "")
            if isinstance(src, str) and src.startswith("./plugins/"):
                expected_dir = src.replace("./plugins/", "")
                if expected_dir not in plugin_dirs:
                    self.err(f"marketplace references {src} but plugins/{expected_dir}/ does not exist")

        # Every plugins/ dir must be in marketplace
        referenced = set()
        for p in mp.get("plugins", []):
            src = p.get("source", "")
            if isinstance(src, str) and src.startswith("./plugins/"):
                referenced.add(src.replace("./plugins/", ""))

        for d in plugin_dirs:
            if d not in referenced:
                self.warn(f"plugins/{d}/ exists but is not listed in marketplace.json")

    def run(self) -> bool:
        self.validate_marketplace()

        plugins_root = self.repo_root / "plugins"
        if plugins_root.exists():
            for plugin_dir in sorted(plugins_root.iterdir()):
                if plugin_dir.is_dir() and not plugin_dir.name.startswith("."):
                    self.validate_plugin(plugin_dir)

        # Report
        if self.warnings:
            for w in self.warnings:
                print(f"WARN: {w}")
        if self.errors:
            for e in self.errors:
                print(f"ERROR: {e}")
            print(f"\n✗ {len(self.errors)} error(s), {len(self.warnings)} warning(s)")
            return False
        print(f"✓ All checks passed ({len(self.warnings)} warning(s))")
        return True


def main():
    repo_root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 \
        else Path(__file__).resolve().parent.parent
    ok = Validator(repo_root).run()
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
