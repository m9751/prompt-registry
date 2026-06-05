---
id: PRM-CDXP-001
title: PowerShell Security Audit Framework — Endpoint Discovery Design
domain: systems-architecture
source_format: Text specification (compliance control IDs + scope description)
target_orchestrator: Codex (via Claude Code Agent dispatch — subagent_type="codex:codex-rescue")
downstream_consumer: Principal Systems Engineer / SRE
version: 1.0.0
last_updated: 2026-06-05
hosted_url: https://raw.githubusercontent.com/m9751/prompt-registry/main/prompts/systems-architecture/PRM-CDXP-001_ps-security-audit-framework.md
use_for: Design a non-remediating PowerShell endpoint discovery script for auditing security posture across application control/CLM, security policy, audit policy/telemetry, and JEA endpoint configuration
---

## Overview

Produces a highly detailed engineering design specification for a read-only PowerShell endpoint discovery script. Grounded in the smokin-knowledge PowerShell domain (5 hard rules + Q-series reference files). Covers Q16 (AppControl/CLM), Q39 (SecurityPolicyDsc), Q40 (AuditPolicy/telemetry), and Q44–Q47 (JEA).

This prompt is dispatched to Codex via Claude Code Agent dispatch. *Registry JSON appends a feedback block after the primary output — score it after reviewing Codex's output, not any self-score Codex may emit.*

## Prompt

```
# Role and Context

Act as a Principal Systems Engineer and Site Reliability Architect specializing in Windows Enterprise Security and PowerShell security architecture.

Design an operational framework for inventorying and auditing the configuration, effective security state, telemetry health, and bypass resilience of PowerShell execution environments across a hybrid Windows enterprise.

The framework will support the following compliance-control areas:

* Q16 — Application Control for Business and Constrained Language Mode
* Q39 — SecurityPolicyDsc and core OS/security-policy state
* Q40 — AuditPolicyDsc and PowerShell telemetry validation
* Q44–Q47 — Just Enough Administration endpoint and Role Capability discovery

---

# Knowledge Foundation — smokin-knowledge PowerShell Domain

Before reasoning about any PowerShell pattern, implementation, or recommendation, apply the following grounded knowledge from the m9751/smokin-knowledge repository. This is the authoritative source of production-pattern truth for this codebase. Do not substitute generic training-set defaults where these rules apply.

## 5 Hard Rules (PowerShell 7.4+, forward-compatible to 7.5+)

1. `pwsh` not `powershell.exe`. Win10/11 ships PS 5.1 as `powershell.exe`. Use `pwsh` (7.4+) — newer syntax (??, &&, ||, ForEach-Object -Parallel, ConvertFrom-Json -AsHashtable) is unavailable in 5.1. If a script must target 5.1, mark it explicitly with a comment header.
2. Trap on Ctrl+C in long-running workers. Task Scheduler kills with STATUS_CONTROL_C_EXIT (0xC000013A / return code 3221225786). Wrap the worker body in `trap { ... ; break }` and emit a shutdown heartbeat. Reference: q1-worker-template-annotated.md, q2-task-scheduler-crash-0xc000013a.md.
3. Prefer `clean { ... }` over `finally { ... }` in advanced functions (PS 7.3+). `clean` is a pipeline-lifecycle block that runs reliably inside advanced functions even on Ctrl+C. For script-scope cleanup (no advanced function wrapper), `finally` remains acceptable — add a one-line comment noting why `clean` was not used. Reference: q5-worker-death-postmortem.md.
4. Encoding: `utf8NoBOM` explicitly. PS 5.1 default is UTF-16 LE BOM; PS 7+ default is utf8NoBOM but DO NOT rely on it — pass `-Encoding utf8NoBOM` explicitly to Set-Content/Out-File/Add-Content/Export-* (CSV / Clixml / etc.). Mixed-BOM files break downstream tooling. Reference: q8-encoding-paths-line-endings.md.
5. `Get-WinEvent -FilterHashtable` over `-FilterXPath`. FilterHashtable is faster, less error-prone, and survives PS version drift. Reference: q7-decision-trees.md, q9-streams-under-task-scheduler.md.

## Key Reference Files (cite as evidence source in findings)

When flagging any finding that touches the patterns below, cite the relevant Q-file as the evidence source rather than generic PowerShell documentation:

| Q-file | Topic |
|--------|-------|
| q1-worker-template-annotated.md | Canonical worker scaffold — Ctrl+C trap, shutdown heartbeat, clean block |
| q2-task-scheduler-crash-0xc000013a.md | Task Scheduler kill behavior, exit code 3221225786, STATUS_CONTROL_C_EXIT |
| q3-bash-to-powershell-idioms.md | Bash to PowerShell idiom translation, common conversion anti-patterns |
| q4-anti-patterns.md | PowerShell anti-patterns to flag during review |
| q5-worker-death-postmortem.md | Worker death analysis patterns, death spiral indicators |
| q7-decision-trees.md | Decision trees for Get-WinEvent, runspace patterns, engine selection |
| q8-encoding-paths-line-endings.md | Encoding, path handling, line-ending behavior on Win11 |
| q9-streams-under-task-scheduler.md | stdout/stderr/stream behavior under Task Scheduler |
| q10-memory-performance.md | Memory and performance patterns for long-running scripts |
| q11-utc-timestamps.md | UTC timestamp handling, timezone-safe patterns |
| q13-filesystemwatcher-cim-startprocess.md | FileSystemWatcher, CIM, Start-Process patterns and failure modes |
| q15-pwsh-remoting-winrm.md | Remoting, WinRM, session configuration patterns |

## Anti-Pattern Anchors from smokin-knowledge

The following anti-patterns are documented in q4-anti-patterns.md and must be flagged if observed:

* Using `finally` in advanced functions instead of `clean` when Ctrl+C resilience is required
* Relying on PS 7+ encoding defaults without explicit `-Encoding utf8NoBOM`
* Using `-FilterXPath` where `-FilterHashtable` is available
* Missing Ctrl+C trap in Task Scheduler workers
* Using `powershell.exe` instead of `pwsh` in 7.4+ contexts
* FileSystemWatcher without bounded error recovery (see q13)

---

# Primary Objective

Produce a highly detailed engineering design specification for a non-remediating endpoint discovery script.

The script must inventory and evaluate the current state of the listed controls without modifying security configuration, policy, services, registry values, files, permissions, JEA endpoints, or endpoint registrations.

Do not provide remediation commands or state-changing security code.

# Permitted Side Effects

The script is primarily read-only, but the following explicitly bounded side effects are permitted:

1. Emit the final structured inventory payload to a pre-existing local Windows Event Log source.
2. Generate approved, benign PowerShell telemetry-validation markers when active telemetry testing is enabled.
3. Generate an approved, benign AMSI behavioral-validation marker when active AMSI testing is enabled.

"Approved" means a static string literal with no executable payload — no eval, no encoded commands, no network calls, no filesystem writes.

The design must clearly separate:

* passive discovery,
* active validation,
* unsupported or externally unverifiable assertions.

The script must never create a new event source, event log, registry key, policy, JEA endpoint, scheduled task, service, or configuration file.

# Deployment and Architectural Constraints

## Local Execution Model

Assume the script executes locally on each endpoint through an existing management or security agent, such as:

* Microsoft Intune,
* Microsoft Configuration Manager,
* EDR,
* SIEM collection agent,
* another local management platform.

Assume execution normally occurs as NT AUTHORITY\SYSTEM.

Do not design around:

* centralized Domain Admin credentials,
* remote interactive administration,
* a central runner authenticating to endpoints over WinRM,
* new network services or transport dependencies.

## Production Safety

The script must be safe for high-utilization production servers.

Prefer low-overhead operations such as:

* direct registry reads,
* safe configuration-file reads,
* targeted Get-CimInstance queries,
* native session-state inspection,
* bounded event-log queries,
* file metadata and signature inspection.

Avoid:

* recursive full-disk searches,
* broad unbounded event-log scans,
* process injection,
* memory modification,
* long-running performance tests,
* expensive WMI enumeration,
* loading or executing untrusted configuration files.

Every potentially expensive operation must include a bounded scope, timeout, maximum-result limit, or equivalent control.

# Output and Telemetry Export

Compile findings into a flat, structured JSON payload suitable for SIEM ingestion.

Write the final payload to a pre-existing custom Windows Event Log source using a designated event ID, such as 9999.

Do not write findings to:

* network file shares,
* remote APIs,
* new local databases,
* newly created event sources,
* newly created event logs.

The design must address Windows Event Log payload-size limits and specify how to handle oversized results through bounded chunking, correlation identifiers, or summarized evidence.

# Required Result Model

Every evaluated item must return one of the following explicit states:

* Pass
* Fail
* NotApplicable
* NotObserved
* AccessDenied
* Unsupported
* Indeterminate

Missing, inaccessible, ambiguous, or unverifiable evidence must never be reported as Pass.

Every finding must include:

* control identifier,
* engine or scope evaluated,
* evidence source,
* observed value,
* effective-state interpretation,
* validation method,
* confidence level,
* limitations,
* result state,
* timestamp,
* correlation identifier where applicable.

# PowerShell Engine Coverage

## Dual-Engine and Multi-Installation Discovery

The design must independently evaluate:

* Windows PowerShell 5.1,
* every discovered PowerShell 7+ installation,
* side-by-side PowerShell installations,
* versioned installations,
* preview installations where discoverable,
* packaged or non-default installations where technically observable.

Do not assume PowerShell 7 exists only in a default installation path.

For each discovered engine, identify:

* executable path,
* engine version,
* architecture,
* $PSHOME,
* configuration sources,
* applicable policy sources,
* effective configuration precedence,
* telemetry channel,
* language mode,
* App Control relationship,
* AMSI capability,
* JEA applicability.

## Configuration Precedence

Do not describe Windows PowerShell 5.1 as exclusively registry-driven or PowerShell 7+ as exclusively JSON-driven.

The design must inspect and explain the precedence of all relevant configuration sources, including:

* machine-level registry policy,
* PowerShell Core registry policy,
* per-installation powershell.config.json,
* applicable per-user configuration,
* engine defaults,
* environment variables where relevant.

Because the script normally executes as SYSTEM, explicitly distinguish:

* machine scope observed,
* SYSTEM account scope observed,
* interactive-user scopes inspected,
* interactive-user scopes not inspected.

Do not represent the SYSTEM account's CurrentUser state as representative of all users.

# Pillar-by-Pillar Engineering Map

For each control pillar, provide:

* exact registry paths,
* configuration-file locations,
* event-log channels,
* WMI or CIM classes,
* environment variables,
* executable or installation-discovery methods,
* required privileges,
* expected values,
* effective-precedence logic,
* passive checks,
* optional active validation checks,
* result interpretation,
* limitations and confidence level.

# Q16 — Application Control and Constrained Language Mode

Design discovery logic to determine:

* whether Application Control for Business, AppLocker, or another system-wide application-control mechanism is present,
* whether the mechanism is configured,
* whether it appears active,
* whether the PowerShell engine reports Constrained Language Mode,
* whether observed Constrained Language Mode appears system-policy-enforced or manually imposed,
* whether Windows PowerShell 5.1 and every discovered PowerShell 7+ installation behave consistently,
* whether bypass-relevant engine or host differences exist.

Do not treat the following as equivalent:

* execution policy,
* manually constrained runspaces,
* App Control-backed system lockdown,
* a single process reporting ConstrainedLanguage.

Clearly distinguish configured state, observed state, effective state, and behaviorally validated state.

# Q39 — Core Security Policy and Engine Configuration

Design read-only discovery for the relevant operating-system, registry, PowerShell, and security-policy settings associated with SecurityPolicyDsc-aligned controls.

For each setting:

* identify the authoritative evidence source,
* identify conflicting sources,
* explain precedence,
* report whether the setting is configured, effective, inaccessible, or indeterminate.

Do not infer effective security state solely from the presence of a registry value.

# Q40 — Audit Policy and PowerShell Telemetry

Evaluate the configuration and operational state of relevant audit and PowerShell telemetry controls, including:

* Script Block Logging,
* Module Logging,
* transcription where applicable,
* protected event logging where applicable,
* relevant Windows audit policy,
* event-log channel state,
* event accessibility,
* event retention or capacity indicators,
* engine-specific differences.

## Script Block Logging Self-Test

Do not report Script Block Logging as operational solely because policy settings are enabled.

Specify a bounded self-test that:

1. Identifies the engine being tested.
2. Records the current newest event record ID or equivalent bookmark.
3. Generates a unique, benign correlation marker.
4. Executes the marker through the target engine.
5. Queries only events created after the bookmark.
6. Confirms that the expected event exists and contains the correlation marker.
7. Separately reports: policy configured, channel enabled, event generated, event readable, marker matched, forwarding status locally unverifiable.

The design must account for permissions, event latency, log rollover, engine-specific channels, and timeout behavior.

# AMSI Integrity and Behavioral Assurance

Design a layered AMSI assessment that separates:

## Configuration Evidence

* registered AMSI providers,
* installed security products,
* service state,
* provider file paths,
* file versions,
* digital signatures,
* observable policy state,
* engine AMSI support.

## Optional Behavioral Evidence

When explicitly authorized, perform a benign AMSI behavioral-validation test and record whether the expected security-product behavior was observed.

## Integrity Limitations

Do not claim that a PowerShell process can conclusively prove that:

* its own AMSI integration is unmodified,
* its process memory is unpatched,
* the AMSI provider chain is uncompromised,
* the kernel or security product is trustworthy.

Report the collected evidence, assurance level, and externally unverifiable properties.

# Q44–Q47 — JEA Deep Discovery

Discover and evaluate registered JEA endpoints and their effective capabilities.

Inspect:

* registered session configurations,
* associated .pssc session-configuration files,
* referenced .psrc Role Capability files,
* role definitions,
* user and group mappings,
* virtual-account configuration,
* group-managed service-account use where applicable,
* transcript settings,
* visible commands,
* visible functions,
* visible providers,
* allowed external commands,
* parameter restrictions,
* ValidateSet,
* ValidatePattern,
* wildcard exposure,
* command aliases,
* executable exposure,
* commands capable of launching processes,
* commands capable of creating new or unrestricted runspaces,
* commands whose parameters enable indirect privilege escalation.

Do not inspect only command names.

Do not dot-source, import, invoke, or otherwise execute discovered .pssc, .psrc, or other configuration files solely for discovery.

Use the safest available non-executing parsing method. Report files that cannot be safely or completely interpreted as Indeterminate.

# Required Anti-Pattern and False-Assurance Analysis

For each control pillar, identify implementation patterns that could produce incomplete, misleading, or falsely compliant results.

At minimum, address the following anti-patterns:

1. Configuration presence treated as proof of effectiveness.
2. Registry-only PowerShell discovery.
3. Default-installation-path assumptions.
4. SYSTEM context treated as representative of interactive users.
5. A single LanguageMode observation treated as proof of App Control-backed enforcement.
6. Execution policy treated as a security boundary.
7. Logging configured treated as logging operational.
8. Local process self-attestation treated as authoritative integrity proof.
9. JEA command-name review without parameter and effective-capability review.
10. Unsafe execution of configuration files during discovery.
11. Wildcard or broad JEA exposure treated as benign.
12. Missing evidence treated as compliant.
13. One PowerShell version's result applied to all installed engines.
14. Event generation treated as proof that SIEM forwarding succeeded.
15. File presence treated as proof that a policy or JEA configuration is registered and active.

For every detected anti-pattern, report:

* affected control,
* observed evidence,
* why it creates false assurance or bypass risk,
* confidence level,
* whether external validation is required.

Do not provide remediation commands.

# Evidence-to-Conclusion Requirement

Every conclusion must include a traceable evidence-to-conclusion chain:

1. Raw evidence source.
2. Observed value.
3. Applicable precedence or interpretation rule.
4. Passive or active validation method.
5. Known limitations.
6. Confidence rating.
7. Final result state.

The design must make it possible for an independent reviewer to understand why each control passed, failed, or remained indeterminate.

# Required Deliverable Structure

Produce the final engineering design using the following sections:

1. Executive architecture summary.
2. Trust boundaries and operating assumptions.
3. Passive-discovery versus active-validation model.
4. PowerShell engine and installation-discovery strategy.
5. Pillar-by-pillar engineering map for Q16, Q39, Q40, and Q44–Q47.
6. Exact evidence sources and configuration-precedence rules.
7. Telemetry self-test design.
8. AMSI assurance model and limitations.
9. JEA deep-inspection design.
10. Anti-pattern and false-assurance analysis.
11. Structured JSON event schema.
12. Performance, timeout, and failure-handling controls.
13. Coverage gaps and externally unverifiable assertions.
14. Evidence-to-conclusion examples.
15. Pseudocode-level discovery workflow.

Do not provide remediation code.

Do not claim certainty where the endpoint cannot provide authoritative evidence.

Prefer explicit limitations and Indeterminate findings over unsupported compliance conclusions.
```
