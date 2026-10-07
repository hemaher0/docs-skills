# docs-skills

This repository contains two independently selectable skill collections:

| Collection | Source root | Role |
| --- | --- | --- |
| [docs-skills](plugins/docs-skills/skills/) | `plugins/docs-skills/skills/` | Route and maintain repository documentation, diagrams, reference notes, and configured work records. |
| [openspec](plugins/openspec/skills/) | `plugins/openspec/skills/` | Explore, plan, implement, synchronize, and archive OpenSpec changes. |

Codex discovers repository skills in `.agents/skills/` and user-wide skills in
`$HOME/.agents/skills/`. The procedures below keep the native repository in a
`vendor/` checkout so its packaged templates remain available, then expose only
the selected complete skill directories through relative symbolic links. Do not
link individual files or the collection root.

The OpenSpec collection requires the native OpenSpec CLI. This repository does
not install it. Follow the
[OpenSpec installation guide](https://github.com/Fission-AI/OpenSpec/blob/main/docs/installation.md)
and run `openspec --version` before invoking an OpenSpec skill. The packaged
OpenSpec skill metadata was generated for CLI 1.8.0; preserve the native CLI's
own store, schema, and compatibility checks.

## Install for a project

Run these commands from the target project's root. The clone command deliberately
fails when `.agents/vendor/docs-skills` already exists so it cannot replace an
existing checkout.

```bash
mkdir -p .agents/vendor .agents/skills
git clone --branch main https://github.com/hemaher0/docs-skills.git .agents/vendor/docs-skills
```

Choose documentation and OpenSpec skills independently. For a selective install,
link each complete skill folder you want. These examples select one skill from
each collection and preserve an existing destination:

```bash
if [ -e .agents/skills/maintaining-documentation ] || [ -L .agents/skills/maintaining-documentation ]; then
  printf '%s\n' '.agents/skills/maintaining-documentation already exists; leaving it unchanged' >&2
else
  ln -s ../vendor/docs-skills/plugins/docs-skills/skills/maintaining-documentation .agents/skills/maintaining-documentation
fi

if [ -e .agents/skills/openspec-propose ] || [ -L .agents/skills/openspec-propose ]; then
  printf '%s\n' '.agents/skills/openspec-propose already exists; leaving it unchanged' >&2
else
  ln -s ../vendor/docs-skills/plugins/openspec/skills/openspec-propose .agents/skills/openspec-propose
fi
```

Replace the final directory name and target with any name in the collection
tables below. Do not use `ln -sf`: an existing file, directory, or broken link
may belong to another installation.

As an alternative, expose every documentation skill with this all-skills block:

```bash
(
  set -eu
  for skill_dir in .agents/vendor/docs-skills/plugins/docs-skills/skills/*; do
    skill_name=${skill_dir##*/}
    destination=.agents/skills/$skill_name
    if [ -e "$destination" ] || [ -L "$destination" ]; then
      printf '%s\n' "$destination already exists; no links created" >&2
      exit 1
    fi
  done
  for skill_dir in .agents/vendor/docs-skills/plugins/docs-skills/skills/*; do
    skill_name=${skill_dir##*/}
    ln -s "../vendor/docs-skills/plugins/docs-skills/skills/$skill_name" ".agents/skills/$skill_name"
  done
)
```

Expose every OpenSpec skill independently with this block:

```bash
(
  set -eu
  for skill_dir in .agents/vendor/docs-skills/plugins/openspec/skills/*; do
    skill_name=${skill_dir##*/}
    destination=.agents/skills/$skill_name
    if [ -e "$destination" ] || [ -L "$destination" ]; then
      printf '%s\n' "$destination already exists; no links created" >&2
      exit 1
    fi
  done
  for skill_dir in .agents/vendor/docs-skills/plugins/openspec/skills/*; do
    skill_name=${skill_dir##*/}
    ln -s "../vendor/docs-skills/plugins/openspec/skills/$skill_name" ".agents/skills/$skill_name"
  done
)
```

Run both all-skills blocks to expose all thirteen skills. Running one does not
select anything from the other collection.

### Configure the project when needed

Reader-facing document work can use the project's existing documentation rules;
installing a documentation skill does not enable work-history capture. If the
project chooses work records, first configure its canonical record repository,
capture policy, audience, and persistence policy. Merge the relevant fields from
[`AGENTS.md`](plugins/docs-skills/templates/AGENTS.md) and
[`AGENTS.local.md`](plugins/docs-skills/templates/AGENTS.local.md) into the
project's effective instructions while preserving existing settings.

The canonical record repository owns its `.docs-schema/`. When it is this target
project, run the following from the project root. The starter is copied only
when no local path or link already exists:

```bash
(
  set -eu
  if [ -e .docs-schema ] || [ -L .docs-schema ]; then
    printf '%s\n' '.docs-schema already exists; leaving the local schema unchanged' >&2
    exit 1
  fi
  cp -R .agents/vendor/docs-skills/plugins/docs-skills/templates/document-system/.docs-schema .docs-schema
  python3 .docs-schema/records.py validate
)
```

The copied directory becomes project-owned and authoritative. Never symlink it
to the vendor checkout, overwrite it during an update, or copy it into a second
repository for the same work history. Migrations require an explicit local
decision and the procedure in its own README.

When the configured canonical repository is a different existing repository,
run this from the target project after replacing the destination placeholder:

```bash
(
  set -eu
  skill_source=$PWD/.agents/vendor/docs-skills/plugins/docs-skills/templates/document-system/.docs-schema
  canonical_record_root=/absolute/path/to/canonical-record-repository
  if [ -e "$canonical_record_root/.docs-schema" ] || [ -L "$canonical_record_root/.docs-schema" ]; then
    printf '%s\n' "$canonical_record_root/.docs-schema already exists; leaving it unchanged" >&2
    exit 1
  fi
  cp -R "$skill_source" "$canonical_record_root/.docs-schema"
  cd "$canonical_record_root"
  python3 .docs-schema/records.py validate
)
```

Do not create another history store merely because its checkout is elsewhere.

For a project newly adopting OpenSpec, initialize its native store from the
project root:

```bash
openspec init --tools none
```

`--tools none` avoids generating duplicate tool skills. Keep an existing
`openspec/` configuration and do not reinitialize or migrate it merely because
these skills were installed.

### Invoke and verify the project install

Invoke a selected skill by its name, for example `$maintaining-documentation`
or `$openspec-propose` in Codex. Other clients may expose the same skill with a
slash command.

Check each selected link and its entrypoint from the project root:

```bash
readlink .agents/skills/maintaining-documentation
test -f .agents/skills/maintaining-documentation/SKILL.md
readlink .agents/skills/openspec-propose
test -f .agents/skills/openspec-propose/SKILL.md
```

Use the current host's skill listing to verify actual availability. A checkout
under `vendor/` or a plugin cache entry is not itself an available skill. Codex
normally detects skill changes automatically; start a new session or restart the
client if the current session does not refresh.

When one skill optionally routes to another, it resolves and uses the exact name
and resource path in that host listing. It does not open an adjacent vendor or
cache copy, because project, global, and plugin installations can be different
revisions.

Project and user-wide skills with the same `name` can both appear; their contents
are not merged, and a project link does not promise to hide a global copy. Remove
or rename the unintended duplicate rather than relying on precedence.

### Update or remove the project install

Update the project-owned source checkout without recreating its links:

```bash
git -C .agents/vendor/docs-skills pull --ff-only
```

Verify the linked `SKILL.md` files and current host listing again. Automatic
change detection normally refreshes the skills; start a new session or restart
the client if needed. Updating the vendor checkout never updates a copied local
`.docs-schema/`.

Before removing a selected skill, inspect the exact link, then unlink only that
destination:

```bash
readlink .agents/skills/maintaining-documentation
unlink .agents/skills/maintaining-documentation
```

Repeat for the other links intentionally installed from this checkout. Keep
`.agents/vendor/docs-skills` while any selected link or project procedure still
uses its skills or templates. Removing skill links does not remove project-owned
records, `.docs-schema/`, OpenSpec artifacts, or project instructions.

## Install globally

A global install makes the selected skills discoverable to projects for that
user. It does not configure work records, documentation policy, OpenSpec, Git,
or publication for any project.

Clone the native source under the user-wide `.agents` root. Do not replace an
existing checkout:

```bash
mkdir -p "$HOME/.agents/vendor" "$HOME/.agents/skills"
git clone --branch main https://github.com/hemaher0/docs-skills.git "$HOME/.agents/vendor/docs-skills"
```

Select documentation and OpenSpec skills independently. For example:

```bash
if [ -e "$HOME/.agents/skills/maintaining-documentation" ] || [ -L "$HOME/.agents/skills/maintaining-documentation" ]; then
  printf '%s\n' "$HOME/.agents/skills/maintaining-documentation already exists; leaving it unchanged" >&2
else
  ln -s ../vendor/docs-skills/plugins/docs-skills/skills/maintaining-documentation "$HOME/.agents/skills/maintaining-documentation"
fi

if [ -e "$HOME/.agents/skills/openspec-propose" ] || [ -L "$HOME/.agents/skills/openspec-propose" ]; then
  printf '%s\n' "$HOME/.agents/skills/openspec-propose already exists; leaving it unchanged" >&2
else
  ln -s ../vendor/docs-skills/plugins/openspec/skills/openspec-propose "$HOME/.agents/skills/openspec-propose"
fi
```

As an alternative, expose all documentation skills:

```bash
(
  set -eu
  for skill_dir in "$HOME"/.agents/vendor/docs-skills/plugins/docs-skills/skills/*; do
    skill_name=${skill_dir##*/}
    destination=$HOME/.agents/skills/$skill_name
    if [ -e "$destination" ] || [ -L "$destination" ]; then
      printf '%s\n' "$destination already exists; no links created" >&2
      exit 1
    fi
  done
  for skill_dir in "$HOME"/.agents/vendor/docs-skills/plugins/docs-skills/skills/*; do
    skill_name=${skill_dir##*/}
    ln -s "../vendor/docs-skills/plugins/docs-skills/skills/$skill_name" "$HOME/.agents/skills/$skill_name"
  done
)
```

Expose all OpenSpec skills independently:

```bash
(
  set -eu
  for skill_dir in "$HOME"/.agents/vendor/docs-skills/plugins/openspec/skills/*; do
    skill_name=${skill_dir##*/}
    destination=$HOME/.agents/skills/$skill_name
    if [ -e "$destination" ] || [ -L "$destination" ]; then
      printf '%s\n' "$destination already exists; no links created" >&2
      exit 1
    fi
  done
  for skill_dir in "$HOME"/.agents/vendor/docs-skills/plugins/openspec/skills/*; do
    skill_name=${skill_dir##*/}
    ln -s "../vendor/docs-skills/plugins/openspec/skills/$skill_name" "$HOME/.agents/skills/$skill_name"
  done
)
```

Run both blocks for all thirteen skills. Existing destinations stop the relevant
block before it creates any links.

### Configure projects that use global skills

Global discovery does not make configuration global. Each project retains its
own documentation rules and native OpenSpec store. If a project enables work
records, merge the global checkout's instruction templates into that project's
effective instructions and copy a project-owned schema only when absent:

```bash
(
  set -eu
  if [ -e .docs-schema ] || [ -L .docs-schema ]; then
    printf '%s\n' '.docs-schema already exists; leaving the local schema unchanged' >&2
    exit 1
  fi
  cp -R "$HOME/.agents/vendor/docs-skills/plugins/docs-skills/templates/document-system/.docs-schema" .docs-schema
  python3 .docs-schema/records.py validate
)
```

For a new OpenSpec project, run `openspec init --tools none` in that project.
Keep existing project configuration. Installing globally does not install the
OpenSpec CLI or initialize any project.

### Invoke, verify, update, or remove the global install

Invoke skills by name as above. Check selected global links directly:

```bash
readlink "$HOME/.agents/skills/maintaining-documentation"
test -f "$HOME/.agents/skills/maintaining-documentation/SKILL.md"
readlink "$HOME/.agents/skills/openspec-propose"
test -f "$HOME/.agents/skills/openspec-propose/SKILL.md"
```

Confirm the current host lists the selected skills. A vendor or cache directory
alone does not establish availability. Skill changes are normally detected
automatically; use a new session or restart the client if they are not refreshed.
Optional routes use the exact installed resource reported by that listing. The
duplicate-name behavior described for project installs also applies here.

Update only the global source checkout:

```bash
git -C "$HOME/.agents/vendor/docs-skills" pull --ff-only
```

Before removing a selected global skill, inspect and unlink its exact destination:

```bash
readlink "$HOME/.agents/skills/maintaining-documentation"
unlink "$HOME/.agents/skills/maintaining-documentation"
```

Keep the global vendor checkout while any remaining global link uses it. Removing
it does not change project-local links, schemas, records, OpenSpec stores, or
instructions.

## Optional plugin compatibility

The repository also retains native plugin manifests for clients that support
plugin marketplaces. The marketplace identifier is `hemaher0-docs-skills`, and
the two independent packages are `docs-skills` and `openspec`:

```bash
codex plugin marketplace add https://github.com/hemaher0/docs-skills.git
codex plugin add docs-skills@hemaher0-docs-skills
codex plugin add openspec@hemaher0-docs-skills
```

Use only the package or packages wanted. Plugin commands and the plugin browser
may write user-level client configuration and managed cache copies, so this is a
separate installation route rather than part of either `.agents/skills`
procedure. Do not enable the same skill names through both routes unless duplicate
entries are intentional. Plugin installation still does not configure a project,
copy `.docs-schema/`, install the OpenSpec CLI, initialize OpenSpec, enable
history capture, authorize Notion or other external writes, run workloads, or
authorize Git publication.

## Skill reference

### Documentation skills

| Skill | Role |
| --- | --- |
| [using-docs-skills](plugins/docs-skills/skills/using-docs-skills/SKILL.md) | Route document work and locate owning work records under configured capture. |
| [coordinating-parallel-document-work](plugins/docs-skills/skills/coordinating-parallel-document-work/SKILL.md) | Assign linked child records and exclusive writers for parallel document work. |
| [maintaining-work-records](plugins/docs-skills/skills/maintaining-work-records/SKILL.md) | Maintain work-item timelines, registered local records, lifecycle, and requested weekly reports. |
| [auditing-documentation](plugins/docs-skills/skills/auditing-documentation/SKILL.md) | Compare repository documentation with its current sources without editing. |
| [maintaining-documentation](plugins/docs-skills/skills/maintaining-documentation/SKILL.md) | Make focused repository documentation changes. |
| [maintaining-diagrams](plugins/docs-skills/skills/maintaining-diagrams/SKILL.md) | Create or update editable diagrams in owned text artifacts. |
| [curating-reference-notes](plugins/docs-skills/skills/curating-reference-notes/SKILL.md) | Maintain reusable sourced notes in a repository-designated reference area. |

The copied [local schema](plugins/docs-skills/templates/document-system/.docs-schema/README.md)
controls work-record types, paths, templates, lifecycle, and validation and remains
usable with ordinary file tools when no documentation skill is available.

### OpenSpec skills

| Skill | Role |
| --- | --- |
| [openspec-explore](plugins/openspec/skills/openspec-explore/SKILL.md) | Explore a change or problem before or during planning. |
| [openspec-propose](plugins/openspec/skills/openspec-propose/SKILL.md) | Create a change and the artifacts needed for implementation. |
| [openspec-update-change](plugins/openspec/skills/openspec-update-change/SKILL.md) | Revise an existing change's planning artifacts. |
| [openspec-apply-change](plugins/openspec/skills/openspec-apply-change/SKILL.md) | Implement and verify tasks from a change. |
| [openspec-sync-specs](plugins/openspec/skills/openspec-sync-specs/SKILL.md) | Intelligently merge delta specs into main specs without archiving. |
| [openspec-archive-change](plugins/openspec/skills/openspec-archive-change/SKILL.md) | Verify, synchronize when needed, and archive a completed change. |

When OpenSpec owns product behavior, its main specs and delta specs remain the
contract. Work records link those artifacts instead of duplicating their design
or tasks. One execution controller governs an active scope, and installation
alone does not authorize implementation, commits, publication, or external sync.

Skill discovery and symbolic-link behavior follow the
[official Codex skills documentation](https://learn.chatgpt.com/docs/build-skills).
