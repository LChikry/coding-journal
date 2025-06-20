import math
import random


w = [.05, random.random()/3, random.random()/3]
h = [1.+math.sin(1+x/.6)*w[0]+math.sin(-.3+x/9.)*w[1]+math.sin(-.2+x/30.)*w[2] for x in range(100)]

def climb(x, h):
	# keep climbing until we've found a summit
	summit = False

	# edit here
	while not summit:
		summit = True         # stop unless there's a way up
		for i in range(max(0, x-5), min(99, x+5)):
			if h[i] > h[x]:
				x = i        # right is higher, go there
				summit = False    # and keep going
	return x


def main(h):       	 
	x0 = random.randint(1, 98)
	x = climb(x0, h)
	
	return x0, x

main(h)