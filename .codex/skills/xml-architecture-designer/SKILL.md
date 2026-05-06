---
name: xml-architecture-designer
description: Use when the user needs to turn early-stage software project ideas or requirements into a structured architecture baseline suitable for requirement snapshot, strict architecture JSON, and Draw.io XML diagram generation.
---

# XML Architecture Designer

Produce a fresh software architecture baseline through three durable outputs:   

1. `.xml/project_requirements.md`
2. `.xml/project_architecture.json`
3. `.xml/project_architecture.drawio`

Do not run this workflow for review, refactoring, documentation, or reverse-engineering tasks unless the user explicitly requests a new baseline.

## Workflow

Execute exactly three steps in order. Do not skip any step or its required reference. Each step has one durable output.

### Step 1: Clarify architecture-model inputs and save requirement snapshot

Run Step 1 in three focused passes:

1. Load and apply [references/project_requirement_inputs.md](references/project_requirement_inputs.md) to determine what project requirement information is needed to support the final architecture model.

2. Based on the user's description and the needed information above, load and apply [references/clarification.md](references/clarification.md) to ask only blocking clarification questions that help complete the project understanding.

3. After the requirements are sufficiently clarified, write a concise requirement snapshot to `.xml/project_requirements.md`. Organize the snapshot in the order specified in the "Global-To-Local Analysis Path" section of `project_requirement_inputs.md`.


### Step 2: Derive architecture model and write JSON

Based on the clarified requirement context from Step 1, load and apply [references/architecture_model.md](references/architecture_model.md) to derive the final architecture model.

Use [assets/project_architecture.example.json](assets/project_architecture.example.json) only as a non-authoritative formatting template, then write the result to `.xml/project_architecture.json`.

### Step 3: Export and verify Draw.io XML

Use `.xml/project_architecture.json` as input and run [scripts/export_to_xml.py](scripts/export_to_xml.py) to validate the JSON and generate `.xml/project_architecture.drawio`.

If validation or export fails, fix `.xml/project_architecture.json` according to the script error and [references/architecture_model.md](references/architecture_model.md), then rerun the script until export succeeds.
