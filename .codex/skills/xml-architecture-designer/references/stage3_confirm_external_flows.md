# Stage 3: Confirm External-Interface Flows

## Input

- Confirmed requirement summary
- Confirmed architecture JSON
- User confirmation that the architecture preview Draw.io page is acceptable

## Task

Identify each external-facing capability and confirm one flow page for each capability. This stage creates a separate flow model after the architecture page has been reviewed by the user.

Use a mixed approach:

1. Draft each flow automatically from the confirmed architecture model.
2. Present the draft as readable steps, not JSON.
3. Ask the user to confirm, remove, add, reorder, or relabel steps.
4. Write `project_flows.json` only after every flow is confirmed.

## External Capability Detection

Prefer these sources, in order:

- Components in `对外接口层`.
- Components in a custom API/interface layer if the user used a different layer name.
- User-confirmed exposed capabilities from requirement clarification.

If no exposed interface is clear, ask the user to identify the external-facing capabilities before drafting flows.

## Automatic Drafting Rules

For each exposed interface:

- Start from the user or client entry point when one exists in `用户层` or `前端`.
- Include relevant `接入层` and `网关层` components when they affect the external request path, such as CDN, WAF, load balancer, authentication, or rate limiting.
- Include the exposed interface component itself.
- Include DTO, service, middleware, repository, storage, and integration components that share the same `feature`.
- Include cross-cutting components with confirmed relevance, such as rate limiting, auth validation, queue publishing, cache read/write, search, object storage, tracing, logging, or alerting.
- Keep the draft as the main success path unless the user asks for exception branches.

Do not silently invent a flow step. If a step is plausible but not confirmed, mark it as a question in the readable draft and ask the user to decide.

## Confirmation Output

For each flow, show a concise table or ordered list:

- Flow label
- Exposed interface
- Ordered nodes by layer and component
- Edge label
- Edge step description

Example:

```text
Flow: 用户登录
Exposed interface: 对外接口层 /user/login

1. 前端 / 用户登录页面 -> 网关层 / 接口限流规则
   Edge: 提交登录请求
   Step: Step 1: 用户从登录入口提交账号密码
2. 网关层 / 接口限流规则 -> 对外接口层 / /user/login
   Edge: 放行登录请求
   Step: Step 2: 网关完成限流检查后转发请求
```

Ask the user to confirm or revise the flow before saving flow JSON.

## Flow JSON Concept

After confirmation, write this concept to `.xml/project_flows.json`:

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

## Completion Condition

This stage is complete only when:

- The architecture preview Draw.io page has already been confirmed by the user.
- Every exposed interface has either a confirmed flow or is explicitly excluded by the user.
- Every flow node references a confirmed architecture component.
- Every flow edge has confirmed `from`, `to`, `label`, and `step`.
- `project_flows.json` has been saved under `.xml/`.
- The final multi-page `.drawio` file has been generated with the bundled export script.
