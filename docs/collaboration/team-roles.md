# 团队角色与责任 / Team Roles and Responsibilities

## 中文

### 前端负责人

负责 `apps/admin-console`，包括页面、路由、状态、组件、可访问性、接口调用和用户侧错误提示。不得在前端复制后端业务规则、存放密钥，或直接依赖算法和固件内部实现。

交付物：可运行页面、接口 Mock、异常状态、关键流程测试、页面说明和演示素材。

### 后端负责人

负责 `services/api-server` 和数据契约主版本，包括认证、授权、业务逻辑、API、数据校验、持久化、审计和部署配置。负责协调前端、算法和嵌入式的公共契约。

交付物：API 文档、错误码、Schema、迁移说明、接口测试、运行说明和可观测性。

### 算法负责人

负责 `ml`，包括数据清洗、特征、个体基线、模型、评估、推理接口和模型版本。必须说明指标、数据来源、偏差、置信度和失败场景。

交付物：可复现实验、评估报告、输入输出契约、模型卡、性能数据和回滚版本。

### 嵌入式负责人

负责 `firmware`，包括采样、BLE、设备协议、固件版本、功耗和设备联调。必须明确单位、字节序、时间戳、采样率、错误状态和兼容性。

交付物：BLE 协议、数据包样例、模拟器或合成数据、设备测试记录和固件兼容矩阵。

### 共同责任

- 公共契约由受影响角色共同审核。
- `data` 由后端主责，算法和嵌入式审核数据语义，前端审核展示需求。
- 安全、隐私、文档和比赛演示不是某一个人的“额外工作”，每个负责人都要对自己的模块负责。
- 负责人缺席时必须指定代理人，不能让关键 PR 无人审核。
- GitHub 用户名确定后，在本文件和 `.github/CODEOWNERS` 中登记。

## English

### Frontend owner

Owns `apps/admin-console`, including pages, routing, state, components, accessibility, API calls, and user-facing error states. The frontend must not duplicate backend business rules, store secrets, or depend directly on algorithm and firmware internals.

Deliverables: runnable UI, API mocks, failure states, critical-flow tests, UI documentation, and demo material.

### Backend owner

Owns `services/api-server` and the primary version of data contracts, including authentication, authorization, business logic, APIs, validation, persistence, auditing, and deployment configuration. Coordinates shared contracts among frontend, algorithm, and embedded owners.

Deliverables: API documentation, error codes, schemas, migration notes, API tests, runbooks, and observability.

### Algorithm owner

Owns `ml`, including cleaning, features, personalized baselines, models, evaluation, inference contracts, and model versions. Must document metrics, data provenance, bias, confidence, and failure modes.

Deliverables: reproducible experiments, evaluation reports, input/output contracts, model cards, performance data, and rollback versions.

### Embedded owner

Owns `firmware`, including sampling, BLE, device protocols, firmware versions, power behavior, and hardware integration. Must define units, byte order, timestamps, sampling rate, error states, and compatibility.

Deliverables: BLE protocol, packet samples, simulator or synthetic data, device test records, and firmware compatibility matrix.

### Shared responsibilities

- Shared contracts require review by every affected role.
- `data` is primarily owned by backend; algorithm and embedded review semantics, while frontend reviews presentation needs.
- Security, privacy, documentation, and competition demos are not one person's extra task. Every owner is accountable within their domain.
- When an owner is unavailable, name a delegate so critical PRs are not left unreviewed.
- Record actual GitHub usernames in this file and `.github/CODEOWNERS` once known.
