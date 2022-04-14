from snake_game import snake_game
import time

game = snake_game()
while True:
    game.game_draw()
    game.game_step_user()
        
    time.sleep(0.1)
