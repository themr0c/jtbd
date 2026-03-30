# Job 27 — Consult technical specifications and configurations

## Metadata

| Field | Value |
| --- | --- |
| Category | Reference |
| Priority | 🟡 Normal |
| Jira |  |
| Sheet row | Job #27 |
| Status | Not started |

## Job statement

When performing advanced customization or automation, I want to look up authoritative parameters, policies, and plugin details so that I can accurately configure the platform and resolve integration issues without guessing.

## Current state

No source references recorded.

## Target structure

| Source section | Proposed JTBD heading |
| --- | --- |
| (Dynamic plugins) Chapter 1. Plugins in Red Hat Developer Hub | Reference dynamic plugin details to verify support status and configuration paths |
| 1.1. Red Hat supported plugins | Reference Red Hat supported plugins to identify production-ready extensions |
| 1.2. Technology Preview plugins | Reference Technology Preview plugins to evaluate upcoming features |
| 1.2.2. Deprecated plugins | Reference deprecated plugins to plan migration strategies |
| (Configuring plugins) Table 12.1. Environment variables... | Reference core service environment variables to override default backend behavior |
| (Configuring plugins) 10.4. Supported Kubernetes custom actions... | Reference Kubernetes custom actions to define scaffolder templates |
| (Authorization) Chapter 9. Permission policies reference | Reference permission policies to define granular access controls |
| (Implicit) Catalog permissions | Reference Catalog permissions to control entity visibility and management |
| (Implicit) Scaffolder permissions | Reference Scaffolder permissions to restrict template execution |
| (Implicit) RBAC permissions | Reference RBAC permissions to secure policy management |
| (Authorization) 10.2. Conditional policies reference | Reference conditional policy rules to filter resource access dynamically |
| (Implicit) Conditional criteria (allOf, anyOf, not) | Reference conditional criteria to combine multiple access rules |
| (Implicit) Conditional object parameters | Reference conditional object schemas to construct valid policy JSON |
| (Orchestrator) 3.3. Orchestrator plugin permissions | Reference Orchestrator permissions to control workflow access |
| (Scorecards) 1.1.1. Supported Scorecard metrics providers | Reference Scorecard metrics to select appropriate health indicators |
| (Implicit) GitHub metrics | Reference GitHub metrics to monitor pull request activity |
| (Implicit) Jira metrics | Reference Jira metrics to track issue resolution velocity |
| (MCP) 1.4. Using the MCP tools... | Reference MCP tool parameters to configure AI client interactions |
| 1.4.1. ... Software Catalog data | Reference Software Catalog tool parameters to filter entity retrieval |
| 1.4.2. ... TechDocs MCP tools | Reference TechDocs tool parameters to retrieve documentation content |

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
- [ ] Brief: https://github.com/themr0c/jtbd/blob/main/docs/jobs/job-27.md
