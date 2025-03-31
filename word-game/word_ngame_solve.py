import tkinter as tk
from tkinter import messagebox
import random
import time
import pyglet
import csv
from datetime import datetime

# 단어 파일에서 단어들을 불러오는 함수
def wordLoad(file_path):
    words = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                clean_word = line.strip()
                if clean_word:  # 빈 줄이 아닌 경우에만 추가
                    words.append(clean_word)
    except FileNotFoundError:
        messagebox.showerror("오류", "단어 파일을 찾을 수 없습니다.")
    return words

# 게임을 시작하는 함수
def gameRun():
    global words, correct_count, total_rounds, start_time, round_count
    
    correct_count = 0
    round_count = 0
    total_rounds = 5
    start_time = time.time()
    
    # 입력 필드와 단어 레이블을 보여줌
    word_label.pack(pady=20)
    entry.pack(pady=10)
    entry.focus()
    start_button.pack_forget()  # 시작 버튼 숨기기
    front_image_label.pack_forget()  # 시작 이미지 숨기기
    
    nextRound()

# 각 라운드를 처리하는 함수
def nextRound():
    global current_word, round_count

    if round_count < total_rounds:
        current_word = random.choice(words)
        word_label.config(text=f"단어를 입력하세요: {current_word}")
        entry.delete(0, tk.END)
        round_count += 1
    else:
        end_time = time.time()
        elapsed_time = end_time - start_time
        saveRecord(correct_count, elapsed_time)
        displayRanks()
        result_message = f"게임 종료! 총 {total_rounds}개 중 {correct_count}개 맞췄습니다.\n"
        result_message += "합격입니다!" if correct_count >= 3 else "불합격입니다."
        result_message += f"\n총 소요 시간: {elapsed_time:.2f}초"
        messagebox.showinfo("결과", result_message)
        root.quit()

# 사용자의 입력을 확인하는 함수
def checkInput(event=None):
    global correct_count
    user_input = entry.get().strip()
    
    if user_input.lower() == current_word.lower():
        correct_count += 1
        play_sound(good_sound)
    else:
        play_sound(bad_sound)
    nextRound()

# 소리를 재생하는 함수
def play_sound(sound_path):
    sound = pyglet.media.load(sound_path, streaming=False)
    sound.play()

# 게임 기록을 저장하는 함수
def saveRecord(correct_count, elapsed_time):
    with open('game_records.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        writer.writerow([correct_count, f"{elapsed_time:.3f}", date_str])

# 게임 기록을 불러와 순위를 계산하고 출력하는 함수
def displayRanks():
    try:
        with open('game_records.csv', 'r') as file:
            reader = csv.reader(file)
            records = sorted(reader, key=lambda x: (-int(x[0]), float(x[1])))

        print("=========== 역대 순위 =============")
        print("id | 맞춘갯수 | 걸린시간 | 등록날짜 | 등수")
        for idx, record in enumerate(records, start=1):
            print(f"({idx}, {record[0]}, '{record[1]}', '{record[2]}', {idx})")
    except FileNotFoundError:
        print("기록된 게임 데이터가 없습니다.")

# 메인 윈도우 초기화
root = tk.Tk()
root.title("워드게임")
root.geometry("800x800")  # 창 크기를 800x800으로 설정

# 단어를 불러오고 변수 초기화
words = wordLoad('/Users/leehojin/Documents/Future_Lab/word_game_problem/data/word.txt')
if not words:
    messagebox.showerror("오류", "단어 목록이 비어 있습니다. 파일에 단어를 추가해주세요.")
    root.destroy()
    exit()

# 소리 파일 경로 설정
good_sound = '/Users/leehojin/Documents/Future_Lab/word_game_problem/assets/good.wav'
bad_sound = '/Users/leehojin/Documents/Future_Lab/word_game_problem/assets/bad.mp3'

# 시작 화면 이미지 경로
front_image_path = '/Users/leehojin/Documents/Future_Lab/word_game_problem/assets/front.png'

# 이미지 로드 및 라벨 설정
try:
    front_image = tk.PhotoImage(file=front_image_path)
    front_image_label = tk.Label(root, image=front_image)
    front_image_label.pack(pady=10)
except tk.TclError:
    front_image_label = tk.Label(root, text="이미지를 로드할 수 없습니다.")
    front_image_label.pack(pady=10)

# 위젯 생성
title_label = tk.Label(root, text="워드게임", font=('Helvetica', 24))  # 타이틀 라벨 추가
title_label.pack(pady=10)

start_button = tk.Button(root, text="시작", command=gameRun, font=('Helvetica', 14))
start_button.pack(pady=20)

word_label = tk.Label(root, text="", font=('Helvetica', 14))  # 게임 시작 전에는 숨김
entry = tk.Entry(root, font=('Helvetica', 14))  # 게임 시작 전에는 숨김
entry.bind("<Return>", checkInput)



# GUI 루프 시작
root.mainloop()