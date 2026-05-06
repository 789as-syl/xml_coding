# Project Requirement Inputs

## Purpose

Use this reference to decide what project information should be inferred, recorded, or clarified before architecture modeling.

First read [project_architecture_json_parameters_and_structure.md](project_architecture_json_parameters_and_structure.md) to understand the target JSON structure: `layers`, layer `child` components, component `feature`, and optional `flows`.

## Why These Inputs Matter

This skill turns early project ideas into a visual architecture baseline.

The final JSON is an intermediate model used to generate Draw.io diagrams that show:

- the whole project architecture: boundaries, layers, components, and capability grouping;
- exposed-interface flows: how users, clients, hosts, schedulers, or external systems enter the project and move through architecture components.

The goal is to make the project structure easier to understand, discuss, develop, maintain, and manage.

Therefore the agent must collect enough context for the agent to derive meaningful layers, components, features, and flow pages.

## Thinking Stance

Think like a product manager preparing architecture clarification.

Do not start from code modules. Start from product intent:

- what problem the project solves;
- who or what uses it;
- what user-visible or consumer-visible capabilities it provides;
- through which interfaces those capabilities are exposed;
- what data, integrations, runtime boundaries, and quality constraints shape delivery.

Then translate that product understanding into architecture-relevant inputs.

## Global-To-Local Analysis Path

### 1. Product goal and scope

Identify what is being built, why it exists, and what belongs inside or outside the project boundary.

Clarify only when the project target, system boundary, or expected diagram scope is unclear.

### 2. Users, actors, and consumers

Identify who or what initiates interaction with the system.

Examples: end users, admins, operators, partner systems, machine clients, CLI users, MCP hosts, SDK consumers, plugin hosts, schedulers, framework callers, or external callbacks.

These define entry points, permission boundaries, trust boundaries, and flow starts.

### 3. Main product scenarios

Identify the main scenarios the architecture should explain.

Focus on core journeys and capability paths, not every detailed user story or edge case.

### 4. Exposed interfaces

Identify how the project is used from the outside.

Examples: Web/mobile/desktop UI, REST/GraphQL/gRPC APIs, webhooks, CLI commands, MCP tools/resources/prompts, SDK methods, package exports, plugin extension points, FFI/ABI entry points, scheduled jobs, or operator actions.

Exposed interfaces are the primary candidates for flow diagrams.

### 5. Capability groups

Group product behavior into stable capabilities that can become JSON `feature` values.

Examples: auth, ingestion, indexing, search, payment, document parsing, code generation, task orchestration, deployment, monitoring, plugin execution.

Clarify when the project description is too vague to identify meaningful capability lanes.

### 6. Architecture-visible responsibilities

Infer components from responsibilities and boundaries.

A responsibility is architecture-visible when it affects interface ownership, business capability, data ownership, runtime behavior, integration role, security boundary, performance behavior, or flow participation.

Ignore helper functions, DTO variants, CRUD variants, UI subcomponents, repository methods, test files, and framework boilerplate unless they change architecture shape.

### 7. Data, state, and artifacts

Identify state or assets that must appear in the architecture.

Examples: SQL/NoSQL stores, object buckets, vector indexes, search indexes, local files, caches, queues, streams, audit logs, archives, generated artifacts, model assets, package bundles, configuration, credentials, or session state.

Clarify only when ownership, persistence, or storage choice changes the diagram.

### 8. External systems and ecosystem

Identify systems outside the project boundary that affect adapters, trust, data ownership, deployment, or flows.

Examples: identity providers, payment gateways, partner APIs, model providers, object storage, search/vector services, registries, hardware backends, browser APIs, file systems, host frameworks, CI/CD systems, or observability backends.

### 9. Runtime, deployment, and operations boundaries

Identify runtime separation only when it affects architecture.

Examples: browser/server split, client/server split, cloud/on-prem split, edge/gateway boundary, containers, Kubernetes, serverless functions, workers, schedulers, async queues, plugins, sandboxes, release pipelines, backup/restore, rollout/rollback, monitoring, or operational controls.

### 10. Architecture-shaping constraints

Capture non-functional constraints only when they alter the architecture.

Examples: security, auditability, multi-tenancy, high availability, latency or throughput budgets, offline mode, compatibility, accessibility, numerical accuracy, isolation, compliance, traceability, or data retention.

### 11. Flow candidates

Select only exposed-interface paths that help explain the baseline.

A good flow candidate has:

- a clear actor or external caller;
- a clear exposed interface;
- a main success path through several architecture components;
- direct value for understanding development or management.

Omit flows when they only repeat the architecture page.

## Infer First

The agent should infer safe working hypotheses before asking questions.

Infer from project wording:

- likely project shape and layer vocabulary;
- likely actors and exposed interfaces;
- likely capability groups;
- likely architecture-visible responsibilities;
- likely data, integration, runtime, deployment, and operations boundaries;
- whether flows will help or create noise.

Use inference to reduce questions. Do not ask for information that can be safely defaulted without changing the final diagram.

## Clarify Only Blocking Gaps

Ask clarification only when the missing answer would materially change at least one final JSON or diagram element:

- selected layers;
- component responsibilities or labels;
- feature grouping;
- exposed interfaces;
- flow inclusion, flow boundaries, or main flow path;
- external systems, integration boundaries, trust boundaries, or data ownership;
- state, data, artifacts, caches, queues, logs, indexes, or generated artifacts;
- runtime, deployment, environment, operations, or packaging boundaries;
- architecture-shaping quality constraints;
- final artifact scope.

Do not clarify details that belong only to PRD expansion, UI layout, API payload fields, database schema, class design, task breakdown, test cases, naming polish, or low-level implementation.

## Sufficiency Rule

Input is sufficient when Step 2 can derive a coherent architecture JSON from:

- user-stated or confirmed product intent;
- architecture-relevant constraints;
- safe internal defaults based on project shape;
- non-blocking assumptions that do not materially change the final architecture or flow diagrams.

When sufficient, proceed to Step 2. Do not continue interviewing for completeness.
