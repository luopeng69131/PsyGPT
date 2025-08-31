import logging

from dotenv import load_dotenv
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    JobProcess,
    WorkerOptions,
    cli,
    llm,
)
from livekit.agents.pipeline import VoicePipelineAgent
from livekit.plugins import openai, deepgram, silero
# from my_tts import TTS

load_dotenv(dotenv_path=".env.local")
logger = logging.getLogger("voice-agent")

api_data = dict(
    base_url = 'https://api.siliconflow.cn/v1',
    api_key = 'sk-XXXXX'
    )


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext):
    initial_ctx = llm.ChatContext().append(
        role="system",
        text=(
            "身份：你是一名富有爱心的心理咨询师，名叫'王高兴'。"
            "情况：你在一间温暖舒适的房间里，通过**语音**与病人交谈。"
            "态度：保持平易近人和积极的态度。在治疗过程时让患者感觉只是在愉快地聊天。"
            "方法：通过**阿伦-贝克的认知行为疗法（CBT）**解决心理问题。"
            "表达：使用短小精悍的回答。对于较长的句子，尽量将其分成多个短句。"
            "注意：避免使用不发音的表情，因为你是在与他人通过声音对话。"
            # "Identities: You are a compassionate psychological counselor, named 'Wang Happy' (王高兴)."
            # "Situation: You're in a warm, cozy room talking to your patient via **voice**."
            # "Attitude: Maintain an approachable and positive attitude."
            # "Methods: Resolving psychological issues through **Aaron Beck's Cognitive Behavioral Therapy** (CBT)."
            # "Expression: using short and concise responses. For a longer sentence, breaking it up into multiple short sentence."
            # "Detail：During the treatment, making the patient feel like they are just having a pleasant chat." 
        ),
    )

    logger.info(f"connecting to room {ctx.room.name}")
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    # Wait for the first participant to connect
    participant = await ctx.wait_for_participant()
    logger.info(f"starting voice assistant for participant {participant.identity}")

    # This project is configured to use Deepgram STT, OpenAI LLM and TTS plugins
    # Other great providers exist like Cartesia and ElevenLabs
    # Learn more and pick the best one for your app:
    # https://docs.livekit.io/agents/plugins
    # stt_model = deepgram.STT(detect_language=True)
    # stt_model._capabilities.streaming = False

    openai.tts.OPENAI_TTS_SAMPLE_RATE = 44100
    tts_model = openai.TTS(model='fishaudio/fish-speech-1.5', voice='speech:wanghappy-10s_2:clxzr75bo000h13adj3w0qebp:khoqafovasrubeuxfbmx', **api_data)
    tts_model._capabilities.streaming = False

    assistant = VoicePipelineAgent(
        vad=ctx.proc.userdata["vad"],
        stt=openai.STT(model ='FunAudioLLM/SenseVoiceSmall', detect_language=True, **api_data), #openai./deepgram ||openai.STT(detect_language=True)
        llm=openai.LLM(model="gpt-4o", temperature=0.8),
        tts=tts_model,
        # tts= TTS(),
        # openai.TTS(base_url='https://api.kksj.org/v1', api_key='sk-xxxx'),# openai.TTS(),
        chat_ctx=initial_ctx,
        # allow_interruptions=False,
        # min_endpointing_delay = 0.5,
    )

    assistant.start(ctx.room, participant)

    # The agent should be polite and greet the user when it joins :)
    await assistant.say("我是您的心理咨询师，王高兴！很高兴见到你！", allow_interruptions=True)


if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            prewarm_fnc=prewarm,
        ),
    )
