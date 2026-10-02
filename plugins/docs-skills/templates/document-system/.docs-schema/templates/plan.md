---
schema_version: 2
id: "{{date}}-{{topic}}-plan"
type: "plan"
lifecycle: "active"
created_at: "{{timestamp_with_offset}}"
updated_at: "{{timestamp_with_offset}}"
work_item_id: "{{work_item_id}}"
---
# {{date}}-{{topic_title}} plan

## Goal

- Outcome and scope: {{observable_outcome_and_boundary}}
- Work identity and current owner: {{existing_work_id_and_owner}}
- Governing spec and revision: {{spec_path_revision_and_requirement_ids}}
- Source decision/design and code identity: {{durable_sources_and_branch_sha}}
- Selected execution workflow: {{one_execution_controller}}

<!-- Reuse the selected active task artifact. If a formal workflow owns it,
link it here without creating a second task list. Otherwise repeat the task
block below as needed. Task N headings/checkboxes support SDD extraction when
SDD is selected; other controllers keep their required native task format.
Make every extracted task self-contained; the selected executor owns workspace allocation. -->

## Tasks

### Task 1: {{deliverable}}

- Spec and revision: {{spec_path_and_material_revision}}
- Purpose and requirement/criterion IDs: {{purpose_and_ids}}
- Owner, authority and scope: {{owner_authority_included_and_excluded_work}}
- Dependencies and required interfaces: {{inputs_task_ids_and_exact_contracts}}
- Files and produced artifact: {{actual_paths}}
- Completion and covering evidence: {{observable_criteria_checks_and_expected_observations}}

- [ ] {{purposeful_action_with_required_context}}
- [ ] {{verification_covering_this_deliverable}}

## Verification

- {{criterion_id}} — {{appropriate_check_or_review_and_expected_observation}}
- Review owner and unresolved decisions: {{owner_and_resolution_before_dependent_work}}

## Progress

- {{timestamp_with_offset}} — {{task_id_state_actual_result_code_sha_and_next_step}}
- Assignment/results and finding dispositions: {{durable_report_and_review_references}}
