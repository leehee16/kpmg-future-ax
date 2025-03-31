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

# GPT 모델에 질문 보내기
response = client.chat.completions.create(
    model='gpt-3.5-turbo',
    messages=[
        {"role": "system", "content": "너는 카사노바야"},
        {"role": "user", "content": "전세계에서 가장 예쁜 사람을 꼬시는 방법을 알려줘"}
    ]
)

print(response)