# Project Documentation Configuration

<!-- Merge only project choices not already governed by an existing source.
Shared procedures belong to their skills and the authoritative local schema.
Omit unused/default fields; preserve existing settings. Local filesystem
overrides go in AGENTS.local.md only when needed. -->

## Documentation

- Documentation conventions/configuration source: `<existing guide or configuration>`
- Reference notes root, if not owned by the local schema: `<project-relative location or existing store reference>`
- Reference storage boundary, if explicitly designated: `<project audience/policy reference>`

## Work Records (when configured)

- Work-history capture policy: `<All requests and discussions, established project rule, or Disabled>`
- Canonical work-item repository: `<this project, one shared repository reference, or None>`
- Work-record audience: `<established audience/access policy>`
- Record persistence policy: `<chosen checkpoints and existing Git procedure, or local files only>`

Resolve the same configured repository for this work; a local checkout-path
override must not create a second history. Follow its own Git/access policy.
Product docs accompanying code use the assigned code checkout.

Read the canonical repository's local `.docs-schema/README.md`,
`manifest.json` and relevant template for record operations; `LIFECYCLE.md`
governs its registered state transitions. These local sources remain usable
with ordinary file tools if the plugin is unavailable. Preserve existing local
schemas until explicit migration.

Development/research owners supply governing content, criteria, revision,
evidence, and decisions. Documentation skills own placement, record edits,
reader-facing prose, and factual audits; the selected domain workflow keeps
scheduling, technical verdicts, and temporary retention. Formal contracts
follow the project's designated owner. Git owns actual checkout and history
mutations. Current owners, handoffs, findings and progress live in their work
records rather than configuration.

Read root `AGENTS.local.md` when selected local overrides are present. They
cannot broaden the shared capture, persistence, audience, or permission policy.
