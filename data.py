import json
# ---------------- SCORE SAVE ----------------
def save_score(score):
    try:
        with open("scores.json", "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(score)
    data = sorted(data, reverse=True)[:5]

    with open("scores.json", "w") as f:
        json.dump(data, f)
