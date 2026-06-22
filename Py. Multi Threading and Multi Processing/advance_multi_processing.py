# ================= PROCESSPOOL EXECUTOR EXAMPLE =================
# This program demonstrates multiprocessing using ProcessPoolExecutor
# which is a high-level way to manage multiple processes.

# ---------------- WHY USE PROCESSPOOL EXECUTOR ----------------
# 1. Automatically manages process creation and destruction
# 2. Uses multiple CPU cores for true parallel execution
# 3. Easier and cleaner than manual multiprocessing
# 4. Best for CPU-bound tasks

# ------------------------------------------------------------

# Import ProcessPoolExecutor → used for managing a pool of processes
from concurrent.futures import ProcessPoolExecutor

# Import time module → used to simulate delay
import time 


# ---------------- FUNCTION ----------------
# This function calculates the square of a number
# It will be executed in separate processes
def square_number(number):
    
    # Simulate heavy computation or delay
    time.sleep(5)
    
    # Return the square result
    # NOTE: Unlike threading example, this function RETURNS a value
    return f"Square: {number*number}"


# ---------------- INPUT DATA ----------------
# A set of numbers to process
numbers = {1, 2, 3, 4, 5}

# ---------------- MAIN BLOCK ----------------
# IMPORTANT:
# This is REQUIRED for multiprocessing
# Prevents infinite process spawning (especially on Windows/macOS)
if __name__ == "__main__":
    
    # ---------------- PROCESS POOL ----------------
    # Create a pool of processes
    # max_workers=3 → at most 3 processes will run at the same time
    with ProcessPoolExecutor(max_workers=3) as executor:
        
        # executor.map() distributes tasks across processes
        # Each number is passed to square_number()
        #
        # Internally:
        # Process 1 → number 1
        # Process 2 → number 2
        # Process 3 → number 3
        # Then reused for 4, 5
        
        results = executor.map(square_number, numbers)
    
    
    # ---------------- RESULTS HANDLING ----------------
    # results is an iterator that contains returned values
    for result in results:
        print(result)


# ================= IMPORTANT UNDERSTANDING =================
# Total tasks = 5 numbers
# Processes available = 3
#
# Execution happens in batches:
# First batch → 3 tasks run (each takes 5 sec)
# Second batch → 2 tasks run (another 5 sec)
#
# Total time ≈ 10 seconds (instead of 25 seconds sequentially)


# ================= EXTRA NOTES =================
# 1. Each process has its own memory space
#    → No shared memory by default
#
# 2. True parallel execution:
#    → Not affected by Python's GIL
#
# 3. Best for:
#    ✔ CPU-heavy tasks (calculations, ML, data processing)
#
# 4. Heavier than threads:
#    → More memory usage
#    → Higher startup cost