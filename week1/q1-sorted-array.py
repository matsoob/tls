import sys
from heapq import heappush, heappop
# The first line of the input contains one integer N, 
# the number of sorted arrays. The next line contains N integers, 
# the lengths of the N arrays. The following N lines contain 
# the sorted elements of the arrays, separated by whitespaces. All elements are integers.

def merge_sorted_arrays(sorted_arrays: list) -> list:
	result = []
	# add arrays to heap
	heap = []
	for arr in sorted_arrays:
		# give  popping last item is O(1), reverse the lists
		arr.reverse()
		if len(arr) != 0:
			heappush(heap, (arr.pop(), arr))

	while len(heap) != 0:
		current = heappop(heap)
		result.append(current[0])
		if len(current[1]) != 0:
			heappush(heap, (current[1].pop(), current[1]))

	return result

n = int(sys.stdin.readline())
lengths = [int(el) for el in sys.stdin.readline().split()]
arrays = [[int(el) for el in sys.stdin.readline().split()]
          for length in lengths]

# 1 <= N <= 23’000

merged = merge_sorted_arrays(arrays)

for el in merged:
    sys.stdout.write(str(el) + ' ')
 









