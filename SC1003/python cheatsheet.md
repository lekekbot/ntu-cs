# Python Cheatsheet

## Data Types

### Basic Data Types
```python
# Integer
x = 10
y = -5

# Float
pi = 3.14
temp = -40.5

# String
name = "Alice"
message = 'Hello World'
multiline = """This is a
multiline string"""

# Boolean
is_valid = True
is_empty = False

# None
result = None
```

### Collection Data Types
```python
# List (mutable, ordered)
fruits = ["apple", "banana", "cherry"]
numbers = [1, 2, 3, 4, 5]
mixed = [1, "two", 3.0, True]

# Tuple (immutable, ordered)
coordinates = (10, 20)
rgb = (255, 128, 0)

# Dictionary (mutable, key-value pairs)
person = {"name": "Alice", "age": 25, "city": "NYC"}
scores = {"math": 95, "science": 88}

# Set (mutable, unordered, unique elements)
unique_nums = {1, 2, 3, 4, 5}
letters = {"a", "b", "c"}
```

## Reserved Keywords & Built-in Names

### Keywords (Cannot be used as variable names)
```python
False      await      else       import     pass
None       break      except     in         raise
True       class      finally    is         return
and        continue   for        lambda     try
as         def        from       nonlocal   while
assert     del        global     not        with
async      elif       if         or         yield
```

### Important Built-in Functions (Avoid overwriting these)
```python
# Common functions to avoid using as variable names
range      # Generate sequence of numbers
len        # Get length
print      # Output to console
input      # Get user input
int        # Integer type/conversion
float      # Float type/conversion
str        # String type/conversion
list       # List type/conversion
dict       # Dictionary type/conversion
set        # Set type/conversion
tuple      # Tuple type/conversion
bool       # Boolean type/conversion
type       # Get object type
open       # Open files
sum        # Sum of iterable
max        # Maximum value
min        # Minimum value
abs        # Absolute value
round      # Round numbers
sorted     # Return sorted list
enumerate  # Add index to iterable
zip        # Combine iterables
map        # Apply function to iterable
filter     # Filter iterable
all        # Check if all true
any        # Check if any true
```

## Operators

### Arithmetic Operators
```python
+    # Addition: 5 + 3 = 8
-    # Subtraction: 5 - 3 = 2
*    # Multiplication: 5 * 3 = 15
/    # Division: 5 / 2 = 2.5
//   # Floor Division: 5 // 2 = 2
%    # Modulus: 5 % 2 = 1
**   # Exponentiation: 5 ** 2 = 25
```

### Comparison Operators
```python
==   # Equal to
!=   # Not equal to
>    # Greater than
<    # Less than
>=   # Greater than or equal to
<=   # Less than or equal to
```

### Logical Operators
```python
and  # Logical AND
or   # Logical OR
not  # Logical NOT
```

### Assignment Operators
```python
=    # Assignment
+=   # Add and assign: x += 5
-=   # Subtract and assign
*=   # Multiply and assign
/=   # Divide and assign
//=  # Floor divide and assign
%=   # Modulus and assign
**=  # Exponent and assign
```

## Built-in Functions

### Common Built-in Functions
```python
# Type Conversion
int()      # Convert to integer
float()    # Convert to float
str()      # Convert to string
bool()     # Convert to boolean
list()     # Convert to list
tuple()    # Convert to tuple
dict()     # Convert to dictionary
set()      # Convert to set

# Input/Output
print()    # Print to console
input()    # Get user input

# Math Functions
abs()      # Absolute value
round()    # Round a number
max()      # Maximum value
min()      # Minimum value
sum()      # Sum of iterable
pow()      # Power function

# Sequence Functions
len()      # Length of sequence
range()    # Generate range of numbers
sorted()   # Return sorted list
reversed() # Reverse iterator
enumerate()# Add counter to iterable
zip()      # Combine iterables

# Type Checking
type()     # Get type of object
isinstance() # Check if instance of class

# Other Useful Functions
help()     # Get help documentation
dir()      # List object attributes
id()       # Get object identity
```

## Control Flow

### If-Elif-Else
```python
if condition:
    # code block
elif another_condition:
    # code block
else:
    # code block
```

### Loops
```python
# For loop
for item in iterable:
    # code block

# While loop
while condition:
    # code block

# Loop control
break      # Exit loop
continue   # Skip to next iteration
pass       # Do nothing (placeholder)
```

## Functions

### Function Definition
```python
# Basic function
def greet():
    print("Hello!")

# Function with parameters
def add(a, b):
    return a + b

# Function with default parameters
def greet_user(name="Guest"):
    print(f"Hello, {name}!")

# Function with arbitrary arguments
def sum_all(*args):
    return sum(args)

# Function with keyword arguments
def describe_pet(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

# Lambda function
square = lambda x: x ** 2
```

## String Methods

```python
str.upper()       # Convert to uppercase
str.lower()       # Convert to lowercase
str.strip()       # Remove whitespace
str.split()       # Split into list
str.join()        # Join list into string
str.replace()     # Replace substring
str.find()        # Find substring index
str.startswith()  # Check if starts with
str.endswith()    # Check if ends with
str.isdigit()     # Check if all digits
str.isalpha()     # Check if all letters
```

## List Methods

```python
list.append()     # Add item to end
list.insert()     # Insert at index
list.remove()     # Remove first occurrence
list.pop()        # Remove and return item
list.clear()      # Remove all items
list.index()      # Find index of item
list.count()      # Count occurrences
list.sort()       # Sort in place
list.reverse()    # Reverse in place
list.copy()       # Create shallow copy
```

## Dictionary Methods

```python
dict.keys()       # Get all keys
dict.values()     # Get all values
dict.items()      # Get key-value pairs
dict.get()        # Get value by key
dict.pop()        # Remove and return value
dict.update()     # Update with another dict
dict.clear()      # Remove all items
```

## File Operations

```python
# Reading a file
with open('file.txt', 'r') as f:
    content = f.read()

# Writing to a file
with open('file.txt', 'w') as f:
    f.write('Hello World')

# Appending to a file
with open('file.txt', 'a') as f:
    f.write('New line')

# Reading lines
with open('file.txt', 'r') as f:
    lines = f.readlines()
```

## Exception Handling

```python
try:
    # code that might raise an exception
    result = 10 / 0
except ZeroDivisionError:
    # handle specific exception
    print("Cannot divide by zero")
except Exception as e:
    # handle any exception
    print(f"Error: {e}")
else:
    # runs if no exception
    print("Success")
finally:
    # always runs
    print("Cleanup")
```

## List Comprehensions

```python
# Basic list comprehension
squares = [x**2 for x in range(10)]

# With condition
evens = [x for x in range(10) if x % 2 == 0]

# Dictionary comprehension
square_dict = {x: x**2 for x in range(5)}

# Set comprehension
unique_squares = {x**2 for x in range(-5, 6)}
```

## Common Patterns

### String Formatting
```python
# f-strings (Python 3.6+)
name = "Alice"
age = 25
print(f"My name is {name} and I'm {age}")

# format() method
print("My name is {} and I'm {}".format(name, age))

# % formatting
print("My name is %s and I'm %d" % (name, age))
```

### Unpacking
```python
# Tuple unpacking
x, y = (10, 20)

# List unpacking
first, *rest = [1, 2, 3, 4, 5]

# Dictionary unpacking
person = {"name": "Alice", "age": 25}
print(**person)
```

### Ternary Operator
```python
result = "Even" if num % 2 == 0 else "Odd"
```