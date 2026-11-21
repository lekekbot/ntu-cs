board_size = 10
# TODO : 1. Initialize a board_sizexboard_size game board with all cells set to 0 (empty)
# Add you code of TODO 1 here
board_sizexboard_size = [[0 for _ in range(board_size)] for _ in range(board_size)]

# TODO : 2.While loop to repeatedly ask for valid attack coordinates
# Add you code of TODO 2 here


def is_valid_attack_coordinates(coords, board_width, board_height, num_layers):
    try:
        row, col, depth = coords.split(",")
        row = ord(row.upper()) - ord("A")  # Convert letter to number (A=0, B=1, ...)
        col = int(col) - 1  # Convert to 0-based index
        depth = int(depth)
        if (
            0 <= row < board_height
            and 0 <= col < board_width
            and 0 <= depth < num_layers
        ):
            return True
        return False
    except (ValueError, IndexError):
        return False


valid_input = False
while not valid_input:
    input_row = (
        input("Please enter the row (A-J) for the attack coordinate: ").strip().upper()
    )
    input_col = input(
        "Please enter the column (1-10) for the attack coordinate: "
    ).strip()

    user_input = f"{input_row},{input_col},0"  # Assuming depth = 0 for surface level
    if is_valid_attack_coordinates(user_input, board_size, board_size, 2):
        valid_input = True
        print("Valid input received:", user_input)
        board_sizexboard_size[ord(input_row) - ord("A")][int(input_col) - 1] = 1  # Mark hit
    else:
        print("Invalid input. Please try again.")

# TODO : 3. For loop to iterate through each row and column of the board
# Add you code of TODO 3 here
for row in range(board_size):
    for col in range(board_size):
        print(board_sizexboard_size[row][col], end=" ")
    print()
