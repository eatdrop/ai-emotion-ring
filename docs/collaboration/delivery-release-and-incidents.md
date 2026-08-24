# 交付、发布与故障处理 / Delivery, Release, and Incident Handling

## 中文

### 里程碑交付

每个里程碑必须包含版本范围、负责人、演示流程、测试结果、已知问题、数据和隐私说明以及回滚方案。比赛演示所用版本必须打 Tag，演示数据必须为合成或经明确授权的数据。

### 发布门禁

- `main` 构建和核心测试通过。
- 接口、算法和固件版本兼容。
- 配置通过环境变量或密钥管理注入。
- 没有真实用户数据、密钥和调试日志进入产物。
- 发布说明中英文一致。
- 明确监控指标、负责人和回滚步骤。

### 版本

应用和服务使用语义化版本。算法模型和固件使用独立版本，并在系统元数据中记录兼容矩阵。

### 故障处理

1. 先保护用户和数据，必要时停用高风险功能。
2. 指定故障负责人和记录人。
3. 记录时间线、影响、临时措施和恢复状态。
4. 恢复后进行无责复盘。
5. 形成修复 Issue、测试和双语复盘文档。

不得在公开 Issue 或日志中粘贴用户数据、Token、密钥和完整生产请求。

## English

### Milestone delivery

Every milestone includes version scope, owners, demo flow, test results, known issues, data/privacy notes, and rollback. Tag competition-demo versions. Demo data must be synthetic or explicitly authorized.

### Release gates

- `main` builds and critical tests pass.
- API, algorithm, and firmware versions are compatible.
- Configuration is injected through environment variables or secret management.
- No real user data, secrets, or debug logs enter artifacts.
- Release notes are consistent in Chinese and English.
- Monitoring, ownership, and rollback steps are explicit.

### Versioning

Applications and services use semantic versioning. Models and firmware use independent versions, with a compatibility matrix recorded in system metadata.

### Incident handling

1. Protect users and data first; disable high-risk functionality when necessary.
2. Name an incident owner and recorder.
3. Record timeline, impact, mitigation, and recovery status.
4. Run a blameless review after recovery.
5. Create remediation Issues, tests, and a bilingual incident report.

Never paste user data, tokens, secrets, or complete production requests into public Issues or logs.
