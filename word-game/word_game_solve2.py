import random
import time
import pyglet

word_file_path = '/Users/leehojin/Documents/Future_Lab/word_game_problem/data/word.txt'
good_sound_path = '/Users/leehojin/Documents/Future_Lab/word_game_problem/assets/good.wav'
bad_sound_path = '/Users/leehojin/Documents/Future_Lab/word_game_problem/assets/bad.mp3'

# Function to load words from the word.txt file
def wordLoad():
    words = []
    try:
        with open(word_file_path, 'r') as file:
            for line in file:
                word = line.strip()
                if word:
                    words.append(word)
    except FileNotFoundError:
        print(f"Error: The file {word_file_path} was not found.")
    return words

# Function to play sound
def playSound(file_path):
    try:
        sound = pyglet.media.load(file_path, streaming=False)
        sound.play()
        # Sleep briefly to allow the sound to play
        time.sleep(sound.duration)
    except Exception as e:
        print(f"Error playing sound: {e}")

# Function to run the word game
def gameRun(words):
    if not words:
        print("No words to play with. Exiting the game.")
        return

    total_rounds = 5
    correct_count = 0
    start_time = time.time()
    
    for _ in range(total_rounds):
        target_word = random.choice(words)
        print(f"Type the word: {target_word}")
        user_input = input("Your input: ").strip()
        
        if user_input == target_word:
            print("Correct!")
            playSound(good_sound_path)
            correct_count += 1
        else:
            print(f"Incorrect! The correct word was: {target_word}")
            playSound(bad_sound_path)
    
    end_time = time.time()
    total_time = end_time - start_time
    result = "Passed" if correct_count >= 3 else "Failed"
    
    print(f"Game over! You got {correct_count} out of {total_rounds} correct.")
    print(f"Total time taken: {total_time:.2f} seconds.")
    print(f"Result: {result}")

if __name__ == "__main__":
    words = wordLoad()
    gameRun(words)