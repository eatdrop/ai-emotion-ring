# 数据治理 / Data Governance

## 中文

本目录仅保存数据结构、字段字典、合成样例和治理说明。真实用户数据、导出的用户资料、日志和设备标识不得进入公开仓库。

### 数据规则

- 每个字段必须定义名称、类型、单位、是否必填、取值范围和缺失值处理。
- 时间统一使用 ISO 8601 UTC；设备原始时间必须保留来源和时区信息。
- 样例数据必须完全合成，不能由真实用户数据简单改名得到。
- 数据结构变更必须有版本号、迁移说明、兼容期和负责人。
- 算法训练数据必须记录授权、去标识化、切分方法和保留期限。
- 删除请求必须覆盖主数据、派生数据、缓存和可定位备份。

### 文档规则

本目录新增或修改的 Markdown 文件必须中英双语，中文在前、英文在后。字段名和代码保持一种写法，不做翻译。

## English

This directory stores only schemas, data dictionaries, synthetic samples, and governance notes. Real user data, exported profiles, logs, and device identifiers must never enter the public repository.

### Data rules

- Every field must define its name, type, unit, required status, valid range, and missing-value handling.
- Use ISO 8601 UTC for time. Preserve source and timezone information for device-originated timestamps.
- Sample data must be fully synthetic and must not be created by merely renaming real user data.
- Schema changes require a version, migration notes, a compatibility window, and an owner.
- Algorithm datasets must document authorization, de-identification, splitting, and retention.
- Deletion requests must cover primary data, derived data, caches, and identifiable backups.

### Documentation rule

Every new or modified Markdown file in this directory must be bilingual, Chinese first and English second. Field names and code identifiers remain unchanged and are not translated.
