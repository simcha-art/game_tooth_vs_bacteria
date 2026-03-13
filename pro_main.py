from bacterias import *
from tooth import *
player = Tooth()
bacteria = [Bacteria(random.randint(300,4000),420) for b in range(10)]
bullets = []
candies = []
score = 0
spawn_timer = 0
game_state = "playing"
