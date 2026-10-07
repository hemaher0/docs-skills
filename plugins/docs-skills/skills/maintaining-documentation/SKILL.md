---
name: maintaining-documentation
description: Use when asked to create, update, or reorganize repository-facing documentation such as setup guides, API explanations, configuration references, or README content. Not for automatic documentation after every code change, research records, release decisions, or OpenSpec change artifacts.
---

# Maintaining Documentation

Produce a repository documentation artifact when the user requests it or the
repository's documented completion policy requires it. Do not infer a new page
or documentation update from every code edit, audit finding, investigation, or
completed task. A question that can be answered in the conversation does not
need a local file.

## Find the source and home

Identify the intended reader and the specific claim or workflow to document.
Read repository guidance, local documentation locations, and neighboring pages.
If a project-local skill owns the target document, apply its ownership and
workspace rules while using this workflow for the requested edit.
Check relevant code, configuration, tests, official interfaces, or user-provided
facts before writing a factual claim. When sources disagree, expose the
conflict instead of choosing a convenient version.

For development finalization, consume the work owner's accepted requirements,
necessary derivations and rationale, actual artifact revision, review outcomes,
and covering evidence. Retain relevant criterion IDs and durable references.
Ask that owner to reconcile missing or conflicting claims before dependent
writing; documentation does not redefine the spec or technical verdict.
Use the implementation's assigned checkout for its accompanying product docs.
Configured work history keeps its separate repository and audience rules.

Keep implemented behavior separate from proposed behavior and verified design
reasons separate from guesses about intent. When a private note informs a public
document, restate only the approved conclusion in terms a reader can understand
without access to that note. Do not copy private paths, raw notes, or secrets.

Edit an existing suitable page first. Create a page when the requested durable
content has no suitable home in the existing structure. Follow the repository's
language, navigation, terminology, and generated-document convention. Do not
assume that every repository uses `docs/`, a changelog, an ADR directory, or a
documentation generator. Replace obsolete instructions instead of layering a
warning over them when the old text is no longer true.

Keep the edit proportional to the requested outcome. Update nearby links,
examples, and navigation only when the change makes them stale. Do not change
implementation code to make documentation claims true; report a code mismatch
as a separate issue. Do not add a branch, worktree, commit, pull request,
release note, TODO, or external mirror as a side effect of documentation work.

Before working records are discarded by their owner, preserve the needed
applied basis and continuation state in the appropriate durable artifacts;
temporary links alone cannot preserve it. Reader-facing pages contain the
facts useful to their audience, while detailed private history stays within
its configured boundary. Return paths, source revision, checks and unresolved
claims to the caller. The development workflow owns subsequent generalization,
affected re-verification/review, and completion; Git owns candidate/message
review and actual commits. This skill adds no independent finalization loop.

When the requested documentation includes a diagram and the current host lists
[maintaining-diagrams](../maintaining-diagrams/SKILL.md), use it for
representation and verification while keeping this document's source and
placement rules. Resolve its exact installed resource from that catalog; the
relative link is documentation, not discovery. A sibling or vendor folder alone
is not availability. When it is not listed, keep the repository's existing
editable format, choose a small Mermaid or text diagram only when no convention
exists, derive every element and relationship from the governing sources, trace
representative paths, and use an existing renderer or syntax check when
available. Report an unverified render; do not install another skill or renderer.

## Verify the result

Re-read changed claims against their sources. Check affected local links,
commands, examples, and navigation with the smallest useful available check.
Use a generator or documentation build when it is the project's source of
truth and the requested update requires it; do not install dependencies or
regenerate unrelated documents merely to complete a small edit. State what
was checked and any material verification gap.

OpenSpec proposals, delta specs, designs, tasks, sync, and archive state remain
owned by the OpenSpec workflow. Use its skill only when the current host lists
it, resolving the exact installed name/resource path from that catalog rather
than an adjacent copy. Otherwise follow the project's native OpenSpec procedure
and CLI-selected paths, instructions, rules, and validation; absence of a
companion skill does not transfer those artifacts to this general documentation
workflow.

For a separately requested internal reference note, use
[curating-reference-notes](../curating-reference-notes/SKILL.md) only when the
current host lists it, resolving the exact installed resource from that catalog
rather than the relative documentation link. Otherwise follow the
repository-designated reference root or registered `reference-note` path and
template with ordinary file tools: update an existing note first, distinguish
verified facts from inference, retain sources and validity bounds, check links,
and validate registered records. Do not read an unlisted skill or place private
working context in reader-facing documentation.
