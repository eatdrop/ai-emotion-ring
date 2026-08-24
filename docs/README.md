# 文档索引与维护规则 / Documentation Index and Maintenance Rules

## 中文

### 阅读顺序

1. [贡献与协作规范](../CONTRIBUTING.md)
2. [产品负责人工作规范](product/README.md)
3. [团队角色与责任](collaboration/team-roles.md)
4. [Git 工作流](collaboration/git-workflow.md)
5. [接口与数据契约](collaboration/interface-contracts.md)
6. [代码评审与质量](collaboration/code-review-and-quality.md)
7. [交付、发布与故障处理](collaboration/delivery-release-and-incidents.md)
8. [沟通与决策记录](collaboration/communication-and-decisions.md)
9. [仓库结构](architecture/repository-structure.md)
10. [MVP 设计](mvp-design.md)

### 文档维护规则

- 所有新增或修改的 Markdown 文件必须中英双语，中文在前、英文在后。
- 两种语言必须表达同一规则；发生冲突时暂停合并并修正文档。
- 代码、字段、路径、命令不需要翻译。
- 文档变更应与实现放在同一个 PR，除非是独立文档修正。
- 架构决策使用 ADR 模板，接口变更使用接口变更模板。
- 文档负责人是内容所属责任域的负责人。
- 每次里程碑结束后检查失效链接、过期字段、过期命令和负责人信息。

## English

### Reading order

1. [Contribution guide](../CONTRIBUTING.md)
2. [Product owner workflow](product/README.md)
3. [Team roles and responsibilities](collaboration/team-roles.md)
4. [Git workflow](collaboration/git-workflow.md)
5. [Interface and data contracts](collaboration/interface-contracts.md)
6. [Code review and quality](collaboration/code-review-and-quality.md)
7. [Delivery, release, and incident handling](collaboration/delivery-release-and-incidents.md)
8. [Communication and decision records](collaboration/communication-and-decisions.md)
9. [Repository structure](architecture/repository-structure.md)
10. [MVP design](mvp-design.md)

### Documentation maintenance rules

- Every new or modified Markdown file must be bilingual, Chinese first and English second.
- Both languages must express the same rule. Resolve conflicts before merging.
- Code, fields, paths, and commands do not need translation.
- Documentation changes belong in the same PR as the implementation unless the PR is a documentation-only correction.
- Use the ADR template for architectural decisions and the API-change template for contract changes.
- The owner of the affected domain owns its documentation.
- At every milestone, review broken links, obsolete fields, outdated commands, and ownership information.
