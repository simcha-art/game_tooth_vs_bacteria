from bacterias import *
from game_tooth_vs_bacteria.obstacles import Cola_pit, Platform
from tooth import *
player = Tooth()
bacteria = [Bacteria(random.randint(300,4000),420) for b in range(10)]
cola_pits = [Cola_pit(955,500),Cola_pit(1970,500),Cola_pit(2970,500)]
bullets = []
candies = []
platforms = [Platform(500,180)]
score = 0
spawn_timer = 0
game_state = "playing"
