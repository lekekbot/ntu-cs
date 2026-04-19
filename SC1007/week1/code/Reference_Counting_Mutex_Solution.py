import threading
import time
import random

# Shared resource
shared_counter = 0
expected_count = 0  # To track expected increments
mutex = threading.Lock()  # Create a mutex lock

def increment_counter(thread_name):
    global shared_counter, expected_count
    
    for i in range(5):  # Reduced iterations to make it clearer
        # Acquire lock before critical section
        mutex.acquire()  # Lock to prevent other threads from accessing
        try:
            # Read
            local_counter = shared_counter
            print(f"{thread_name} reads: {local_counter}")
            
            # Simulate some processing time
            time.sleep(0.1)
            
            # Increment
            local_counter += 1
            print(f"{thread_name} increments to: {local_counter}")
            
            # Simulate more processing time
            time.sleep(0.1)
            
            # Write back
            shared_counter = local_counter
            print(f"{thread_name} writes back: {shared_counter}")
            print("-" * 50)
            
            expected_count += 1
        finally:
            mutex.release()  # Always release the lock, even if an error occurs
            time.sleep(0.1)  # Give other thread a chance to acquire lock

# Create two threads
thread1 = threading.Thread(target=increment_counter, args=("Thread-1",))
thread2 = threading.Thread(target=increment_counter, args=("Thread-2",))

start_time = time.time()

# Start threads
thread1.start()
thread2.start()

# Wait for threads to complete
thread1.join()
thread2.join()

end_time = time.time()

print(f"\nExpected final count: {expected_count}")
print(f"Actual final count: {shared_counter}")
print(f"Lost updates: {expected_count - shared_counter}")
print(f"Time taken: {end_time - start_time:.2f} seconds")