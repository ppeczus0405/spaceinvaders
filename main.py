import game

if __name__ == "__main__":
    my_game = game.Game()
    while my_game.is_running():
        my_game.handle_events()
        my_game.update()
        my_game.render()