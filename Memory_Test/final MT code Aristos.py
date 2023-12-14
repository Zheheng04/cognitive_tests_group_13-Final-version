import sys
import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import messagebox
from tkinter.font import Font
from tkinter import ttk
import time
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from datetime import datetime
from openpyxl import load_workbook
from PIL import ImageTk, Image

from tkinter import simpledialog

def send_to_google_form(data_dict, form_url):
    ''' Helper function to upload information to a corresponding google form
        You are not expected to follow the code within this function!
    '''
    form_id = form_url[34:90]
    view_form_url = f'https://docs.google.com/forms/d/e/{form_id}/viewform'
    post_form_url = f'https://docs.google.com/forms/d/e/{form_id}/formResponse'

    page = requests.get(view_form_url)
    content = BeautifulSoup(page.content, "html.parser").find('script', type='text/javascript')
    content = content.text[27:-1]
    result = json.loads(content)[1][1]
    form_dict = {}

    loaded_all = True
    for item in result:
        if item[1] not in data_dict:
            print(f"Form item {item[1]} not found. Data not uploaded.")
            loaded_all = False
            return False
        form_dict[f'entry.{item[4][0][0]}'] = data_dict[item[1]]

    post_result = requests.post(post_form_url, data=form_dict)
    return post_result.ok

class MemoryTest(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Memory Test")

        self.font = Font(size=30)

        self.font1 = Font(size=25)

        self.layout = tk.Frame(self)
        self.layout.pack()

        # Welcome message
        welcome_label = tk.Label(self.layout, text="===Welcome to the Memory Test===")
        welcome_label.config(font=self.font)
        welcome_label.pack()

        # User ID input
        id_instructions_label = tk.Label(self.layout, text="=== Enter Your Anonymised ID ===\n\nTo generate an anonymous 4-letter unique user identifier please enter:\n- two letters based on the initials (first and last name) of a childhood friend\n- two letters based on the initials (first and last name) of a favourite actor / actress\n\nE.g. if your friend was called Charlie Brown and film star was Tom Cruise then your unique identifer would be CBTC")
        id_instructions_label.pack()

        self.id_input = tk.Entry(self.layout)
        self.id_input.pack()

        self.id_button = tk.Button(self.layout, text="Submit", command=self.on_id_submit)
        self.id_button.pack()

        # Gender input
        gender_question_label = tk.Label(self.layout, text="Please enter your gender: Male or Female")
        gender_question_label.pack()
        self.gender_input = tk.Entry(self.layout)
        self.gender_input.pack()

        self.gender_button = tk.Button(self.layout, text="Submit", command=self.on_gender_submit)
        self.gender_button.pack()

        # Start test button
        self.start_test_button = tk.Button(self.layout, text="Start Test", command=self.start_test)
        self.start_test_button.config(state="normal")
        self.start_test_button.pack()

        # Test result labels
        self.test_result_labels = []
        for i in range(3):
            label = tk.Label(self.layout)
            label.pack()
            self.test_result_labels.append(label)

    def on_id_submit(self):
        user_id = self.id_input.get().strip()
        if len(user_id) != 4 or not user_id.isalpha():
            messagebox.showwarning("Invalid ID", "Please enter a valid 4-letter ID.")
        else:
            self.user_id = user_id
            self.id_input.config(state="disabled")
            self.id_button.config(state="disabled")
            self.gender_input.config(state="normal")
            self.gender_button.config(state="normal")

    def on_gender_submit(self):
        gender = self.gender_input.get().strip()
        if gender != "Male" and gender != "Female":
            messagebox.showwarning("Invalid Gender", "Please enter either Male or Female.")
        else:
            self.gender = gender
            self.gender_input.config(state="disabled")
            self.gender_button.config(state="disabled")
            self.start_test_button.config(state="normal")
            self.show_message(f"Hello, {self.user_id}! Let's get started with the test.")

    def conduct_test(self, test_image, questions_and_answers):
        # self.clear_layout()

        image = Image.open(test_image)
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(self.layout, image=photo)
        label.image = photo  # Keep a reference!
        label.pack()
        label.config(width=600, height=500)

        # self.repaint()
        # print(test_image)

        if test_image != "memory_test1.png":
            self.show_message("Levels Up!!!")
        else:
            self.show_message(" ")
        time.sleep(30)
        self.clear_layout()
        # self.layout.update()y
        self.show_message("Go!")
        # self.master.update()
        # self.layout.after(2000, self.layout.destroy)
        # self.layout.after(2000, self.show_message, "Go!")
        self.clear_layout()
        score = 0
        start_time = time.time()

        for question, correct_answer in questions_and_answers.items():
            self.show_message(question)
            user_answer = self.get_user_input()
            user_answer = user_answer.strip().lower()

            if user_answer == correct_answer.lower():
                self.show_message("Correct!")
                score += 1
            else:
                self.show_message(f"Incorrect. The correct answer is: {correct_answer}")

        duration = time.time() - start_time

        self.show_message(
            f"Your score for the test is: {score} out of {len(questions_and_answers)}. Time taken: {duration:.2f} seconds")
        # self.layout.after(2000, self.show_message, " ")
        time.sleep(2)
        return score, duration

    class MemoryTest(tk.Tk):
        def __init__(self):
            self.font1 = Font(size=20)  # Existing font for introductions
            self.question_font = Font(size=18)

        def display_sentence(self, sentence, delay):
            """ Display a sentence after a specified delay """

            def show():
                label = tk.Label(self.layout, text=sentence, font=self.font1)
                label.pack()

            self.after(delay, show)

    def start_test(self):
        self.clear_layout()
        label = tk.Label(self.layout,
                         text="There are three small tests in this section, getting harder each time.\nEach test consists of a grid of coloured shapes for 30 seconds.\n Memorize them and answer some questions as soon as possible.",
                         font=self.font1)
        label.pack()
        self.update()
        time.sleep(4)
        # self.after(2000)
        test_images = ["memory_test1.png", "memory_test2.png", "memory_test3.png"]
        self.questions = [
            {
                "What is the color of the circle?": 'yellow',
                "What shape was above the heart?": "square",
                "What shape was between the star and the moon?": "heart",
                "What shape was below the triangle?": "star"
            },
            {
                "What is the color of the moon?": 'red',
                "What is the shape in the top right corner?": 'sun',
                "How many shapes are yellow?": '4',
                "What is the color of the star?": 'green'
            },
            {
                "What is the color of the cloud?": 'yellow',
                "Which direction is the arrow pointing?": 'right',
                "What is the shape between the circle and the sun?": 'pentagon',
                "What is the shape in the bottom left corner?": 'sun'
            }
        ]

        self.test_scores = []
        self.test_durations = []

        self.clear_layout()

        for i in range(3):
            self.show_message(f"Test {i+1}")
            score, duration = self.conduct_test(test_images[i], self.questions[i])
            self.test_scores.append(score)
            self.test_durations.append(duration)
            self.clear_layout()

        self.show_results()

    def show_message(self, message):
        label = tk.Label(self.layout, text=message)
        label.pack()
        self.layout.update()
        # self.layout.after(2000)

    def clear_layout(self, total_percentage=None):
        for widget in self.layout.winfo_children():
            widget.destroy()
        self.layout.update()

    def show_results(self):
        self.clear_layout()
        total_questions = (len(self.questions[0]) + len(self.questions[1]) + len(self.questions[2]))
        total_percentage = sum(self.test_scores) / total_questions
        total_percentage_score = total_percentage * 100
        score_label_text: str = f'Your total score is: {total_percentage_score:.2f}%'
        score_label = tk.Label(self.layout, text=score_label_text, font=self.font1)
        score_label.pack()
        df = pd.read_excel('Memory test.xlsx')
        baseline_scores = df['Total_Percentage']

        plt.figure(figsize=(15, 10))
        plt.hist(baseline_scores, bins=20, alpha=0.7, label='Baseline Scores')
        plt.axvline(total_percentage_score, color='red', linestyle='dashed', linewidth=2,
                    label=f'Your Score: {total_percentage_score:.2f}%')

        plt.title('Your Performance vs Baseline')
        plt.xlabel('Scores (%)')
        plt.ylabel('Number of Participants')
        plt.legend()
        plt.grid(True)
        plt.show()

        data = list(df['Total_Percentage'])
        data.append(total_percentage_score)
        sorted_data = sorted(data, reverse=True)
        ranking = sorted_data.index(total_percentage_score) + 1
        label_text = f"{self.user_id}! Your score is ranked as {ranking}\nwe wish to record your response data.\nto an anonymised public data repository.\nYour data will be used for educational teaching purposes\npractising data analysis and visualisation.\nPlease type yes in the box below if you consent to the upload?"
        label = tk.Label(self.layout, text=label_text, font=self.font1)
        label.pack()


        user_answer = self.get_user_input()
        if user_answer == "yes":
            wb = load_workbook(filename='Memory test.xlsx')
            sheet = wb['第 1 张表单回复']
            new_data = [datetime.now().strftime("%m/%d/%Y %H:%M:%S"), self.user_id, self.user_id, self.gender,
                        self.test_scores[0] / len(self.questions[0]),
                        self.test_scores[1] / len(self.questions[1]),
                        self.test_scores[2] / len(self.questions[2]),
                        sum(self.test_scores) / (
                                len(self.questions[0]) + len(self.questions[1]) + len(self.questions[2]))]
            sheet.append(new_data)
            wb.save('Memory test.xlsx')
            self.show_message("Thanks - your data will be uploaded.")
            upload_button = ttk.Button(self.layout, text="Upload Results", command=self.upload_results)
            upload_button.pack()
        else:
            self.show_message("No problem we hope you enjoyed the test.")



    def get_user_input(self):
        root = self.layout.winfo_toplevel()

        user_input = tk.StringVar()

        def submit_user_input():
            user_input.set(entry.get())
            root.quit()

        entry = tk.Entry(self.layout, textvariable=user_input)
        entry.pack()
        entry.focus_set()

        submit_button = tk.Button(self.layout, text="Submit", command=submit_user_input)
        submit_button.pack()

        root.mainloop()

        return user_input.get()

    def upload_results(self):
        data_dict = {
            "User ID": self.user_id,
            "Gender": self.gender,
            "Section_1_Accuracy": self.test_scores[0]/len(self.questions[0]),
            "Section_1_Duration": self.test_durations[0],
            "Section_2_Accuracy": self.test_scores[1]/len(self.questions[1]),
            "Section_2_Duration": self.test_durations[1],
            "Section_3_Accuracy": self.test_scores[2]/len(self.questions[2]),
            "Section_3_Duration": self.test_durations[2],
            'Total_Percentage': sum(self.test_scores)/(len(self.questions[0]) + len(self.questions[1]) + len(self.questions[2])),
            'Total_Duration': self.test_scores[0]/len(self.questions[0]) + self.test_scores[1]/len(self.questions[1]) + self.test_scores[2]/len(self.questions[2])
        }

        form_url = "https://docs.google.com/forms/d/e/1FAIpQLSc6yhsfZx1bj-p5Bz9dmuA3QQr8VBpRstlGApfqwuRNbQu41g/formResponse"
        send_to_google_form(data_dict, form_url)
        self.show_message("Results uploaded successfully!")


if __name__ == "__main__":
    memory_test = MemoryTest()
    memory_test.mainloop()
if __name__ == "__main__":
    memory_test = MemoryTest()
    memory_test.mainloop()