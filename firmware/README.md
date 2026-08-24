# 固件与嵌入式接入 / Firmware and Embedded Integration

## 中文

本目录由嵌入式负责人维护，定义硬件接入、BLE 协议、采样行为和设备侧测试边界。当前仓库不包含供应商私有固件或设备密钥。

### 责任边界

- 定义服务 UUID、特征 UUID、命令、字节序、单位和时间戳规则。
- 记录采样频率、量程、精度、丢包和异常值策略。
- 提供合成数据、协议示例和可重复的设备联调步骤。
- 维护固件版本与协议版本的兼容关系。
- 向后端交付稳定的数据契约，不直接修改后端存储结构。

### 强制规则

- 协议字段变更必须先提交文档并通知后端和算法负责人。
- 真实设备标识、配对密钥、签名证书和供应商私密资料不得提交。
- 必须测试断连、重连、低电量、重复包、乱序包和无效数据。
- 本目录新增或修改的 Markdown 文件必须中英双语，中文在前、英文在后。

## English

This directory is owned by the embedded lead and defines hardware integration, BLE protocols, sampling behavior, and device-side testing. Vendor-private firmware and device secrets are not included.

### Responsibility boundary

- Define service UUIDs, characteristic UUIDs, commands, byte order, units, and timestamp rules.
- Document sampling frequency, range, accuracy, packet loss, and outlier handling.
- Provide synthetic data, protocol examples, and reproducible integration steps.
- Maintain compatibility between firmware and protocol versions.
- Deliver a stable data contract to the backend without directly changing backend storage.

### Mandatory rules

- Protocol-field changes require documentation and notification to backend and algorithm owners first.
- Never commit real device identifiers, pairing keys, signing certificates, or vendor-confidential material.
- Test disconnects, reconnects, low battery, duplicates, out-of-order packets, and invalid data.
- Every new or modified Markdown file in this directory must be bilingual, Chinese first and English second.
