# Job 07 — Configure core infrastructure

## Metadata

| Field | Value |
| --- | --- |
| Category | Configure |
| Priority | 🟡 Normal |
| Jira |  |
| Sheet row | Job #7 |
| Status | Not started |

## Job statement

When tailoring the platform deployment, I want to configure storage, networking, and compute resources so that the instance integrates correctly and securely with my IT infrastructure.

## Current state

No source references recorded.

## Target structure

| Source section | Proposed JTBD heading |
| --- | --- |
| Chapter 1. Provisioning and using your custom... configuration | Provision custom configurations to persist settings on restart |
| 1.1. Provisioning your custom... | Provision config maps and secrets to inject external configurations |
| 1.2. Using the... Operator to run Developer Hub... | Run the Operator-based instance to apply custom resources |
| 1.2.1. Injecting extra files... | Inject extra files and variables to configure container environments |
| 1.3. Using the... Helm chart to run Developer Hub... | Run the Helm-based instance to apply custom values |
| Chapter 2. Red Hat Developer Hub default configuration | Analyze default resource topology to understand the deployment footprint |
| 2.1. ... default configuration guide | Review default Kubernetes resources to identify created objects |
| 2.2. Automated Operator features | Leverage automated Operator metadata to ensure resource discovery |
| 2.3. Mounts for default Secrets and... PVCs | Configure mount paths to customize secret and storage locations |
| Chapter 3. Configuring external PostgreSQL databases | Connect to an external PostgreSQL database to ensure production data persistence |
| 3.1. Configuring ... using the Operator | Configure the Operator connection to use an external database |
| 3.2. Configuring ... using the Helm Chart | Configure the Helm chart connection to use an external database |
| 3.3. Migrating local databases... | Migrate local data to external storage to preserve existing state |
| Chapter 4. Configuring... deployment when using the Operator | Patch the Operator deployment to customize resource limits and sidecars |
| Chapter 5. Configuring high availability... | Configure high availability to ensure service reliability during outages |
| Chapter 6. Running... behind a corporate proxy | Configure corporate proxy settings to enable external network access |
| 6.1. The NO_PROXY exclusion rules | Define NO_PROXY rules to bypass the proxy for internal traffic |
| 6.2/6.3 Configuring proxy information... | Set proxy environment variables to route traffic correctly |
| Chapter 7. Configuring... TLS connection... | Configure TLS connections to secure internal cluster communication |
| Chapter 8. Using the dynamic plugins cache | Configure the dynamic plugins cache to improve instance startup time |
| 8.2/8.3 Creating a PVC for the dynamic plugin cache... | Create cache PVCs to persist plugin data across restarts |
| Chapter 9. Enabling the... plugin assets cache | Enable plugin asset caching to improve frontend load performance |

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
- [ ] Brief: https://github.com/themr0c/jtbd/blob/main/docs/jobs/job-07.md
