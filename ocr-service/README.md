# OCR 微服务

基于 PaddleOCR 的独立文字识别服务，提供 HTTP API 接口供其他项目调用。

## 特性

- ✅ **独立部署**：完全独立的微服务，不依赖任何其他项目
- ✅ **跨项目调用**：任何语言的项目都可以通过 HTTP 接口调用
- ✅ **高性能**：OCR 引擎只初始化一次，常驻内存，响应速度快
- ✅ **易于迁移**：整个目录可以随意移动到任何位置
- ✅ **自动化脚本**：提供一键安装、启动、测试脚本

## 快速开始

### 1. 首次使用（环境初始化）

```bash
cd /Users/liuwu/Desktop/test/ocr-service
chmod +x *.sh
./setup.sh
```

这个脚本会自动：
- 创建 Python 虚拟环境
- 安装所有依赖（PaddleOCR、FastAPI 等）
- 下载 OCR 模型文件

⏱️ 预计耗时：3-5 分钟（取决于网络速度）

### 2. 启动服务

```bash
./start.sh
```

启动成功后，您会看到：
```
🚀 启动 OCR 微服务...
📡 服务地址: http://0.0.0.0:8000
📖 API 文档: http://0.0.0.0:8000/docs
```

### 3. 测试服务

打开新的终端窗口：

```bash
cd /Users/liuwu/Desktop/test/ocr-service
./test.sh
```

或手动测试：

```bash
# 健康检查
curl http://localhost:8000/

# OCR 识别（需要替换为实际图片路径）
curl -X POST -F "file=@test.jpg" http://localhost:8000/ocr/extract
```

### 4. 停止服务

在运行服务的终端按 `Ctrl+C`

## API 接口说明

### 1. 健康检查

**接口**: `GET /`

**返回示例**:
```json
{
  "service": "OCR 微服务",
  "status": "running",
  "version": "1.0.0",
  "timestamp": "2026-01-28T12:00:00"
}
```

### 2. OCR 文字识别（简洁版）

**接口**: `POST /ocr/extract`

**参数**:
- `file`: 图片文件（支持 jpg, png, bmp, tiff, webp）

**返回示例**:
```json
{
  "code": 200,
  "message": "识别成功",
  "data": {
    "texts": [
      "第一行文字",
      "第二行文字",
      "第三行文字"
    ],
    "count": 3
  }
}
```

### 3. OCR 文字识别（详细版）

**接口**: `POST /ocr/extract_detail`

**参数**:
- `file`: 图片文件

**返回示例**:
```json
{
  "code": 200,
  "message": "识别成功",
  "data": {
    "results": [
      {
        "text": "识别的文字",
        "confidence": 0.98,
        "coordinates": [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
      }
    ],
    "count": 1
  }
}
```

## 在其他项目中调用

### Python 调用示例

```python
import requests

# OCR 识别
url = "http://localhost:8000/ocr/extract"
files = {'file': open('test.jpg', 'rb')}
response = requests.post(url, files=files)
result = response.json()

print(result['data']['texts'])  # 输出识别的文字列表
```

### Java 调用示例

```java
// 使用 OkHttp
OkHttpClient client = new OkHttpClient();

RequestBody requestBody = new MultipartBody.Builder()
    .setType(MultipartBody.FORM)
    .addFormDataPart("file", "test.jpg",
        RequestBody.create(new File("test.jpg"), MediaType.parse("image/jpeg")))
    .build();

Request request = new Request.Builder()
    .url("http://localhost:8000/ocr/extract")
    .post(requestBody)
    .build();

Response response = client.newCall(request).execute();
String result = response.body().string();
```

### JavaScript/Node.js 调用示例

```javascript
const FormData = require('form-data');
const fs = require('fs');
const axios = require('axios');

const form = new FormData();
form.append('file', fs.createReadStream('test.jpg'));

axios.post('http://localhost:8000/ocr/extract', form, {
  headers: form.getHeaders()
})
.then(response => {
  console.log(response.data.data.texts);
})
.catch(error => {
  console.error(error);
});
```

### cURL 调用示例

```bash
curl -X POST \
  -F "file=@/path/to/image.jpg" \
  http://localhost:8000/ocr/extract
```

## 目录迁移

这个服务是完全独立的，您可以将整个 `ocr-service` 目录移动到任何位置：

```bash
# 移动到其他位置
mv /Users/liuwu/Desktop/test/ocr-service /Users/liuwu/Projects/ocr-service

# 进入新位置
cd /Users/liuwu/Projects/ocr-service

# 直接启动（无需重新配置）
./start.sh
```

## 生产环境部署建议

### 1. 使用进程管理器（推荐 Supervisor 或 systemd）

创建 systemd 服务文件 `/etc/systemd/system/ocr-service.service`:

```ini
[Unit]
Description=OCR 微服务
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/ocr-service
ExecStart=/path/to/ocr-service/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：
```bash
sudo systemctl start ocr-service
sudo systemctl enable ocr-service  # 开机自启
```

### 2. 使用 Nginx 反向代理

```nginx
server {
    listen 80;
    server_name ocr.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 3. 配置 HTTPS（使用 Let's Encrypt）

```bash
sudo certbot --nginx -d ocr.yourdomain.com
```

## 性能优化

### 1. 使用 GPU 加速（如果有 NVIDIA GPU）

修改 `app.py` 中的初始化参数：
```python
ocr_util = PaddleOCRUtil(use_gpu=True, ocr_version='PP-OCRv4')
```

### 2. 调整并发数

修改 `app.py` 中的 uvicorn 配置：
```python
uvicorn.run(
    app,
    host="0.0.0.0",
    port=8000,
    workers=4  # 根据 CPU 核心数调整
)
```

## 常见问题

### Q: 首次启动很慢？
A: 首次运行时会自动下载 OCR 模型文件（约 100MB），请耐心等待。模型会缓存在 `~/.paddleocr/` 目录，后续启动会很快。

### Q: 如何更换 OCR 模型版本？
A: 修改 `app.py` 中的 `ocr_version` 参数，可选值：`PP-OCRv4`、`PP-OCRv3` 等。

### Q: 如何修改服务端口？
A: 修改 `app.py` 最后的 `port=8000` 为其他端口。

### Q: 支持哪些图片格式？
A: 支持 jpg, jpeg, png, bmp, tiff, webp 等常见格式。

## 技术栈

- **Web 框架**: FastAPI 0.115.0
- **OCR 引擎**: PaddleOCR 2.9.1
- **深度学习框架**: PaddlePaddle 3.0.0b2
- **图像处理**: OpenCV, Pillow
- **ASGI 服务器**: Uvicorn

## 许可证

MIT License

## 联系方式

如有问题，请联系项目维护者。
