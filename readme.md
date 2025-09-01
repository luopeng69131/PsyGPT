<p align="center">
  <img src="assets/chat_transparent.png" alt="PsyGPT Logo" width="200"/>
</p>

<!-- # PsyGPT -->

**PsyGPT** 是一个**抚慰心灵**的AI实时语音聊天机器人，希望能帮助用户治愈抑郁等心理问题。
该AI采用**阿伦·贝克的认知行为疗法**作为核心治疗方法论。语音声线可由**真人声音**驱动。

<!-- --- -->

## 示例 Demo

[B站：【我把一个小时两千元的心理咨询服务做成了开源免费的AI心理咨询师】](https://www.bilibili.com/video/BV1WSkEY6EUd/?share_source=copy_web)

<!-- --- -->

## 提前准备

运行 PsyGPT 前，需要准备以下**API key**和真人声音的**录音**：

* **[Livekit](https://livekit.io/) key**：用于实时语音交互，Livekit 主要提供了一个与 AI 实时互动的直播间。

* **OpenAI API key**：国内建议选择合适的中转平台，问答模型使用了 `GPT-4o` （AI 模型需要具有良好的心理咨询专业能力）。

* **[硅基流动](https://siliconflow.cn/) key**：提供 `TTS`（语音合成）和 `STT`（语音识别）服务。

* **克隆人物的语音声音**：需要提前准备 **10-30 秒的参考音频**（清晰、无噪音、自然语速的语音录音）。  
  <!-- - 将参考音频通过 `upload_ref_voice.py` 脚本上传到硅基平台，并获得对应的 **speech ID**。  
  - 在 `PsyGPT.py` 的 `voice` 字段中填写该 speech ID，以便在运行时使用目标声线进行心理咨询对话。   -->


## 使用流程

### 1. 配置环境

确保安装了 **Livekit 的 Python SDK** 及相关依赖。  
安装 Livekit 的详细步骤可参考 [YouTube 教程](https://www.youtube.com/watch?v=_8VHac0M7d8&ab_channel=AiAustin)。

```bash
pip install -r requirements.txt
```

<!-- --- -->

### 2. 填写 key

1. 在 `env.local` 文件中替换相关 key：  

2. 在PsyGPT.py的 `api_data` 变量中补充 **硅基的 key**（用于 TTS & STT）。

<!-- --- -->

### 3. 上传 AI 声线参考音频

1. **录制一段 10s-30s 的参考音频**（建议为目标声线的清晰语音）。  
2. 在 `upload_ref_voice.py` 中填入**硅基的 key**，**音频文字内容**和**音频在本地路径**，并运行脚本完成声线上传。  
   ```bash
   python upload_ref_voice.py
   ```
3. 脚本执行后，你会获得一个 **speech ID**，如：  
   ```
   speech:wanghappy-10s_2:clxzr75bo000h13adj3w0qebp:khoqafovasrubeuxfbmx
   ```
4. 打开 `PsyGPT.py`，在 TTS 初始化处修改 `voice` 字段，例如：  

   ```python
   tts_model = openai.TTS(
       model="fishaudio/fish-speech-1.5",
       voice="speech:wanghappy-10s_2:clxzr75bo000h13adj3w0qebp:khoqafovasrubeuxfbmx",
       **api_data
   )
   ```

<!-- --- -->

### 4. 启动 PsyGPT 并开启心理咨询之旅
运行PsyGPT服务：
```bash
python PsyGPT.py start
```
进入 Livekit 直播间后，即可与 PsyGPT 进行互动。

<!-- --- -->

## 致谢

视频中语音声音由 **上海贝克心理治疗师 王高兴** 的声线支持。

## 免责声明

本项目仅用于 **学习研究与心理健康辅助探索**，不能替代专业的心理医生或治疗师服务。  
请勿将本项目用于 **违法、违规、侵犯他人隐私或权利** 的场景。  
开发者对因使用本项目而产生的任何直接或间接后果不承担法律责任。  

更多使用限制与规范，请参阅 [《可接受使用政策 (AUP)》](./AUP.md)。
