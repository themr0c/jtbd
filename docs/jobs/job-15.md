# Job 15 — Integrate development and infrastructure tools

## Metadata

| Field | Value |
| --- | --- |
| Category | Extend |
| Priority | 🟡 Normal |
| Jira |  |
| Sheet row | Job #15 |
| Status | Not started |

## Job statement

When integrating our toolchain, I want to configure plugins for CI/CD, virtualization, and infrastructure so that developers can visualize pipelines and workloads directly within the portal.

## Current state

No source references recorded.

## Target structure

| Source section | Proposed JTBD heading |
| --- | --- |
| (Config) Chapter 2 / (Using) Chapter 2: Argo CD | Integrate Argo CD to visualize GitOps deployment statuses |
| (Config) Chapter 6 / (Using) Chapter 6: Tekton | Integrate Tekton to track CI pipeline execution results |
| (Config) Chapter 7 / (Using) Chapter 7: Topology | Integrate Topology to visualize Kubernetes workloads graphically |
| (Config) Chapter 10: Kubernetes custom actions | Configure Kubernetes custom actions to enable scaffolding operations |
| (Config) Chapter 1. Installing Ansible plug-ins... | Integrate Ansible to enable automation workflows |
| (Config) Chapter 9. ServiceNow Custom actions... | Integrate ServiceNow to automate ITSM record management |

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
- [ ] Brief: https://github.com/themr0c/jtbd/blob/main/docs/jobs/job-15.md
