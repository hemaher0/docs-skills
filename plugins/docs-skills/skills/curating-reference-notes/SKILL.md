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
canonical document repository has configured record definitions, follow their registered
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

For a separately requested reader-facing update, use
[maintaining-documentation](../maintaining-documentation/SKILL.md) only when
the current host lists it; a sibling or vendor folder alone is not availability.
Resolve its exact installed resource from that catalog rather than the relative
documentation link. Otherwise follow the repository's documentation rules with
ordinary file tools: edit the existing suitable page from its current source of
truth, keep the change focused, and check affected links and commands. Do not
read or require the unlisted companion. OpenSpec artifacts and managed
experiment records remain under their native or configured workflows. This skill does not make
those updates as a side effect of curating a reference note.

## Verify and finish

Re-read the changed note for accurate provenance, current versus superseded
claims, and enough context for a later reader to continue the work. Check
affected local links and run the local schema validator when present. Follow any
repository-specific review or local commit requirement for this storage area.
Do not infer permission to push, publish, mirror, or change another repository
from a request to maintain a note.
