---
name: maintaining-diagrams
description: Use when creating or updating an editable diagram in a repository document to explain components, dependencies, interactions, control flow, or state changes. Also use for a diagram in a managed text artifact when its owning workflow permits the edit. Not for scientific plots, UI mockups, or rendered image assets.
---

# Maintaining Diagrams

Create or update a diagram when the user requests one or when an authorized
document update specifically needs a visual explanation. A code or design
change alone does not require a diagram. If the user only asks for an
explanation, respond in the conversation unless a durable artifact is
requested or required by repository policy.

## Establish the question and owner

Identify what the reader should learn and which document owns the diagram.
Read that document, its applicable repository rules, and the sources that
define the relationships being shown. Use code and configuration for current
implementation, and the governing specification for intended behavior.
Distinguish implemented, proposed, and uncertain relationships; do not infer
design intent solely from code.

For an OpenSpec artifact, follow its OpenSpec workflow for artifact paths,
schema rules, and write approval. For a research record or another managed
artifact, follow its owner. This skill guides the diagram's representation
and verification; it does not authorize a new artifact or override its owner.

## Choose a useful representation

- Use a structure or dependency diagram for components and ownership.
- Use a sequence diagram when order and participants matter.
- Use a flowchart for decisions, branches, and repeated steps.
- Use a state diagram for transitions and their triggering conditions.

Show only the elements and relationships needed to answer the reader's
question. Use names that can be traced to the source or are clearly defined
in the document. Make the meaning of arrows and conditions clear. Include
failure, retry, or cancellation paths when they affect the point being
explained; do not invent a path to fill a visual gap.

Keep an existing diagram's editable source format. For a new text diagram in
Markdown with no repository convention, Mermaid is a reasonable default when
the intended reader can render it. Otherwise use the repository's supported
format or a simple text diagram. Keep one source of truth when a diagram is
referenced from multiple pages. Update nearby explanation and links that the
diagram change makes stale; avoid unrelated layout or naming changes.

## Verify

Trace representative paths and relationships against the governing sources.
Check labels, direction, ordering, conditions, and the distinction between
current and proposed behavior. Use an existing diagram renderer or syntax
check when available and relevant. If rendering cannot be checked, state that
limit and review the editable source directly. Do not install a renderer or
create generated image files solely for a small diagram edit.

Report the diagram location and what it explains. Do not change code, Git
state, release artifacts, or external mirrors as a side effect.
