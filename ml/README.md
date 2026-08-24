# 算法与机器学习 / Algorithm and Machine Learning

## 中文

本目录由算法负责人维护，用于生理信号处理、特征工程、个体基线、模型评估和推理接口。

### 责任边界

- 定义算法输入、输出、版本和置信度含义。
- 使用经授权、去标识化的数据进行训练和评估。
- 记录数据集来源、切分方式、指标、偏差和已知失败场景。
- 提供可复现的训练或评估命令。
- 与后端通过版本化推理契约协作，不直接依赖前端或设备实现。

### 强制规则

- 不将趋势评分描述为医学诊断。
- 不提交真实用户原始数据、模型访问密钥或含个人信息的产物。
- 模型变更必须说明指标变化和回滚方案。
- 输入输出字段变化必须先更新双语接口文档。
- 本目录新增或修改的 Markdown 文件必须中英双语，中文在前、英文在后。

## English

This directory is owned by the algorithm lead and covers physiological-signal processing, feature engineering, personalized baselines, model evaluation, and inference contracts.

### Responsibility boundary

- Define algorithm inputs, outputs, versions, and confidence semantics.
- Train and evaluate only on authorized, de-identified data.
- Record dataset provenance, splits, metrics, bias, and known failure modes.
- Provide reproducible training or evaluation commands.
- Integrate with the backend through a versioned inference contract without depending directly on frontend or device implementations.

### Mandatory rules

- Never describe trend scores as medical diagnoses.
- Never commit raw user data, model access secrets, or artifacts containing personal information.
- Every model change must document metric impact and rollback.
- Input or output field changes require a bilingual contract update first.
- Every new or modified Markdown file in this directory must be bilingual, Chinese first and English second.
