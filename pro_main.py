from bacterias import *
from tooth import *
player = Tooth()
bacteria = [ShooterBacteria(random.randint(300,4000),460) for b in range(10)]
bullets = []
candies = []
score = 0
spawn_timer = 0
game_state = "playing"
