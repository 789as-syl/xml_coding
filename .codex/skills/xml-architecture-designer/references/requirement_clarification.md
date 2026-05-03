# Requirement Clarification

## Goal

Clarify the project from broad intent to concrete design inputs before any downstream stage begins. This step must gather enough confirmed information to support architecture layer confirmation, component confirmation, architecture JSON generation, Draw.io architecture export, external-interface flow confirmation, flow JSON generation, and final multi-page Draw.io export.

The purpose is not to collect every possible detail. The purpose is to understand the project goal, scale, operating scenario, user groups, exposed capabilities, business capabilities, data needs, integration needs, architecture capabilities, and non-functional constraints well enough that later stages can proceed without unsupported assumptions.

## Clarification Order

Follow this order. Do not start by asking detailed technical or non-functional questions.

### 1. Understand the project as a whole

First identify the project's overall context:

- One-sentence project purpose
- Business or operational problem being solved
- Primary application scenario
- Expected project scale, such as prototype, internal tool, departmental system, public product, enterprise system, or platform-level system
- Main user groups and their access patterns
- Expected usage scope, such as single team, single organization, multi-organization, public internet users, partners, or internal operators

The goal of this round is to understand what kind of system is being designed and how large the architecture should be.

### 2. Confirm project goal and boundaries

After the overall context is clear, confirm:

- What outcome the system must achieve
- What is explicitly out of scope
- Whether the system is replacing, integrating with, or extending an existing system
- Whether the architecture should optimize for quick delivery, stable operations, future expansion, or platform reuse

Do not move into detailed business functions until the user has confirmed the project goal and boundary.

### 3. Clarify business functions and external capabilities

Then identify the business capabilities that the architecture must support:

- Main business modules
- Core user workflows
- Important status changes or approval flows
- Required management or operations functions
- Data import, export, reporting, search, notification, or audit functions
- External-facing APIs, user entry points, webhook receivers, partner-facing capabilities, or other exposed abilities
- Background jobs, batch processing, or event-driven processes

For every exposed ability that may need a later flow page, clarify:

- Who or what initiates the flow
- The user-facing entry point or external API name
- The main success path
- Important gateway, authentication, rate limit, validation, service, repository, middleware, storage, or integration steps
- Whether the flow is synchronous, asynchronous, or mixed

Ask for business functions in groups. Avoid turning this into a full product requirements document unless the user asks for that depth.

### 4. Recommend architecture capabilities based on scale and scenario

After the project goal, scale, scenario, users, and business functions are clear, recommend capability-level design options for the user to confirm.

These recommendations should be architecture capabilities, not detailed implementation choices. Mention concrete technologies only as examples when they help the user understand the capability.

Use rules like these:

- If the system has frequent reads, shared sessions, hot data, or repeated expensive queries, recommend a caching capability, such as Redis.
- If the system has high concurrency, burst traffic, slow downstream operations, or workflows that can be processed later, recommend asynchronous processing, such as a message queue.
- If the system has long-running tasks, scheduled synchronization, report generation, or periodic cleanup, recommend a scheduler or background job capability.
- If the system has files, media, generated documents, or large binary data, recommend object storage.
- If the system needs keyword search, filtering across large text, or operational search, recommend a search capability.
- If the system has multiple clients, partner access, unified authentication, traffic control, or API routing, recommend an API gateway capability.
- If the system has multiple user roles, sensitive data, or administrative operations, recommend authentication, authorization, audit logging, and permission management.
- If the system has cross-system integration, data synchronization, or event notification needs, recommend integration adapters and event publishing.
- If the system has public access, high traffic, or business-critical availability, recommend observability, alerting, scaling, and failover capabilities.
- If the system is expected to grow into a platform or multi-module product, recommend modular boundaries and independent service or module ownership.

Present recommendations as choices for the user to confirm. Example style:

```text
Based on the current scale and scenario, I recommend these architecture capabilities:

1. Caching capability for hot data and session acceleration.
2. Async processing capability for slow or bursty workflows.
3. Object storage capability for uploaded files and generated documents.

Please confirm which capabilities are required, optional, or unnecessary.
```

### 5. Clarify data, integration, and flow details

After business capabilities and recommended architecture capabilities are confirmed, clarify:

- Main data entities
- Data volume and growth expectations
- Data retention and archive needs
- Query complexity and reporting needs
- Transaction consistency requirements
- External systems to integrate with
- Integration direction, such as inbound API, outbound API, webhook, event stream, file exchange, or scheduled sync
- Cross-layer flow steps that must be shown later, especially from exposed interface to service, middleware, repository, storage, and external systems

### 6. Clarify non-functional requirements last

Clarify non-functional requirements after the project shape and capabilities are known:

- Performance targets
- Concurrency or traffic expectations
- Availability and recovery expectations
- Security, privacy, audit, and compliance needs
- Scalability expectations
- Deployment environment
- CI/CD, monitoring, logging, tracing, and alerting expectations
- Operational constraints, such as team size, maintenance cost, delivery timeline, or infrastructure limits

## Question Strategy

- Ask 2-4 questions per round.
- Move from broad project context to narrow architecture drivers.
- Do not start with technology stack details unless the user has already made technology constraints clear.
- Recommend capability-level design options based on the project scale and scenario.
- Ask the user to classify recommended capabilities as required, optional, or unnecessary.
- Keep explicit assumptions when the user leaves an answer open.
- Do not proceed to any downstream stage until the project goal, scale, scenario, user groups, exposed capabilities, business functions, data needs, integration needs, key architecture capabilities, and non-functional constraints are confirmed.

## Completion Output

Do not output JSON in this step.

End with a concise confirmed requirements summary:

- Project goal and scope
- Project scale and application scenario
- User groups and access patterns
- Core business functions
- External-facing capabilities and likely flow pages
- Confirmed architecture capabilities
- Main data and integration needs
- Non-functional requirements
- Assumptions and open points

Ask the user to confirm or revise this summary before moving to the next downstream stage.
