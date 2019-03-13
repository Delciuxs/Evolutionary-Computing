# 14 3
# 10 1 7

from sys import stdin, stdout

def main():

	print("COIN CHANGE PROBLEM")
	print("Enter the change and the amount of coins: ")
	change, numCoins = map(int, stdin.readline().split())
	
	denominations = list()
	print("Enter the denominations of the coins: ")
	denominations = list(map(int, stdin.readline().split()))

	print("Select a solving paradigm")
	print("1) Greedy")
	print("2) DynamicProgramming")
	option = int(stdin.readline())

	if option == 1:
		print("Solving with Greedy")
		denominations.sort()

		amountCoinsUsed = 0
		coinsUsed = {}
		aux = 0

		for i in range(len(denominations) - 1, -1, -1):
			aux = int(change / denominations[i])
			amountCoinsUsed += aux
			change = change - (denominations[i] * (aux))
			coinsUsed[denominations[i]] = int(aux)


		print("The minimum used coins were: " + str(amountCoinsUsed))
		for key in coinsUsed:
			print("For the denomination " + str(key) + ", were used: " + str(coinsUsed[key]) + " coins")
		

	elif option == 2:
		print("Solving with DynamicProgramming")
		denominations.insert(0,0)
		coinsUsed = {}

		for i in range(1, len(denominations)):
			coinsUsed[denominations[i]] = 0
		
		memo = list()
		for i in range(0,numCoins + 1):
			memo.append([-1] * (change + 1))

		for i in range(0,numCoins + 1):
			memo[i][0] = 0

		for i in range(1,change + 1):
			if i % denominations[1] == 0:
				memo[1][i] = int(i / denominations[1])
			else:
				memo[1][i] = change + 1

		for i in range(2, numCoins + 1):
			for j in range(1, change + 1):
				if j < denominations[i]:
					memo[i][j] = memo[i - 1][j]
				else:
					memo[i][j] = min(memo[i - 1][j], memo[i][j - denominations[i]] + 1)

		i = numCoins
		j = change

		while True:
			if i == 0 or j == 0:
				break
			if memo[i][j] == memo[i - 1][j]:
				i = i - 1
			else:
				coinsUsed[denominations[i]] += 1
				j = j - denominations[i]

		stdout.write("The minimum used coins were: " + str(memo[numCoins][change]) + "\n")
		for key in coinsUsed:
			print("For the denomination " + str(key) + ", were used: " + str(coinsUsed[key]) + " coins")


main()