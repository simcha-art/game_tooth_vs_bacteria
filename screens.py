from bacterias import *

# ---------------- RESET LEVEL ----------------
def reset_level(player, bacteria, bullets, candies):
    player.hp = 100
    player.rect.topleft = (100, 400)
    bullets.clear()
    candies.clear()
    bacteria[:] = [Bacteria(random.randint(300,4000),460) for b in range(10)]
