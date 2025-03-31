import csv
from langchain_community.chat_models import ChatOllama
from langchain.schema import HumanMessage

# Ollama LLM 초기화
llm = ChatOllama(model="llama3.1:8b")

input_file = 'output.csv'
output_file = 'google_my_maps_data.csv'

def get_detailed_address(name, district):
    prompt = f"서울특별시 {district}에 있는 '{name}' 아파트의 정확한 주소를 알려주세요. 도로명 주소로 답변해 주세요."
    messages = [HumanMessage(content=prompt)]
    response = llm.invoke(messages)
    return response.content

with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = ['Name', 'Address', 'Description']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for row in reader:
        name = row['단지명']
        district = row['자치구']
        
        # LLM을 사용하여 상세 주소 생성
        detailed_address = get_detailed_address(name, district)
        
        description = f"순위: {row['순위']}, 총 임대 세대수: {row['총 임대 세대수']}, 최초입주: {row['최초입주']}, 전용면적: {row['전용면적 (㎡)']}"
        
        writer.writerow({
            'Name': name,
            'Address': detailed_address,
            'Description': description
        })

print(f"데이터가 {output_file}로 저장되었습니다.")

