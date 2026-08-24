# 沟通与决策记录 / Communication and Decision Records

## 中文

### 固定节奏

- 周一：确定本周目标、负责人、接口依赖和验收标准。
- 周三：同步进度、阻塞、风险和契约变化。
- 周五：合并、联调、演示和复盘。
- 紧急阻塞不等待例会，应立即在 Issue 中通知受影响负责人。

### 记录位置

- Issue：任务、缺陷、验收标准和负责人。
- Pull Request：实现、评审、测试和合并记录。
- ADR：不可轻易逆转的架构决策。
- 接口文档：API、BLE、算法和数据契约。
- 会议纪要：结论、负责人和截止时间，不记录无结论的长篇聊天。

### 决策规则

事实和测试结果优先于职位。无法达成一致时，由受影响范围最大的责任人组织决策；涉及产品范围由项目负责人决定，涉及安全和隐私时选择风险更低的方案。临时决策必须注明失效时间和复审日期。

所有正式 Markdown 记录必须中英双语。

## English

### Cadence

- Monday: set weekly goals, owners, contract dependencies, and acceptance criteria.
- Wednesday: synchronize progress, blockers, risks, and contract changes.
- Friday: merge, integrate, demonstrate, and review.
- Do not wait for a meeting when blocked; notify affected owners in an Issue immediately.

### System of record

- Issue: task, defect, acceptance criteria, and owner.
- Pull Request: implementation, review, tests, and merge record.
- ADR: architectural decisions that are costly to reverse.
- Contract documents: API, BLE, algorithm, and data contracts.
- Meeting notes: decisions, owners, and deadlines—not long undecided chat transcripts.

### Decision rules

Evidence and test results take priority over title. If agreement is impossible, the owner with the broadest affected scope facilitates the decision. The project lead decides product scope; choose the lower-risk option for security and privacy. Temporary decisions require an expiry and review date.

All formal Markdown records must be bilingual.
