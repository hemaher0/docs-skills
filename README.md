# docs-skills

This repository provides two independently selectable collections:

| Collection | Source | Purpose |
| --- | --- | --- |
| docs-skills | `plugins/docs-skills/skills/` | Documentation, diagrams, reference notes, and work records. |
| openspec | `plugins/openspec/skills/` | OpenSpec proposals, implementation, spec synchronization, and archival. |

Keep the source under `.agents/vendor/` and link the chosen skill folders into
`.agents/skills/`. Each project can choose its own skills and source revision.
User-wide installations use the same structure under `$HOME/.agents/`.
Claude Code uses `.claude/skills/` and `~/.claude/skills/`; see
[Use with Claude Code](#use-with-claude-code).

## Install for a project

Run from the project root:

```bash
mkdir -p .agents/vendor .agents/skills
git clone --branch main https://github.com/hemaher0/docs-skills.git .agents/vendor/docs-skills
```

Install documentation skills:

```bash
for source in .agents/vendor/docs-skills/plugins/docs-skills/skills/*; do
  [ -f "$source/SKILL.md" ] || continue
  skill="${source##*/}"
  destination=".agents/skills/$skill"
  if [ -e "$destination" ] || [ -L "$destination" ]; then
    printf 'Preserve existing path: %s\n' "$destination" >&2
    continue
  fi
  ln -s "../vendor/docs-skills/plugins/docs-skills/skills/$skill" "$destination"
done
```

If you also use OpenSpec, install its skills independently:

```bash
for source in .agents/vendor/docs-skills/plugins/openspec/skills/*; do
  [ -f "$source/SKILL.md" ] || continue
  skill="${source##*/}"
  destination=".agents/skills/$skill"
  if [ -e "$destination" ] || [ -L "$destination" ]; then
    printf 'Preserve existing path: %s\n' "$destination" >&2
    continue
  fi
  ln -s "../vendor/docs-skills/plugins/openspec/skills/$skill" "$destination"
done
```

To select individual skills, replace `skills/*` in the loop's first line with
`skills/maintaining-documentation` for one skill, or
`skills/{maintaining-documentation,auditing-documentation}` for a selected set.
Use OpenSpec skill names for its loop. Existing files, directories, and links
are preserved; the loop continues installing the remaining skills.

The vendor checkout retains the collection's templates. Link complete skill
folders. Relative links remain valid when the whole project moves.

Start a new Codex session in the project and check the current available-skills
list. Invoke a selected skill by name, such as `$maintaining-documentation` or
`$openspec-propose`. Check its link and entrypoint with:

```bash
readlink .agents/skills/maintaining-documentation
test -f .agents/skills/maintaining-documentation/SKILL.md
```

Update this project's source checkout:

```bash
git -C .agents/vendor/docs-skills pull --ff-only
```

Remove a selected skill after checking that its destination is the intended link:

```bash
readlink .agents/skills/maintaining-documentation
unlink .agents/skills/maintaining-documentation
```

Keep the vendor checkout while other selected skills or project procedures use
it. Project records, copied schemas, and OpenSpec artifacts retain their own
lifecycle.

## Install globally

Run from any directory. These skills are shared across this user's projects:

```bash
mkdir -p "$HOME/.agents/vendor" "$HOME/.agents/skills"
git clone --branch main https://github.com/hemaher0/docs-skills.git "$HOME/.agents/vendor/docs-skills"
```

Install documentation skills:

```bash
for source in "$HOME"/.agents/vendor/docs-skills/plugins/docs-skills/skills/*; do
  [ -f "$source/SKILL.md" ] || continue
  skill="${source##*/}"
  destination="$HOME/.agents/skills/$skill"
  if [ -e "$destination" ] || [ -L "$destination" ]; then
    printf 'Preserve existing path: %s\n' "$destination" >&2
    continue
  fi
  ln -s "../vendor/docs-skills/plugins/docs-skills/skills/$skill" "$destination"
done
```

If you also use OpenSpec:

```bash
for source in "$HOME"/.agents/vendor/docs-skills/plugins/openspec/skills/*; do
  [ -f "$source/SKILL.md" ] || continue
  skill="${source##*/}"
  destination="$HOME/.agents/skills/$skill"
  if [ -e "$destination" ] || [ -L "$destination" ]; then
    printf 'Preserve existing path: %s\n' "$destination" >&2
    continue
  fi
  ln -s "../vendor/docs-skills/plugins/openspec/skills/$skill" "$destination"
done
```

Select a subset by changing `skills/*` as in the project examples. Start a new
Codex session and confirm the selected names and locations in its skill list.
Restart the host if the list does not refresh. Check a global link with:

```bash
readlink "$HOME/.agents/skills/maintaining-documentation"
test -f "$HOME/.agents/skills/maintaining-documentation/SKILL.md"
```

Update the global source checkout:

```bash
git -C "$HOME/.agents/vendor/docs-skills" pull --ff-only
```

Remove a selected global link after inspecting it:

```bash
readlink "$HOME/.agents/skills/maintaining-documentation"
unlink "$HOME/.agents/skills/maintaining-documentation"
```

Keep the source while other global links use it. Each project keeps its own
documentation settings, schema, and native OpenSpec store.

## Optional project configuration

Ordinary documentation edits use the project's existing rules. Work records are
optional and use the templates and checker bundled inside
[maintaining-work-records](plugins/docs-skills/skills/maintaining-work-records/SKILL.md).
They require no framework copy in the project root. Configure capture, storage,
and audience only when the project chooses to keep records.

For a custom record format, create `.agents/config/docs-skills/schema.json`
from the [default schema](plugins/docs-skills/skills/maintaining-work-records/references/schema.json)
and edit its rules. Keep every type needed by existing records. Custom templates
are optional; shared templates remain in the skill. See the
[record configuration guide](plugins/docs-skills/skills/maintaining-work-records/references/README.md)
for custom paths, fields, states, calendars, and templates, or selecting an
external schema with `--schema`.

A new custom type can start from the supplied
[custom schema template](plugins/docs-skills/skills/maintaining-work-records/templates/custom-schema/schema.json)
and matching [note template](plugins/docs-skills/skills/maintaining-work-records/templates/custom-schema/templates/note.md).
The configuration guide explains how to copy, edit, and validate them.

Project settings can be merged from [AGENTS.md](plugins/docs-skills/templates/AGENTS.md)
and [AGENTS.local.md](plugins/docs-skills/templates/AGENTS.local.md) when needed.

OpenSpec skills need the native CLI; documentation skills can be used on their
own. Follow the [OpenSpec installation guide](https://github.com/Fission-AI/OpenSpec/blob/main/docs/installation.md)
if needed and check `openspec --version`. These packaged skills were generated
for CLI 1.8.0. For a new OpenSpec project, run `openspec init --tools none` from
its root to initialize the store without generating duplicate tool skills.
Preserve an existing store and configuration.

## Use with Claude Code

Claude Code discovers project skills in `.claude/skills/<name>/SKILL.md` and
personal skills in `~/.claude/skills/<name>/SKILL.md`. The skill folders in
this repository work there without conversion. Keep the source checkout
described above and expose the selected skills from the project root, for
example:

```bash
mkdir -p .claude/skills
for skill in using-docs-skills maintaining-work-records; do
  destination=".claude/skills/$skill"
  if [ -e "$destination" ] || [ -L "$destination" ]; then
    printf 'Preserve existing path: %s\n' "$destination" >&2
    continue
  fi
  ln -s "../../.agents/vendor/docs-skills/plugins/docs-skills/skills/$skill" "$destination"
done
for skill in openspec-propose openspec-apply-change; do
  destination=".claude/skills/$skill"
  if [ -e "$destination" ] || [ -L "$destination" ]; then
    printf 'Preserve existing path: %s\n' "$destination" >&2
    continue
  fi
  ln -s "../../.agents/vendor/docs-skills/plugins/openspec/skills/$skill" "$destination"
done
```

The link targets are relative to `.claude/skills`. For personal skills, run
the same loop with `$HOME/.claude/skills` and the global source checkout under
`$HOME/.agents/vendor`; the relative targets stay the same. Where symbolic
links are unavailable, such as Windows without Developer Mode, copy each
selected folder completely instead and copy it again after updating the source.

Use a skill by its name, for example `/maintaining-work-records`, or let Claude
select it from its description. Confirm that the name appears in the session's
skill list; start a new session if a newly added folder is not listed.

Claude Code can also install this repository as a plugin marketplace:

```bash
claude plugin marketplace add hemaher0/docs-skills
claude plugin install docs-skills@hemaher0-docs-skills
claude plugin install openspec@hemaher0-docs-skills
```

Inside a session, `/plugin marketplace add hemaher0/docs-skills` and
`/plugin install <plugin>@<marketplace>` do the same. Plugin skills are
namespaced, for example `/openspec:openspec-propose`. Installation records the
plugin in user settings by default; `--scope project` or `--scope local` records
it in the project's shared or local settings instead. Installed plugins are
separate copies from the folders above, so a skill exposed both ways appears
twice.

Claude Code reads `CLAUDE.md`. It reads `AGENTS.md` only when no `CLAUDE.md` or
`CLAUDE.local.md` exists in the working directory or above it (Claude Code
2.1.277 or later) and does not read `AGENTS.local.md` by itself. When a project
keeps shared instructions in `AGENTS.md` and also has a `CLAUDE.md`, add an
`@AGENTS.md` line to `CLAUDE.md`. An instruction in `AGENTS.md` to read
`AGENTS.local.md` keeps local configuration in effect.

## Availability and plugin installation

Use the exact installed name and resource path from the current host's skill
list. A vendor folder or cache entry alone does not establish availability.
Optional routes retain their own fallback when a companion skill is absent.

Project, global, and plugin copies with the same name can all appear. Codex
does not merge them or promise precedence; remove the unintended exposure.

The optional plugin marketplace [manifest](.agents/plugins/marketplace.json)
contains [docs-skills](plugins/docs-skills/.codex-plugin/plugin.json) and
[openspec](plugins/openspec/.codex-plugin/plugin.json). Its identifier is
`hemaher0-docs-skills`. Claude Code reads the same packages through
[.claude-plugin/marketplace.json](.claude-plugin/marketplace.json) and each
plugin's `.claude-plugin/plugin.json`. The host's plugin installation route
creates managed cache copies and can write user-level configuration. Choose
either package independently and follow the host's plugin instructions for that
route.

## Skills

| Documentation skill | Purpose |
| --- | --- |
| [using-docs-skills](plugins/docs-skills/skills/using-docs-skills/SKILL.md) | Route document work to its owner. |
| [coordinating-parallel-document-work](plugins/docs-skills/skills/coordinating-parallel-document-work/SKILL.md) | Coordinate writers and linked work records. |
| [maintaining-work-records](plugins/docs-skills/skills/maintaining-work-records/SKILL.md) | Maintain work history, records, and weekly reports. |
| [auditing-documentation](plugins/docs-skills/skills/auditing-documentation/SKILL.md) | Check documentation against its sources. |
| [maintaining-documentation](plugins/docs-skills/skills/maintaining-documentation/SKILL.md) | Edit repository documentation. |
| [maintaining-diagrams](plugins/docs-skills/skills/maintaining-diagrams/SKILL.md) | Maintain editable diagrams. |
| [curating-reference-notes](plugins/docs-skills/skills/curating-reference-notes/SKILL.md) | Maintain reusable sourced notes. |

| OpenSpec skill | Purpose |
| --- | --- |
| [openspec-explore](plugins/openspec/skills/openspec-explore/SKILL.md) | Investigate a problem or change. |
| [openspec-propose](plugins/openspec/skills/openspec-propose/SKILL.md) | Create a proposal and planning artifacts. |
| [openspec-update-change](plugins/openspec/skills/openspec-update-change/SKILL.md) | Revise an existing plan. |
| [openspec-apply-change](plugins/openspec/skills/openspec-apply-change/SKILL.md) | Implement and verify a change. |
| [openspec-sync-specs](plugins/openspec/skills/openspec-sync-specs/SKILL.md) | Merge delta specifications. |
| [openspec-archive-change](plugins/openspec/skills/openspec-archive-change/SKILL.md) | Verify and archive completed work. |

Skill discovery follows the [official Codex skills documentation](https://learn.chatgpt.com/docs/build-skills).
