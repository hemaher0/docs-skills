---
schema_version: 2
id: "{{date}}-{{topic}}-tdd"
type: "tdd"
lifecycle: "active"
created_at: "{{timestamp_with_offset}}"
updated_at: "{{timestamp_with_offset}}"
work_item_id: "{{work_item_id}}"
---
# {{date}}-{{topic_title}} TDD

<!-- Use for an actual warranted TDD cycle whose trace needs durable retention.
The registered creation condition does not require a test cycle for every
change. Keep baseline/manual/refactoring verification in the existing work
record or domain report when no TDD cycle applies. Do not invent RED evidence.
Preserve observed results even if work remains incomplete. -->

## Behavior and specification

- {{behavior_and_governing_spec_revision_requirement_or_criterion_id}}

## Test cases

- {{test_id_input_expected_output_and_regression_boundary}}

## RED

- {{test_id_command_observed_failure_reason_timestamp_and_source_revision}}

## GREEN

- {{minimal_change_command_observed_result_and_code_sha}}

## REFACTOR

- {{cleanup_or_not_needed_protected_behavior_and_covering_results}}

## Verification

- {{criterion_id_check_actual_observation_environment_revision_and_evidence}}
- Broader checks only when project policy or affected risk requires them: {{checks_or_not_needed_reason}}
- Remaining limits, findings and current owner: {{actual_limits_and_dispositions}}
