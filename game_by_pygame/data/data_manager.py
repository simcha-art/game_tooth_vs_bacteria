import json
import csv
import os


class DataManager:
    def __init__(self):
        self.data_dir = 'data'
        self.settings_file = os.path.join(self.data_dir, 'settings.json')
        self.leaderboard_file = os.path.join(self.data_dir, 'leaderboard.csv')

        # מוודא שתיקיית data קיימת
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        # יצירת קובץ ה-CSV עם כותרות אם הוא לא קיים
        if not os.path.exists(self.leaderboard_file):
            with open(self.leaderboard_file, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Name', 'Score'])  # כותרות העמודות

        # יצירת קובץ JSON התחלתי אם הוא לא קיים
        if not os.path.exists(self.settings_file):
            self.save_settings({"volume": 1.0, "difficulty": "normal"})

    # --- פונקציות JSON ---
    def save_settings(self, data):
        """מקבל מילון (dictionary) ושומר אותו לקובץ JSON"""
        with open(self.settings_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def load_settings(self):
        """קורא את קובץ ה-JSON ומחזיר מילון"""
        with open(self.settings_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    # --- פונקציות CSV ---
    def add_score(self, name, score):
        """מוסיף שורה חדשה של שחקן וניקוד לסוף קובץ ה-CSV"""
        with open(self.leaderboard_file, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([name, score])

    def get_top_scores(self, limit=5):
        """קורא את ה-CSV, ממיין לפי הניקוד הגבוה ביותר ומחזיר רשימה"""
        scores = []
        with open(self.leaderboard_file, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # מדלג על שורת הכותרת (Name, Score)
            for row in reader:
                if len(row) == 2:
                    scores.append({"name": row[0], "score": int(row[1])})

        # מיון הרשימה מהגבוה לנמוך
        scores.sort(key=lambda x: x['score'], reverse=True)
        return scores[:limit]  # מחזיר רק את ה-N הראשונים