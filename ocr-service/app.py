"""
OCR 微服务 - 基于 PaddleOCR 的独立文字识别服务
提供 HTTP API 接口供其他项目调用
"""
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import tempfile
from pathlib import Path
from ocr_util import PaddleOCRUtil
from datetime import datetime

# 初始化 FastAPI 应用
app = FastAPI(
    title="OCR 微服务",
    description="基于 PaddleOCR 的独立文字识别服务",
    version="1.0.0"
)

# 配置 CORS（允许跨域访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境建议配置具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局初始化 OCR 引擎（只初始化一次，提高性能）
print("🔄 正在初始化 PaddleOCR 引擎...")
ocr_util = PaddleOCRUtil(use_gpu=False, ocr_version='PP-OCRv4')
print("✅ PaddleOCR 引擎初始化完成")


@app.get("/")
async def root():
    """服务健康检查"""
    return {
        "service": "OCR 微服务",
        "status": "running",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/ocr/extract")
async def extract_text(file: UploadFile = File(...)):
    """
    OCR 文字识别接口（支持图片和 PDF）
    
    返回包含页码、坐标、置信度和文字的结构化数据
    """
    allowed_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp', '.pdf'}
    file_ext = Path(file.filename).suffix.lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件格式: {file_ext}。支持的格式: {', '.join(allowed_extensions)}"
        )
    
    temp_file = None
    try:
        content = await file.read()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
            temp_file.write(content)
            temp_path = temp_file.name
        
        print(f"📄 开始识别文件: {file.filename}")
        # 使用新方法提取带元数据的结果
        results = ocr_util.extract_text_with_meta(temp_path)
        print(f"✅ 识别完成，共识别出 {len(results)} 页数据")
        
        return JSONResponse(
            status_code=200,
            content={
                "code": 200,
                "message": "识别成功",
                "data": {
                    "pages": results,
                    "total_pages": len(results)
                }
            }
        )
    
    except Exception as e:
        print(f"❌ OCR 识别失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"OCR 识别失败: {str(e)}")
    
    finally:
        if temp_file and os.path.exists(temp_path):
            try:
                os.unlink(temp_path)
            except Exception as e:
                print(f"⚠️  清理临时文件失败: {str(e)}")


if __name__ == "__main__":
    print("🚀 启动 OCR 微服务...")
    print("📡 服务地址: http://0.0.0.0:8000")
    print("📖 API 文档: http://0.0.0.0:8000/docs")
    print("=" * 50)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
