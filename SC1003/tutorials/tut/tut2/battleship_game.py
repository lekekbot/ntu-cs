import random
import os
import time

class Board:
    def __init__(self):
        # Create a 10x10 grid with two layers (surface=1, underwater=0)
        # 0 = empty, 1 = ship, 2 = hit, 3 = miss
        self.surface_layer = [[0 for _ in range(10)] for _ in range(10)]
        self.underwater_layer = [[0 for _ in range(10)] for _ in range(10)]
        self.rows = "ABCDEFGHIJ"
        self.cols = range(1, 11)
    
    def is_valid_coordinate(self, row, col, depth):
        """Check if the coordinates are valid."""
        return (
            row in self.rows and 
            1 <= col <= 10 and
            depth in [0, 1]
        )
    
    def get_layer(self, depth):
        """Return the appropriate layer based on depth."""
        return self.surface_layer if depth == 1 else self.underwater_layer
    
    def place_ship(self, ship, start_row, start_col, depth, orientation):
        """Place a ship on the board."""
        # Convert row letter to index
        row_idx = self.rows.index(start_row)
        col_idx = start_col - 1  # Convert to 0-indexed
        
        # Check if placement is valid
        if not self.is_valid_placement(ship, row_idx, col_idx, depth, orientation):
            return False
        
        # Place the ship
        layer = self.get_layer(depth)
        for i in range(ship.length):
            if orientation == "horizontal":
                layer[row_idx][col_idx + i] = 1
            else:  # vertical
                layer[row_idx + i][col_idx] = 1
        
        # Store ship's position
        positions = []
        for i in range(ship.length):
            if orientation == "horizontal":
                positions.append((row_idx, col_idx + i, depth))
            else:  # vertical
                positions.append((row_idx + i, col_idx, depth))
        ship.positions = positions
        
        return True
    
    def is_valid_placement(self, ship, row_idx, col_idx, depth, orientation):
        """Check if ship placement is valid."""
        # Check if ship is allowed at this depth
        if ship.name == "Carrier" and depth == 0:
            return False
        
        # Check if ship fits on the board
        if orientation == "horizontal" and col_idx + ship.length > 10:
            return False
        if orientation == "vertical" and row_idx + ship.length > 10:
            return False
        
        # Check for overlaps
        layer = self.get_layer(depth)
        for i in range(ship.length):
            if orientation == "horizontal":
                if layer[row_idx][col_idx + i] != 0:
                    return False
            else:  # vertical
                if layer[row_idx + i][col_idx] != 0:
                    return False
        
        return True
    
    def attack(self, row, col, depth):
        """Attack a position on the board."""
        # Convert row letter to index
        row_idx = self.rows.index(row)
        col_idx = col - 1  # Convert to 0-indexed
        
        layer = self.get_layer(depth)
        
        # Check if already attacked
        if layer[row_idx][col_idx] in [2, 3]:
            return "redundant"
        
        # Check if hit or miss
        if layer[row_idx][col_idx] == 1:  # Ship present
            layer[row_idx][col_idx] = 2  # Mark as hit
            return "hit"
        else:  # Empty space
            layer[row_idx][col_idx] = 3  # Mark as miss
            return "miss"
    
    def display(self, show_ships=True):
        """Display the board."""
        # Clear screen for better visualization
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("  Surface Layer (Depth = 1)")
        print("  " + " ".join(str(i) for i in self.cols))
        for i, row in enumerate(self.rows):
            print(f"{row} ", end="")
            for j in range(10):
                cell = self.surface_layer[i][j]
                if cell == 0:
                    print("· ", end="")
                elif cell == 1:
                    print("S " if show_ships else "· ", end="")
                elif cell == 2:
                    print("X ", end="")
                elif cell == 3:
                    print("O ", end="")
            print()
        
        print("\n  Underwater Layer (Depth = 0)")
        print("  " + " ".join(str(i) for i in self.cols))
        for i, row in enumerate(self.rows):
            print(f"{row} ", end="")
            for j in range(10):
                cell = self.underwater_layer[i][j]
                if cell == 0:
                    print("· ", end="")
                elif cell == 1:
                    print("S " if show_ships else "· ", end="")
                elif cell == 2:
                    print("X ", end="")
                elif cell == 3:
                    print("O ", end="")
            print()

class Ship:
    def __init__(self, name, length):
        self.name = name
        self.length = length
        self.positions = []  # List of (row, col, depth) tuples
        self.hits = 0
    
    def is_sunk(self):
        """Check if the ship is sunk."""
        return self.hits == self.length
    
    def register_hit(self):
        """Register a hit on the ship."""
        self.hits += 1
        return self.is_sunk()


class Submarine(Ship):
    def __init__(self):
        super().__init__("Submarine", 3)
        # Submarine can be placed on both layers


class Carrier(Ship):
    def __init__(self):
        super().__init__("Carrier", 4)
        # Carrier can only be placed on the surface layer


class Player:
    def __init__(self, is_computer=False):
        self.board = Board()
        self.ships = [Submarine(), Carrier()]
        self.is_computer = is_computer
        self.opponent_board = Board()  # To track attacks
        self.name = "Computer" if is_computer else "Player"
    
    def place_ships(self):
        """Place ships on the board."""
        if self.is_computer:
            self._place_ships_computer()
        else:
            self._place_ships_user()
    
    def _place_ships_user(self):
        """Let the user place their ships."""
        self.board.display(show_ships=True)
        
        for ship in self.ships:
            placed = False
            while not placed:
                print(f"\nPlacing {ship.name} ({ship.length} units long)")
                try:
                    coord_input = input("Enter starting coordinates (e.g., A,4,1 for row A, column 4, depth 1): ")
                    row, col, depth = coord_input.split(",")
                    row = row.strip().upper()
                    col = int(col.strip())
                    depth = int(depth.strip())
                    
                    if not self.board.is_valid_coordinate(row, col, depth):
                        print("Invalid coordinates. Row must be A-J, column 1-10, depth 0-1.")
                        continue
                    
                    if ship.name == "Carrier" and depth == 0:
                        print("Carrier can only be placed on the surface layer (depth = 1).")
                        continue
                    
                    orientation = input("Enter orientation (h for horizontal, v for vertical): ").strip().lower()
                    orientation = "horizontal" if orientation == "h" else "vertical"
                    
                    placed = self.board.place_ship(ship, row, col, depth, orientation)
                    if not placed:
                        print("Cannot place ship there. Check for overlaps or out-of-bounds.")
                except (ValueError, IndexError):
                    print("Invalid input format. Please use format: A,4,1")
            
            self.board.display(show_ships=True)
    
    def _place_ships_computer(self):
        """Randomly place computer ships."""
        for ship in self.ships:
            placed = False
            while not placed:
                row = random.choice(self.board.rows)
                col = random.randint(1, 10)
                depth = 1 if ship.name == "Carrier" else random.choice([0, 1])
                orientation = random.choice(["horizontal", "vertical"])
                
                placed = self.board.place_ship(ship, row, col, depth, orientation)
    
    def make_move(self, opponent):
        """Make a move against the opponent."""
        if self.is_computer:
            return self._make_move_computer(opponent)
        else:
            return self._make_move_user(opponent)
    
    def _make_move_user(self, opponent):
        """Let the user make a move."""
        valid_move = False
        while not valid_move:
            try:
                coord_input = input("\nEnter attack coordinates (e.g., A,4,1): ")
                row, col, depth = coord_input.split(",")
                row = row.strip().upper()
                col = int(col.strip())
                depth = int(depth.strip())
                
                if not self.board.is_valid_coordinate(row, col, depth):
                    print("Invalid coordinates. Row must be A-J, column 1-10, depth 0-1.")
                    continue
                
                # Make the attack
                result = opponent.board.attack(row, col, depth)
                
                if result == "redundant":
                    print("You already attacked this position. Try again.")
                    continue
                
                valid_move = True
                
                # Update opponent_board to track attacks
                row_idx = self.board.rows.index(row)
                col_idx = col - 1
                layer = self.opponent_board.get_layer(depth)
                layer[row_idx][col_idx] = 2 if result == "hit" else 3
                
                # Check if a ship was hit and potentially sunk
                if result == "hit":
                    print("HIT!")
                    for ship in opponent.ships:
                        if (row_idx, col_idx, depth) in ship.positions:
                            sunk = ship.register_hit()
                            if sunk:
                                print(f"You sunk the opponent's {ship.name}!")
                else:
                    print("MISS!")
                
                # Display the opponent's board (from player's perspective)
                self.opponent_board.display(show_ships=False)
                
            except (ValueError, IndexError):
                print("Invalid input format. Please use format: A,4,1")
        
        return True
    
    def _make_move_computer(self, opponent):
        """Computer makes a random move."""
        valid_move = False
        while not valid_move:
            row = random.choice(self.board.rows)
            col = random.randint(1, 10)
            depth = random.randint(0, 1)
            
            # Make the attack
            result = opponent.board.attack(row, col, depth)
            
            if result == "redundant":
                continue
            
            valid_move = True
            
            # Check if a ship was hit and potentially sunk
            row_idx = self.board.rows.index(row)
            col_idx = col - 1
            
            print(f"\nComputer attacks {row},{col},{depth}")
            
            if result == "hit":
                print("Computer HIT your ship!")
                for ship in opponent.ships:
                    if (row_idx, col_idx, depth) in ship.positions:
                        sunk = ship.register_hit()
                        if sunk:
                            print(f"Computer sunk your {ship.name}!")
            else:
                print("Computer MISSED!")
            
            # Give the player time to see the computer's move
            time.sleep(1)
        
        return True
    
    def all_ships_sunk(self):
        """Check if all ships are sunk."""
        return all(ship.is_sunk() for ship in self.ships)


def display_welcome():
    """Display welcome message and game instructions."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("====================================")
    print("   WELCOME TO BATTLESHIP GAME!")
    print("====================================")
    print("\nGame Rules:")
    print("1. The game board is a 10x10 grid with two layers: surface (depth=1) and underwater (depth=0).")
    print("2. Rows are labeled A-J, and columns are numbered 1-10.")
    print("3. You have two ships: a Submarine (3 units) and a Carrier (4 units).")
    print("4. The Submarine can be placed on both layers, while the Carrier can only be on the surface.")
    print("5. Ships can be placed horizontally or vertically.")
    print("6. Take turns with the computer to attack coordinates.")
    print("7. The first to sink all opponent's ships wins!")
    print("\nCoordinate Format: A,4,1 (Row A, Column 4, Depth 1)")
    print("\nBoard Symbols:")
    print("· = Empty space")
    print("S = Your ship (only visible on your board)")
    print("X = Hit")
    print("O = Miss")
    print("\nPress Enter to start the game...")
    input()


def play_game():
    """Main game function."""
    display_welcome()
    
    # Create players
    player = Player(is_computer=False)
    computer = Player(is_computer=True)
    
    # Place ships
    print("\nPlace your ships:")
    player.place_ships()
    
    print("\nComputer is placing its ships...")
    computer.place_ships()
    time.sleep(1)
    
    # Game loop
    current_player = player  # Player goes first
    opponent = computer
    
    while True:
        if current_player.is_computer:
            print("\nComputer's turn:")
        else:
            print("\nYour turn:")
            # Show player's board with their ships
            player.board.display(show_ships=True)
        
        # Make move
        current_player.make_move(opponent)
        
        # Check for win condition
        if opponent.all_ships_sunk():
            winner = current_player.name
            break
        
        # Switch players
        current_player, opponent = opponent, current_player
    
    # Game over
    print(f"\n{winner} wins the game!")
    if winner == "Player":
        print("Congratulations! You've sunk all the computer's ships!")
    else:
        print("The computer has sunk all your ships. Better luck next time!")
    
    # Ask to play again
    play_again = input("\nDo you want to play again? (y/n): ").strip().lower()
    if play_again == 'y':
        play_game()
    else:
        print("Thanks for playing! Goodbye!")


if __name__ == "__main__":
    play_game()