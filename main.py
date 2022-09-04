from algorithm import algorithm

def print_matrix(matrix):
	for row in matrix:
		str1 = "["
		for number in row:
			num_frac = number.as_integer_ratio()
			if num_frac[1] == 1:
				str1 += str(num_frac[0]) + ',\t'
			else:
				if len(str(num_frac[0])) > 10:
					str1 += str(num_frac[0]/num_frac[1])[:8] + ",\t"
				else:
					str1 += str(num_frac[0]) + "/" + str(num_frac[1]) + ",\t"
		str1 = str1[:-2] + "]"
		print(str1)

saved_matrices = {}


def help_cmd(cmd_input):
	print(help_lines)

def exit_cmd(cmd_input):
	exit()

def display_cmd(cmd_input):
	try:
		if len(cmd_input) > 1:
			print_matrix(saved_matrices[cmd_input[2]])
		else:
			for matrix in saved_matrices:
				print('\n')
				print(matrix)
				print_matrix(saved_matrices[matrix])
				print('\n')
	except:
		print("Your command isn't formatted properly. Remember to use spaces between commands, switches, and parameters.")



def save_cmd(cmd_input):
	try:
		rows = 0
		columns = 0
		number_list = []
		matrix = []

		#this will assign our variables to the parameters after the switches
		for cmd_index in range(len(cmd_input)):
			if cmd_input[cmd_index] == "-r":
				rows = int(cmd_input[cmd_index + 1])
			elif cmd_input[cmd_index] == "-c":
				columns = int(cmd_input[cmd_index + 1])
			elif cmd_input[cmd_index] == "-m":
				number_list = cmd_input[cmd_index + 1].split(",")
		
		for row in range(rows):
			matrix.append([])
			for col in range(columns):
				if len(number_list) != 0:
					matrix[row].append(float(number_list[0]))
					number_list.pop(0)
				else:
					matrix[row].append(0.0)
		
		saved_matrices[cmd_input[1]] = matrix
		display_cmd(["display", "-n", cmd_input[1]])

	except:
		print("Your command isn't formatted properly. Remember to use spaces between commands, switches, and parameters.")


def add_cmd(cmd_input):
	try:
		matrix = saved_matrices[cmd_input[1]]
		number_list = []

		for cmd_index in range(len(cmd_input)):
			if cmd_input[cmd_index] == "-m":
				if cmd_index + 1 == len(cmd_input):
					number_list.append(0.0)
					break
				else:
					number_list = cmd_input[cmd_index + 1].split(",")

		matrix.append([])
		for num in range(len(matrix[0])):
			if len(number_list) != 0:
				matrix[-1].append(float(number_list[0]))
				number_list.pop(0)
			else:
				matrix[-1].append(0.0)

		display_cmd(["display", "-n", cmd_input[1]])

	except:
		print("Your command isn't formatted properly. Remember to use spaces between commands, switches, and parameters.")

def remove_cmd(cmd_input):
	try:
		if len(cmd_input) == 2:
			saved_matrices.pop(cmd_input[1])
		else:
			saved_matrices[cmd_input[1]].pop(int(cmd_input[3]))
			display_cmd(["display", "-n", cmd_input[1]])
	except:
		print("Your command isn't formatted properly. Remember to use spaces between commands, switches, and parameters.")

def switch_cmd(cmd_input):
	try:
		matrix = saved_matrices[cmd_input[1]]
		row1 = int(cmd_input[2])
		row2 = int(cmd_input[3])

		matrix[row1], matrix[row2] = matrix[row2], matrix[row1]
		display_cmd(["display", "-n", cmd_input[1]])
	except:
		print("Your command isn't formatted properly. Remember to use spaces between commands, switches, and parameters.")


def manipulate_cmd(cmd_input):
	try:
		matrix = saved_matrices[cmd_input[1]]
		matrix_row_index = int(cmd_input[2])

		manipulated_row = matrix[matrix_row_index].copy()
		other_row = []
		is_adding_to_other_row = False

		for cmd_index in range(len(cmd_input)):
			if cmd_input[cmd_index] == "-m":
				manipulated_row = [num * float(cmd_input[cmd_index + 1]) for num in matrix[matrix_row_index]]
			elif cmd_input[cmd_index] == "-d":
				manipulated_row = [num / float(cmd_input[cmd_index + 1]) for num in matrix[matrix_row_index]]
			elif cmd_input[cmd_index] == "-a":
				scalar, row = tuple(cmd_input[cmd_index + 1].split("x"))
				other_row = [num * float(scalar) for num in matrix[int(row)]]
				is_adding_to_other_row = True

		if is_adding_to_other_row:
			manipulated_row = [manipulated_row[i] + other_row[i] for i in range(len(other_row))]
		matrix[matrix_row_index] = manipulated_row

		display_cmd(["display", "-n", cmd_input[1]])

	except:
		print("Your command isn't formatted properly. Remember to use spaces between commands, switches, and parameters.")


def solve_cmd(cmd_input):
	try:
		verbose = False

		if cmd_input[-1] == "-v":
			verbose = True

		saved_matrices[cmd_input[1]] = algorithm(saved_matrices[cmd_input[1]], verbose)
		print("\nRREF:")
		display_cmd(["display", "-n", cmd_input[1]])
	except:
		print("Your command isn't formatted properly. Remember to use spaces between commands, switches, and parameters.")


dict_of_commands = {
	"help": help_cmd,
	"exit": exit_cmd,
	"display": display_cmd,
	"save": save_cmd,
	"add": add_cmd,
	"remove": remove_cmd,
	"switch": switch_cmd,
	"manipulate": manipulate_cmd,
	"solve": solve_cmd,
}

help_lines = """
help\t\t\t\t\t\t- Displays information about commands.

exit\t\t\t\t\t\t- Exits the program.

display\t\t\t\t\t\t- Prints all saved matrices with their names.
	-n [str]\t\t\t\t\tdisplays only the matrix with name [str]

save [str]\t\t\t\t\t- Stores a matrix in Random Access Memory with name [str].
	-r [int]\t\t\t\t\tspecifies the number of rows in the matrix
	-c [int]\t\t\t\t\tspecifies the number of columns in the matrix
	-m [num],[num],[num]...\t\t\t\tadds numbers to the matrix (enter the entire matrix here)

add [str]\t\t\t\t\t- Adds a row to saved matrix with name [str].
	-m [num],[num],[num]...\t\t\t\tadds numbers to the new row (enter the entire row here)

remove [str]\t\t\t\t\t- Removes matrix [str] from Random Access Memory.
	-r [int]\t\t\t\t\tremoves row [int] from matrix [str] (first row is 0)

switch [str] [int] [int]\t\t\t- Switches two rows [int] [int] in matrix [str].

manipulate [str] [int]\t\t\t\t- Allows you to make changes to row [int] of matrix [str].
	-a [int]x[int1]\t\t\t\t\tadds row [int1] times scalar [int] to the manipulated row
	-m [int]\t\t\t\t\tmultiplies the manipulated row by [int] (runs before -a switch)
	-d [int]\t\t\t\t\tdivides the manipulated row by [int] (runs before -a switch)

solve [str]\t\t\t\t\t- Converts the matrix [str] to reduced row echelon form.
	-v\t\t\t\t\t\tverbose
"""


def main():
	print("matrix manipulation command line program (type help for help)")

	while True:
		cmd_input = input('main.py>')
		split_cmd = cmd_input.split(' ')
		for cmd in dict_of_commands:
			if split_cmd[0] == cmd:
				dict_of_commands[split_cmd[0]](split_cmd)
				break
		else:
			print(f"'{cmd_input}' is not a valid command. Type help for help.")

main()