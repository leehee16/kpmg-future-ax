import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import random
import time
import pyglet
import pymysql
from pymysql import MySQLError
from datetime import datetime

# 데이터베이스 연결 설정
def create_connection():
    try:
        connection = pymysql.connect(
            host='localhost',
            user='leehee',
            password='1112',
            database='games_db',
            cursorclass=pymysql.cursors.DictCursor
        )
        print("MySQL 데이터베이스에 성공적으로 연결되었습니다.")
        return connection
    except MySQLError as e:
        print(f"오류: {e}")
        return None

# 게임 기록을 저장하는 함수
def save_record(connection, correct_count, elapsed_time):
    try:
        with connection.cursor() as cursor:
            insert_query = """
            INSERT INTO wordgame (corr_cnt, exe_time, reg_date)
            VALUES (%s, %s, %s);
            """
            registered_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(insert_query, (correct_count, round(elapsed_time, 1), registered_at))
            connection.commit()
            print(f"기록이 저장되었습니다: {correct_count}, {round(elapsed_time, 1)}, {registered_at}")
            update_ranks(connection)
            return cursor.lastrowid
    except MySQLError as e:
        print(f"데이터 삽입 오류: {e}")
        return None

# 게임 기록을 불러와 순위를 계산하고 업데이트하는 함수
def update_ranks(connection):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, corr_cnt, exe_time FROM wordgame ORDER BY corr_cnt DESC, exe_time ASC")
            records = cursor.fetchall()

            for rank, record in enumerate(records, start=1):
                id = record['id']
                update_query = "UPDATE wordgame SET irank = %s WHERE id = %s"
                cursor.execute(update_query, (rank, id))

            connection.commit()
            print("순위가 성공적으로 업데이트되었습니다.")
    except MySQLError as e:
        print(f"순위 업데이트 오류: {e}")

# 게임 기록을 불러와 순위를 계산하고 출력하는 함수
def fetch_and_display_ranks(connection):
    try:
        with connection.cursor() as cursor:
            select_query = """
            SELECT * FROM wordgame
            ORDER BY irank ASC;
            """
            cursor.execute(select_query)
            records = cursor.fetchall()

            if records:
                rank_window = tk.Toplevel(root)
                rank_window.title("역대 순위")
                rank_window.geometry("800x400")

                tree = ttk.Treeview(rank_window, columns=('id', '맞춘개수', '걸린시간', '등록날짜', '등수'), show='headings')
                tree.heading('id', text='ID')
                tree.heading('맞춘개수', text='맞춘개수')
                tree.heading('걸린시간', text='걸린시간')
                tree.heading('등록날짜', text='등록날짜')
                tree.heading('등수', text='등수')

                tree.column('id', width=50, anchor='center')
                tree.column('맞춘개수', width=100, anchor='center')
                tree.column('걸린시간', width=100, anchor='center')
                tree.column('등록날짜', width=150, anchor='center')
                tree.column('등수', width=50, anchor='center')

                for record in records:
                    id, correct_count, elapsed_time, registered_at, irank = record['id'], record['corr_cnt'], float(record['exe_time']), record['reg_date'], record['irank']
                    formatted_elapsed_time = round(elapsed_time, 1)
                    formatted_date = datetime.strptime(registered_at, '%Y-%m-%d %H:%M:%S').strftime('%y%m%d %H:%M')
                    tree.insert('', 'end', values=(id, correct_count, formatted_elapsed_time, formatted_date, irank))

                tree.pack(expand=True, fill='both')
            else:
                messagebox.showinfo("역대 순위", "기록된 데이터가 없습니다.")
    except MySQLError as e:
        print(f"데이터 가져오기 오류: {e}")
        messagebox.showinfo("역대 순위", f"데이터 가져오기 오류 발생: {e}")

# 플레이어의 순위를 가져오는 함수
def get_player_rank(connection, player_id):
    try:
        with connection.cursor() as cursor:
            query = "SELECT irank FROM wordgame WHERE id = %s"
            cursor.execute(query, (player_id,))
            result = cursor.fetchone()
            return result['irank'] if result else None
    except MySQLError as e:
        print(f"순위 가져오기 오류: {e}")
        return None

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
        player_id = save_record(connection, correct_count, elapsed_time)
        player_rank = get_player_rank(connection, player_id)
        rank_message = f"등수: {player_rank}"
        result_message = f"게임 종료! 총 {total_rounds}개 중 {correct_count}개 맞췄습니다.\n"
        result_message += "합격입니다!" if correct_count >= 3 else "불합격입니다!"
        result_message += f"\n총 소요 시간: {round(elapsed_time, 1)}초\n{rank_message}"
        messagebox.showinfo("결과", result_message)
        fetch_and_display_ranks(connection)

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

# 메인 윈도우 초기화
root = tk.Tk()
root.title("워드게임")
root.geometry("800x700")  # 창 크기를 800x600으로 설정

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

# 데이터베이스 연결 설정
connection = create_connection()

# GUI 루프 시작
root.mainloop()