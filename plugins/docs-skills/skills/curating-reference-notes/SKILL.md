---
name: curating-reference-notes
description: Use when asked to create, update, or retire reusable internal reference notes in a repository-designated area such as references/. Not for merely reading sources, answering a question, reader-facing documentation, OpenSpec artifacts, or managed research experiment records.
---

# Curating Reference Notes

Maintain sourced facts or methods that multiple work items can reuse. Keep
task-specific decisions and discussion in the work item. Create a note when
the user requests a durable reference or the local schema's `reference-note`
creation condition is met. When history capture is configured, follow it in
the owning work item even if no separate reference note is created.

## Choose the location and scope

Read repository and local instructions before writing. When the configured
canonical document repository has `.docs-schema`, follow its registered
`reference-note` path, template, metadata, and validity fields. Otherwise
follow the user or repository's designated reference root. Check its
visibility and whether it lives in a separate repository, then follow that
area's access and persistence rules.

Update an existing note on the same subject first. Create a focused new note
when the requested reusable context has no suitable home. Keep raw tool output,
transient work logs, and unrelated sources out of the note. Link primary
sources or record enough provenance to distinguish what was observed, inferred,
decided, and left unresolved. Preserve dates or conditions when they determine
whether a conclusion is still valid.

## Keep the record useful

When new evidence changes a conclusion, revise the affected part and mark the
superseded judgment. Do not treat publication of one conclusion as a reason to
discard other still-useful context. Retire or archive a whole note only when
its role has ended and the repository's policy permits that action. Do not
copy private source text, local identifiers, secrets, or sensitive data into
a public document.

Reader-facing repository documentation uses
[maintaining-documentation](../maintaining-documentation/SKILL.md) when that
separate update is requested. OpenSpec artifacts and managed experiment
records remain under their owning workflows. This skill does not make those
updates as a side effect of curating a reference note.

## Verify and finish

Re-read the changed note for accurate provenance, current versus superseded
claims, and enough context for a later reader to continue the work. Check
affected local links and run the local schema validator when present. Follow any repository-specific review or local commit
requirement for this storage area. Do not infer permission to push, publish,
mirror, or change another repository from a request to maintain a note.
