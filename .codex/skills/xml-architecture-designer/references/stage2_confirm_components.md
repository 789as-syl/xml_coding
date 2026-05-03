# Stage 2: Clarify Components Per Architecture Layer

## Input

- Confirmed requirement summary
- Confirmed architecture layer list from Stage 1

## Task

Clarify which detailed components belong to each confirmed architecture layer. Work layer by layer, confirm the component list for the current layer, then continue to the next layer.

This stage is still a clarification and confirmation stage. Do not output the complete JSON model, do not save files, and do not generate XML in this stage.

## Component Model

Each architecture layer has:

- `label`: the confirmed Chinese architecture layer name
- `child`: the component list under this layer

Each component under `child` has:

- `label`: the component name
- `feature`: the business capability key this component belongs to

Do not expose or use component `id`, `style`, `children`, or any layout fields in this stage.

## Internal Structure Example

Use this structure internally after layers and components are clarified. Components should be detailed capability-level items, not broad container names:

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
        },
        {
          "label": "JWT刷新服务",
          "feature": "user"
        },
        {
          "label": "JWT验证服务",
          "feature": "user"
        },
        {
          "label": "订单创建服务",
          "feature": "order"
        }
      ]
    }
  ]
}
```

This example is only a structure reference. Do not output it unless the user explicitly asks to see the internal structure.

## Feature Rules

- `feature` must be stable across layers for the same business capability.
- Use concise lowercase feature keys, such as `user`, `auth`, `order`, `payment`, `report`, `notification`, `inventory`, `gateway`, `ops`, or `infra`.
- Do not create different feature names for the same capability across layers.
- Components with the same `feature` inside one architecture layer will be wrapped by one feature swimlane in the Draw.io architecture page.
- Components with the same `feature` across different architecture layers will be aligned vertically in the Draw.io architecture and flow pages.
- The same layer must not contain duplicate `(label, feature)` pairs, because flow JSON references components by layer, label, and feature.
- If the feature key is uncertain, ask the user to clarify before continuing.

Example:

- `登录页面`, `/auth/login`, `LoginRequest`, `用户登录服务`, `JWT验证服务`, and `users表` should share the same feature key, such as `user`.
- `订单列表页`, `/orders`, `CreateOrderRequest`, `订单创建服务`, and `orders表` should share the same feature key, such as `order`.
- Cross-cutting components such as rate limiting or observability may use capability keys such as `gateway`, `ops`, or another confirmed non-business feature key.

## Component Granularity Rules

- Components must be detailed enough to show concrete responsibilities inside each architecture layer.
- Avoid broad container names such as `UserService`, `OrderService`, `AuthModule`, `AdminModule`, or `DataRepository` when they hide multiple responsibilities.
- Split broad service/module names into specific business actions, validation actions, query actions, synchronization actions, background tasks, or integration actions.
- Keep related detailed components under the same `feature` when they belong to the same business capability.
- Do not split into low-level implementation details such as individual helper functions, private methods, utility classes, or framework boilerplate.
- Good service-layer component labels describe concrete capabilities, such as `用户登录服务`, `用户注册服务`, `JWT刷新服务`, `JWT验证服务`, `订单创建服务`, `订单取消服务`, or `报表生成服务`.
- Good API-layer component labels describe concrete interfaces, such as `/user/login`, `/user/register`, `/token/refresh`, `/orders/create`, or `/reports/export`.
- Good DTO-layer component labels describe concrete request/response structures, such as `LoginRequest`, `LoginResponse`, `RefreshTokenRequest`, or `CreateOrderRequest`.
- Good repository-layer component labels describe concrete data access responsibilities, such as `查询用户凭证`, `保存用户资料`, `查询订单明细`, or `更新订单状态`.
- If a component label sounds like a whole module rather than a concrete responsibility, ask whether it should be split before confirming it.

## Layer-Specific Component Guidance

Use the confirmed architecture layers from Stage 1. Clarify components according to the layer's responsibility:

- 用户层: browsers, mobile apps, mini programs, admin consoles, third-party clients, partners, or external systems that initiate flows.
- 前端: pages, views, routes, state modules, form screens, dashboards, or client-side modules.
- 接入层: CDN, load balancer, WAF, DDoS protection, ingress, or edge routing components.
- 网关层: unified route rules, authentication middleware, rate limiter, gateway logging, request aggregation, or API gateway policies.
- 对外接口层: REST endpoints, GraphQL resolvers, gRPC services, webhook receivers, or external API controllers.
- DTO层: request DTOs, response DTOs, event payloads, command objects, or API schema objects.
- 服务层: business services, use-case services, workflow managers, command handlers, or application services.
- 中间件层: cache, message queue, scheduler, async task processor, search engine, object storage, notification channel, or distributed lock.
- Repository层: repositories, DAOs, persistence adapters, query objects, or database gateways.
- 数据存储层: database tables, collections, indexes, object buckets, file stores, search indexes, or persistent topics.
- 基础设施层: Kubernetes resources, service discovery, secrets, cloud resources, infrastructure-as-code modules, or service mesh components.
- 部署层: CI/CD pipeline, build workflow, deploy workflow, artifact registry, migration job, release strategy, or rollback process.
- 运维监控层: tracing, logging, metrics, alerting, feature flags, A/B tests, or operational dashboards.
- 其他: custom components required by a confirmed custom layer.

## Clarification Rules

- Clarify components one architecture layer at a time.
- For each layer, identify the component `label` and `feature`.
- Ask the user to confirm, revise, add, remove, rename, or split components for the current layer.
- Prefer splitting broad components into detailed capability-level components before asking for confirmation.
- If a component is uncertain, ask a targeted follow-up question instead of guessing.
- If a component belongs to multiple possible layers, ask the user to confirm the ownership.
- If the layer should have no components, confirm that explicitly with the user.
- Do not proceed to architecture JSON generation until every confirmed architecture layer has a confirmed `child` component list.

## Completion Condition

This stage is complete only when every confirmed architecture layer has a confirmed component list using this concept:

```json
{
  "label": "架构层名称",
  "child": [
    {
      "label": "组件名称",
      "feature": "业务功能标识"
    }
  ]
}
```
