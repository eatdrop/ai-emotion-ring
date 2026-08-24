# 贡献与协作规范 / Contribution and Collaboration Guide

## 中文

本规范适用于前端、后端、算法和嵌入式四位负责人，以及后续加入的协作者。

### 1. 基本原则

1. 责任域清晰：目录负责人对本域质量负责。
2. 接口优先：跨域开发先确定契约，再分别实现。
3. 小步提交：一个 PR 只解决一个主题。
4. 可复现：功能、算法和设备联调必须提供可重复步骤。
5. 安全默认：不提交密钥、真实用户数据、日志或个人信息。
6. 文档同步：代码、接口、协议、配置或流程变化必须同步文档。
7. 双语强制：所有新增或修改的 Markdown 文件必须中文在前、英文在后。

### 2. 分支与提交

- `main`：可演示、可发布的稳定分支，禁止直接推送。
- `develop`：日常集成分支。
- `feature/frontend-<topic>`
- `feature/backend-<topic>`
- `feature/ml-<topic>`
- `feature/firmware-<topic>`
- `fix/<topic>`、`docs/<topic>`、`chore/<topic>`

提交格式：`type(scope): summary`，例如 `feat(api): add device ingestion endpoint`。推荐类型：`feat`、`fix`、`docs`、`test`、`refactor`、`perf`、`security`、`chore`。

### 3. Issue 与 PR

开发前创建 Issue，说明目标、范围、验收标准、负责人和依赖。PR 必须：

- 关联 Issue；
- 说明做了什么、为什么做、影响哪些模块；
- 提供测试证据和回滚方式；
- 标明接口、Schema、配置、安全和隐私影响；
- 完成双语文档检查；
- 获得受影响责任域负责人审核。

禁止将未完成、无法运行或接口未对齐的代码合入 `main`。

### 4. 接口和数据变更

- API、BLE、算法输入输出和数据 Schema 都属于公共契约。
- 契约变更先写文档，标注版本、兼容性、迁移方式和废弃时间。
- 字段名、类型、单位、时间格式、错误码和空值语义必须明确。
- 破坏性变更必须经过所有受影响负责人同意。
- 前端不得绕过后端直接依赖算法或设备内部实现。

### 5. 评审与完成定义

至少检查正确性、边界条件、性能、安全、隐私、可维护性、可观测性和文档。完成意味着：验收标准通过、必要测试通过、文档同步、无新增敏感信息、可回滚、责任人明确。

### 6. 文档语言规范

每个 Markdown 文件都应包含对应的中文和英文内容。推荐结构：

```markdown
# 中文标题 / English Title

## 中文
...

## English
...
```

不得只翻译标题而保留单语正文。代码、JSON 字段、路径、命令和产品专有名词可保持原文。若修改旧文档，修改者必须同时更新两种语言；无法完成时不得合并。

## English

This guide applies to the four owners—frontend, backend, algorithm, and embedded—and to future contributors.

### 1. Core principles

1. Clear ownership: domain owners are accountable for quality in their areas.
2. Contract first: agree on shared contracts before implementing across domains.
3. Small changes: one PR should address one coherent topic.
4. Reproducibility: features, models, and hardware integration require repeatable steps.
5. Secure by default: never commit secrets, real user data, logs, or personal information.
6. Documentation parity: code, contract, protocol, configuration, or process changes require matching documentation.
7. Mandatory bilingual docs: every new or modified Markdown file must contain Chinese first and English second.

### 2. Branches and commits

- `main`: stable, demo-ready, and releasable; direct pushes are forbidden.
- `develop`: daily integration branch.
- `feature/frontend-<topic>`
- `feature/backend-<topic>`
- `feature/ml-<topic>`
- `feature/firmware-<topic>`
- `fix/<topic>`, `docs/<topic>`, and `chore/<topic>`

Use `type(scope): summary`, for example `feat(api): add device ingestion endpoint`. Recommended types are `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `security`, and `chore`.

### 3. Issues and Pull Requests

Create an Issue before development and state the goal, scope, acceptance criteria, owner, and dependencies. Every PR must:

- link its Issue;
- explain what changed, why, and which modules are affected;
- provide test evidence and a rollback method;
- identify API, schema, configuration, security, and privacy impact;
- complete the bilingual-documentation check;
- obtain review from every affected domain owner.

Do not merge incomplete, non-runnable, or contract-misaligned work into `main`.

### 4. Contract and data changes

- APIs, BLE protocols, algorithm inputs/outputs, and data schemas are shared contracts.
- Document contract changes first, including version, compatibility, migration, and deprecation date.
- Define field names, types, units, time format, error codes, and null semantics.
- Breaking changes require agreement from all affected owners.
- The frontend must not bypass the backend and depend directly on algorithm or device internals.

### 5. Review and definition of done

Review correctness, edge cases, performance, security, privacy, maintainability, observability, and documentation. Done means acceptance criteria pass, required tests pass, documentation is synchronized, no sensitive information was added, rollback is possible, and ownership is clear.

### 6. Documentation language policy

Every Markdown file must include corresponding Chinese and English content. Use this structure:

```markdown
# 中文标题 / English Title

## 中文
...

## English
...
```

Translating only headings while leaving a single-language body is not sufficient. Code, JSON fields, paths, commands, and product-specific terms may remain unchanged. Anyone editing an existing document must update both languages; otherwise the change must not be merged.
