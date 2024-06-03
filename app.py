from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import time
import random

app = Flask(__name__)
DATABASE = 'typing_speed_test.db'

# List of sample paragraphs
sample_paragraphs = [
    "To be, or not to be, that is the question: Whether 'tis nobler in the mind to suffer The slings and arrows of outrageous fortune, Or to take arms against a sea of troubles And by opposing end them. To die: to sleep; No more; and by a sleep to say we end The heart-ache and the thousand natural shocks That flesh is heir to, 'tis a consummation Devoutly to be wish'd.",
    "The quick brown fox jumps over the lazy dog. This sentence is often used in typing tests because it contains every letter of the English alphabet at least once. It's a classic phrase that has been used for generations to assess typing speed and accuracy. The quick brown fox is a common character in literature and folklore, symbolizing agility and cleverness. The lazy dog, on the other hand, represents the opposite—sluggishness and inactivity.",
    "In the beginning God created the heavens and the earth. Now the earth was formless and empty, darkness was over the surface of the deep, and the Spirit of God was hovering over the waters. And God said, 'Let there be light,' and there was light. God saw that the light was good, and he separated the light from the darkness. God called the light 'day,' and the darkness he called 'night.' And there was evening, and there was morning—the first day.",
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
    "To exist, or not to exist, therein lies the quandary: Is it nobler to confront the slings and arrows of outrageous fortune, or to embark upon a crusade against a deluge of tribulations and, by opposing, bring about their cessation? To cease to exist; to slumber; No more; and through sleep, to declare an end to the anguish and the myriad natural calamities that flesh is heir to, it is an aspiration devoutly to be wished. To cease to exist, to slumber; To slumber: perchance to dream: ah, therein lies the conundrum."
]

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    paragraph = random.choice(sample_paragraphs)
    return render_template('index.html', paragraph=paragraph)

@app.route('/result', methods=['POST'])
def result():
    try:
        typed_text = request.form['text']
        original_text = request.form['original_text']
        start_time = float(request.form['start_time'])
        end_time = time.time()
        time_taken = end_time - start_time
        words = typed_text.split()
        word_count = len(words)
        wpm = (word_count / time_taken) * 60

        # Calculate accuracy
        correct_chars = sum(1 for a, b in zip(typed_text, original_text) if a == b)
        accuracy = (correct_chars / len(original_text)) * 100

        wpm = round(wpm, 2)
        time_taken = round(time_taken, 2)
        accuracy = round(accuracy, 2)

        print(f"Typed Text: {typed_text}")
        print(f"Original Text: {original_text}")
        print(f"Start Time: {start_time}")
        print(f"End Time: {end_time}")
        print(f"Time Taken: {time_taken}")
        print(f"Words: {words}")
        print(f"WPM: {wpm}")
        print(f"Accuracy: {accuracy}")

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO results (text, time_taken, wpm, accuracy) VALUES (?, ?, ?, ?)', (typed_text, time_taken, wpm, accuracy))
        conn.commit()
        conn.close()

        return render_template('result.html', wpm=wpm, time_taken=time_taken, accuracy=accuracy)
    except Exception as e:
        print(f"Error: {e}")
        return "Internal Server Error", 500

