keywords = [
	'UNITEDKINGDOM', 'SINGAPORE', 'GERMANY', 'ARGENTINA',
	'NETHERLANDS', 'PORTUGAL', 'INDONESIA', 'AUSTRALIA'
]

board = [
	['J', 'Y', 'B', 'Y', 'Q', 'V', 'W', 'G', 'B', 'Q', 'F', 'D', 'D', 'U', 'L', 'H', 'M'],
	['D', 'G', 'O', 'C', 'G', 'V', 'N', 'K', 'Z', 'C', 'R', 'U', 'B', 'A', 'O', 'I', 'K'],
	['U', 'G', 'E', 'U', 'H', 'E', 'W', 'J', 'W', 'T', 'O', 'Y', 'N', 'U', 'M', 'N', 'V'],
	['N', 'H', 'U', 'R', 'D', 'B', 'R', 'J', 'I', 'V', 'U', 'I', 'T', 'P', 'G', 'H', 'W'],
	['I', 'H', 'H', 'O', 'O', 'I', 'E', 'M', 'Z', 'W', 'T', 'J', 'M', 'D', 'T', 'S', 'V'],
	['T', 'M', 'V', 'O', 'I', 'P', 'O', 'U', 'A', 'N', 'B', 'E', 'D', 'X', 'T', 'W', 'X'],
	['E', 'Z', 'H', 'B', 'B', 'Q', 'A', 'U', 'E', 'N', 'W', 'C', 'W', 'C', 'B', 'O', 'N'],
	['D', 'L', 'U', 'S', 'A', 'D', 'F', 'G', 'N', 'R', 'Y', 'Y', 'G', 'W', 'W', 'S', 'R'],
	['K', 'H', 'Y', 'I', 'I', 'R', 'R', 'M', 'N', 'I', 'P', 'H', 'A', 'B', 'R', 'W', 'P'],
	['I', 'T', 'Q', 'M', 'S', 'A', 'H', 'I', 'M', 'I', 'R', 'U', 'N', 'Z', 'Y', 'H', 'S'],
	['N', 'E', 'T', 'H', 'E', 'R', 'L', 'A', 'N', 'D', 'S', 'H', 'U', 'N', 'K', 'E', 'Z'],
	['G', 'F', 'K', 'L', 'N', 'L', 'A', 'G', 'U', 'T', 'R', 'O', 'P', 'B', 'I', 'U', 'E'],
	['D', 'C', 'P', 'G', 'O', 'G', 'G', 'A', 'R', 'U', 'P', 'U', 'E', 'O', 'P', 'K', 'M'],
	['O', 'J', 'B', 'T', 'D', 'N', 'T', 'A', 'X', 'O', 'B', 'X', 'Z', 'M', 'J', 'C', 'C'],
	['M', 'J', 'F', 'P', 'N', 'S', 'L', 'L', 'X', 'B', 'V', 'C', 'Y', 'W', 'T', 'K', 'E'],
	['R', 'X', 'I', 'S', 'I', 'I', 'Z', 'W', 'A', 'M', 'K', 'S', 'L', 'N', 'H', 'V', 'S'],
	['A', 'O', 'J', 'O', 'A', 'E', 'G', 'T', 'X', 'M', 'C', 'Z', 'P', 'C', 'I', 'O', 'U'],
]

def construct_lookup_table(board):
	lookup_table = {}

	# n^2 construction
	for row_index, row in enumerate(board):
		for col_index, col in enumerate(row):
			index = row_index, col_index

			try:
				lookup_table[col].append(index)
			except:
				lookup_table[col] = [index]

	return lookup_table

def find_word_in_grid():
	pass

def solve(board, keywords):
	"""
	idea 0: traverse the board + trie traversal 					O(search: n^2, traverse: nlogn)
																	n^3 for searching array of keyword
																	(do search everytime for each keyword)

	idea 1: hashmap + trie traversal from first letter				O(construct: n^2, traverse: nlogn)
	idea 2: hashmap + check first letter and last letter alignment	O(construct: n^2: matching: n)
																	(at most n^2 bcs HASHMAP CONSTRUCTION)
	"""
	letters_index_lookup = construct_lookup_table(board)  # lookup table for indexes. letter: [(row, col)]
	result = []

	# n search
	for keyword in keywords:
		FOUND = False
		first_letter_indexes = letters_index_lookup[keyword[0]]  # all possible index
		
		# constant index search
		for index in first_letter_indexes:
			# depth first search
			# on a 3x3 grid, excluding current index (8), start from top-left, end in bottom-right
			# beware of bounds error, use max against 0; min against length of board
			grid_start = max(index[0] - 1, 0), max(index[1] - 1, 0)
			grid_end = min(index[0] + 1, len(board) - 1), min(index[1] + 1, len(board) - 1)
			
			for i in range(grid_start[0], grid_end[0] + 1):  # +1 inclusive
				for j in range(grid_start[1], grid_end[1] + 1):  # +1 inclusive
					# skip index (exlucing current index)
					if i == index[0] and j == index[1]:
						continue

					keyword_index = [index]  # index lists
					if board[i][j] == keyword[1]:  # try to match with the 2nd word
						# now, follow the pathway!! step through the keyword while matching along the way
						step = i - index[0], j - index[1]  # explanation of step below (in example)

						# add found 2nd word to found list
						keyword_index.append((i, j))

						# len(keyword) matching
						# start matching from the 3rd letter (index 2), until the end
						for pointer in range(2, len(keyword)):
							# step * pointer: step is the increment of pointer
							# example: for the word 'GERMANY' we find G in (1 4), and match E in (2 5)
							# 		   our step was E - G: (2 5) - (1 4) = (1 1), we go bottom-right
							#
							#		   we step along the way for GE-RMANY, that is length of GERMANY - 2
							#		   and it's implicit in range(2, len(keyword) + 1): 8 - 2, 6
							#		   don't forget the +1 inclusive range, so 6 - 1, it's 5
							#
							#		   now, to start stepping, we do step*pointer + initial index
							#		   because to get to 'R' in (3 6), we must increment initial index (1 4)
							#		   by R - G: (3 6) - (1 4) = (2 2) and we got (2 2) from step * pointer
							#		   (our step was (1 1) and our pointer start from 2)
							next_step = step[0]*pointer + index[0], step[1]*pointer + index[1]

							# stop searching if the letter doesn't match
							if board[next_step[0]][next_step[1]] == keyword[pointer]:
								keyword_index.append(next_step)
							else:
								break  # break from pathway
					
					if len(keyword_index) == len(keyword):
						FOUND = True
						result.append(keyword_index)
						break  # break from col grid
				
				if FOUND:
					break  # break from row grid

			if FOUND:
				break  # break from index search. LMAO LOOK AT THIS. FUCK ME:)
		
	return result

def check_answer(answer):
	correct = [
		[(2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (10, 0), (11, 0), (12, 0), (13, 0), (14, 0)],
		[(10, 10), (9, 9), (8, 8), (7, 7), (6, 6), (5, 5), (4, 4), (3, 3), (2, 2)],
		[(1, 4), (2, 5), (3, 6), (4, 7), (5, 8), (6, 9), (7, 10)],
		[(9, 5), (8, 6), (7, 7), (6, 8), (5, 9), (4, 10), (3, 11), (2, 12), (1, 13)],
		[(10, 0), (10, 1), (10, 2), (10, 3), (10, 4), (10, 5), (10, 6), (10, 7), (10, 8), (10, 9), (10, 10)],
		[(11, 12), (11, 11), (11, 10), (11, 9), (11, 8), (11, 7), (11, 6), (11, 5)],
		[(15, 4), (14, 4), (13, 4), (12, 4), (11, 4), (10, 4), (9, 4), (8, 4), (7, 4)],
		[(8, 12), (9, 11), (10, 10), (11, 9), (12, 8), (13, 7), (14, 6), (15, 5), (16, 4)],
	]
	
	if len(answer) != len(correct):
		print('Wrong Answer')
		return
	
	for a, c in zip(answer, correct):
		for e1, e2 in zip(a, c):
			if e1 != e2:
				print('Wrong Answer')
				return

	print("Correct!")

answer = solve(board, keywords)

# this would print the result
# for keyword, index in zip(keywords, answer):
	# print(keyword, index)

check_answer(answer)
