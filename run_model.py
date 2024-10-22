from AI_agent import ai_agent
from snake_game import snake_game
import torch
import time


agent = ai_agent()
agent.model.load_state_dict(torch.load("QNet_model_best.pth"))
game = snake_game(width=200,height=200,section_size=50)

while True:
    
    state = game.inputs_AI()
    final_move = agent.get_play_action(state)
    game.game_draw()
    _ , done, _, _ = game.game_step_ai(final_move)
    if done:  
        print(f"Max Foods:{len(game.snake.body_sections)}")
        game.reset()
    time.sleep(0.05)