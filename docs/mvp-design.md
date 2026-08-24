# 最小可行产品设计 / Minimum Viable Product Design

## 中文

### 产品目标

MVP 用于验证：可穿戴设备采集的生理信号能否通过稳定的数据链路形成个人基线、趋势提示和可执行的健康建议。MVP 不验证医疗诊断能力，也不承诺识别人的真实情绪。

### 核心用户流程

1. 用户或测试人员绑定设备。
2. 设备采集并上传带时间戳的生理数据。
3. 后端完成身份校验、数据校验、存储和查询。
4. 算法基于个体历史数据计算基线、趋势和置信度。
5. 前端展示数据质量、趋势、解释和建议。
6. 管理端查看设备、用户、数据质量和系统运行状态。

### MVP 必须包含

- 用户认证和最小权限控制。
- 设备绑定、解绑、在线状态和数据上传。
- 心率等基础生理数据的接收、校验、存储和查询。
- 个人基线与趋势评分，且输出置信度和数据质量。
- 管理端的数据看板、用户列表、设备列表和趋势报告。
- 可追踪的接口错误、日志规范和最小测试。
- 数据脱敏、删除策略和公开仓库安全规则。

### 暂不纳入 MVP

- 医疗诊断或疾病预测。
- 在缺少真实合规数据时大规模训练复杂模型。
- 同时支持大量硬件型号。
- 复杂会员、支付、社交和内容社区。
- 未经验证的自动干预或高风险建议。
- 为比赛展示而制作但无法进入真实用户流程的孤立功能。

### 成功指标

- 设备数据成功入库率。
- 数据字段和时间戳有效率。
- API 成功率与延迟。
- 算法输出覆盖率、稳定性和置信度校准情况。
- 用户是否理解趋势含义并能采取行动。
- 关键流程是否能在真实设备上重复演示。

### 当前限制

当前仓库提供管理端和后端基础代码。移动端、真实设备固件、完整算法训练流程和生产部署能力尚不能仅凭仓库内容确认，必须作为后续里程碑验证。

## English

### Product goal

The MVP validates whether physiological signals collected by a wearable device can flow through a reliable data pipeline and produce personalized baselines, trend indicators, and actionable health guidance. It does not validate medical diagnosis or claim to identify a person's true emotional state.

### Core user flow

1. A user or tester binds a device.
2. The device collects and uploads timestamped physiological data.
3. The backend authenticates, validates, stores, and serves the data.
4. The algorithm calculates baselines, trends, confidence, and data quality from personal history.
5. The frontend presents quality, trends, explanations, and suggestions.
6. The admin console exposes device, user, data-quality, and system status.

### MVP requirements

- User authentication and least-privilege access.
- Device binding, unbinding, online status, and data upload.
- Reception, validation, storage, and querying of basic physiological data.
- Personalized baseline and trend scores with confidence and data-quality indicators.
- Admin dashboards, user lists, device lists, and trend reports.
- Traceable API errors, logging conventions, and minimum tests.
- Data de-identification, deletion rules, and public-repository safety.

### Out of scope for the MVP

- Medical diagnosis or disease prediction.
- Large-scale complex-model training without compliant real-world data.
- Simultaneous support for many hardware models.
- Complex memberships, payments, social features, or content communities.
- Unvalidated automated interventions or high-risk advice.
- Isolated demo features that cannot enter a real user workflow.

### Success metrics

- Device-data ingestion success rate.
- Field and timestamp validity rate.
- API success rate and latency.
- Algorithm coverage, stability, and confidence calibration.
- Whether users understand the trend and can take action.
- Whether the critical flow can be repeatedly demonstrated with real hardware.

### Current limitations

The repository currently contains an admin console and backend foundation. A mobile client, real device firmware, a complete model-training pipeline, and production deployment cannot be confirmed from the repository alone and must be validated in later milestones.
