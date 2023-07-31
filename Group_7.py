from Game import Game

filepath = input("Enter filepath: ")
game = Game(filepath)
choose = int(input("Enter level 1->4: "))

if choose == 1:
    game.play_game_level_1()
    game.save_result(1)
elif choose == 2:
	game.play_game_level_2()
	game.save_result(2)
elif choose == 3:
	game.play_game_level_3()
	game.save_result(3)
elif choose == 4:
	game.play_game_level_4()
	game.save_result(4)
else:
    print("Invalid level")
