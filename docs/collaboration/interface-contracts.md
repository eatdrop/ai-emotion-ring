# 接口与数据契约 / Interface and Data Contracts

## 中文

### 契约范围

公共契约包括 REST API、WebSocket、BLE、设备数据包、算法输入输出、数据库 Schema、事件格式和错误码。

### 变更流程

1. 创建接口变更 Issue。
2. 使用模板说明现状、目标、示例、兼容性和迁移计划。
3. 由所有受影响负责人审核。
4. 确定版本和废弃期限。
5. 更新 Mock、实现、测试和双语文档。
6. 联调后记录结果。

### 字段要求

每个字段必须明确：名称、类型、单位、必填性、范围、精度、时间格式、空值、默认值、隐私等级和示例。时间统一使用 ISO 8601 UTC；设备时间必须说明校时策略。

### 典型依赖方向

```text
设备/固件 -> 后端数据接入 -> 算法推理 -> 后端业务 API -> 前端
```

前端不直接调用算法服务或解析原始 BLE 包。算法不直接读取生产数据库。嵌入式不依赖后端内部表结构。

### 兼容性

- 新增可选字段通常是向后兼容。
- 删除字段、改名、改类型、改单位、改语义属于破坏性变更。
- 破坏性变更必须升级主版本，并提供迁移期。
- 后端应在兼容期同时接受旧版和新版，或提供明确适配层。

## English

### Contract scope

Shared contracts include REST APIs, WebSockets, BLE, device packets, algorithm inputs/outputs, database schemas, event formats, and error codes.

### Change process

1. Create a contract-change Issue.
2. Use the template to describe current behavior, target behavior, examples, compatibility, and migration.
3. Obtain review from all affected owners.
4. Set a version and deprecation deadline.
5. Update mocks, implementation, tests, and bilingual documentation.
6. Record integration results.

### Field requirements

Every field must define name, type, unit, required status, range, precision, time format, null behavior, default, privacy class, and example. Use ISO 8601 UTC. Device time must document clock synchronization.

### Dependency direction

```text
Device/Firmware -> Backend ingestion -> Algorithm inference -> Backend business API -> Frontend
```

The frontend does not call the algorithm directly or parse raw BLE packets. The algorithm does not read the production database directly. Firmware does not depend on backend table internals.

### Compatibility

- Adding an optional field is usually backward compatible.
- Removing, renaming, retyping, changing units, or changing semantics is breaking.
- Breaking changes require a major version and migration window.
- During the compatibility period, the backend should accept both versions or provide an explicit adapter.
