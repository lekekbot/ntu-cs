import threading
import time
import random  # To add random delays

# Shared resource
shared_counter = 0
expected_count = 0  # Track the total expected increments

# Function that increments the shared counter
def increment_counter(thread_name):
    global shared_counter, expected_count
    for _ in range(5):
        # Read the current value
        temp = shared_counter
        print(f"{thread_name} reads: {temp}")
        
        # Simulate processing time
        time.sleep(random.uniform(0.0001, 0.001))
        
        # Increment the value
        temp += 1
        print(f"{thread_name} increments to: {temp}")
        
        # Simulate processing time
        time.sleep(random.uniform(0.0001, 0.001))
        
        # Write the updated value back
        shared_counter = temp
        print(f"{thread_name} writes back: {shared_counter}")
        
        # Track the total expected increments
        expected_count += 1

# Create two threads with names for logging
thread1 = threading.Thread(target=increment_counter, args=("Thread-1",))
thread2 = threading.Thread(target=increment_counter, args=("Thread-2",))

# Start the threads
thread1.start()
thread2.start()

# Wait for both threads to finish
thread1.join()
thread2.join()

# Print results
print(f"\nExpected final count: {expected_count}")
print(f"Actual final count: {shared_counter}")
print(f"Lost updates: {expected_count - shared_counter}")