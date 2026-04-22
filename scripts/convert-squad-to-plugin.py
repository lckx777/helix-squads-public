#!/usr/bin/env python3
"""
convert-squad-to-plugin.py

Convert one squad from the Source-of-Truth (~/.claude/skills/squads/squads/<name>)
to a Claude Code plugin directory (<marketplace-repo>/plugins/<name>/).

Mapping strategy (decided by Hermes based on Claude Code plugin spec oct/2025):

  SoT                              | Plugin layout                  | Why
  ---------------------------------|--------------------------------|----
  squad.yaml                       | .claude-plugin/plugin.json     | Manifest (normalized)
  squad.yaml (copy)                | squad.yaml                     | Preserve legacy for reverse compat
  agents/*.md                      | agents/*.md                    | Direct — native plugin format
  tasks/*.md                       | skills/<task-name>/SKILL.md    | Tasks are procedural knowledge → model-invoked skills
  chains/*.yaml                    | commands/<chain>.md            | Chains are user-invoked entry points → slash commands
  workflows/*.yaml                 | workflows/*.yaml               | Kept as-is, read by skills
  checklists/*.md                  | references/checklists/*.md     | Static reference material
  config/*.md                      | references/config/*.md         | Static reference material
  data/**                          | references/data/**             | Static knowledge base
  scripts/*.sh                     | scripts/*.sh                   | Helpers retained
  README.md                        | README.md                      | Direct
  _TEMPLATE.md                     | _TEMPLATE.md                   | Preserved

For each task converted to SKILL.md, a frontmatter block is generated:

  ---
  description: <first non-blank sentence of the task, or explicit `description:` frontmatter>
  ---

Chain YAML files are wrapped in a commands/<chain>.md that describes the
sequence in natural language — Claude Code commands don't execute YAML engines,
so the model interprets the chain steps at runtime. Original YAML is preserved
alongside for reference.

Usage:
  python3 convert-squad-to-plugin.py <squad-name> <output-root>

Example:
  python3 convert-squad-to-plugin.py stack-auditors ~/dev/helix-squads-marketplaces/helix-squads-public/plugins

Exit codes:
  0 — success
  1 — SoT squad not found
  2 — output dir already exists (refuses to overwrite)
  3 — parse/write error
"""
from __future__ import annotations

import json
import os
import re
import shutil
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.stderr.write("ERROR: pyyaml required. Install: pip install pyyaml\n")
    sys.exit(3)


SOT_ROOT = Path.home() / ".claude" / "skills" / "squads" / "squads"

# Directories in the SoT that map 1:1 into the plugin root
PASSTHROUGH_DIRS = {"agents", "workflows", "scripts"}

# Directories that get moved under references/
REFERENCE_DIRS = {"checklists", "config", "data", "schemas", "standards", "templates", "hooks", "scenarios"}


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text)
    return text.strip("-")


def extract_description_from_md(md_content: str, fallback: str) -> str:
    """Extract a one-line description from a markdown task/checklist file.

    Priority:
      1. YAML frontmatter `description:` field
      2. First non-blank line after a level-1 or level-2 heading
      3. First non-blank line
      4. Fallback (provided by caller)
    """
    # Frontmatter
    fm_match = re.match(r"^---\n(.*?)\n---\n", md_content, re.DOTALL)
    if fm_match:
        try:
            fm = yaml.safe_load(fm_match.group(1))
            if isinstance(fm, dict) and fm.get("description"):
                return str(fm["description"]).strip().split("\n")[0]
        except yaml.YAMLError:
            pass

    # Strip frontmatter if present for subsequent searches
    body = re.sub(r"^---\n.*?\n---\n", "", md_content, count=1, flags=re.DOTALL)

    # First non-blank line after heading
    lines = body.split("\n")
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        if line.startswith("#"):
            # Skip heading, find first content line after
            for next_line in lines[i + 1 :]:
                next_line = next_line.strip()
                if next_line and not next_line.startswith("#"):
                    return next_line[:200]
            continue
        return line[:200]

    return fallback


def load_squad_yaml(squad_dir: Path) -> dict:
    squad_yaml_path = squad_dir / "squad.yaml"
    if not squad_yaml_path.exists():
        return {}
    try:
        with open(squad_yaml_path) as f:
            return yaml.safe_load(f) or {}
    except yaml.YAMLError as e:
        sys.stderr.write(f"WARN: could not parse squad.yaml: {e}\n")
        return {}


def build_plugin_manifest(squad_name: str, squad_yaml: dict) -> dict:
    """Generate .claude-plugin/plugin.json from squad.yaml data."""
    description = squad_yaml.get("description", f"Helix squad: {squad_name}")
    if isinstance(description, str):
        description = description.strip().split("\n")[0]
        # Truncate on word boundary if too long (400 char cap)
        if len(description) > 400:
            description = description[:397].rsplit(" ", 1)[0] + "..."

    version = str(squad_yaml.get("version", "1.0.0"))
    author_raw = squad_yaml.get("author", "Luca Pimenta")
    if isinstance(author_raw, str):
        author = {"name": author_raw}
    elif isinstance(author_raw, dict):
        author = author_raw
    else:
        author = {"name": "Luca Pimenta"}

    manifest = {
        "name": squad_name,
        "version": version,
        "description": description,
        "author": author,
        "license": squad_yaml.get("license", "MIT"),
        "keywords": list(squad_yaml.get("tags", []))[:10],
        "homepage": f"https://github.com/lckx777/helix-squads-public/tree/main/plugins/{squad_name}",
        "repository": "https://github.com/lckx777/helix-squads-public",
    }
    # Dedupe keywords
    seen = set()
    manifest["keywords"] = [k for k in manifest["keywords"] if not (k in seen or seen.add(k))]
    return manifest


def copy_passthrough(src: Path, dst: Path):
    """Copy directory verbatim, skipping .backup-* subdirs."""
    if not src.exists():
        return
    dst.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        if item.name.startswith(".backup"):
            continue
        target = dst / item.name
        if item.is_dir():
            shutil.copytree(item, target, dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns(".backup*"))
        else:
            shutil.copy2(item, target)


def convert_tasks_to_skills(tasks_src: Path, skills_dst: Path):
    """Each tasks/<name>.md becomes skills/<name>/SKILL.md with frontmatter."""
    if not tasks_src.exists():
        return 0
    skills_dst.mkdir(parents=True, exist_ok=True)
    count = 0
    for task_file in sorted(tasks_src.iterdir()):
        if not task_file.is_file() or not task_file.suffix == ".md":
            continue
        if task_file.name.startswith("."):
            continue
        task_name = task_file.stem
        skill_dir = skills_dst / task_name
        skill_dir.mkdir(parents=True, exist_ok=True)

        with open(task_file) as f:
            content = f.read()

        # Check if already has frontmatter
        has_fm = content.startswith("---\n")
        description = extract_description_from_md(content, f"Execute task: {task_name}")

        if has_fm:
            # Keep existing frontmatter but ensure `description` field exists
            fm_match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
            if fm_match:
                try:
                    fm = yaml.safe_load(fm_match.group(1)) or {}
                    if "description" not in fm:
                        fm["description"] = description
                    body = content[fm_match.end():]
                    new_fm = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True).strip()
                    content = f"---\n{new_fm}\n---\n{body}"
                except yaml.YAMLError:
                    pass  # leave as-is
        else:
            # Prepend frontmatter
            content = f"---\ndescription: {description}\n---\n\n{content}"

        with open(skill_dir / "SKILL.md", "w") as f:
            f.write(content)
        count += 1
    return count


def convert_chains_to_commands(chains_src: Path, commands_dst: Path, plugin_root: Path):
    """Each chains/<name>.yaml becomes commands/<name>.md describing the sequence.

    Original YAML is preserved at plugin_root/chains/<name>.yaml for reference.
    """
    if not chains_src.exists():
        return 0
    commands_dst.mkdir(parents=True, exist_ok=True)
    chains_dst = plugin_root / "chains"
    chains_dst.mkdir(parents=True, exist_ok=True)

    count = 0
    for chain_file in sorted(chains_src.iterdir()):
        if not chain_file.is_file() or chain_file.suffix not in {".yaml", ".yml"}:
            continue
        if chain_file.name.startswith("."):
            continue

        chain_name = chain_file.stem
        # Preserve raw YAML
        shutil.copy2(chain_file, chains_dst / chain_file.name)

        # Generate markdown command
        try:
            with open(chain_file) as f:
                chain_data = yaml.safe_load(f) or {}
        except yaml.YAMLError:
            chain_data = {}

        chain_desc = chain_data.get("description", f"Execute chain: {chain_name}")
        steps = chain_data.get("steps") or chain_data.get("sequence") or []

        md = f"""---
description: {chain_desc}
---

# {chain_name}

{chain_desc}

## Execution

This command triggers the `{chain_name}` chain. The canonical chain
definition lives at `chains/{chain_file.name}` within this plugin.

"""
        if isinstance(steps, list) and steps:
            md += "Follow these steps in order:\n\n"
            for i, step in enumerate(steps, 1):
                if isinstance(step, dict):
                    step_name = step.get("name") or step.get("id") or f"step-{i}"
                    step_agent = step.get("agent") or step.get("mentor") or ""
                    step_task = step.get("task") or step.get("action") or ""
                    md += f"{i}. **{step_name}**"
                    if step_agent:
                        md += f" — agent: `{step_agent}`"
                    if step_task:
                        md += f" — task: `{step_task}`"
                    md += "\n"
                else:
                    md += f"{i}. {step}\n"
        else:
            md += (
                "See the YAML file for detailed step sequence. Execute each step "
                "by invoking the specified agent and task in order, passing "
                "outputs forward as inputs to subsequent steps.\n"
            )

        md += f"\n## Arguments\n\n$ARGUMENTS will be passed as the initial input to step 1.\n"

        with open(commands_dst / f"{chain_name}.md", "w") as f:
            f.write(md)
        count += 1
    return count


def move_references(squad_dir: Path, plugin_root: Path) -> int:
    """Move checklists/, config/, data/, schemas/, etc. under references/."""
    references_root = plugin_root / "references"
    count = 0
    for ref_name in REFERENCE_DIRS:
        src = squad_dir / ref_name
        if src.exists() and src.is_dir():
            dst = references_root / ref_name
            dst.mkdir(parents=True, exist_ok=True)
            for item in src.iterdir():
                if item.name.startswith(".backup"):
                    continue
                if item.is_dir():
                    shutil.copytree(item, dst / item.name, dirs_exist_ok=True,
                                    ignore=shutil.ignore_patterns(".backup*"))
                else:
                    shutil.copy2(item, dst / item.name)
                count += 1
    return count


def write_plugin_readme(plugin_root: Path, squad_name: str, squad_yaml: dict,
                       stats: dict):
    description = squad_yaml.get("description", f"Helix squad: {squad_name}")
    if isinstance(description, str):
        description = description.strip()

    readme = f"""# {squad_name}

{description}

## Install

```
claude plugin marketplace add lckx777/helix-squads-public
claude plugin install {squad_name}@helix-squads-public
```

## Components

- **{stats['agents']}** agents — persona bodies in `agents/`
- **{stats['skills']}** skills — model-invoked tasks in `skills/`
- **{stats['commands']}** commands — user-invoked slash commands in `commands/`
- **{stats['workflows']}** workflows — pipeline definitions in `workflows/`
- **{stats['references']}** reference files — static knowledge in `references/`

## Invocation

After install, skills are namespaced with the plugin name. For example:

```
/{squad_name}:<skill-name>
```

Agents can be invoked via the Task tool when Claude's orchestration layer
routes to them automatically based on their `description` frontmatter.

## Source

This plugin is converted from the canonical source-of-truth at
`~/.claude/skills/squads/squads/{squad_name}/` by the script
`scripts/convert-squad-to-plugin.py` in the marketplace repository.
"""
    with open(plugin_root / "README.md", "w") as f:
        f.write(readme)


def convert(squad_name: str, output_root: Path):
    squad_dir = SOT_ROOT / squad_name
    if not squad_dir.exists():
        sys.stderr.write(f"ERROR: squad not found at {squad_dir}\n")
        sys.exit(1)

    plugin_root = output_root / squad_name
    if plugin_root.exists():
        sys.stderr.write(
            f"ERROR: output path already exists: {plugin_root}\n"
            "  Refusing to overwrite. Delete it first or use a different output root.\n"
        )
        sys.exit(2)

    plugin_root.mkdir(parents=True, exist_ok=True)

    # 1. Manifest
    squad_yaml = load_squad_yaml(squad_dir)
    manifest = build_plugin_manifest(squad_name, squad_yaml)
    manifest_dir = plugin_root / ".claude-plugin"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    with open(manifest_dir / "plugin.json", "w") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        f.write("\n")

    # 2. Preserve original squad.yaml for legacy consumers
    if (squad_dir / "squad.yaml").exists():
        shutil.copy2(squad_dir / "squad.yaml", plugin_root / "squad.yaml")

    # 3. Passthrough dirs (agents, workflows, scripts)
    for dir_name in PASSTHROUGH_DIRS:
        copy_passthrough(squad_dir / dir_name, plugin_root / dir_name)

    # 4. Tasks → skills
    skills_count = convert_tasks_to_skills(squad_dir / "tasks", plugin_root / "skills")

    # 5. Chains → commands (+ preserve raw YAML)
    commands_count = convert_chains_to_commands(
        squad_dir / "chains", plugin_root / "commands", plugin_root
    )

    # 6. References (checklists, config, data, schemas, etc.)
    references_count = move_references(squad_dir, plugin_root)

    # 7. README
    stats = {
        "agents": len(list((plugin_root / "agents").glob("*.md"))) if (plugin_root / "agents").exists() else 0,
        "skills": skills_count,
        "commands": commands_count,
        "workflows": len(list((plugin_root / "workflows").glob("*"))) if (plugin_root / "workflows").exists() else 0,
        "references": references_count,
    }
    write_plugin_readme(plugin_root, squad_name, squad_yaml, stats)

    # 8. Copy squad-level README if present (overwrites the generated one if exists)
    squad_readme = squad_dir / "README.md"
    if squad_readme.exists():
        # Prepend the generated install section to the existing README
        with open(squad_readme) as f:
            existing = f.read()
        install_section = f"""# {squad_name}

> This plugin is part of the [Helix Squads Public Marketplace](https://github.com/lckx777/helix-squads-public).

## Quick install

```
claude plugin marketplace add lckx777/helix-squads-public
claude plugin install {squad_name}@helix-squads-public
```

---

"""
        if not existing.lstrip().startswith("#"):
            existing = f"# {squad_name}\n\n{existing}"
        with open(plugin_root / "README.md", "w") as f:
            f.write(install_section + existing)

    # 9. Copy _TEMPLATE.md if present
    template_md = squad_dir / "_TEMPLATE.md"
    if template_md.exists():
        shutil.copy2(template_md, plugin_root / "_TEMPLATE.md")

    print(f"✓ Converted {squad_name}")
    print(f"  Output: {plugin_root}")
    print(f"  Stats:  agents={stats['agents']} skills={stats['skills']} "
          f"commands={stats['commands']} workflows={stats['workflows']} "
          f"references={stats['references']}")
    return stats


def main():
    if len(sys.argv) != 3:
        sys.stderr.write(__doc__ + "\n")
        sys.exit(3)
    squad_name = sys.argv[1]
    output_root = Path(sys.argv[2]).expanduser().resolve()
    if not output_root.exists():
        output_root.mkdir(parents=True, exist_ok=True)
    convert(squad_name, output_root)


if __name__ == "__main__":
    main()
