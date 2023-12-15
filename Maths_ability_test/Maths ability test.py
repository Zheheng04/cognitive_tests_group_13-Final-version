from IPython.display import display, Image, clear_output, HTML
import time
import random
import requests
from bs4 import BeautifulSoup
import json
import tkinter as tk
from tkinter import messagebox
import pandas as pd
import numpy as np
random.seed(1)

def generate_a_question(difficulty):
    num_1 = random.randint(1, 10)
    num_2 = random.randint(10, 20)
    num_3 = random.randint(10, 25)
    num_4 = random.randint(1, 10)
    operator_1 = random.choice(["+", "-"])
    operator_2 = "*"

    if difficulty == 1:
        question1 = f"{num_1}{operator_1}{num_2}"
        print(question1)
        start_time = time.time()
        answer = float(input("Your answer is"))
        result = eval(question1)
        while answer != result:
            answer = float(input("Your answer is"))

        end_time = time.time()
        time_taken = end_time - start_time

    if difficulty == 2:
        question2 = f"{num_1}{operator_1}{num_2}{operator_2}{num_4}"
        print(question2)
        start_time = time.time()
        answer = float(input("Your answer is"))
        result = eval(question2)
        while answer != result:
            answer = float(input("Your answer is"))

        end_time = time.time()
        time_taken = end_time - start_time

    if difficulty == 3:
        question3 = f"{num_1}{operator_1}{num_2}{operator_2}{num_3}"
        print(question3)
        start_time = time.time()
        answer = float(input("Your answer is"))
        result = eval(question3)
        while answer != result:
            answer = float(input("Your answer is"))

        end_time = time.time()
        time_taken = end_time - start_time
    return time_taken

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

# Main codes
## Creating GUI using tkinter
class MathsAbilityTest(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Maths Ability Test")
        self.geometry("400x300")
        self.information_collection()
    def information_collection(self):
        # Welcome message display
        self.welcome_message = tk.Label(self, text="Welcome to the Maths Ability Test!")
        self.welcome_message.pack()
        # Collect name
        self.name_label = tk.Label(self, text="Please enter your name")
        self.name_label.pack()
        self.name_entry = tk.Entry(self)
        self.name_entry.pack()
        # ID instructions adn collect anonymous ID
        self.instructions_label = tk.Label(self, text="""
        Enter your anonymised ID
        To generate an anonymous 4-letter unique user identifier please enter:
        - two letters based on the initials (first and last name) of a childhood friend
        - two letters based on the initials (first and last name) of a favourite actor / actress
        e.g. if your friend was called Charlie Brown and film star was Tom Cruise
        then your unique identifer would be CBTC""")
        self.instructions_label.pack()
        self.ID_entry = tk.Entry(self)
        self.ID_entry.pack()
        # Gender collection
        self.gender_label = tk.Label(self, text="Please enter your gender: M or F")
        self.gender_label.pack()
        self.gender_entry = tk.Entry(self)
        self.gender_entry.pack()
        # Test start
        self.test_start_button = tk.Button(self, text="Click to start the test", command=self.start_test)
        self.test_start_button.pack()
        self.test_starts_label = tk.Label(self, text="Please answer the question below (Not in GUI)")
        self.test_starts_label.pack()


    def start_test(self):
        name = self.name_entry.get()
        user_ID = self.ID_entry.get()
        gender = self.gender_entry.get()
        messagebox.showinfo("Test starts now", f"Your name is {name} and your ID is {user_ID}")
        # Section 1
        total_time = 0
        score = 0
        while total_time <= 60:
            time_taken = generate_a_question(1)
            total_time += time_taken
            score = score + 1
            clear_output()

        section1_score = score
        print(f"The total time taken for Section 1 is {total_time}s")
        print(f"The score for Section 1 is {section1_score}")
        time.sleep(2)
        print("Level up!!!")
        time.sleep(2)

        # Section 2
        while 60 < total_time <= 120:
            time_taken = generate_a_question(2)
            total_time += time_taken
            score = score + 2
            clear_output()

        section2_score = score - section1_score
        print(f"The total time taken for Section 2 is {total_time}s")
        print(f"The score for Section 2 is {section2_score}")
        print(f"The total score is {score}")
        time.sleep(2)
        print("Level up!!!")
        time.sleep(2)

        # Section 3
        while 120 < total_time <= 180:
            time_taken = generate_a_question(3)
            total_time += time_taken
            score = score + 3
            clear_output()

        section3_score = score - section2_score - section1_score
        print(f"The total time taken for the test is {total_time}s")
        print(f"The score for Section 1 is {section1_score}")
        print(f"The score for Section 2 is {section2_score}")
        print(f"The score for Section 3 is {section3_score}")
        print(f"Final score for the maths ability test is {score}")
        print("End of test!")

        print("Please read:")
        print("")
        print("we wish to record your response data")
        print("to an anonymised public data repository. ")
        print("Your data will be used for educational teaching purposes")
        print("practising data analysis and visualisation.")
        print("")
        print("Please type   yes   in the box below if you consent to the upload.")
        result = input("> ")
        if result == "yes":
            print("Thanks - your data will be uploaded.")
            data_dict = {
                'Name': name,
                'Gender': gender,
                'Anonymised ID': user_ID,
                'Section1_score': section1_score,
                'Section2_score': section2_score,
                'Section3_score': section3_score,
                'Total_score': score,
        }
            form_url = 'https://docs.google.com/forms/d/e/1FAIpQLSdExGNp9YhkhuOQhPhl4KiUmUAsxGqXh2J49Q3DpQ3kSCMm_g/viewform?usp=sf_link'
            send_to_google_form(data_dict, form_url)
        else:
            print("No problem we hope you enjoyed the test.") \
        # Show ranking
        maths_df = pd.read_csv('Maths ability test results.csv')
        data = list(maths_df['Total_score'].values)
        data.append(score)
        sorted_data = sorted(data, reverse=True)
        ranking = sorted_data.index(score) + 1
        print(f"Your ranking among all participants ({len(maths_df)}) is {ranking}")
run = MathsAbilityTest()
run.mainloop()