import csv

# 입력 파일과 출력 파일 이름 설정
input_file = './data.md'
output_file = 'output.csv'

# 칼럼 이름 정의
columns = [
    "순위", "단지명", "자치구", "총 임대 세대수", "최초입주", 
    "전용면적 (㎡)", "총모집", "예비자모집", "계산값", "보정값"
]

# 데이터를 저장할 리스트
data = []

# 입력 파일 읽기
with open(input_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 데이터 파싱
for i in range(0, len(lines), 20):  # 20줄씩 건너뛰며 처리 (한 항목이 20줄)
    if i + 19 < len(lines):  # 충분한 줄이 남아있는지 확인
        순위 = lines[i].strip()
        단지명 = lines[i+2].strip()
        자치구 = lines[i+4].strip()
        총임대세대수 = lines[i+6].strip()
        최초입주 = lines[i+8].strip()
        전용면적 = lines[i+10].strip()
        총모집 = lines[i+12].strip()
        예비자모집 = lines[i+14].strip()
        계산값 = lines[i+16].strip()
        보정값 = lines[i+18].strip()
        
        row = [순위, 단지명, 자치구, 총임대세대수, 최초입주, 전용면적, 총모집, 예비자모집, 계산값, 보정값]
        data.append(row)

# CSV 파일로 저장
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(columns)  # 칼럼 이름 쓰기
    writer.writerows(data)  # 데이터 쓰기

print(f"데이터가 {output_file}로 저장되었습니다.")
print(f"총 {len(data)}개의 항목이 처리되었습니다.")
