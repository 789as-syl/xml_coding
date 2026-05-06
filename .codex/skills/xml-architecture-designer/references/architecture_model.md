# Architecture Model

## Purpose

Use this reference to design `.xml/project_architecture.json` from the clarified requirement context.

First read [project_architecture_json_parameters_and_structure.md](project_architecture_json_parameters_and_structure.md) to understand the target JSON parameters, structure, and constraints.

## Inputs

- Current conversation context.
- `.xml/project_requirements.md` from the requirement clarification step.
- JSON structure rules from `project_architecture_json_parameters_and_structure.md`.
- Optional mature reference architectures for the same project type when the architecture style or domain convention is unclear.

Use reference architectures only to inform design. Do not copy their names, folders, or components mechanically.

## Modeling Approach

Based on the clarified requirement context, infer the project type and choose an architecture style that fits that type.

Different project types require different architecture views. A Web/API system, frontend app, CLI tool, MCP service, SDK/plugin, RAG/Agent system, platform tool, and runtime component should not be forced into the same layer vocabulary.

Before writing JSON, reason through:

1. What type of project is this?
2. What mature architecture style fits this project type?
3. What business capabilities or functional modules should become `feature` values?
4. What responsibility layers are needed for this architecture view?
5. What architecture-visible components belong under each layer?
6. Which exposed-interface paths, if any, should become `flows`?
7. Can the model guide later feature/module-first code organization?

If the project type or architecture style is unclear, search for mature enterprise-grade or widely used open-source projects of the same type. Use them only to extract architecture-level patterns, such as common layers, module boundaries, interface surfaces, runtime boundaries, and deployment concerns. Do not mechanically copy their names, folders, components, or technology choices.

## Business-Capability First Design

Design the architecture around business capabilities or functional modules.

The preferred direction is:

business capability feature -> architecture layer -> architecture-visible component

## Architecture-to-Code Directory Reference

The architecture model has a reference relationship with the code directory structure used in later development.

Recommended organization is feature/module-first: group code by business capability first, then by architecture layer inside each feature module.

For example, if the server layer contains auth and order features, code may be organized as:

/auth/server/
/order/server/

If auth contains architecture-visible components such as register service and login service, they may map to:

/auth/server/RegisterService.java
/auth/server/LoginService.java

Other architecture layers and components may follow the same mapping principle.

This mapping is not required to fit every project or technology stack, but it should be used as the main design reference when appropriate.