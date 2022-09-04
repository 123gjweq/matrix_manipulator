def print_matrix(matrix, last_printed): #used if verbose is on
	if matrix != last_printed:
		print('\n')
		for row in matrix:
			str1 = "["
			for number in row:
				num_frac = number.as_integer_ratio()
				if num_frac[1] == 1:
					str1 += str(num_frac[0]) + ",\t"
				else:
					if len(str(num_frac[0])) > 10:
						str1 += str(num_frac[0]/num_frac[1])[:8] + ",\t"
					else:
						str1 += str(num_frac[0]) + "/" + str(num_frac[1]) + ",\t"
			str1 = str1[:-2] + "]"
			print(str1)
		return matrix


def multiply_row(row, scalar):
	return [i * scalar for i in row]

def add_rows(row1, row2):
	return [row1[i] + row2[i] for i in range(len(row1))]

def find_pivot(matrix, pivot_coords):
	for row in range(len(matrix)):
		for num in range(len(matrix[0])):
			if matrix[row][num] != 0 and row > pivot_coords[0]:
				return (row, num)

def gcf(row):
	gcf = 1
	for i in range(1, int(max(row) + 1) // 2):
		for x in row:
			if x / i != x // i:
				break
		else:
			gcf = i
	return [i / gcf for i in row]

def convert_pivots_to_1(matrix, pivot_list):
	for pivot in pivot_list:
		row, num = pivot
		matrix[row] = [i / matrix[row][num] for i in matrix[row]]


def make_zeros(matrix, pivot):
	if pivot == None: #check if we have gotten all the pivots
		return 1

	pivot_row, pivot_col = pivot
	for row in range(pivot_row + 1, len(matrix)):
		current_row = []
		manipulated_row = []

		if matrix[pivot_row][pivot_col] == 0:
			continue

		current_row = multiply_row(matrix[pivot_row], matrix[row][pivot_col])
		manipulated_row = multiply_row(matrix[row], -matrix[pivot_row][pivot_col])
		matrix[row] = gcf(add_rows(current_row, manipulated_row))

	return 0

def make_reduced_zeros(matrix, pivot):
	pivot_row, pivot_col = pivot
	for row in range(pivot_row - 1, -1, -1):
		current_row = []
		manipulated_row = []

		if matrix[pivot_row][pivot_col] == 0:
			continue

		current_row = multiply_row(matrix[pivot_row], matrix[row][pivot_col])
		manipulated_row = multiply_row(matrix[row], -matrix[pivot_row][pivot_col])
		matrix[row] = gcf(add_rows(current_row, manipulated_row))

def organize_rows(matrix):
	list_of_values_and_indexes = []
	new_matrix = []
	for row in range(len(matrix)):
		row_value = 0
		for num in range(len(matrix[0])):
			row_value = num
			if matrix[row][num] != 0:
				break
		list_of_values_and_indexes.append((row_value, row))
	list_of_values_and_indexes.sort()
	for i in list_of_values_and_indexes:
		new_matrix.append(matrix[i[1]])
	return new_matrix

def algorithm(matrix, verbose):
	pivot_list = []
	pivot_coords = (-1, -1)
	last_printed = []

	while True:
		matrix = organize_rows(matrix)
		if verbose:
			last_printed = print_matrix(matrix, last_printed)

		pivot_coords = find_pivot(matrix, pivot_coords)
		done = make_zeros(matrix, pivot_coords)

		if verbose:
			last_printed = print_matrix(matrix, last_printed)

		if not done:
			pivot_list.append(pivot_coords)
		else:
			pivot_list = pivot_list[::-1]
			break

	convert_pivots_to_1(matrix, pivot_list)

	for pivot in pivot_list:
		make_reduced_zeros(matrix, pivot)
		if verbose:
			last_printed = print_matrix(matrix, last_printed)

	convert_pivots_to_1(matrix, pivot_list)
	matrix = organize_rows(matrix)

	return matrix