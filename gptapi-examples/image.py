from openai import OpenAI
import os
from dotenv import load_dotenv

# .env 파일에서 환경변수 로드
load_dotenv()

# 환경변수에서 OpenAI API 키 가져오기
api_key = os.getenv('OPEN_API_KEY')

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=api_key)

print("인증 성공")


#이미지 
response = client.images.generate(
    model="dall-e-3",
    prompt="imagining a bear and a rabbit with their bodies joined together, sharing a single torso. The bear would have brown fur and be on one side, while the rabbit, with white fur, would be on the other side. ",
    size = "1024x1024",
    quality="standard",
    n=1,
)
image_url=response.data[0].url

print(image_url)


from PIL import Image

import urllib.request

def display_jpeg_image(url):
    try:
        image_path, _ = urllib.request.urlretrieve(url, "test.jpg")
        print(image_path)
        image = Image.open(image_path)
        image.show()
    except Exception as e:
        print("Error:", e)

jpeg_image_path = "https://cdn.kbmaeil.com/news/photo/201904/811074_839900_5653.jpg"
display_jpeg_image(jpeg_image_path)

