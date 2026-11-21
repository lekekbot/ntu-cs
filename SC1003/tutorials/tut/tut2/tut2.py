# TODO : 1. There are two players in the game. Initialize their names as string
# Add you code of TODO 1 here

player1 = "Computer"
player2 = "User"


# TODO : 2. There are two layers in the sea. Initialize the integer variable layer
# Add you code of TODO 2 here
layer = 2
# TODO : 3. The battleship board is 10 by 10 dimension. Initialize the integer variables
# width and height
# Add you code of TODO 3 here
width = 10
height = 10
# TODO : 4. Initialize a boolean variable that will be used to indicate
# whether user input is valid or not, two boolean variables hit and miss that indicate
# whether the ship is hit or missed
# Add you code of TODO 4 here
valid = False
hit = False
miss = False

# TODO : 5. The ships have only two orientation, either vertical or horizontal.
# Initialize a variable as ship orientation
# Add you code of TODO 5 here
ori = "v"
# TODO : 6. The coordinates of where to put ship or where to hit on the board have a
# specific format. Create a string variable as coordinates
# Add you code of TODO 6 here
coor = "A,4,1"
# TODO : 7. There are only two types of ships. Initialize two string variables as ship names
# Add you code of TODO 7 here
ship1 = "sumbarine"
ship2 = "carrier"
# TODO : 8. Initialize a string variable holding a welcome message that can be displayed to user
# Add you code of TODO 8 here
welmes = "Welcome to the Battleship!"

print(player1, player2)
print(layer)
print(width, height)
print(valid, hit, miss)
print(ori)
print(coor)
print(ship1, ship2)
print(welmes)

# TODO : 9. Take user input for attack coordinates and display the result.
# Add you code of TODO 9 here
attack_coor = input("Please enter coordinate of the attack center point in following this format (row,col,depth). E.g. A,4,1 Note: depth = 0 represents the subsea layer, and depth = 1 represents the surface level.")
if is_valid_attack_coordinates(attack_coor, width, height, layer):
    print("Hit at area: ", attack_coor)
else:
    print("Invalid attack coordinates.")

print(attack_coor)


def is_valid_attack_coordinates(coords, board_width, board_height, num_layers):
    """
    Check if the attack coordinates are valid.
    
    Args:
        coords (str): The attack coordinates in the format 'row,col,depth' (e.g., 'A,4,1')
        board_width (int): The width of the board
        board_height (int): The height of the board
        num_layers (int): The number of layers in the sea
        
    Returns:
        bool: True if the coordinates are valid, False otherwise
    """
    try:
        # Split the coordinates string
        parts = coords.strip().split(',')
        
        if len(parts) != 3:
            return False
        
        row_letter = parts[0].upper()
        col = int(parts[1])
        depth = int(parts[2])
        
        # Convert row letter to row number (A -> 0, B -> 1, etc.)
        row = ord(row_letter) - ord('A')
        
        # Check if the values are within the board boundaries
        if not (0 <= row < board_height):
            return False
        
        if not (1 <= col <= board_width):
            return False
        
        if not (0 <= depth < num_layers):
            return False
        
        return True
    except:
        # If any error occurs during parsing (e.g., invalid integer conversion)
        return False
