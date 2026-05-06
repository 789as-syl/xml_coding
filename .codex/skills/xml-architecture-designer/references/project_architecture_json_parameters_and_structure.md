# Project Architecture JSON Parameters And Structure

## Purpose

Explain the parameters and structure of `.xml/project_architecture.json`.

## 1. layers

`layers` is the ordered architecture structure.

Each layer represents one architecture boundary or concern, such as users, interfaces, services, adapters, data, runtime, deployment, or operations.

## 2. Layer components and feature

Each layer has `child` components.

A component is an architecture-visible responsibility inside that layer.

`feature` groups related components across layers into the same capability lane.

Use `feature: null` for shared, structural, operational, or cross-cutting components that do not belong to one capability.

## 3. flows

`flows` is optional.

Each flow describes one exposed-interface path, such as user request, API call, CLI command, MCP tool call, SDK method, webhook, scheduled job, or external integration path.

Each flow contains `feature`, `label`, and `edges`.

Each edge contains `from`, `to`, and `label`. `from` and `to` must match existing component labels in `layers`.

Flow endpoint labels should be unique across the architecture model so the exporter can resolve them unambiguously.

## 4. JSON example

Use `assets/project_architecture.example.json` as the concise structure example.

Read it only as an example of shape and parameter usage, not as a fixed architecture template.

## 5. Architecture-to-code mapping

The architecture component model has a reference relationship with the code directory structure used in later development.

In this skill, the recommended code organization is mainly feature/module-first: use business capabilities or functional modules as the primary directory grouping, and then organize implementation units by architecture layer inside each feature module.

For example, if the `server` layer contains two features, `auth` and `order`, the code may be organized as:

/auth/server/
/order/server/

If the auth feature contains architecture-visible components such as register service and login service, they may be mapped as:

/auth/server/RegisterService.java
/auth/server/LoginService.java

Other architecture layers and components may follow the same mapping idea.

This relationship is not required to fit every project or every technology stack. It is only a design reference: the architecture model should be structured so that it can guide later modular code organization, but it must not become a mechanical file inventory.

## Rules

- Top-level JSON may contain only `layers` and optional `flows`.
- `layers` is required and must be non-empty.
- Layer labels must be unique, ordered, and architecture-oriented.
- Each layer must contain only `label` and `child`.
- Each component must contain only `label` and `feature`.
- Component labels must describe responsibilities, not code files, helper functions, or implementation inventory.
- Use one stable non-null `feature` for the same capability across layers.
- Use JSON `null`, not fake strings like `"none"`, `"null"`, `"misc"`, or `"common"`.
- Include `flows` only when exposed-interface paths add clarity.
- Each flow should describe one main consumer-visible capability path.
- Every flow edge `from` and `to` must match an existing component label in `layers`.
- Do not add metadata, descriptions, styles, layout fields, comments, or trailing commas.
