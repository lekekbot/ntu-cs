import gc
import time

# ================ Generation 0 (Young/Temporary Objects) ================
print("\nGeneration 0 - Young/Temporary Objects:")
temp_result = 10 + 20        # Temporary calculation
print(f"Temporary result: {temp_result}")  # Use
print(f"Garbage count before deletion: {gc.get_count()}")  
# Shows (gen0=high, gen1=low, gen2=low) as temp calculation created

del temp_result              # Object becomes eligible for collection
print(f"Garbage count after deletion: {gc.get_count()}")  
# Shows slightly lower gen0 count as temp_result was collected

# ================ Generation 1 (Middle-Aged Objects) ================
print("\nGeneration 1 - Middle-Aged Objects:")
# Score tracking survives multiple updates
game_scores = 0
score_history = []

for round in range(3):
   new_score = 10 * (round + 1)    # Calculate round score
   game_scores += new_score        # Update total
   score_history.append(new_score) # Keep track of history
   print(f"Round {round + 1} score: {new_score}")
   print(f"Total score: {game_scores}")
   print(f"Score history: {score_history}")
   print(f"Garbage count after round: {gc.get_count()}")  
   # First round: (gen0=~386, gen1=~6, gen2=~2) - Initial objects created
   # Second round: (gen0=~370, gen1=~6, gen2=~2) - Some gen0 objects collected
   # Third round: (gen0=~370, gen1=~6, gen2=~2) - Stabilized counts
   time.sleep(0.1)  # Simulate game round time

# ================ Generation 2 (Old Objects/Circular References) ================
print("\nGeneration 2 - Circular References:")
# Create circular reference
list1 = []
list2 = []
list1.append(list2)    # list1 references list2
list2.append(list1)    # list2 references list1

print("Circular reference created:")
print(f"list1 contains: {list1}")
print(f"list2 contains: {list2}")
print(f"Garbage count with circular reference: {gc.get_count()}")
# Shows (gen0=~370, gen1=~3, gen2=0) - Circular reference just created

# Break reference and collect
del list1
del list2
gc.collect()  # Final cleanup - forces garbage collection of all generations
print(f"Final garbage count: {gc.get_count()}")
# Shows (gen0=~33, gen1=0, gen2=0)
# - 33 objects in gen0 are Python internal objects
# - gen1 and gen2 are empty as all objects were collected