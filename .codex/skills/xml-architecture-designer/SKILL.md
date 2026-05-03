---
name: xml-architecture-designer
description: Design new-project software architecture through requirement clarification, step-by-step layer/component confirmation, architecture JSON export, human-reviewed Draw.io architecture pages, and confirmed external-interface flow pages. Use when Codex needs to create `.xml/` architecture JSON, separate flow JSON, and a multi-page `.drawio` file with architecture and per-interface flow diagrams.
---

# XML Architecture Designer

Use this skill to design a new project's architecture and export Draw.io-compatible architecture and flow diagrams.

The workflow is intentionally incremental. Do not generate all JSON in one pass. Clarify requirements, confirm architecture layers, confirm components layer by layer, export the architecture JSON and architecture page, pause for user review, then confirm external-interface flows before generating flow JSON and final multi-page Draw.io output.

Requirement clarification will not discover every detail upfront. During later layer design, component design, architecture export, and flow design, ask targeted follow-up questions whenever uncertainty affects correctness. Do not guess, invent missing facts, or silently fill important gaps.

## Workflow

### Step 0: Clarify requirements

Read [references/requirement_clarification.md](references/requirement_clarification.md).

Ask focused questions until the project goal, scope, users, exposed capabilities, core workflows, integrations, data, non-functional needs, deployment expectations, and technology preferences are clear enough to design the architecture and later external-interface flows.

End this step with a short requirements summary and ask the user to confirm or revise it.

### Step 1: Confirm architecture layers

Read [references/stage1_confirm_layers.md](references/stage1_confirm_layers.md).

Propose the architecture layers as a human-readable list. Do not output JSON in this intermediate step.

The confirmed order controls the top-to-bottom order in the Draw.io architecture page. Ask the user to confirm, remove, rename, or reorder layers before continuing.

### Step 2: Confirm components per layer

Read [references/stage2_confirm_components.md](references/stage2_confirm_components.md).

Work through the confirmed layers one by one or in small batches. For each layer, propose detailed components and assign each component a stable `feature` value.

Do not output JSON in this intermediate step. Show a readable table or bullet list and ask for confirmation before moving to the next layer or architecture export.

### Step 3: Export architecture JSON and Draw.io preview

Read [references/final_model_and_export.md](references/final_model_and_export.md).

After all layers and components are confirmed, create the architecture JSON using the required `layers -> label -> child -> label/feature` schema. Save it under `.xml/` in the current project directory.

Immediately run the bundled script to generate the architecture preview Draw.io file:

```bash
python .codex/skills/xml-architecture-designer/scripts/export_to_xml.py .xml/project_architecture.json
```

Pause after the architecture preview is generated. Tell the user to open the `.drawio` file and confirm whether the content and layout are correct. Do not generate flow JSON or flow pages until the user confirms the architecture page.

### Step 4: Confirm external-interface flows and export final Draw.io

Read [references/stage3_confirm_external_flows.md](references/stage3_confirm_external_flows.md).

After the user confirms the architecture page, identify each external-facing capability, draft a flow for each one, and ask the user to confirm or revise the flow steps and edge labels.

Save confirmed flows as a separate `.xml/project_flows.json` file. Then run:

```bash
python .codex/skills/xml-architecture-designer/scripts/export_to_xml.py .xml/project_architecture.json --flows .xml/project_flows.json
```

The final `.drawio` file must contain one architecture page followed by one flow page for each confirmed external-interface flow.

## Required Model Rules

- Intermediate stages should be readable summaries for user confirmation, not JSON dumps.
- Write architecture JSON and flow JSON only after the relevant information is confirmed.
- Save all generated JSON and Draw.io files under `.xml/`.
- The architecture JSON must use top-level `layers`.
- `layers` must be a non-empty array.
- Each layer must include only `label` and `child`.
- Each component in `child` must include only `label` and `feature`.
- Every component must include a non-empty `feature`.
- Do not include `project`, `id`, `style`, `components`, `children`, or extra metadata in architecture JSON.
- Keep the architecture JSON schema consistent across all outputs.
- Flow JSON is separate from architecture JSON and must reference confirmed architecture components.
- If a layer, component, feature key, exposed interface, flow node, edge, label, step, capability, data need, or output decision is uncertain, pause and ask the user to clarify before writing the relevant JSON.
- Record only confirmed facts and explicit user-approved assumptions in generated models.

## Bundled Resources

- `references/requirement_clarification.md`: requirement interview and confirmation guidance
- `references/stage1_confirm_layers.md`: layer proposal and confirmation rules
- `references/stage2_confirm_components.md`: layer-by-layer component confirmation rules
- `references/final_model_and_export.md`: architecture JSON, preview export, and final export rules
- `references/stage3_confirm_external_flows.md`: external-interface flow confirmation rules
- `scripts/export_to_xml.py`: converts architecture JSON and optional flow JSON into a `.drawio` file
