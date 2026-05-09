"""
FastAPI 后端主程序
Backend API Server

运行: python -m uvicorn backend.app.main:app --reload
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
from pathlib import Path
import uuid
from datetime import datetime

# ===== 初始化 FastAPI 应用 =====
app = FastAPI(
    title="🎙️ AI 口播智能体 API",
    description="智能音色克隆和文字转语音服务",
    version="1.0.0",
)

# ===== 跨域设置 =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== 数据模型 =====

class VoiceCloneRequest(BaseModel):
    """音色克隆请求"""
    voice_name: str  # 音色名称
    description: Optional[str] = None  # 描述


class SpeechSynthesisRequest(BaseModel):
    """语音合成请求"""
    text: str  # 要合成的文本
    voice_id: str  # 音色 ID
    emotion_level: float = 0.7  # 表情度 (0-1)
    speed_factor: float = 1.0  # 语速倍数
    prosody_enabled: bool = True  # 是否启用抑扬顿挫


class VoiceInfo(BaseModel):
    """音色信息"""
    voice_id: str
    voice_name: str
    created_at: str
    description: Optional[str] = None


# ===== 全局变量 =====
OUTPUT_DIR = Path("output")
VOICES_DIR = Path("data/voices")
OUTPUT_DIR.mkdir(exist_ok=True)
VOICES_DIR.mkdir(parents=True, exist_ok=True)


# ===== 健康检查 =====
@app.get("/", tags=["状态"])
def root():
    """API 根路由"""
    return {
        "app": "AI 口播智能体",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health", tags=["状态"])
def health_check():
    """健康检查"""
    return {"status": "healthy"}


# ===== 音色管理 API =====

@app.post("/api/v1/voices/clone", tags=["音色管理"])
async def clone_voice(
    voice_name: str,
    audio_file: UploadFile = File(...),
    description: Optional[str] = None
):
    """
    上传音频并克隆音色
    
    - **voice_name**: 给音色起个名字
    - **audio_file**: 3-5 分钟的 MP3/WAV 音频文件
    - **description**: 可选的描述信息
    """
    try:
        # 验证文件
        if audio_file.content_type not in ["audio/mpeg", "audio/wav", "audio/mp4"]:
            raise HTTPException(status_code=400, detail="不支持的音频格式，请上传 MP3 或 WAV 文件")
        
        # 保存上传的文件
        voice_id = str(uuid.uuid4())
        audio_path = VOICES_DIR / f"{voice_id}_raw.wav"
        
        content = await audio_file.read()
        with open(audio_path, "wb") as f:
            f.write(content)
        
        # TODO: 调用音色克隆模型
        # from backend.services.voice_clone import clone_voice_features
        # result = clone_voice_features(str(audio_path))
        
        return {
            "status": "success",
            "voice_id": voice_id,
            "voice_name": voice_name,
            "message": f"✓ 音色 '{voice_name}' 已保存，正在处理..."
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"音色克隆失败: {str(e)}")


@app.get("/api/v1/voices", tags=["音色管理"])
def list_voices():
    """
    获取所有已保存的音色列表
    """
    try:
        voices = []
        for voice_dir in VOICES_DIR.glob("*"):
            if voice_dir.is_dir():
                # 读取元数据
                # TODO: 从数据库读取
                voices.append({
                    "voice_id": voice_dir.name,
                    "voice_name": voice_dir.name,
                    "created_at": datetime.now().isoformat()
                })
        
        return {
            "status": "success",
            "voices": voices,
            "count": len(voices)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/v1/voices/{voice_id}", tags=["音色管理"])
def delete_voice(voice_id: str):
    """
    删除指定音色
    """
    try:
        # TODO: 从数据库删除 + 删除文件
        return {
            "status": "success",
            "message": f"✓ 音色已删除"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===== 语音合成 API =====

@app.post("/api/v1/synthesis", tags=["文字转语音"])
async def synthesize_speech(request: SpeechSynthesisRequest):
    """
    合成语音
    
    - **text**: 要合成的文字（最多 1000 字）
    - **voice_id**: 使用哪个音色
    - **emotion_level**: 表情度 (0.0-1.0)
    - **speed_factor**: 语速倍数 (0.5-2.0)
    """
    try:
        # 参数验证
        if not request.text:
            raise HTTPException(status_code=400, detail="文字不能为空")
        
        if len(request.text) > 1000:
            raise HTTPException(status_code=400, detail="文字不能超过 1000 字")
        
        if not (0 <= request.emotion_level <= 1):
            raise HTTPException(status_code=400, detail="表情度应在 0-1 之间")
        
        # TODO: 调用 TTS 合成引擎
        # from backend.services.tts import synthesize
        # output_file = synthesize(
        #     text=request.text,
        #     voice_id=request.voice_id,
        #     emotion=request.emotion_level,
        #     speed=request.speed_factor,
        #     prosody=request.prosody_enabled
        # )
        
        # 生成输出文件路径
        output_filename = f"output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
        output_path = OUTPUT_DIR / output_filename
        
        return {
            "status": "success",
            "task_id": str(uuid.uuid4()),
            "text": request.text,
            "voice_id": request.voice_id,
            "output_file": output_filename,
            "message": "✓ 正在生成，请稍候..."
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"合成失败: {str(e)}")


@app.get("/api/v1/synthesis/{task_id}", tags=["文字转语音"])
def get_synthesis_status(task_id: str):
    """
    查询合成状态
    """
    try:
        # TODO: 从任务队列查询状态
        return {
            "task_id": task_id,
            "status": "completed",  # pending / processing / completed / failed
            "progress": 100,
            "output_file": "output_20260509_153000.mp3"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/download/{filename}", tags=["文件下载"])
def download_file(filename: str):
    """
    下载生成的音频文件
    """
    try:
        file_path = OUTPUT_DIR / filename
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="文件不存在")
        
        return FileResponse(
            path=file_path,
            media_type="audio/mpeg",
            filename=filename
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===== 统计信息 =====

@app.get("/api/v1/stats", tags=["统计"])
def get_statistics():
    """
    获取系统统计信息
    """
    try:
        # 计算音色数量
        voice_count = len(list(VOICES_DIR.glob("*")))
        
        # 计算输出文件数量
        output_count = len(list(OUTPUT_DIR.glob("*.mp3")))
        
        return {
            "status": "success",
            "voice_count": voice_count,
            "output_count": output_count,
            "storage_used_mb": sum(f.stat().st_size for f in OUTPUT_DIR.glob("*")) / (1024 * 1024)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===== 错误处理 =====

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """HTTP 异常处理"""
    return {
        "status": "error",
        "error_code": exc.status_code,
        "message": exc.detail
    }


# ===== 启动事件 =====

@app.on_event("startup")
async def startup_event():
    """应用启动时执行"""
    print("✅ API 服务已启动")
    print(f"📁 工作目录: {Path.cwd()}")
    print(f"📚 音色库: {VOICES_DIR}")
    print(f"📁 输出目录: {OUTPUT_DIR}")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时执行"""
    print("❌ API 服务已关闭")


# ===== 启动命令 =====
# uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
