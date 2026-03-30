# Job 26 — Maintain platform versioning

## Metadata

| Field | Value |
| --- | --- |
| Category | Upgrade |
| Priority | 🟡 Normal |
| Jira |  |
| Sheet row | Job #26 |
| Status | Not started |

## Job statement

When a new version is released, I want to upgrade the Red Hat Developer Hub instance using the Operator or Helm chart so that I can access the latest features, security patches, and performance improvements without disrupting the environment.

## Current state

No source references recorded.

## Target structure

| Source section | Proposed JTBD heading |
| --- | --- |
| (Upgrading) Chapter 1. Upgrading the Red Hat Developer Hub Operator | Upgrade using the Operator to update the managed instance via OLM |
| (Upgrading) 1. ... Approval Strategy (Implicit) | Approve the InstallPlan to trigger the Operator update |
| (Upgrading) Chapter 2. Upgrading the Red Hat Developer Hub Helm Chart | Upgrade using the Helm chart to apply the latest release artifacts |
| (Upgrading) 2. ... OpenShift Container Platform CLI (Implicit) | Apply Helm upgrades via CLI to automate version updates |
| (Orchestrator) 3.2. Upgrading the Orchestrator plugin from 1.7 to 1.8 | Upgrade the Orchestrator plugin to ensure compatibility with RHDH 1.8 |
| (AKS) Upgrade | Upgrade the Helm deployment on AKS to apply the latest chart version |
| (GKE) To upgrade your deployment | Upgrade the Helm deployment on GKE to apply the latest chart version |

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
- [ ] Brief: https://github.com/themr0c/jtbd/blob/main/docs/jobs/job-26.md
