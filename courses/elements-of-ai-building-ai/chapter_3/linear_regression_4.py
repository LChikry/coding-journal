import numpy as np
from io import StringIO


train_string = '''
25 2 50 1 500 127900
39 3 10 1 1000 222100
13 2 13 1 1000 143750
82 5 20 2 120 268000
130 6 10 2 600 460700
115 6 10 1 550 407000
'''

test_string = '''
36 3 15 1 850 196000
75 5 18 2 540 290000
'''

def main():
	np.set_printoptions(precision=1)    # this just changes the output settings for easier reading
	
	train_file = StringIO(train_string)
	test_file = StringIO(test_string)
	df_train = np.genfromtxt(train_file, skip_header=1)
	df_test = np.genfromtxt(test_file, skip_header=1)
	
	x_train = df_train[:,:-1]
	y_train = df_train[:,-1]
	x_test = df_test[:,:-1]
	y_test = df_test[:,-1]

	c = np.linalg.lstsq(x_train, y_train)[0]
	print(c)

	# this will print out the predicted prics for the two new cabins in the test data set
	print(x_test @ c)
	# print(y_test)

main()
