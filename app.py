from flask import Flask, render_template, jsonify, request
import random
import uuid

app = Flask(__name__)


class Tooth:
    def __init__(self):
        self.hp = 100
        self.score = 0
        self.damage = 10

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0


class Entity:
    def __init__(self, x, y):
        self.id = str(uuid.uuid4())
        self.x = x
        self.y = y


class Bacteria(Entity):
    def __init__(self, y_pos, hp, speed, reward, size):
        # האויבים מתחילים עכשיו מצד שמאל של המסך (x=0)
        super().__init__(x=0, y=y_pos)
        self.hp = hp
        self.speed = speed
        self.reward = reward
        self.size = size

    def move(self):
        # האויבים נעים ימינה, אז מוסיפים ל-x
        self.x += self.speed


class SugarGerm(Bacteria):
    def __init__(self, y_pos):
        # מהירות רנדומלית בין 5 ל-12
        super().__init__(y_pos, hp=10, speed=random.randint(5, 12), reward=10, size=30)


class PlaqueBoss(Bacteria):
    def __init__(self, y_pos):
        # מהירות רנדומלית בין 2 ל-5
        super().__init__(y_pos, hp=50, speed=random.randint(2, 5), reward=50, size=60)


class Projectile(Entity):
    def __init__(self, x, y, damage):
        super().__init__(x, y)
        self.speed = 15
        self.damage = damage
        self.size = 20

    def move(self):
        # המשחה נורית שמאלה, אז מחסירים מה-x
        self.x -= self.speed


class GameEngine:
    def __init__(self):
        self.tooth = Tooth()
        self.enemies = []
        self.projectiles = []
        self.game_over = False

    def spawn_enemy(self):
        if self.game_over: return
        y_pos = random.randint(50, 350)
        if random.random() > 0.8:
            self.enemies.append(PlaqueBoss(y_pos))
        else:
            self.enemies.append(SugarGerm(y_pos))

    def shoot(self, target_y):
        if self.game_over: return
        # הירייה יוצאת מהמיקום של השן בצד ימין (x=700)
        self.projectiles.append(Projectile(700, target_y, self.tooth.damage))

    def update_state(self):
        if self.game_over: return

        # תנועת אויבים ופגיעה בשן
        for enemy in self.enemies[:]:
            enemy.move()
            # האויב פוגע בשן כשהוא מגיע ל-x=700 בצד ימין
            if enemy.x >= 700:
                self.tooth.take_damage(10)
                self.enemies.remove(enemy)
                if self.tooth.hp <= 0:
                    self.game_over = True

        # תנועת קליעים ובדיקת פגיעות
        for p in self.projectiles[:]:
            p.move()
            hit = False
            for enemy in self.enemies[:]:
                # חישוב התנגשות
                if abs(p.y - enemy.y) < enemy.size and abs(p.x - enemy.x) < enemy.size:
                    enemy.hp -= p.damage
                    if enemy.hp <= 0:
                        self.tooth.score += enemy.reward
                        self.enemies.remove(enemy)
                    hit = True
                    break

            # מסירים את הקליע אם הוא פגע במשהו או יצא מהמסך מצד שמאל (x < 0)
            if hit or p.x < 0:
                self.projectiles.remove(p)


game = GameEngine()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_state', methods=['GET'])
def get_state():
    game.update_state()
    return jsonify({
        "hp": game.tooth.hp,
        "score": game.tooth.score,
        "enemies": [{"id": e.id, "x": e.x, "y": e.y, "hp": e.hp, "size": e.size} for e in game.enemies],
        "projectiles": [{"id": p.id, "x": p.x, "y": p.y, "size": p.size} for p in game.projectiles],
        "game_over": game.game_over
    })


@app.route('/spawn', methods=['POST'])
def spawn():
    game.spawn_enemy()
    return jsonify({"status": "ok"})


@app.route('/shoot', methods=['POST'])
def shoot():
    data = request.json
    game.shoot(data.get('y', 0))
    return jsonify({"status": "shot_fired"})


@app.route('/reset', methods=['POST'])
def reset():
    global game
    game = GameEngine()
    return jsonify({"status": "reset"})


if __name__ == '__main__':
    app.run(debug=True)