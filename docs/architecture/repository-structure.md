# 仓库结构与所有权 / Repository Structure and Ownership

## 中文

| 路径 | 主要负责人 | 内容 | 跨域变更要求 |
|---|---|---|---|
| `docs/product` | 产品 | PRD、用户研究、路线图、验收标准 | 需求变化需产品负责人确认 |
| `apps/admin-console` | 前端 | 页面、路由、状态、接口调用 | API 变化需后端确认 |
| `services/api-server` | 后端 | API、认证、业务、存储 | 模型与设备契约需相应负责人确认 |
| `ml` | 算法 | 特征、基线、模型、评估、推理契约 | 输入输出变化需后端确认 |
| `firmware` | 嵌入式 | BLE、采样、设备协议、联调工具 | 协议变化需后端和算法确认 |
| `data` | 后端主责，五方按需共审 | 数据字典、Schema、合成样例、治理 | 四方共同评审 |
| `docs` | 文档主题负责人 | 产品、架构、接口、决策和协作规范 | 按主题邀请相关负责人 |
| `scripts` | 脚本所属模块负责人 | 本地测试和辅助工具 | 禁止写入真实凭据 |

### 所有权原则

- 产品负责人对产品价值、需求范围和验收负责；技术目录负责人对技术质量和最终合并负责，任何所有权都不能跳过评审。
- 跨两个及以上责任域的变更必须至少由受影响域的一名负责人审核。
- 公共契约先更新文档和版本，再修改实现。
- 临时跨目录修改必须在 PR 中说明原因、影响和后续负责人。
- 实际 GitHub 用户名确定后，应同步更新 `.github/CODEOWNERS`。

### 双语文档

所有新增或修改的 Markdown 文件必须采用中文在前、英文在后的双语结构。代码、字段名、路径和命令只保留一种原始写法。

## English

| Path | Primary owner | Contents | Cross-domain requirement |
|---|---|---|---|
| `docs/product` | Product | PRDs, user research, roadmap, acceptance criteria | Product approval for requirement changes |
| `apps/admin-console` | Frontend | Pages, routing, state, API calls | Backend approval for API changes |
| `services/api-server` | Backend | APIs, authentication, business logic, storage | Relevant approval for model and device contracts |
| `ml` | Algorithm | Features, baselines, models, evaluation, inference contracts | Backend approval for input/output changes |
| `firmware` | Embedded | BLE, sampling, device protocols, integration tools | Backend and algorithm approval for protocol changes |
| `data` | Backend primary, reviewed by all affected domains | Dictionaries, schemas, synthetic samples, governance | Review by all affected roles |
| `docs` | Document-topic owner | Product, architecture, contracts, decisions, collaboration | Review by relevant domain owners |
| `scripts` | Owning module | Local tests and helpers | Real credentials are forbidden |

### Ownership principles

- The product owner is accountable for value, scope, and acceptance. Technical directory owners are accountable for technical quality and final merging. No ownership removes review requirements.
- Changes spanning two or more domains require approval from at least one owner of every affected domain.
- Update and version shared contracts before changing implementations.
- Temporary cross-directory edits must explain the reason, impact, and follow-up owner in the PR.
- Update `.github/CODEOWNERS` after the team's actual GitHub usernames are known.

### Bilingual documentation

Every new or modified Markdown file must use a Chinese-first, English-second structure. Code, field names, paths, and commands remain in their original single form.
