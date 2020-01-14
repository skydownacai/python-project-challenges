class chess:
	def __init__(self):

		self.board = [[0 for i in range(5)] for j in range(5)]

		self.avaliable_position = 25 #可下的网格数


		print("Scenario: New game")

		self.displayboard()

	def displayboard(self):

		print("    1  2  3  4  5 ")

		print("   |-------------|")

		for i in range(5):

			print("{}  |{}  {}  {}  {}  {}|".format(i+1,self.board[i][0],self.board[i][1],self.board[i][2],self.board[i][3],self.board[i][4]))

		print("   |-------------|")

	def check_player_win(self):

		for i in range(4):

			for j in range(4):

					if self.board[i][j] == 1 and self.board[i + 1][j] == 1 and self.board[i][j + 1] == 1  and self.board[i + 1][j + 1] == 1:

						return True

		return  False
	@staticmethod
	def index_to_pos(index):

		row = int(index / 5)

		column = index - row * 5

		return row , column

	
def oneToken():

	board = chess()

	player_won = False

	display_message = "Player-1: input square to play:"

	while board.avaliable_position >= 1:


		while True:

			choice = int(input(display_message))

			player1_x , player1_y = chess.index_to_pos(choice - 1)

			if board.board[player1_x][player1_y] == 0 :

					board.board[player1_x][player1_y] = 1

					board.avaliable_position -= 1

					break
			else:

				display_message = "Square is occpuied. Try again:"


		board.displayboard()

		if board.check_player_win():

			player_won = True

			break

		display_message = "Player-1: input square to play:"

		##computer step

		import random


		random_choice = random.randint(1,25)

		print("Player-2: input square to play:",random_choice)

		computer_x, computer_y = chess.index_to_pos(random_choice - 1)

		if board.board[computer_x][computer_y] == 0:

			board.avaliable_position -= 1

		board.board[computer_x][computer_y] = 2

		board.displayboard()

	if player_won:

		print("Player-1 wins! End of game")

	else:

		print("computer won!")
def twoTokens():
	board = chess()

	player_won = False

	display_message = "Player-1: input square to play:"

	while board.avaliable_position >= 1:

		while True:

			choice = int(input(display_message))

			player1_x, player1_y = chess.index_to_pos(choice - 1)

			if board.board[player1_x][player1_y] == 0:

				board.board[player1_x][player1_y] = 1

				board.avaliable_position -= 1

				break
			else:

				display_message = "Square is occpuied. Try again:"

		board.displayboard()

		if board.check_player_win():
			player_won = True

			break

		display_message = "Player-1: input square to play:"

		##computer step

		import random

		for i in range(2):
			random_choice = random.randint(1, 25)

			print("Player-2: input square to play:", random_choice)

			computer_x, computer_y = chess.index_to_pos(random_choice - 1)

			if board.board[computer_x][computer_y] == 0:

				board.avaliable_position -= 1

			board.board[computer_x][computer_y] = 2

			board.displayboard()

	if player_won:

		print("Player-1 wins! End of game")

	else:

		print("computer won!")

def threeTokens():
	board = chess()

	player_won = False

	display_message = "Player-1: input square to play:"

	while board.avaliable_position >= 1:

		while True:

			choice = int(input(display_message))

			player1_x, player1_y = chess.index_to_pos(choice - 1)

			if board.board[player1_x][player1_y] == 0:

				board.board[player1_x][player1_y] = 1

				board.avaliable_position -= 1

				break
			else:

				display_message = "Square is occpuied. Try again:"

		board.displayboard()

		if board.check_player_win():
			player_won = True

			break

		display_message = "Player-1: input square to play:"

		##computer step

		import random

		for i in range(3):

			random_choice = random.randint(1, 25)

			print("Player-2: input square to play:", random_choice)

			computer_x, computer_y = chess.index_to_pos(random_choice - 1)

			if board.board[computer_x][computer_y] == 0:
				board.avaliable_position -= 1

			board.board[computer_x][computer_y] = 2

			board.displayboard()

	if player_won:

		print("Player-1 wins! End of game")

	else:

		print("computer won!")

def main():
	option = ""

	while option != "X":

		print("Main Menu")

		print("Test 1: player-2 placing one token")

		print("Test 2: player-2 placing two tokens ")

		print("Test 3: player-2 placing three tokens ")

		print("X: Exit")

		print()

		option = input("Select an option: 1,2,3 or X: ")

		option = option.upper()

		while option not in ("1", "2", "X"):

			print("Invalid option, Please try again!")

			option = input("Enter 1, 2, 3or X: ")

			option = option.upper()

		if option == "1":

			oneToken()

		elif option == "2":

			twoTokens()

		elif option == "3":

			threeTokens()

threeTokens()