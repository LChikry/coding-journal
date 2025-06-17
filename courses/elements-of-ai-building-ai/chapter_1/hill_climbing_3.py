import random
import math

def accept_prob(S_old, S_new, T):
	if S_new > S_old: return 1.0

	s = - (S_old - S_new)
	return math.exp(s/T)

# the above function will be used as follows. this is shown just for
# your information; you don't have to change anything here
def accept(S_old, S_new, T):
	if random.random() < accept_prob(S_old, S_new, T):
		print(True)
	else:
		print(False)
