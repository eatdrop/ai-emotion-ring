# 团队角色与责任 / Team Roles and Responsibilities

## 中文

团队采用五个责任域：产品、前端、后端、算法和嵌入式。产品负责人决定“为什么做、给谁做、先做什么、怎样算完成”；技术负责人决定“如何可靠、安全、可维护地实现”。

### 产品负责人

负责 `docs/product` 和产品需求，包括用户研究、问题定义、产品目标、需求优先级、用户流程、验收标准、版本范围、指标和需求变更记录。

交付物：用户画像、场景与痛点、PRD、原型说明、优先级、验收标准、版本计划、用户反馈、竞品与商业假设。

产品负责人可以决定需求价值和优先级，但不能单方面指定具体技术实现、承诺未经技术评估的交付时间，或把医疗诊断作为未经验证的产品结论。

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

### 决策边界

| 决策 | 主责 | 必须参与 |
|---|---|---|
| 用户问题、价值和优先级 | 产品 | 项目负责人、相关技术负责人 |
| 用户流程和验收标准 | 产品 | 前端、后端 |
| API 与存储设计 | 后端 | 前端、算法、嵌入式中的受影响方 |
| 模型方案和评估标准 | 算法 | 产品、后端 |
| BLE、采样和固件设计 | 嵌入式 | 后端、算法 |
| 发布范围 | 产品 | 五个责任域 |
| 发布技术门禁 | 对应技术负责人 | 所有受影响技术域 |
| 比赛最终取舍与对外承诺 | 项目负责人 | 产品负责人及相关技术负责人 |

### 共同责任

- 产品验收不能替代技术评审，技术测试也不能替代产品验收。
- 技术负责人发现需求不可行、风险过高或证据不足时，必须及时提出，不得静默实现。
- 需求变化必须由产品负责人更新 PRD、验收标准和优先级，再进入开发。
- `data` 由后端主责；产品定义使用目的，算法和嵌入式审核语义，前端审核展示需求。
- 安全、隐私、文档和比赛演示由每个负责人对自己的责任域负责。
- GitHub 用户名确定后，在本文件和 `.github/CODEOWNERS` 中登记。

## English

The team has five ownership domains: product, frontend, backend, algorithm, and embedded. The product owner decides why to build, for whom, what comes first, and what counts as accepted. Technical owners decide how to implement it reliably, securely, and maintainably.

### Product owner

Owns `docs/product` and product requirements, including user research, problem definition, product goals, priorities, user flows, acceptance criteria, release scope, metrics, and requirement-change records.

Deliverables: personas, scenarios and pain points, PRDs, prototype notes, priorities, acceptance criteria, release plans, user feedback, competitor analysis, and business hypotheses.

The product owner may decide value and priority, but must not unilaterally dictate technical implementation, promise dates without technical assessment, or present unvalidated medical diagnosis as a product conclusion.

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

### Decision boundaries

| Decision | Accountable owner | Required participants |
|---|---|---|
| User problem, value, and priority | Product | Project lead and affected technical owners |
| User flow and acceptance criteria | Product | Frontend and backend |
| API and storage design | Backend | Affected frontend, algorithm, and embedded owners |
| Model design and evaluation criteria | Algorithm | Product and backend |
| BLE, sampling, and firmware design | Embedded | Backend and algorithm |
| Release scope | Product | All five domains |
| Technical release gates | Relevant technical owner | All affected technical domains |
| Competition trade-offs and external commitments | Project lead | Product and affected technical owners |

### Shared responsibilities

- Product acceptance does not replace technical review, and technical testing does not replace product acceptance.
- Technical owners must raise infeasibility, excessive risk, or insufficient evidence early rather than silently implementing.
- Requirement changes require the product owner to update the PRD, acceptance criteria, and priority before development.
- `data` is backend-owned; product defines purpose, algorithm and embedded review semantics, and frontend reviews presentation.
- Every owner is accountable for security, privacy, documentation, and competition demos in their domain.
- Record actual GitHub usernames in this file and `.github/CODEOWNERS` once known.
