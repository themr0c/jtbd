# Job 23 — Govern component compliance

## Metadata

| Field | Value |
| --- | --- |
| Category | Administer |
| Priority | 🟡 Normal |
| Jira |  |
| Sheet row | Job #23 |
| Status | Not started |

## Job statement

When maintaining the software catalog, I want to enforce development standards and monitor component health so that I can ensure all registered software meets our security and quality benchmarks.

## Current state

No source references recorded.

## Target structure

| Source section | Proposed JTBD heading |
| --- | --- |
| Chapter 1. Evaluate project health using Scorecards | Govern component compliance with Scorecards to enforce standards |
| 1.1. Component health... | Scorecard capabilities to evaluate service readiness |
| 1.2.1. Enabling Scorecards | Enable the Scorecard plugin to start monitoring component health |
| 1.2.2. Installing... to view metrics | Configure RBAC for Scorecards to control access to health metrics |
| 1.3.1. Integrating GitHub health metrics... | Integrate GitHub metrics to track code health and pull requests |
| 1.3.2. Integrating Jira health metrics... | Integrate Jira metrics to track issue resolution and project velocity |
| 1.4. Scorecard metric thresholds | Define metric thresholds to standardize health scoring |
| 1.4.4. Standardize... across components | Set global thresholds to enforce consistent quality gates |
| 1.4.5. Override rules... | Override thresholds per entity to accommodate specific project needs |
| (Monitoring component health...) | Monitor component health to identify risks and compliance gaps |

## Rewrite instructions

Each heading must express an action + outcome (why the reader does this step).
Replace noun-phrase titles with outcome-oriented equivalents.
Keep all technical steps intact — only headings change.

Apply to: _Confirm source file with CS_

## Acceptance criteria

- [ ] All headings follow action + outcome pattern
- [ ] No heading is a noun phrase only ("Installation", "Prerequisites")
- [ ] Source sections from the table above are all addressed
- [ ] PR linked to this Jira task
- [ ] Brief: https://github.com/themr0c/jtbd/blob/main/docs/jobs/job-23.md
