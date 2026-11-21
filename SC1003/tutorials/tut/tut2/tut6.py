BOARD_SIZE = 10


# Function 1: Initialize an empty board
def init_board():
    ## TODO: Return a BOARD_SIZE x BOARD_SIZE list of lists with all cells set to 0
    return [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]


# Function 2: Get starting position for a ship
def get_ship_position(ship_name):
    ## TODO: Prompt the user for coordinates in "row,col" format
    ## Convert to tuple of integers and return
    while True:
        try:
            row, col = map(
                int, input(f"Enter {ship_name} position (row,col): ").split(",")
            )
            if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                return (row, col)
            else:
                print(
                    "Invalid position. Please enter coordinates within the board range."
                )
        except ValueError:
            print("Invalid input. Please enter coordinates in the format 'row,col'.")


# Function 3: Place ship on the board
def place_ship(board, start_pos, length, symbol):
    ## TODO: Place the ship horizontally from start_pos for 'length' cells
    row, col = start_pos
    for i in range(length):
        board[row][col + i] = symbol


# Function 4: Display the board
def display_board(board):
    ## TODO: Print each row of the board
    for row in board:
        print(" ".join(map(str, row)))


# Function 5: Check attack validity
def check_attack(board, row, col):
    ## TODO: Return True if coordinates are within range, else False
    if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
        return True
    return False


def get_attack():
    ## TODO: Prompt the user for attack coordinates in "row,col" format
    ## Convert to tuple of integers and return
    while True:
        try:
            row, col = map(int, input("Enter attack position (row,col): ").split(","))
            if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                return (row, col)
            else:
                print(
                    "Invalid position. Please enter coordinates within the board range."
                )
        except ValueError:
            print("Invalid input. Please enter coordinates in the format 'row,col'.")


def apply_attack(board, row, col):
    ## TODO: Check if the cell is empty (0)
    ## If empty, mark as hit (1) and return True
    ## If not empty, return False
    if board[row][col] == 0:
        board[row][col] = "O"
        print("Miss!")
        return True
    elif board[row][col] == "C" or board[row][col] == "S":
        ship_symbol = board[row][col]
        ship_length = next(
            ship["length"] for ship in ships.values() if ship["symbol"] == ship_symbol
        )
        ship_name = next(
            name for name, details in ships.items() if details["symbol"] == ship_symbol
        )
        board[row][col] = "X"
        if check_ship_sunk(board, ship_symbol, ship_length):
            print(f"{ship_name} sunk!")
        else:
            print("Hit!")
        return True
    return False


def check_ship_sunk(board, ship_symbol, ship_length):
    ## using ship_symbol to check if all cells of the ship have been hit (symbol 'X')
    # Count the number of 'X' marks for the given ship symbol
    hit_count = sum(row.count("X") for row in board)
    # Count the total number of cells that should be occupied by the ship
    ship_count = sum(row.count(ship_symbol) for row in board)
    # Ship is sunk if number of hits equals ship length and no original symbols remain
    return hit_count == ship_length and ship_count == 0


# -----------------------
# Main Program
# -----------------------
# Initialize board
game_board = init_board()
# Dictionary to store ships: name, length, symbol
ships = {
    "Carrier": {"length": 5, "symbol": "C"},
    "Submarine": {"length": 3, "symbol": "S"},
}
# Get and place each ship
for name, details in ships.items():
    start_pos = get_ship_position(name)
    place_ship(game_board, start_pos, details["length"], details["symbol"])
# Display the final board with ships placed
display_board(game_board)
# Example attack check

game_end = False

while not game_end:
    attack_row, attack_col = get_attack()
    if apply_attack(game_board, attack_row, attack_col):
        display_board(game_board)
    else:
        print("Invalid attack. Try again.")
    # Check if all ships are sunk by looking for any remaining ship symbols on the board
    all_ships_sunk = True
    for row in game_board:
        for cell in row:
            if cell in [ship["symbol"] for ship in ships.values()]:
                all_ships_sunk = False
                break
        if not all_ships_sunk:
            break

    if all_ships_sunk:
        print("Game Over! All ships have been sunk!")
        game_end = True
