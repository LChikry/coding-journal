import numpy as np

data = [[1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
		[1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
		[1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
		[1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1],
		[1, 1, 1, 0, 1, 3, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1]]

def get_man_distance(a, b):
	sm = list(range(len(a)))
	sm = list(map(lambda i: abs(a[i]-b[i]), sm))
	return sum(sm)


def find_nearest_pair(data):
	N = len(data)
	dist = np.empty((N, N), dtype=float)

	for i in range(N):
		for j in range(N):
			if i == j:
				dist[i][j] = np.inf
				continue
			
			dist[i][j] = get_man_distance(data[i], data[j])
	print(np.unravel_index(np.argmin(dist), dist.shape))

find_nearest_pair(data)