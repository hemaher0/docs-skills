---
name: using-docs-skills
description: Use to route repository document discovery, writing, placement, management, modification, or review to its owner, and locate the owning work item when project history capture is configured.
---

# Using Docs Skills

Read effective project instructions and their referenced configuration. Read
root `AGENTS.local.md` when it exists. Shared capture, persistence, audience
and document rules stay in their existing policy sources. When history capture is
configured, follow that policy, locate the canonical work-item repository and
its local `.docs-schema/manifest.json`, and find the owning node by subject and
links. Append to it or create one from the local template. The local schema
wins over this plugin's bundled starter. Report a missing required source
without silently creating a second history. Reader-facing document work that
does not require work records can proceed under its own project rules.
Installation alone does not enable history capture. Installation and project
configuration follow the source README and its templates. Ordinary document
work uses the effective settings and resolves only gaps material to that work. Use
[maintaining-work-records](../maintaining-work-records/SKILL.md)
for configured capture and local record types.

Keep schema paths/types in the canonical repository's `.docs-schema`, formal
store configuration in its native tool, and document commands/conventions in
their existing configuration or project guide. Inspect runtime facts rather
than copying them into local settings. A selected external checkout override
must resolve the same configured canonical repository, not another history.

The work-item tree preserves enough context to reconstruct the goal, accepted
scope, consequential decisions and rationale, progress, evidence, unresolved
issues, and next action. The recorder owns capture criteria and policy defaults;
message length or type does not determine significance. A separate `decision`,
`design`, `plan`, or `tdd` requires its registered creation condition.
When parallel agents need durable history, use
[coordinating-parallel-document-work](../coordinating-parallel-document-work/SKILL.md)
to give independent tasks separate linked work items and one owner for each
overlapping artifact. The local schema controls whether child nodes are
available; do not silently replace an older schema.

## Find the authoritative content

Determine whether the task concerns a product behavior contract, experiment,
local work history, reusable knowledge, public reader-facing documentation, or
a domain-owned artifact. Search existing files and applicable project rules
before choosing a location. Preserve user-designated paths and formats unless
they conflict with the governing owner. Use the following owners:

- **Product behavior:** Identify the project's governing contract. When
  OpenSpec owns it, read the relevant main spec first. For a changed or missing
  contract, use its CLI-selected store, schema, and paths to write delta
  requirements and testable scenarios. Proposal, design, and tasks alone do
  not establish that contract. Check a bug against an existing main spec when
  it violates one. If the active schema cannot provide a required spec, surface
  the configuration problem. Without OpenSpec, follow the project's configured
  contract process; do not replace any required spec with a local plan.
- **Research experiments:** Use research-skills when installed, or the
  project's configured experiment workflow. That workflow owns its scientific
  protocol, template, root, and evidence. Link it from the work item. If none
  is configured, surface the gap instead of inventing a record format. This
  router handles document placement and edits without changing the scientific
  rules or sending the work back in a loop.
- **Local work history and weekly reports:**
  [maintaining-work-records](../maintaining-work-records/SKILL.md) owns them.
- **Reusable sourced note:**
  [curating-reference-notes](../curating-reference-notes/SKILL.md) owns its
  evidence and validity; the local `reference-note` schema owns its path.
- **Reader-facing documentation:**
  [maintaining-documentation](../maintaining-documentation/SKILL.md) owns
  focused edits and retirement; [auditing-documentation](../auditing-documentation/SKILL.md)
  owns factual audits. A requested read-only review remains read-only.
- **Editable diagrams:** [maintaining-diagrams](../maintaining-diagrams/SKILL.md)
  owns representation and verification; the containing artifact keeps its
  owner and path.

Domain workflows still determine their content, authorization, and lifecycle.
When they forward document work here, resolve the correct source and location,
perform the file operation with their rules, then return evidence to the caller.
Use specialized installed workflows or native commands where they own an
artifact, especially OpenSpec. Do not route back and forth indefinitely.

Preserve the chain from original intent and necessary derived requirements to
spec criteria, active tasks, assignment results, review findings, and evidence.
Link existing identities rather than renaming them. A durable `plan` or `design`
can be the selected artifact or retain its decisions; it does not create a
second active plan. Exactly one selected execution workflow controls task
scheduling and review retries. Documentation audit checks claims against
sources; technical review and Git candidate/message review keep their owners.

## Finish

Check the changed document against its owner, sources, format, and links. Run
the local schema validator for changed local records. State which record and
domain artifact were updated and any unresolved configuration or evidence gap.
Product documentation accompanies its implementation in the assigned code
checkout. Canonical work history uses its configured repository, audience, and
persistence policy. Use the project's Git procedure for actual allocation,
commits, integration, and publication; this router does not authorize them.
Keep private history out of public artifacts. Return changed paths, source
revision, checks, and unresolved claims to the requesting owner without
declaring implementation completion or disposing of its temporary records.
