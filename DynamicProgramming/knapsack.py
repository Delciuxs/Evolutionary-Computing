from sys import stdin, stdout

def main():
	stdout.write("KNAPSACK\n")

	stdout.write("Enter the number of objects and the capacity\n")
	numObjects, capacity = map(int, stdin.readline().split())
	values = list()
	sizes  = list()
	usedObjects = {}

	stdout.write("Enter the value of each object\n")
	values = list(map(int, stdin.readline().split()))
	stdout.write("Enter the size of each object\n")
	sizes = list(map(int, stdin.readline().split()))

	stdout.write("Select a solving paradigm\n")
	stdout.write("1) Greedy\n")
	stdout.write("2) DynamicProgramming\n")
	option = int(stdin.readline())

	if option == 1:
		stdout.write("Solving with Greedy\n")
		objects = list()

		for i in range(0, numObjects):
			objects.append((values[i], sizes[i]))

		objects.sort()
		remainingSize = capacity
		maxValue = 0

		for i in range(len(objects)-1, -1, -1):
			if remainingSize - objects[i][1] >= 0:
				remainingSize = remainingSize - int(objects[i][1])
				maxValue = maxValue + int(objects[i][0])
				usedObjects[i] = (objects[i][0], objects[i][1])

		stdout.write("The maximum value is " + str(maxValue) + "\n")
		for key in usedObjects:
			stdout.write("Used the object with value: " + str(usedObjects[key][0]) + 
									" and size: " + str(usedObjects[key][1]) + "\n")
			

	elif option == 2:
		stdout.write("Solving with DynamicProgramming\n")
		values.insert(0,0)
		sizes.insert(0,0)


		memo = list()
		for i in range(numObjects + 1):
			memo.append([0] * (capacity + 1))

		for i in range(1, numObjects + 1):
			for j in range(1, capacity + 1):
				if sizes[i] > j:
					memo[i][j] = memo[i-1][j]
				else:
					memo[i][j] = max(memo[i-1][j], memo[i-1][j-sizes[i]] + values[i])

		i = numObjects
		j = capacity

		while True:
			if i == 0:
				break
			if memo[i][j] == memo[i-1][j]:
				i = i - 1
			else:
				usedObjects[i] = (values[i], sizes[i])
				j = j - sizes[i]
				i = i - 1


		stdout.write("The maximum value is " + str(memo[numObjects][capacity]) + "\n")
		for key in usedObjects:
			stdout.write("Used the object with value: " + str(usedObjects[key][0]) + 
				" and size: " + str(usedObjects[key][1]) + "\n")

main()