# AI 情绪戒指 / AI Emotion Ring

## 中文

AI 情绪戒指是一个面向生理信号趋势评估、个体基线分析和健康行为干预的企业级产品原型。本项目不提供医疗诊断，模型输出必须被表述为趋势、风险提示或辅助信息。

### 仓库结构

- `apps/admin-console`：Vue 3 + Vite 管理端前端。
- `services/api-server`：Flask API、认证和业务服务。
- `ml`：算法、特征工程、模型评估和推理边界。
- `firmware`：BLE 协议、设备接入和嵌入式边界。
- `data`：数据结构、合成样例和数据治理。
- `docs`：产品、架构和协作文档。
- `scripts`：本地测试辅助脚本。

### 本地运行

后端：

```powershell
cd services/api-server
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:JWT_SECRET_KEY = "请替换为足够长的随机开发密钥"
python run.py
```

管理端：

```powershell
cd apps/admin-console
npm install
npm run dev
```

API 默认地址为 `http://localhost:5000`，Vite 开发服务器通常使用 `http://localhost:5173`。

### 协作入口

开始开发前必须阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 和 [协作文档索引](docs/README.md)。所有新增或修改的 Markdown 文档必须采用中英双语，中文在前、英文在后；Pull Request 必须检查这一项。

### 安全边界

公开仓库不允许提交签名密钥、真实用户数据、运行日志、访问令牌、环境文件、依赖缓存或可识别个人的信息。

## English

AI Emotion Ring is an enterprise-oriented product prototype for physiological-signal trend assessment, personalized baselines, and health-behavior intervention. It is not a medical diagnostic system. Model outputs must be described as trends, risk indicators, or decision-support information.

### Repository layout

- `apps/admin-console`: Vue 3 + Vite administration frontend.
- `services/api-server`: Flask APIs, authentication, and business services.
- `ml`: algorithms, feature engineering, model evaluation, and inference boundary.
- `firmware`: BLE protocols, device integration, and embedded boundary.
- `data`: schemas, synthetic samples, and data governance.
- `docs`: product, architecture, and collaboration documentation.
- `scripts`: local test helpers.

### Local development

Backend:

```powershell
cd services/api-server
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:JWT_SECRET_KEY = "replace-with-a-long-random-development-secret"
python run.py
```

Admin console:

```powershell
cd apps/admin-console
npm install
npm run dev
```

The API defaults to `http://localhost:5000`; the Vite development server normally uses `http://localhost:5173`.

### Collaboration entry point

Read [CONTRIBUTING.md](CONTRIBUTING.md) and the [documentation index](docs/README.md) before development. Every new or modified Markdown file must be bilingual, with Chinese first and English second. Pull Requests must explicitly verify this requirement.

### Security boundary

Never commit signing keys, real user data, runtime logs, access tokens, environment files, dependency caches, or personally identifiable information to this public repository.
