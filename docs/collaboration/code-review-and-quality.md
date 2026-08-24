# 代码评审与质量 / Code Review and Quality

## 中文

### 评审顺序

1. 需求和范围是否正确。
2. 接口、数据和兼容性是否一致。
3. 正常流程、边界条件和失败流程是否正确。
4. 是否存在安全、隐私和权限问题。
5. 性能、资源、并发和设备约束是否合理。
6. 是否可测试、可观察、可回滚和可维护。
7. 文档是否中英双语且与实现同步。

### 各域最低测试

- 前端：关键组件、路由、加载/空/错误状态和主流程。
- 后端：认证、权限、参数校验、核心 API、错误码和数据访问。
- 算法：数据校验、特征、基线、指标、回归和性能。
- 嵌入式：协议解析、断连重连、丢包、乱序、低电量和异常值。
- 跨域：使用版本固定的契约样例完成端到端联调。

### 严重级别

- P0：密钥或隐私泄露、数据破坏、权限绕过、无法回滚。
- P1：核心流程不可用、结果严重错误、广泛兼容性问题。
- P2：非核心缺陷、明显性能或维护问题。
- P3：可改进的可读性、命名或文档问题。

P0/P1 未解决不得合并。P2 应在合并前解决或建立明确 Issue。P3 可记录后处理。

### 完成定义

代码可运行、验收标准通过、测试证据存在、公共契约已更新、双语文档同步、无敏感信息、监控和错误信息足够、回滚路径明确。

## English

### Review order

1. Confirm the requirement and scope.
2. Confirm contract, data, and compatibility consistency.
3. Review happy paths, edge cases, and failure paths.
4. Review security, privacy, and authorization.
5. Review performance, resources, concurrency, and device constraints.
6. Confirm testability, observability, rollback, and maintainability.
7. Confirm bilingual documentation matches the implementation.

### Minimum tests by domain

- Frontend: critical components, routing, loading/empty/error states, and main flows.
- Backend: authentication, authorization, validation, core APIs, error codes, and data access.
- Algorithm: data validation, features, baselines, metrics, regression, and performance.
- Embedded: protocol parsing, disconnect/reconnect, packet loss, ordering, low battery, and outliers.
- Cross-domain: end-to-end integration using versioned contract fixtures.

### Severity

- P0: secret or privacy exposure, data destruction, authorization bypass, or no rollback.
- P1: critical flow unavailable, seriously incorrect results, or broad compatibility failure.
- P2: non-critical defect or significant performance/maintenance issue.
- P3: readability, naming, or documentation improvement.

P0/P1 findings block merging. P2 must be fixed or tracked in an explicit Issue. P3 may be recorded for follow-up.

### Definition of done

Code runs, acceptance criteria pass, test evidence exists, shared contracts are updated, bilingual documentation is synchronized, no sensitive information is added, monitoring and errors are sufficient, and rollback is clear.
