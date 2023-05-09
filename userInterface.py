import tkinter as tk
from runModel import run_score_model, run_win_model
from confTeams import get_teams
import warnings

warnings.filterwarnings('ignore')

new_team1_name = None
new_team2_name = None


def win_model():
    if neutral.get():
        place = 2
    else:
        place = 0
    win_prob = run_win_model(conf.get(), team1_name.get(), team2_name.get(), place)
    if win_prob > 50:
        score_var.set(team1_name.get() + "\nwin probability:\n\n" + str(round(win_prob, 2)) + "%")
    else:
        score_var.set(team2_name.get() + "\nwin probability:\n\n" + str(round(100 - win_prob, 2)) + "%")


def score_model():
    if neutral.get():
        place = 2
    else:
        place = 0
    score_str = str(run_score_model(conf.get(), team1_name.get(), team2_name.get(), place)).strip('[]')
    score_str = score_str.strip(' ').split(' ')
    print(score_str)
    team1_str = score_str[0]
    team1_score.set(team1_str[:5])
    team2_str = score_str[-1]
    team2_score.set(team2_str[:5])


def conf_select(*args):
    global new_team1_name, new_team2_name
    score_var.set("")
    team1_score.set("")
    team2_score.set("")
    selected_conf = conf.get()
    new_teams = get_teams(selected_conf)

    new_team1_name = tk.StringVar()
    new_team1_name.set(new_teams[0])
    team1_name.set(new_team1_name.get())

    new_team1_drop = tk.OptionMenu(window, new_team1_name, *new_teams, command=team_select)
    new_team1_drop.config(width=20, font=15)
    new_team1_drop.grid(row=2, column=0, sticky="e")

    new_team2_name = tk.StringVar()
    new_team2_name.set(new_teams[1])
    team2_name.set(new_team2_name.get())

    new_team2_drop = tk.OptionMenu(window, new_team2_name, *new_teams, command=team_select)
    new_team2_drop.config(width=20, font=15)
    new_team2_drop.grid(row=2, column=2, sticky="w")


def team_select(*args):
    global new_team1_name, new_team2_name
    score_var.set("")
    team1_score.set("")
    team2_score.set("")
    try:
        team1_name.set(new_team1_name.get())
        team2_name.set(new_team2_name.get())
    except AttributeError:
        pass


window = tk.Tk()

window.rowconfigure([0, 1, 2, 3, 4, 5, 6], weight=1)
window.columnconfigure([0, 1, 2], weight=1)

label = tk.Label(window, text="College Basketball Predictor", font=50)
label.grid(row=0, column=1)

conferences = ["ACC", "Big10", "Big12", "BigEast", "PAC12", "SEC"]
conf = tk.StringVar()
conf.set(conferences[0])

conf_drop = tk.OptionMenu(window, conf, *conferences, command=conf_select)
conf_drop.config(width=20, font=15)
conf_drop.grid(row=1, column=1)

teams = get_teams(conf.get())
team1_name = tk.StringVar()
team1_name.set(teams[0])

team1_drop = tk.OptionMenu(window, team1_name, *teams, command=team_select)
team1_drop.config(width=20, font=15)
team1_drop.grid(row=2, column=0, sticky="e")

team2_name = tk.StringVar()
team2_name.set(teams[1])

team2_drop = tk.OptionMenu(window, team2_name, *teams, command=team_select)
team2_drop.config(width=20, font=15)
team2_drop.grid(row=2, column=2, sticky="w")

neutral = tk.BooleanVar()
checkbox = tk.Checkbutton(window, text="Neutral Site", variable=neutral, font=10, height=5, command=team_select)
checkbox.grid(row=2, column=1)

team1_score = tk.StringVar()
team1 = tk.Label(window, textvariable=team1_score, text="", font=15)
team1.grid(row=3, column=0, sticky="e")

score_var = tk.StringVar()
score = tk.Label(window, textvariable=score_var, text="", font=15)
score.grid(row=3, column=1)

team2_score = tk.StringVar()
team2 = tk.Label(window, textvariable=team2_score, text="", font=15)
team2.grid(row=3, column=2, sticky="w")

btn_score = tk.Button(master=window, text="Score", width=20, command=score_model, bd=6, font=15)
btn_score.grid(row=4, column=0, sticky="e")

btn_win = tk.Button(master=window, text="Win Probability", width=20, command=win_model, bd=6, font=15)
btn_win.grid(row=4, column=2, sticky="w")

width = window.winfo_screenwidth()
height = window.winfo_screenheight()

window.geometry("%dx%d" % (width, height))

window.mainloop()
