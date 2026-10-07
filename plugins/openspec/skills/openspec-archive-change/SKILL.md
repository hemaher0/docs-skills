---
name: openspec-archive-change
description: Archive a completed change in the experimental workflow. Use when the user wants to finalize and archive a change after implementation is complete.
allowed-tools: Bash(openspec:*)
license: MIT
metadata:
  author: openspec
  version: "1.0"
  generatedBy: "1.8.0"
---

Archive a completed change in the experimental workflow.

Work-item updates below follow the project's work-history capture policy;
a configured storage location does not enable capture. Requested spec sync,
archive operations, and preservation of native change artifacts do not depend
on enabling work-item history.

For an adopted change after a code branch merge, verify the actual merge SHA,
implementation, tests, and selected delta requirements; sync only adopted
requirements and verify the main specs before archive. For an abandoned code
branch, do not sync its unadopted requirements. Record the abandonment reason,
last SHA, and useful evidence in the configured work item, then use the
existing archive procedure's warnings and choices without inventing a main
contract. `archived` means preserved history. Route work-item updates through a
current host-listed documentation skill or the local `.docs-schema` and normal
file tools otherwise. Do not create a document branch.
If a change mixes adopted and unadopted requirements, reconcile its delta
artifacts first so the sync input describes only adopted behavior; preserve
the discarded rationale in the work item or archived change history.

A companion skill is available only when the current host's skill catalog lists
it. Resolve and read/invoke the exact installed name and resource path reported
by that catalog. A vendor checkout, sibling folder, symlink target, or plugin
cache entry is not availability. For required history capture, use a listed
documentation skill; otherwise apply the configured policy with the
project-owned manifest, lifecycle, template, checker, and ordinary file tools.
Do not read or install an unlisted skill. Spec synchronization never depends on
another skill: the full native fallback is included in step 4.

**Store selection:** If the user names a store (a store is a standalone OpenSpec repo registered on this machine) or the work lives in one, run `openspec store list --json` to discover registered store ids, then pass `--store <id>` on the commands that read or write specs and changes (`new change`, `status`, `instructions`, `list`, `show`, `validate`, `archive`, `doctor`, `context`, `view`). Once selected, treat `--store <id>` as sticky for the rest of the workflow. Every unscoped example of those commands below is shorthand: before running it, append the flag. For example, run `openspec status --change "<name>" --json --store "<id>"`, not the unscoped form shown below. Other commands do not take the flag. Hints printed by commands already carry the flag; keep it on follow-ups. Without a store, commands act on the nearest local `openspec/` root.

`<capability-path>` is the spec directory relative to `specs/` (for example, `user-auth` or `identity/user-auth`). Preserve the full path from each delta spec when resolving its main spec.

**Input**: Optionally specify a change name. If omitted, check if it can be inferred from conversation context. If vague or ambiguous you MUST prompt for available changes.

**Steps**

1. **Select the change**

   If a name is provided, use it. Otherwise:
   - Infer from conversation context if the user mentioned a change
   - Auto-select if only one active change exists
   - If ambiguous, run `openspec list --json` to get available changes and ask the user to select one

   When prompting, show only active changes (not already archived).
   Include the schema used for each change if available.

   Always announce: "Using change: <name>" and how to override (e.g., `$openspec-archive-change (Codex) or /openspec-archive-change (other agents) <other>`).

   **Load current archive inputs before the existing archive checks:**

   After resolving the selected change and planning root, run:
   ```bash
   openspec instructions archive --change "<name>" --json
   ```
   Keep the same selected-root flags on this command. This lookup is advisory and
   optional: it only supplies extra prompt inputs, so it must never block archiving.
   If it exits non-zero or returns invalid JSON — for example on an older CLI that
   does not support this command yet — continue the archive workflow with no
   context and no operation guidance. Do not report an error and do not stop.

   A successful response may omit both optional fields. Treat `context` as a
   required prompt-level input: read and consider it, and apply relevant project
   facts, conventions, and constraints. Treat `operationGuidance` as optional
   additive advice: read and consider every entry, and follow entries that are
   applicable and compatible with the built-in archive workflow.

   Keep both fields separate from built-in steps, explicit user choices, resolved
   paths, CLI checks, and command contracts. If context conflicts with one of those
   controlling inputs, report the conflict and preserve the controlling value. If
   guidance is inapplicable or conflicts with a controlling input, do not follow it
   and explain why. Do not infer replacement paths, skipped prompts, or flags from
   either field, and do not copy their text verbatim into specs, change artifacts,
   or archive summaries unless the user separately asks for it. These are
   prompt-level behavior contracts, not enforceable checks.

2. **Check artifact completion status**

   Run `openspec status --change "<name>" --json` to check artifact completion.

   Parse the JSON to understand:
   - `schemaName`: The workflow being used
   - `planningHome`, `changeRoot`, `artifactPaths`, and `actionContext`: path and scope context
   - `artifacts`: List of artifacts with their status (`done`, `skipped`, or other)

   **If any artifacts are neither `done` nor `skipped`** (skipped artifacts satisfy the requirement - the change declares skip_specs):
   - Display warning listing incomplete artifacts
   - Ask the user to confirm they want to proceed
   - Proceed if user confirms

3. **Check task completion status**

   Read the tasks file (typically `tasks.md`) to check for incomplete tasks.

   Count tasks marked with `- [ ]` (incomplete) vs `- [x]` (complete).

   **If incomplete tasks found:**
   - Display warning showing count of incomplete tasks
   - Ask the user to confirm they want to proceed
   - Proceed if user confirms

   **If no tasks file exists:** Proceed without task-related warning.

4. **Assess delta spec sync state**

   Use `artifactPaths.specs.existingOutputPaths` from status JSON as the only
   delta-spec source. If the `specs` entry is missing or
   `existingOutputPaths` is empty, proceed without a sync prompt and do not infer
   delta specs from other artifacts.

   **If delta specs exist:**
   - Compare each delta spec with its corresponding main spec at `<planningHome.root>/openspec/specs/<capability-path>/spec.md` (use the store-aware `planningHome.root` from step 2, not a hardcoded repo path)
   - Determine what changes would be applied (adds, modifications, removals, renames)
   - Show a combined summary before prompting

   **Prompt options:**
   - If adopted product requirements still need sync: "Sync now", "Cancel".
     Do not archive adopted behavior while its main spec is stale.
   - If the linked code branch was abandoned and requirements were not adopted:
     "Archive without syncing", "Cancel". Preserve the reason and evidence in
     the work item; the main spec must remain unchanged.
   - If already synced: "Archive now", "Sync anyway", "Cancel"

   Route on the answer:
   - "Cancel" — stop, do not archive
   - "Archive without syncing" or "Archive now" — proceed only in the
     corresponding case above
   - "Sync now" or "Sync anyway" — sync, then verify (below)
   - Anything else — ask again rather than archiving

   Before a selected sync writes any main spec, run
   `openspec instructions specs --change "<name>" --json` once with the same
   selected-root flags. Require a zero exit status and valid artifact-instruction
   JSON. If the lookup fails or returns invalid JSON, report the error and stop
   before writing any main spec or moving the change. A valid response with omitted
   `rules` is the no-rules case. Apply returned `rules` only to the content and
   form of main specs produced by this merge; do not use them as archive guidance,
   change CLI behavior, or copy the rule text into any output file.

   Perform the sync synchronously before moving `changeRoot`. If the current
   host lists `openspec-sync-specs`, it may be invoked inline with the complete
   `existingOutputPaths` list and the fetched specs-rule snapshot; wait for it
   and do not fetch the snapshot again. If the host does not list that skill,
   do not read its sibling folder. Perform this native fallback directly:

   1. For every path in `artifactPaths.specs.existingOutputPaths`, derive its
      complete `<capability-path>` beneath the change's `specs/` directory. Read
      the whole delta and corresponding main spec at
      `<planningHome.root>/openspec/specs/<capability-path>/spec.md`. Do not
      infer, omit, or add delta paths.
   2. Merge semantic requirement blocks into a single `## Requirements` section
      in the main spec. For ADDED, add a missing requirement; when its name
      already exists, update it as an implicit MODIFIED, or make no change when
      it already matches. For MODIFIED, apply its statement and named scenario
      changes while preserving every existing scenario or other content the
      delta does not change; a target that already carries those changes is a
      no-op. For REMOVED, remove the complete named requirement block, or treat
      its absence as an already-applied no-op. For RENAMED, replace the exact
      FROM heading with TO and preserve its body. If FROM is absent and TO is
      present, accept a no-op only after verifying that TO's body and the
      delta-named content match the intended already-applied result. Stop on
      unresolved states such as an actual MODIFIED target that is absent, an
      ambiguous requirement name, both rename names being present, neither
      rename name being present, or a rename destination whose body conflicts.
      Never copy delta operation headings into a main spec and never guess.
   3. For a new capability, create the main spec only from valid ADDED
      requirements. Use the delta's `## Purpose` body when present, otherwise a
      brief visible TBD Purpose, then add one canonical `## Requirements`
      section. For an existing capability, its Purpose is authoritative; do not
      replace it with a delta Purpose. Apply the fetched artifact `rules` to the
      content and form without copying their text into the spec.
   4. If removal would leave no requirement blocks, delete the main `spec.md`
      and then its empty capability directory only when all of these hold: this
      run actually removed the final requirement; the pre-sync file was not
      already empty; it has a `## Purpose`; every other nonblank line belongs to
      its title, Purpose, Requirements header, canonical requirements,
      scenarios, or fenced examples; the change's `.openspec.yaml` declares
      `retire_capabilities: true`; and the resolved file remains inside the real
      main specs root without following a capability-directory symlink outside
      it. If any condition fails, leave that capability unchanged, report the
      exact blocker (including a missing marker when that is the only issue),
      and stop before archive. Never leave an empty `## Requirements` section.
   5. Preserve main-spec order and all content not named by the delta. The merge
      must be idempotent: repeating it yields no further change. After all
      selected paths are merged, run `openspec validate --specs` with the same
      selected-root flags. A non-zero result stops the archive; do not claim the
      sync succeeded or move the change.
   6. Retain a merge summary for the archive result: requirements
      added/modified/removed/renamed per capability, every new spec with a TBD
      Purpose, and every retired `spec.md` with its prior Purpose. For a retired
      file in the caller's checkout, include a pasteable checkout-scoped Git
      recovery command; for a selected external store, give store-scoped
      recovery guidance instead.

   Whether the host-listed skill or native fallback performed the merge, keep it
   synchronous. A background sync can lose its input when step 5 moves the
   change.

   Then re-run the comparison from the top of this step against every capability that has a delta spec in `artifactPaths.specs.existingOutputPaths` — not only the ones the sync reports it touched. A successful sync leaves nothing left to apply, so each capability must now read as already synced:
   - ADDED requirements present
   - MODIFIED requirements carrying the scenario and description changes named in the delta, with their other scenarios intact
   - REMOVED requirements gone — and where this sync retired a capability (removed its last requirement, leaving `## Requirements` empty), its main spec deleted rather than left empty; a spec the sync deliberately kept and reported is also a match
   - RENAMED requirements present under the new name and absent under the old one

   If the sync failed, or any capability does not match, report what differs and stop — do not archive. Nothing has moved and `changeRoot` is intact, so the user can fix the mismatch or re-run the sync and start the archive again.

5. **Perform the archive**

   Create an `archive` directory under `planningHome.changesDir` if it doesn't exist:
   ```bash
   mkdir -p "<planningHome.changesDir>/archive"
   ```

   Generate the target name: use the change name as-is when it already starts with a `YYYY-MM-DD-` prefix; otherwise prepend the current date as `YYYY-MM-DD-<change-name>`. Never stack a second date (same rule as `openspec archive`).

   **Check if target already exists:**
   - If yes: Fail with error, suggest renaming existing archive or using different date
   - If no: Move `changeRoot` to the archive directory

   ```bash
   mv "<changeRoot>" "<planningHome.changesDir>/archive/<target-name>"
   ```

6. **Display summary**

   Show archive completion summary including:
   - Change name
   - Schema that was used
   - Archive location
   - Whether specs were synced (if applicable)
   - Note about any warnings (incomplete artifacts/tasks)

**Output On Success**

```markdown
## Archive Complete

**Change:** <change-name>
**Schema:** <schema-name>
**Archived to:** the archive path derived from `planningHome.changesDir`/<target-name>/
**Specs:** <"✓ Synced to main specs" only if the step 4 verification passed; otherwise "No delta specs" or "Sync skipped">

<"All artifacts complete. All tasks complete." — or, if archived with warnings, list them instead (e.g. "Archived with 2 incomplete tasks")>
```

**Guardrails**
- Announce the selected change; prompt for selection when it is ambiguous
- Use artifact graph (openspec status --json) for completion checking
- Don't block archive on warnings - just inform and confirm
- Preserve .openspec.yaml when moving to archive (it moves with the directory)
- Show clear summary of what happened
- If sync is requested, use a host-listed `openspec-sync-specs` skill inline or
  perform step 4's native intelligent merge; never read or require an unlisted
  sibling skill
- Never archive while a spec sync is still in flight — run the sync inline and verify the main specs before moving `changeRoot`
- If delta specs exist, always run the sync assessment and show the combined summary before prompting
- Apply relevant runtime context and report conflicts; operation guidance remains advisory
- Consider every guidance entry and explain any inapplicable or conflicting advice
- Existing CLI checks, resolved paths, prompts, and command contracts are unchanged
- Artifact rules constrain only the specs being written and are never operation guidance
- Never copy runtime context, operation guidance, or artifact-rule text verbatim into output files
