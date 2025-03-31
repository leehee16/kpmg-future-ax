from openai import OpenAI
import os
from dotenv import load_dotenv

# .env 파일에서 환경변수 로드
load_dotenv()

# 환경변수에서 OpenAI API 키 가져오기
api_key = os.getenv('open_api_key')

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=api_key)

print("인증 성공")


from pathlib import Path
with client.audio.speech.with_streaming_response.create(
    model="tts-1",
    voice="alloy",
    input="오늘은 내가 가장 행복한 날입니다."
) as response:
    response.stream_to_file("speech.mp3")


# 음성 파일 open
audio_file= open("audio.mp3", "rb")

# speech to text 변환
# 스크립트로 변환
response = client.audio.transcriptions.create(
# 영어번역
# response = client.audio.translations.create(
model="whisper-1",
file=audio_file,
response_format="text"
)
print(response)

print(response.replace(".", "\n"))
