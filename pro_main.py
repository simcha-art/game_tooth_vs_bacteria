from bacterias import *
from obstacles import *
from tooth import *
player = Tooth()
bacteria = [RegularBacteria(random.randint(300,4000),420) for b in range(10)]
bullets = []
candies = []
cola_pits = [Cola_pit(955,500),Cola_pit(1970,500),Cola_pit(2970,500)]
platforms = [Platform(400,200)]
score = 0
spawn_timer = 0
game_state = "playing"
