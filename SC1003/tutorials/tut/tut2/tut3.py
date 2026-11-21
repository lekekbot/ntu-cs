# For beginners, all code in a single file without functions
board_size = 10
valid_orientations = ["horizontal", "vertical"]
# Exercise 1: Basic Conditional Statements
x, y = 5, 8


# TODO : 1. Check if coordinates are within the valid range
def check_coord(x, y):
    if x <= 10 and x > 0 and y <= 10 and y > 0:
        return True
    return False


print(f"coord are {x}, {y} valid: ", check_coord(x, y))

# Add you code of TODO 1 here
# One more example
x, y = 10, -1
# TODO : 2. Check if coordinates are within the valid range
print(f"coord are {x}, {y} valid: ", check_coord(x, y))

# Copy your code of TODO 1 here to test on x, y = 10, -1


# Exercise 2: Conditional with Logical Operators
x, y, orientation = 4, 6, "horizontal"


# TODO : 3. Validate user input for coordinates and orientation
def check_orientation(orientation):
    if orientation in valid_orientations:
        return True
    return False


# Add you code of TODO 3 here
# One more example
x, y, orientation = 11, 3, "diagonal"


def validate_user_input(x, y, coordinate):
    if check_coord(x, y) and check_orientation(coordinate):
        return True
    return False


print(f'input {x}, {y}, {orientation} valid: ', validate_user_input(x, y, orientation))

# TODO : 4. Validate user input for coordinates and orientation
# Copy your code of TODO 3 here to test on x, y, orientation = 11, 3, 'diagonal'
# Exercise 3: Nested Conditionals

x, y, ship_length, orientation = 3, 5, 4, "horizontal"
print(f'input {x}, {y}, {orientation} valid: ', validate_user_input(x, y, orientation))


def validate_ship_input(x, y, ship_length, orientation):
    if not validate_user_input(x, y, orientation):
        return False
    if orientation == "horizontal":
        if y + ship_length - 1 > 10:
            return False
    elif orientation == "vertical":
        if x + ship_length - 1 > 10:
            return False
    return True


# TODO : 5. Validate the placement of a ship
# Add you code of TODO 5 here
print(f'placement {x}, {y}, {ship_length}, {orientation} valid: ', validate_ship_input(x, y, ship_length, orientation))


# One more example
x, y, ship_length, orientation = 7, 7, 4, "vertical"
# TODO : 6. Validate the placement of a ship
# Copy your code of TODO 5 here to test on x, y, ship_length, orientation = 7, 7, 4, 'vertical'
print(f'placement {x}, {y}, {ship_length}, {orientation} valid: ', validate_ship_input(x, y, ship_length, orientation))
