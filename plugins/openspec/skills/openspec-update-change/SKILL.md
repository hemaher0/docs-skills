---
name: openspec-update-change
description: Update an OpenSpec change by revising its existing planning artifacts and keeping them coherent with one another. Use when the user wants to revise a change's plan, fold new decisions into it, or reconcile its artifacts after an edit. Never edits code.
allowed-tools: Bash(openspec:*)
license: MIT
metadata:
  author: openspec
  version: "1.0"
  generatedBy: "1.8.0"
---

Revise a change's existing planning artifacts and keep them coherent. This
workflow edits planning artifacts; other workflows own creation of missing
artifacts and implementation. Continue through those owners only when the
user's existing request authorizes the next activity and required gates are
satisfied. A planning revision alone does not authorize code changes.

When the revision changes product behavior, compare it with the relevant main
spec and revise the existing delta spec's requirements and scenarios too. If a
needed spec artifact does not exist, this update workflow cannot create it:
report that gap and use the CLI-supported artifact creation workflow. Do not
claim a proposal/design/tasks-only change is complete or substitute a local
plan. Follow the project's work-history capture policy; a configured storage
location does not enable capture. When that policy requires it, append the
revision and source links to the owning work item through docs-skills when
available, otherwise through the local
`.docs-schema` and normal file tools.

**Store selection:** If the user names a store (a store is a standalone OpenSpec repo registered on this machine) or the work lives in one, run `openspec store list --json` to discover registered store ids, then pass `--store <id>` on the commands that read or write specs and changes (`new change`, `status`, `instructions`, `list`, `show`, `validate`, `archive`, `doctor`, `context`, `view`). Once selected, treat `--store <id>` as sticky for the rest of the workflow. Every unscoped example of those commands below is shorthand: before running it, append the flag. For example, run `openspec status --change "<name>" --json --store "<id>"`, not the unscoped form shown below. Other commands do not take the flag. Hints printed by commands already carry the flag; keep it on follow-ups. Without a store, commands act on the nearest local `openspec/` root.

**Input**: Optionally specify a change name. If omitted, check if it can be inferred from conversation context. If vague or ambiguous you MUST prompt for available changes.

`$openspec-continue-change (Codex) or /openspec-continue-change (other agents)` is an expanded-profile workflow and may not be installed. Before suggesting it anywhere below, verify that it is available. If it is unavailable, `openspec status --change "<name>" --json` shows the next artifact and `openspec instructions "<artifact-id>" --change "<name>" --json` explains how to create it.

**Steps**

1. **Select the change**

   If a name is provided, use it. Otherwise:
   - Infer from conversation context if the user mentioned a change
   - Auto-select if only one active change exists
   - If ambiguous, run `openspec list --json` to get available changes sorted by most recently modified, and ask the user to select one

   When prompting, present a manageable set of relevant active changes as options,
   including a contextually relevant older change when needed. Show:
   - Change name
   - Schema (from `schema` field if present, otherwise "spec-driven")
   - Status (e.g., "0/5 tasks", "complete", "no tasks")
   - How recently it was modified (from `lastModified` field)

   Recommend a change only when the request or established work context supports
   that choice. Modification time helps order the list; it does not establish intent.

   Always announce: "Using change: <name>" and how to override (e.g., `$openspec-update-change (Codex) or /openspec-update-change (other agents) <other>`).

2. **Get the change's artifacts**
   ```bash
   openspec status --change "<name>" --json
   ```
   Parse the JSON to understand current state. The response includes:
   - `schemaName`: The workflow schema being used (e.g., "spec-driven")
   - `artifacts`: Array of artifacts with their status ("done", "skipped", "ready", "blocked")
   - `isPlanningComplete`: Boolean indicating if all planning artifacts are complete. Older CLI versions expose the same value as `isComplete`.
   - `planningHome`, `changeRoot`, `artifactPaths`, and `actionContext`: path and scope context. Use these instead of assuming repo-local paths.

   The artifact ids and paths come from the active schema - do NOT assume them, and do NOT branch on hardcoded artifact names. Custom schemas must work unchanged.

   The files to edit are `artifactPaths.<id>.existingOutputPaths` - the concrete files that exist on disk, already glob-expanded for glob artifacts (e.g. `specs/**/*.md`). Do NOT write to `resolvedOutputPath`: for a glob artifact it is still the glob pattern, not a real file.

3. **Understand the request**
   - If the user asked for a specific revision ("the design now uses X"), that is the starting edit.
   - If they only said "update" / "make this coherent", treat it as a coherence review: read the existing artifacts and check them against each other for contradictions, gaps, and duplication.

4. **Read and reconcile**
   - Read the artifact(s) the request touches and the change's other existing artifacts.
   - Apply the requested edit. Then check every other existing artifact against it - in ANY direction: an edit to a later artifact may require revising an earlier one, not only the other way around. Build order is a useful reading order, not a constraint on which artifacts may be revised.
   - Note everything that is now inconsistent, missing, or contradictory.
   - Revise only files that already exist (`existingOutputPaths`). Do NOT create artifacts that don't exist yet, and do NOT invent new files under a glob artifact - note them and point the user to `$openspec-continue-change (Codex) or /openspec-continue-change (other agents)` to create them.
   - If the change is already coherent, say so and make no edits.

5. **Apply authorized revisions, one artifact at a time**
   - Explain the revisions and their purpose, then apply edits within the
     user's existing authorization. A request to revise or reconcile the
     artifacts already covers the necessary edits in that scope.
   - Ask only for a material unresolved choice, work outside that scope, or a
     project-required approval not already granted. Wait before its dependent
     edits; unrelated authorized work may continue.
   - If the user rejects a revision, do not write it - leave that artifact unchanged.
   - When a substantial rewrite is needed, get that artifact's rules and template first:
     ```bash
     openspec instructions "<artifact-id>" --change "<name>" --json
     ```

6. **Continue authorized next steps, or provide guidance**
   Preserve responsibility boundaries: the next workflow owns its activity.
   If the user already requested that activity, continue through its available
   workflow or CLI-supported alternative after required gates. Otherwise
   report it as a recommendation without performing it.
   - Artifacts still missing -> route authorized creation to the available
     artifact workflow or CLI-supported alternative; otherwise explain what
     remains to be created.
   - Existing implementation -> compare it with the revised plan and identify
     needed code changes; use the apply workflow when implementing them is
     already authorized, otherwise recommend it. Checked task boxes alone do
     not establish that the revised behavior is implemented or verified.
   - Everything implemented and verified -> use the archive workflow only when
     archival is requested; otherwise recommend it as the next option.

**Output**

After each invocation, show:
- Which artifacts were revised (and which proposed revisions were rejected)
- Anything deferred to `$openspec-continue-change (Codex) or /openspec-continue-change (other agents)` (not-yet-created artifacts or files)
- Where the change stands and the recommended next command

**Guardrails**
- When a requested revision includes a diagram, use an available document workflow to route diagram representation and verification; otherwise follow the project's diagram convention. Keep the existing artifact paths, rules, and authorization boundaries in control.
- Edit planning artifacts in this workflow. If code changes are already
  authorized, transition to the apply workflow after reconciling the plan and
  required gates; otherwise report the implementation needed without changing code.
- Use the artifact ids and paths reported by `openspec status`; never branch on hardcoded artifact names.
- Edit only the concrete files in `existingOutputPaths`; never write to a glob `resolvedOutputPath`.
- Do not advance the build frontier: no new artifacts, no new files under glob artifacts - that is `$openspec-continue-change (Codex) or /openspec-continue-change (other agents)`'s job.
- Preserve existing authorization and explicit rejections. Resolve only
  missing material decisions or required approvals before dependent edits.
- If the request changes the change's *intent* rather than refining it, first verify whether the expanded-profile `$openspec-new-change (Codex) or /openspec-new-change (other agents)` workflow is available. If it is, recommend starting fresh with `$openspec-new-change (Codex) or /openspec-new-change (other agents)` (the "Update vs. Start Fresh" heuristic). If it is unavailable, ask for a distinct unused change name and recommend `openspec new change "<new-change-name>"` instead.
