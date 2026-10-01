# docs-skills

A Codex plugin marketplace with two independently installable plugins:

| Plugin | Role |
| --- | --- |
| [docs-skills](plugins/docs-skills/.codex-plugin/plugin.json) | Route all document work and preserve request history in a local document schema. |
| [openspec](plugins/openspec/.codex-plugin/plugin.json) | Explore, plan, implement, synchronize, and archive OpenSpec changes. |

## Install and configure

Installing the plugin makes its skills available. **Recording work history
requires the project setup below.**

### 1. Install for a project

Use a repository marketplace and project configuration. Run these commands from
the **target project's root**, with Git access to this repository:

```bash
mkdir -p .agents/vendor .agents/plugins .codex
git clone --branch main https://github.com/hemaher0/docs-skills.git .agents/vendor/docs-skills
```

Create or merge the following into the target project's
`.agents/plugins/marketplace.json`:

```json
{
  "name": "project-skills",
  "plugins": [
    {
      "name": "docs-skills",
      "source": {
        "source": "local",
        "path": "./.agents/vendor/docs-skills/plugins/docs-skills"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Productivity"
    },
    {
      "name": "openspec",
      "source": {
        "source": "local",
        "path": "./.agents/vendor/docs-skills/plugins/openspec"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Productivity"
    }
  ]
}
```

Keep existing marketplace entries. When using multiple skill repositories, add
their entries to the same `plugins` array. Paths resolve from the target
project's root. If its marketplace already has a different `name`, keep that
name and use it in the configuration keys below.

Merge this setting into the target project's `.codex/config.toml`:

```toml
[plugins."docs-skills@project-skills"]
enabled = true
```

The OpenSpec entry makes that plugin available separately. Enable it only if
needed by adding this setting to the same project configuration:

```toml
[plugins."openspec@project-skills"]
enabled = true
```

Open the target project as a trusted project in Codex, restart the app if using
the desktop client, and start a **new Codex session**. Project configuration is
loaded only for trusted projects. The marketplace source and enablement belong
to this project; Codex may still store installed copies in its shared cache.
See the [official repository marketplace and project configuration guide](https://developers.openai.com/plugins/build/plugins).

### 2. Configure each project that needs work records

1. Choose **one canonical work-item repository**: the project repository or
   an existing document repository. Follow its access policy and use its
   configured primary branch; do not create document branches.
2. In the chosen document repository, copy the entire
   [starter `.docs-schema/`](plugins/docs-skills/templates/document-system/.docs-schema/README.md)
   directory **only if no local `.docs-schema/` exists**. Find it under
   `.agents/vendor/docs-skills/plugins/docs-skills/templates/document-system/`
   in the target project. Commit the copied schema in the chosen repository.
   If an older local schema already exists, follow its
   [explicit version 2 migration](plugins/docs-skills/templates/document-system/.docs-schema/README.md)
   before using linked child work items.
3. In the **project root**, merge the
   [project `AGENTS.md` template](plugins/docs-skills/templates/AGENTS.md)
   into `AGENTS.md` without overwriting existing rules. Create or update
   `AGENTS.local.md` from the
   [local configuration template](plugins/docs-skills/templates/AGENTS.local.md)
   and fill in its work-record settings. If the document repository is
   separate, configure its absolute path here.
4. From the chosen document repository, run:

   ```bash
   python3 .docs-schema/records.py validate
   ```

Start a new Codex session after installation and project setup. Installation
does not copy templates or choose a work-item repository for you.

## Update or remove from a project

From the target project's root, update its source checkout:

```bash
git -C .agents/vendor/docs-skills pull --ff-only
```

Restart the app if using the desktop client and start a new Codex session so
the local plugin is refreshed.

To disable it for this project, set
`plugins."docs-skills@project-skills".enabled = false` in
`.codex/config.toml`, using the project's actual marketplace name. To remove
the project setup, remove that configuration entry and only the `docs-skills`
entry from `.agents/plugins/marketplace.json`. Keep other plugins' entries.
Disable or remove `openspec@project-skills` independently in the same way.
Keep the source checkout while either plugin still uses it; remove it separately
once neither plugin needs it.

## Repository documentation

| Skill | Role |
| --- | --- |
| [using-docs-skills](plugins/docs-skills/skills/using-docs-skills/SKILL.md) | Locate the owning work-item node for every request and route document work to its owner. |
| [coordinating-parallel-document-work](plugins/docs-skills/skills/coordinating-parallel-document-work/SKILL.md) | Give parallel tasks linked child records and integrate them without competing writes. |
| [maintaining-work-records](plugins/docs-skills/skills/maintaining-work-records/SKILL.md) | Maintain work-item timelines, specialized local records, lifecycle, and manually requested weekly reports. |
| [auditing-documentation](plugins/docs-skills/skills/auditing-documentation/SKILL.md) | Compare documentation claims with current sources without changing files. |
| [maintaining-documentation](plugins/docs-skills/skills/maintaining-documentation/SKILL.md) | Make a focused repository documentation change when requested or required by repository policy. |
| [maintaining-diagrams](plugins/docs-skills/skills/maintaining-diagrams/SKILL.md) | Create or update an editable diagram that explains a repository document or managed text artifact. |
| [curating-reference-notes](plugins/docs-skills/skills/curating-reference-notes/SKILL.md) | Maintain reusable internal notes in the repository-designated reference area. |

The copied [local schema](plugins/docs-skills/templates/document-system/.docs-schema/README.md)
controls record types, paths, templates, and validation; it works with ordinary
file tools when this plugin is unavailable. The schema also documents its
[template sources](plugins/docs-skills/templates/document-system/.docs-schema/TEMPLATE_SOURCES.md).

## OpenSpec

| Skill | Role |
| --- | --- |
| [openspec-explore](plugins/openspec/skills/openspec-explore/SKILL.md) | Explore an idea or change before deciding its scope. |
| [openspec-propose](plugins/openspec/skills/openspec-propose/SKILL.md) | Create a proposal and its planning artifacts. |
| [openspec-update-change](plugins/openspec/skills/openspec-update-change/SKILL.md) | Revise an existing change's planning artifacts. |
| [openspec-apply-change](plugins/openspec/skills/openspec-apply-change/SKILL.md) | Implement tasks from an OpenSpec change. |
| [openspec-sync-specs](plugins/openspec/skills/openspec-sync-specs/SKILL.md) | Sync a change's delta specs into the main specs. |
| [openspec-archive-change](plugins/openspec/skills/openspec-archive-change/SKILL.md) | Archive a completed change. |

OpenSpec owns product behavior contracts; work items link its artifacts. The
plugin supplies skills but not the CLI. Follow the
[official OpenSpec installation guide](https://github.com/Fission-AI/OpenSpec/blob/main/docs/installation.md).
For a new project, `openspec init --tools none` avoids generating a second set
of tool skills. Keep an existing project's OpenSpec configuration.
