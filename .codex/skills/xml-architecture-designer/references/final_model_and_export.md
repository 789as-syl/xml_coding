# Final Model And Export

## Input

- Confirmed requirement summary
- Confirmed architecture layer list from Stage 1
- Confirmed detailed component list for every architecture layer from Stage 2
- User confirmation that the architecture preview is acceptable before flow export
- Confirmed external-interface flows from Stage 3 when generating final multi-page output

## Task

Generate the architecture JSON file and save it under `.xml/`. Then immediately run the bundled export script to generate the architecture preview Draw.io file in the same `.xml/` directory.

Stop after architecture preview export and ask the user to inspect the `.drawio` file. Do not write flow JSON and do not generate flow pages until the user confirms that the architecture page content and layout are acceptable.

After the user confirms the architecture preview, convert confirmed external-interface flows into separate flow JSON and run the bundled export script with `--flows` to generate the final multi-page Draw.io file.

Do not redesign the architecture in this stage. Only convert confirmed layer, component, and flow decisions into the required JSON structures. If any layer, component, feature value, flow node, edge, label, or step is still uncertain, ask the user to clarify before writing the relevant JSON file.

## Architecture JSON Schema

Use this architecture JSON structure:

```json
{
  "layers": [
    {
      "label": "服务层",
      "child": [
        {
          "label": "用户登录服务",
          "feature": "user"
        },
        {
          "label": "用户注册服务",
          "feature": "user"
        }
      ]
    }
  ]
}
```

## Architecture Schema Rules

- The top-level object must contain only `layers`.
- `layers` must be a non-empty array. Do not use an object for `layers`.
- Every layer must include only `label` and `child`.
- Every layer `label` must be a confirmed Chinese architecture layer name from Stage 1.
- Every layer `child` must be an array.
- Every component in `child` must include only `label` and `feature`.
- Every component `label` must be a confirmed detailed component from Stage 2.
- Every component `feature` must be non-empty and stable across layers for the same business capability.
- The same layer must not contain duplicate `(label, feature)` pairs.
- Do not include `project`, `id`, `style`, `components`, `children`, descriptions, layout, or metadata.
- Do not invent missing layers, components, or feature values.
- Record only confirmed facts and explicit user-approved assumptions.

## Flow JSON Schema

Use this separate flow JSON structure after the architecture preview is confirmed:

```json
{
  "flows": [
    {
      "feature": "user",
      "label": "用户登录",
      "exposed_interface": {
        "layer": "对外接口层",
        "label": "/user/login",
        "feature": "user"
      },
      "nodes": [
        {
          "id": "login_page",
          "ref": {
            "layer": "前端",
            "label": "用户登录页面",
            "feature": "user"
          }
        }
      ],
      "edges": [
        {
          "from": "login_page",
          "to": "login_api",
          "label": "提交登录请求",
          "step": "Step 1: 用户从登录入口提交账号密码"
        }
      ]
    }
  ]
}
```

Flow rules:

- The top-level object must contain only `flows`.
- `flows` must be a non-empty array.
- Every flow must include only `feature`, `label`, `exposed_interface`, `nodes`, and `edges`.
- `exposed_interface` and every node `ref` must reference an existing confirmed architecture component by `layer`, `label`, and `feature`.
- Every flow node must have a unique `id` inside that flow.
- Every edge must reference existing node IDs with `from` and `to`.
- Every edge must include non-empty `label` and `step`.
- Do not include unconfirmed, inferred-only, or decorative flow edges in final flow JSON.

## Export Commands

Architecture preview:

```bash
python .codex/skills/xml-architecture-designer/scripts/export_to_xml.py .xml/project_architecture.json
```

Final multi-page Draw.io after flow confirmation:

```bash
python .codex/skills/xml-architecture-designer/scripts/export_to_xml.py .xml/project_architecture.json --flows .xml/project_flows.json
```

The script creates or overwrites the `.drawio` file beside the architecture JSON file automatically when no output path is provided.

## Draw.io Layout Rules

- The architecture page must show layers from top to bottom.
- Different architecture layers should use different color styles.
- Components with the same `feature` inside one layer must be wrapped by the same feature swimlane.
- Components with the same `feature` across different layers must keep the same horizontal position so they read vertically.
- The architecture page may include default down-flow layer connectors from one layer to the next; these are only structural connectors.
- Flow pages must copy the architecture page layout.
- In each flow page, components outside the current flow should remain in place but be transparent or visually muted.
- Flow pages must render the confirmed edges with arrow lines whose labels include both `step` and `label`.

## User-Facing Output

After architecture preview export succeeds, report only:

- Architecture JSON path
- Architecture Draw.io path
- Export success
- A clear pause instruction asking the user to inspect the `.drawio` architecture page and confirm whether content and layout are correct

After final multi-page export succeeds, report only:

- Architecture JSON path
- Flow JSON path
- Final Draw.io path
- Number of generated flow pages
- Any confirmed assumptions kept in the models
- Whether the export script succeeded

Do not paste full JSON unless the user asks to see it.
