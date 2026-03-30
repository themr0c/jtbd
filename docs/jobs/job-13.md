# Job 13 — Manage the plugin ecosystem

## Metadata

| Field | Value |
| --- | --- |
| Category | Extend |
| Priority | 🟡 Normal |
| Jira |  |
| Sheet row | Job #13 |
| Status | Not started |

## Job statement

When building a tailored developer platform, I want to discover, install, and manage dynamic plugins so that I can add new capabilities without rebuilding or restarting the core platform.

## Current state

No source references recorded.

## Target structure

| Source section | Proposed JTBD heading |
| --- | --- |
| (Intro) Chapter 1. Plugins in Red Hat Developer Hub | Explore the plugin architecture to understand extension capabilities |
| (Install) Chapter 1. Installing dynamic plugins... | Install dynamic plugins to add functionality without downtime |
| 1.1. Installing dynamic plugins... using the Operator | Install plugins via the Operator to manage extensions declaratively |
| 1.1. Installing dynamic plugins... using the Helm Chart | Install plugins via Helm to integrate with existing chart deployments |
| (Install) 1.2. Dynamic plugins dependency management | Manage plugin dependencies to ensure required resources exist |
| (Install) Chapter 2. Install plugins from OCI registries... | Install plugins from OCI registries to use custom or private extensions |
| (Install) Chapter 6. Extensions in Red Hat Developer Hub | Manage plugins via the Extensions UI to simplify administration |
| 6.1. Viewing available plugins | Browse the plugin marketplace to discover available extensions |

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
- [ ] Brief: https://github.com/themr0c/jtbd/blob/main/docs/jobs/job-13.md
