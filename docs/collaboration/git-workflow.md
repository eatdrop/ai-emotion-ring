# Git 工作流 / Git Workflow

## 中文

### 分支

- `main`：稳定、可演示、可发布；禁止直接推送。
- `develop`：日常集成。
- 功能分支从 `develop` 创建，保持短生命周期。
- 紧急修复从 `main` 创建 `hotfix/<topic>`，完成后同步回 `develop`。

### 命名

- `feature/product-<topic>`
- `feature/product-<topic>`
- `feature/frontend-<topic>`
- `feature/backend-<topic>`
- `feature/ml-<topic>`
- `feature/firmware-<topic>`
- `fix/<topic>`
- `docs/<topic>`
- `chore/<topic>`

### 提交

使用 `type(scope): summary`。标题使用祈使语气、简短明确，不添加“最终版”等无意义描述。避免把格式化、重构和功能混在同一提交。

### Pull Request

- 一个 PR 只处理一个主题。
- 建议不超过约 400 行有效改动；超过时说明无法拆分的理由。
- PR 必须关联 Issue、通过测试、完成自查和双语文档检查。
- 作者不能作为唯一审批人。
- 跨域 PR 需要每个受影响域至少一名负责人批准。
- 用户流程、验收标准、产品文案或版本范围变化需要产品负责人批准。
- 修改公共契约时，文档提交应早于或与实现同时合并。
- 使用 squash merge 保持主线清晰，提交标题遵循约定。

### 冲突和回滚

冲突由变更作者解决，并请求受影响文件的负责人复查。高风险变更必须提供功能开关、兼容层或明确的回滚提交。

## English

### Branches

- `main`: stable, demo-ready, and releasable; direct pushes are forbidden.
- `develop`: daily integration.
- Create short-lived feature branches from `develop`.
- Create `hotfix/<topic>` from `main` for emergencies and merge it back into `develop`.

### Naming

- `feature/frontend-<topic>`
- `feature/backend-<topic>`
- `feature/ml-<topic>`
- `feature/firmware-<topic>`
- `fix/<topic>`
- `docs/<topic>`
- `chore/<topic>`

### Commits

Use `type(scope): summary`. Keep titles imperative and concise; avoid labels such as “final version.” Do not mix formatting, refactoring, and feature behavior in one commit.

### Pull Requests

- One PR addresses one coherent topic.
- Prefer fewer than about 400 effective changed lines; explain why a larger change cannot be split.
- Every PR links an Issue, passes tests, completes self-review, and verifies bilingual documentation.
- The author cannot be the only approver.
- Cross-domain PRs require at least one approval from every affected domain.
- Changes to user flows, acceptance criteria, product copy, or release scope require product-owner approval.
- Shared-contract documentation must merge before or with implementation.
- Use squash merge to keep the mainline clear and follow the commit convention.

### Conflicts and rollback

The change author resolves conflicts and requests re-review from owners of affected files. High-risk changes require a feature flag, compatibility layer, or explicit rollback commit.
