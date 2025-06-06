from flask import Flask, render_template, request, redirect, url_for
import json
import os
import random
from datetime import datetime, timedelta
from urllib.parse import unquote

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")
SHIFTS_FILE = os.path.join(os.path.dirname(__file__), "shifts.json")

def add_suffix(day):
    if 10 <= day <= 20:
        return f"{day}th"
    suffixes = {1: "st", 2: "nd", 3: "rd"}
    return f"{day}{suffixes.get(day % 10, 'th')}"

def get_dates(date):
    days_list = []
    dates_list = []

    for i in range(-3, 4):
        adjusted_date = date + timedelta(days=i)
        days_list.append(adjusted_date.strftime('%a'))  
        dates_list.append(f"{adjusted_date.strftime('%b')} {add_suffix(adjusted_date.day)}")

    return days_list, dates_list

def load_workers(weekday):
    with open(SHIFTS_FILE, "r") as file:
        data = json.load(file)
    working_employees = [[],[],[]]
    departments = [[],[],[]]
    shift_conversion = {"06:00 - 14:00":0, "14:00 - 22:00":1,"22:00 - 06:00":2}
    for i in data["employees"]:
        if weekday in i["workdays"]:
            working_employees[shift_conversion.get(i["shift_time_range"])].append(i["name"])
            departments[shift_conversion.get(i["shift_time_range"])].append(i["role"])
    
    return departments, working_employees

def load_data():
    with open(DATA_FILE, "r") as file:
        data = json.load(file)
    threat_order = {"red": 1, "orange": 2, "green": 3} 
    data["tagged_individuals"].sort(key=lambda x: threat_order.get(x["threat_level"], 3))
    
    name_order = {person["name"]: i for i, person in enumerate(data["tagged_individuals"])}

    data["media_posts"].sort(key=lambda post: name_order.get(post["tagged_individual"], len(name_order)))

    return data

def update_data(new_entry):
    color_dict = {"low":"green","medium":"orange","high":"red"}
    new_entry["threat_level"] = color_dict[new_entry["threat_level"]]
    data = load_data()
    data["tagged_individuals"].append({
        "name": new_entry['tagged_individual'],
        "threat_level": new_entry['threat_level'],
        "message": new_entry['alert_message'],
        "notes": new_entry['additional_info']
    })
    data["media_posts"].append({
        "username": new_entry['alert_message'],
            "message": "No recent posts on this account",
            "tagged_individual": new_entry['tagged_individual'],
            "posted": ""
    })
    #data["news_alerts"].push({})

    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


@app.route('/', methods=["GET", "POST"])
def dashboard():
    data = load_data()
    name = random.choice(data["tagged_individuals"])["name"]
    index = next((i for i, p in enumerate(data["tagged_individuals"]) if p["name"] == name), None)

    return render_template("dashboard.html", individuals=data["tagged_individuals"], random_profile=data["tagged_individuals"][index], socials=data["media_posts"], rand_index=index)

@app.route('/upload', methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        new_entry = request.form.to_dict()
        update_data(new_entry)
        return redirect(url_for('dashboard'))  

    return render_template("upload.html")
@app.route('/profile', methods=["GET", "POST"])
def profile():
    data = load_data()
    name = request.args.get("name")
    
    index = next((i for i, p in enumerate(data["tagged_individuals"]) if p["name"] == name), None)
    return render_template("profile.html", profile=data["tagged_individuals"][index], username=data["media_posts"][index])
@app.route('/reports')
def reports():
    return render_template("reports.html")
@app.route('/workflows')
def workflows():
    intervals = [6,8,11,14,16,19,22]
    curr_time = datetime.now().hour
    row_num = max(((curr_time - 6) // 2.7) + 2,1)
    if curr_time in intervals:
        row_num += 1
    row_num = row_num if row_num <= 7 else 1
    return render_template('workflows.html', row=row_num)
@app.route('/shifts')
def shifts():
    #Need to get current date, list of selected dates, all shift workers based on shift, notes for each worker
    today = datetime.today()
    date = request.args.get("date")
    if date:
        decoded_date = unquote(date)
        month, day = decoded_date.split()
        day = ''.join(filter(str.isdigit, day)) 
        today = datetime.strptime(f"{month} {day} 2025", "%b %d %Y")
    days, dates = get_dates(today)
    weekday = today.strftime("%A")
    return render_template('shifts.html', datelist=dates, daylist=days, curr_date=datetime.today().strftime("%a %b %-d"), shiftlist=load_workers(weekday)[1], departmentlist=load_workers(weekday)[0])
if __name__ == '__main__':
    app.run(debug=True)
