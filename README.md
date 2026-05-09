# 🎙️ AI口播智能体 - Talking Agent

一个智能口播系统，支持**个人音色克隆**、**自然语音生成**和**感情化表达**的自媒体内容生成工具。

## 🎯 核心功能

### 1. 音色克隆（Voice Cloning）
- 通过用户提供的音频样本（3-5分钟）进行音色学习
- 提取音高、语速、音量、��鸣等声学特征
- 保留个人音色特质的长期记忆

### 2. 智能文字转语音（Expressive TTS）
- 支持纯文本输入转换为自然语音
- 自动检测句子情感倾向和语境
- 动态调整音调、停顿、速度

### 3. 情感化表达（Prosody Control）
- 🎭 **句子级情感**：根据标点符号和语义自动调整语调
- ⏱️ **停顿控制**：在自然的语义边界处插入恰当停顿
- 📊 **动态速率**：强调词汇加快或减速，制造张力
- 🎼 **音高变化**：避免单调，使用抑扬顿挫

## 🏗️ 技术架构

```
┌─────────────────────────────────────────────────────────┐
│                    前端交互层                             │
│        (Web UI / 命令行 / API)                          │
└────────────────┬────────────────────────────────────────┘
                 │
    ┌────────────┼────────────┬──────────────┐
    │            │            │              │
    ▼            ▼            ▼              ▼
┌─────────┐ ┌─────────┐ ┌──────────┐ ┌─────────────┐
│ 音色管理 │ │文本处理 │ │ 情感分析 │ │ 语音合成    │
│ 模块    │ │ 模块   │ │  模块   │ │ 引擎       │
└─────────┘ └─────────┘ └──────────┘ └─────────────┘
    │            │            │              │
    └────────────┼────────────┴──────────────┘
                 │
         ┌───────▼────────┐
         │  音频输出模块   │
         │ (MP3/WAV/M4A)  │
         └────────────────┘
```

## 📋 实现路线图

### Phase 1: 基础架构 (第1-2周)
- [ ] 项目结构搭建
- [ ] API接口定义
- [ ] 数据库设计（用户、音色库、任务队列）

### Phase 2: 音色克隆引擎 (第3-4周)
- [ ] 音频预处理（降噪、归一化）
- [ ] 声学特征提取（Mel-Spectrogram, F0等）
- [ ] 音色指纹生成和存储

### Phase 3: 情感化TTS (第5-7周)
- [ ] 文本情感分析模块
- [ ] 停顿和语速预测
- [ ] 基础TTS引擎集成
- [ ] Prosody参数动态调整

### Phase 4: 质量优化 (第8周)
- [ ] 合成音频后处理
- [ ] A/B测试和优化
- [ ] 性能和延迟优化

## 🛠️ 技术栈推荐

### 后端
- **语言**: Python 3.10+
- **框架**: FastAPI / Flask
- **音频处理**: librosa, soundfile, scipy
- **TTS引擎**: 
  - Tortoise-TTS (高质量，支持多说话人)
  - Vall-E X (最新，效果最好)
  - Glow-TTS + HiFi-GAN (轻量级)
- **情感分析**: Transformers (BERT-based)
- **声学特征**: VoiceConversionWebUI, resemblyzer

### 前端
- **Web UI**: React / Vue3
- **音频播放**: Wavesurfer.js
- **实时录音**: RecordRTC

### 部署
- Docker容器化
- GPU支持（CUDA 12.0+）
- 消息队列：Redis / Celery（异步处理）

## 📁 项目结构

```
talking/
├── README.md
├── requirements.txt
├── docker-compose.yml
├── .github/
│   └── workflows/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models/          # 数据模型
│   │   ├── api/             # API路由
│   │   ├── services/        # 业务逻辑
│   │   │   ├── voice_clone/
│   │   │   ├── tts/
│   │   │   ├── emotion/
│   │   │   └── prosody/
│   │   ├── utils/
│   │   └── config.py
│   ├── ml_models/           # 预训练模型
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   └── package.json
└── docs/
    ├── api.md
    ├── architecture.md
    └── deployment.md
```

## 🔑 关键实现要点

### 1. 音色克隆流程
```
用户上传示例音频(3-5min)
         ↓
    音频预处理（降噪/正规化）
         ↓
    提取声学特征（Speaker Embedding）
         ↓
    生成音色指纹 & 存储
         ↓
    后续生成时引用此音色
```

### 2. 情感化表达系统
- **文本分析**：标点符号、关键词识别、句子类型分类
- **情感预测**：NLP模型推断文本的情感倾向（正/中/负）
- **参数映射**：
  - 疑问句 → 音高上升 + 末端停顿
  - 感叹句 → 加强语调 + 提高音量
  - 强调词 → 减速 + 提高音量
  - 逗号 → 短停顿 (0.2s)
  - 句号 → 长停顿 (0.5s)

### 3. 合成优化
- **Mel-Spectrogram调整**：根据情感参数动态修改频谱
- **音高轮廓曲线**：实现自然的抑扬顿挫
- **能量调整**：强调重点词汇
- **后��理**：去除合成伪影，提升自然度

## 🚀 快速开始

```bash
# 克隆项目
git clone https://github.com/uway444me-beep/talking.git
cd talking

# 创建虚拟环境
python -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动服务
python backend/app/main.py

# 访问API文档
# http://localhost:8000/docs
```

## 📞 API示例

### 上传音色样本
```bash
POST /api/v1/voices/clone
Content-Type: multipart/form-data

{
  "voice_name": "my_voice",
  "audio_file": <binary>
}
```

### 生成语音
```bash
POST /api/v1/synthesis
{
  "text": "你好，欢迎来到我的频道！",
  "voice_id": "my_voice",
  "emotion": "positive",
  "prosody_level": 0.8
}
```

## 📚 参考资源

- [Tortoise-TTS](https://github.com/neonbjb/tortoise-tts)
- [VALL-E X](https://github.com/Plachtaa/VALL-E-X)
- [librosa文档](https://librosa.org/)
- [Hugging Face Transformers](https://huggingface.co/transformers/)
- [SpeechBrain](https://speechbrain.github.io/)

## 🤝 贡献指南

欢迎提交Issue和PR！

## 📄 许可证

MIT License

---

**下一步**：查看 `docs/` 目录获取详细的架构设计和API文档
