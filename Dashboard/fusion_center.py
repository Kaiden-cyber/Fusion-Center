from flask import Flask, render_template, request, redirect, url_for
import json
import os
import random

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")

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
    """Find profile by name and return index."""
    name = request.args.get("name")
    
    index = next((i for i, p in enumerate(data["tagged_individuals"]) if p["name"] == name), None)
    return render_template("profile.html", profile=data["tagged_individuals"][index], username=data["media_posts"][index])


if __name__ == '__main__':
    app.run(debug=True)
