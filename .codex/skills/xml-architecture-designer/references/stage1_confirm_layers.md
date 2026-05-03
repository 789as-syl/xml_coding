# Stage 1: Clarify Architecture Layers

## Input

- Confirmed requirement summary
- Confirmed architecture capabilities from the requirement clarification stage

## Task

Clarify which architecture layers are required for the project. This stage is not for producing a user-facing JSON output. It is for determining and confirming the architecture layer structure that later stages will use.

Architecture layer names must use Chinese labels. Each architecture layer is represented only by its layer name at this stage. Do not expose `id`, `style`, layout, or any final JSON structure to the user.

## Layer Selection Rules

Use the confirmed requirements and architecture capabilities to decide which layers are needed.

- 前端: add when the project has a user interface, such as Web, mobile, or desktop.
- 用户层: add when the diagram should show human users, browsers, mobile apps, third-party clients, partners, or other actors that initiate external flows.
- 接入层: add when CDN, load balancing, DDoS protection, ingress, or edge traffic handling is needed.
- 网关层: add when unified routing, authentication, rate limiting, gateway logging, or request aggregation is needed.
- 对外接口层: add when the system exposes REST, GraphQL, gRPC, webhook, or other external APIs.
- DTO层: add when request and response parameter structures must be defined. Usually add this whenever 对外接口层 exists.
- 服务层: add when business logic needs encapsulation. Recommend this when the system is more than simple CRUD.
- 中间件层: add when the system needs message queues, cache, scheduled tasks, async processing, search, object storage, or similar supporting capabilities.
- Repository层: add when data access abstraction is needed for testing, database switching, persistence isolation, or cleaner service boundaries.
- 数据存储层: add when persistent data is required, including SQL, NoSQL, files, object storage metadata, search indexes, or other durable stores.
- 基础设施层: add when container orchestration, Kubernetes, service mesh, infrastructure as code, cloud resources, or environment management is needed.
- 部署层: add when CI/CD pipelines, automated release strategy, artifact delivery, deployment workflow, or migration automation is needed.
- 运维监控层: add when tracing, logging, metrics, alerting, feature flags, A/B testing, or operational dashboards are relevant to the architecture.
- 其他: add custom layers only when the confirmed requirements clearly need a layer not covered above.

## Clarification Rules

- Do not output JSON in this stage.
- Do not produce the final architecture model in this stage.
- Clarify the layer structure with the user when a layer is uncertain.
- Ask targeted questions for uncertain layers instead of guessing.
- Keep the layer list concise enough to support later component design.
- The confirmed layer order becomes the top-to-bottom order in the Draw.io architecture and flow pages.
- Merge layers when the project is small and separation adds no value.
- Split layers when scale, ownership, deployment, security, or operational needs justify separation.
- Do not proceed to component clarification until the architecture layer list is confirmed.

## Internal Layer Definition Example

After clarification, the internal architecture layer definition should be a simple ordered list of Chinese layer names:

```json
["用户层", "前端", "网关层", "对外接口层", "DTO层", "服务层", "中间件层", "Repository层", "数据存储层", "部署层", "运维监控层"]
```

This example is for internal structure definition only. Do not present it as a required output unless the user explicitly asks to see the layer definition.
