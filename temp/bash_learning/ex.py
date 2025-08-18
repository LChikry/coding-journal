def draw_figure():
	SIZE = int(input("Enter figure size: "))

	for row in range(SIZE):
		print("+"*(SIZE-row) + 'o' * (row*2+1) + '+'*(SIZE-row))

draw_figure()