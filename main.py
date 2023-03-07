import requests
from tkinter import *
import os
import html
import pandas as pd

my_dir = os.getcwdb()
photo = my_dir + bytes("\\background.png", encoding='windows-1255')
data = my_dir + bytes("\\data.csv", encoding='windows-1255')
data = data.decode()


class Quiz:
    def __init__(self):
        self.cur = ""
        self.ans = ""
        self.q_bank = {}
        self.s = 0
        self.n = 0
        self.to_show = ""
        self.df = pd.read_csv(data, index_col=0)
        self.hs = self.df.iloc[0, 0]
        self.new_set()
        self.new_q()

    def new_set(self):
        response = requests.get(
            'https://opentdb.com/api.php?amount=50&difficulty=easy&type=booleanhttps://opentdb.com/api'
            '.php?amount=50&difficulty=easy&type=boolean').json()
        self.q_bank = response['results']

    def new_q(self):
        self.cur = html.unescape(self.q_bank[0]['question'])
        self.ans = self.q_bank[0]['correct_answer']
        self.n += 1
        self.to_show = f'Q{self.n} {self.cur} \n(True/False)? \nYour current score is {self.s}\n'

    def score(self):
        self.s += 1


my_q = Quiz()
window = Tk()
window.title("MR RIDDLE")
window.config(padx=10, pady=10, bg='black', highlightthickness=0)


def t_answer():
    global my_q
    user_answer = 'True'
    if user_answer == my_q.ans:
        my_q.score()
        if my_q.s > my_q.hs:
            my_q.hs = my_q.s
            my_q.df.iloc[0, 0] = my_q.hs
            canvas0.itemconfig(sc_txt, text=f'HIGHEST SCORE: {my_q.hs}')
            my_q.df.to_csv('data.csv')
        my_q.new_set()
        canvas.itemconfig(tt, text=my_q.to_show)
        my_q.new_q()
        canvas.itemconfig(tt, text=my_q.to_show)
    else:
        my_q.to_show = f'GAME OVER YOUR FINAL SCORE IS {my_q.s}'
        canvas.itemconfig(tt, text=my_q.to_show)
        t_but.config(state="disabled")
        f_but.config(state="disabled")


def f_answer():
    global my_q
    user_answer = 'False'
    if user_answer == my_q.ans:
        my_q.score()
        if my_q.s > my_q.hs:
            my_q.hs = my_q.s
            my_q.df.iloc[0, 0] = my_q.hs
            canvas0.itemconfig(sc_txt, text=f'HIGHEST SCORE: {my_q.hs}')
            my_q.df.to_csv('data.csv')
        canvas0.itemconfig(sc_txt, text=my_q.hs)
        my_q.new_set()
        canvas.itemconfig(tt, text=my_q.to_show)
        my_q.new_q()
        canvas.itemconfig(tt, text=my_q.to_show)
    else:
        my_q.to_show = f'GAME OVER YOUR FINAL SCORE IS {my_q.s}'
        canvas.itemconfig(tt, text=my_q.to_show)
        t_but.config(state="disabled")
        f_but.config(state="disabled")


def reset():
    global my_q
    my_q = Quiz()
    canvas.itemconfig(tt, text=my_q.to_show)
    t_but.config(state="active")
    f_but.config(state="active")


canvas0 = Canvas(window, width=1200, height=20, bg='black', highlightthickness=0)
canvas0.grid(row=0, column=1)
sc_txt = canvas0.create_text(600, 10, text=f'HIGHEST SCORE: {my_q.hs}', font=("Helvetica", 18, "bold"), fill='white')
photo_frame = Frame(window, padx=5, pady=5, bg='black', highlightthickness=0)
photo_frame.grid(row=1, column=1)
canvas = Canvas(photo_frame, height=400, width=1200, bg='black', highlightthickness=0)
img = PhotoImage(file=photo)
canvas.create_image(800, 200, image=img)
tt = canvas.create_text(420, 100, text=my_q.to_show, font=("Helvetica", 12, "bold"), fill='white')
canvas.grid(row=0, column=1)

buttons_frame = Frame(window, padx=5, pady=5, bg='black', highlightthickness=0)
buttons_frame.grid(row=2, column=1)
t_but = Button(buttons_frame, bg='green', text='TRUE', command=t_answer, padx=30, pady=20, font=("Helvetica", 12, "bold"))
t_but.grid(row=0, column=0, padx=30)
f_but = Button(buttons_frame, bg='Red', text='FALSE', command=f_answer, padx=30, pady=20, font=("Helvetica", 12, "bold"))
f_but.grid(row=0, column=1, padx=30)
r_but = Button(buttons_frame, bg='Blue', text='RESET', command=reset, padx=30, pady=20, font=("Helvetica", 12, "bold"))
r_but.grid(row=0, column=2, padx=30)

window.mainloop()


