# ================= THREADPOOL EXECUTOR EXAMPLE =================
# This program demonstrates multithreading using ThreadPoolExecutor
# which is a higher-level and easier way to manage threads.

# ---------------- WHY USE THREADPOOL EXECUTOR ----------------
# 1. Automatically manages thread creation and destruction
# 2. Reuses threads (thread pooling) → more efficient
# 3. Cleaner and simpler code compared to manual threading

# ------------------------------------------------------------

# Import ThreadPoolExecutor → used for managing a pool of threads
from concurrent.futures import ThreadPoolExecutor

# Import time module → used to simulate delay
import time


# ---------------- FUNCTION ----------------
# This function will be executed by multiple threads
# It takes a number as input
def print_numbers(number):
    
    # Loop runs 5 times
    for i in range(5):
        
        # Simulate I/O delay (like API call or file read)
        time.sleep(1)
        
        # Print the given number
        # NOTE: Each thread will print its assigned number
        print(f"Number: {number}")
    
    # Function does NOT return anything → returns None by default


# ---------------- INPUT DATA ----------------
# A set of numbers to process
numbers = {1, 2, 3, 4, 5}

# NOTE:
# Each number will be passed to the function separately


# ---------------- THREAD POOL ----------------
# Create a pool of threads using "with" context manager
# max_workers=3 → at most 3 threads will run at the same time
with ThreadPoolExecutor(max_workers=3) as executor:
    
    # executor.map() works like Python's map()
    # It applies the function to each element in "numbers"
    #
    # Internally:
    # - It assigns tasks to available threads
    # - Runs them concurrently
    # - Reuses threads efficiently
    #
    # Example:
    # Thread 1 → number 1
    # Thread 2 → number 2
    # Thread 3 → number 3
    # Then threads are reused for 4, 5
    
    results = executor.map(print_numbers, numbers)


# ---------------- RESULTS HANDLING ----------------
# executor.map() returns an iterator of results
# Since print_numbers() returns nothing,
# each result will be None

for result in results:
    print(result)   # This will print "None" for each item


# ================= IMPORTANT UNDERSTANDING =================
# Total tasks = 5 numbers
# Threads available = 3
#
# Execution happens in batches:
# First batch → 3 tasks run
# Second batch → remaining 2 tasks run
#
# Each task takes ≈ 5 seconds (5 × 1 sec)
#
# So total time ≈ 10 seconds (instead of 25 seconds sequentially)


# ================= EXTRA NOTES =================
# 1. ThreadPoolExecutor is part of concurrent.futures module
#
# 2. Best for:
#    ✔ I/O-bound tasks (like threading)
#
# 3. It simplifies:
#    - Thread creation
#    - Task assignment
#    - Resource management
#
# 4. Avoids manual handling of:
#    - start()
#    - join()