import config
import time
from game import Game

if __name__ == "__main__":
    my_game = Game()
    while my_game.is_running():
        # TIME MEASURE FOR FPS LIMITER
        frame_start = time.time()

        # GAME ACTIONS
        my_game.handle_events()
        my_game.update()
        my_game.render()
        # GAME ACTIONS

        frame_time = (time.time() - frame_start) * 1000
        desired_frame_time = 1000 / config.FPS
        if frame_time < desired_frame_time:
            time.sleep((desired_frame_time - frame_time) / 1000)