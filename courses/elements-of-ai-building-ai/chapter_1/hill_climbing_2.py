import random

def main():
	prob = random.random()
	
	if prob < 0.8:
		favourite = "dogs"
	elif prob < 0.9:
		favourite = "cats"
	else:
		favourite = "bats"

	print("I love " + favourite)


main()