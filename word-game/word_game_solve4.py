import random
import time
import tkinter as tk
from tkinter import messagebox
import pyglet

word_file_path = '/Users/leehojin/Documents/Future_Lab/word_game_problem/data/word.txt'
good_sound_path = '/Users/leehojin/Documents/Future_Lab/word_game_problem/assets/good.wav'
bad_sound_path = '/Users/leehojin/Documents/Future_Lab/word_game_problem/assets/bad.mp3'

class WordGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Word Game")
        self.root.geometry("400x300")

        self.label = tk.Label(root, text="난이도를 선택해주세요:", font=("Arial", 14))
        self.label.pack(pady=10)

        self.difficulty_var = tk.StringVar(value="상")
        self.difficulty_buttons_frame = tk.Frame(root)
        self.difficulty_buttons_frame.pack()
        self.create_difficulty_buttons()

        self.start_button = tk.Button(root, text="게임 시작", command=self.start_game, font=("Arial", 14))
        self.start_button.pack(pady=10)

        self.word_label = tk.Label(root, text="", font=("Arial", 14))
        self.word_label.pack()

        self.entry = tk.Entry(root, font=("Arial", 14))
        self.entry.bind("<Return>", self.check_word)
        self.entry.pack_forget()  # 초기에는 입력 칸을 숨깁니다.

        self.result_label = tk.Label(root, text="", font=("Arial", 14))
        self.result_label.pack(pady=10)

        self.time_label = tk.Label(root, text="", font=("Arial", 12))
        self.time_label.pack(pady=5)

        self.restart_button = tk.Button(root, text="게임 다시 시작", command=self.restart_game, font=("Arial", 14))
        self.restart_button.pack(pady=10)
        self.restart_button.pack_forget()  # 초기에는 숨겨진 상태

        self.start_time = 0
        self.target_word = ""
        self.total_rounds = 0
        self.current_round = 0
        self.time_limit = 0
        self.fastest_time = float('inf')
        self.fastest_word = ""
        self.words = []
        self.load_words()

    def create_difficulty_buttons(self):
        difficulties = [("상", "상"), ("중", "중"), ("하", "하")]
        for text, mode in difficulties:
            button = tk.Radiobutton(self.difficulty_buttons_frame, text=text, variable=self.difficulty_var, value=mode, font=("Arial", 14))
            button.pack(anchor=tk.W)

    def load_words(self):
        try:
            with open(word_file_path, 'r') as file:
                self.words = [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            messagebox.showerror("Error", f"The file {word_file_path} was not found.")
            self.words = []

    def play_sound(self, file_path):
        try:
            sound = pyglet.media.load(file_path, streaming=False)
            sound.play()
        except Exception as e:
            print(f"Error playing sound: {e}")

    def start_game(self):
        difficulty = self.difficulty_var.get()
        if difficulty == '상':
            self.total_rounds = 5
            self.time_limit = 2
        elif difficulty == '중':
            self.total_rounds = 5
            self.time_limit = 3
        elif difficulty == '하':
            self.total_rounds = 3
            self.time_limit = 4
        else:
            messagebox.showerror("Error", "올바른 난이도를 선택해주세요.")
            return
        
        self.label.config(text=f"난이도: {difficulty}, 단어 수: {self.total_rounds}, 제한 시간: {self.time_limit}초")
        self.start_button.pack_forget()
        self.entry.pack()
        self.current_round = 0
        self.fastest_time = float('inf')
        self.fastest_word = ""
        self.next_word()

    def check_word(self, event=None):
        elapsed_time = time.time() - self.start_time
        self.process_result(elapsed_time)
        self.current_round += 1
        if self.current_round < self.total_rounds:
            self.root.after(2000, self.next_word)
        else:
            self.end_game()

    def process_result(self, elapsed_time):
        user_input = self.entry.get().strip()
        if user_input == self.target_word and elapsed_time <= self.time_limit:
            self.result_label.config(text=f"Correct! ({elapsed_time:.2f} seconds)")
            self.play_sound(good_sound_path)
            if elapsed_time < self.fastest_time:
                self.fastest_time = elapsed_time
                self.fastest_word = self.target_word
        else:
            self.result_label.config(text=f"Incorrect! The correct word was: {self.target_word}")
            self.play_sound(bad_sound_path)
        self.entry.delete(0, tk.END)

    def next_word(self):
        if self.words:
            self.target_word = random.choice(self.words)
            self.word_label.config(text=self.target_word)
            self.start_time = time.time()
            self.result_label.config(text="")
            self.entry.pack()
            self.entry.focus_set()
            self.update_time()  # Reset the timer update loop
        else:
            self.word_label.config(text="No words available.")
            self.result_label.config(text="")
            self.time_label.config(text="")

    def update_time(self):
        if self.start_time:
            remaining_time = self.time_limit - (time.time() - self.start_time)
            if remaining_time > 0:
                self.time_label.config(text=f"Time left: {remaining_time:.2f} seconds")
                self.root.after(100, self.update_time)
            else:
                self.time_label.config(text="Time's up!")
                self.process_result(self.time_limit + 1)  # Force fail the word due to time out
                self.current_round += 1
                if self.current_round < self.total_rounds:
                    self.root.after(2000, self.next_word)
                else:
                    self.end_game()

    def end_game(self):
        self.word_label.config(text="")
        self.label.config(text="축하해!")
        self.result_label.config(text=f"가장 빠른 단어: {self.fastest_word} ({self.fastest_time:.2f} seconds)")
        self.time_label.config(text="")
        self.entry.pack_forget()  # 게임 종료 후 입력 칸 숨기기
        self.restart_button.pack()  # 게임 다시 시작 버튼 표시

    def restart_game(self):
        self.label.config(text="난이도를 선택해주세요:")
        self.entry.pack_forget()
        self.result_label.config(text="")
        self.time_label.config(text="")
        self.fastest_time = float('inf')
        self.fastest_word = ""
        self.current_round = 0
        self.restart_button.pack_forget()
        self.start_button.pack()
        for widget in self.difficulty_buttons_frame.winfo_children():
            widget.destroy()
        self.create_difficulty_buttons()

if __name__ == "__main__":
    root = tk.Tk()
    app = WordGameApp(root)
    root.mainloop()