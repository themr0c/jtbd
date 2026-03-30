# Job 14 — Develop and deploy custom dynamic plugins

## Metadata

| Field | Value |
| --- | --- |
| Category | Extend |
| Priority | 🟡 Normal |
| Jira |  |
| Sheet row | Job #14 |
| Status | Not started |

## Job statement

When standard plugins do not meet our needs, I want to develop, package, and deploy custom dynamic plugins so that I can extend the platform with bespoke functionality and logic.

## Current state

No source references recorded.

## Target structure

| Source section | Proposed JTBD heading |
| --- | --- |
| Develop and deploy dynamic plugins | Develop and deploy dynamic plugins in Red Hat Developer Hub |
| Overview of dynamic plugins | Understand the dynamic plugin development lifecycle |
| Prepare your development environment | Prepare the development environment to build plugins |
| Develop a new plugin | Develop a new plugin using the scaffolding tool |
| Convert a custom plugin into a dynamic plugin | Convert existing plugins to dynamic plugins for runtime loading |
| Publish and deploy plugins | Publish plugins to an OCI registry for distribution |
| Verify plugins locally | Verify plugins locally to ensure functionality before deployment |
| Deploy plugins | Deploy custom plugins to the platform |
| Maintain and scale plugins to ensure long-term stability | Maintain and scale plugins to ensure long-term stability |
| Examples | Reference example plugin implementations |
| (Config) Chapter 8. Front-end plugin wiring | Configure front-end wiring to integrate custom UI components |
| 8.3. Defining dynamic routes... | Define dynamic routes to expose new plugin pages |
| 8.6. Using mount points | Use mount points to inject custom content into existing views |
| (Config) Chapter 11. Configuring... Events Module | Configure the Events Module to react to external signals |
| (Config) Chapter 12. Overriding Core Backend... | Override core backend services to customize low-level platform behavior |

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
- [ ] Brief: https://github.com/themr0c/jtbd/blob/main/docs/jobs/job-14.md
