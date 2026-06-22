"""
Real-World Example: Multiprocessing for CPU-bound Tasks
Scenario: Factorial Calculation
Factorial calculations, especially for large numbers, involve significant computational work. 
Multiprocessing can be used to distribute the workload across multiple CPU cores, improving performance.
"""
# ================= REAL-WORLD MULTIPROCESSING EXAMPLE =================
# Scenario: Factorial Calculation (CPU-bound task)
# ---------------- WHY MULTIPROCESSING HERE ----------------
# Factorial of large numbers requires heavy computation.
# This is a CPU-bound task (not waiting, but actively computing).
#
# Multiprocessing helps by:
# ✔ Using multiple CPU cores
# ✔ Running tasks in parallel
# ✔ Reducing total execution time

# ------------------------------------------------------------

# Import multiprocessing → used to create multiple processes
import multiprocessing

# Import math → provides factorial function
import math

# Import sys → used to control system-level settings
import sys

# Import time → used to measure execution time
import time


# ---------------- IMPORTANT SETTING ----------------
# Python has a safety limit for converting very large integers to strings.
# Factorials of large numbers (like 5000!) are HUGE.
#
# This line increases the allowed limit to avoid errors when printing.
sys.set_int_max_str_digits(100000)


# ---------------- FUNCTION ----------------
# Function to compute factorial of a number
def computer_factorial(number):
    
    # Print message when computation starts
    print(f"Computing factorial of {number}")
    
    # Compute factorial using math library
    # This is CPU-intensive for large numbers
    result = math.factorial(number)
    
    # Print result (VERY LARGE NUMBER)
    print(f"Factorial of {number} is {result}")
    
    # Return result
    return result


# ---------------- MAIN BLOCK ----------------
# Required for multiprocessing to prevent infinite process spawning
if __name__ == "__main__":
    
    # List of numbers for which factorial will be computed
    numbers = [5000, 6000, 700, 8000]

    # Record start time
    start_time = time.time()

    
    # ---------------- PROCESS POOL ----------------
    # Create a pool of worker processes
    # By default → uses number of CPU cores available
    
    with multiprocessing.Pool() as pool:
        
        # pool.map() distributes tasks across processes
        # Each number is sent to computer_factorial()
        #
        # Example:
        # Process 1 → factorial(5000)
        # Process 2 → factorial(6000)
        # Process 3 → factorial(700)
        # Process 4 → factorial(8000)
        
        results = pool.map(computer_factorial, numbers)


    # Record end time
    end_time = time.time()


    # ---------------- OUTPUT ----------------
    # Print all results (list of factorial values)
    print(f"Results : {results}")
    
    # Print total execution time
    print(f"Time taken : {end_time - start_time} seconds")


# ================= IMPORTANT UNDERSTANDING =================
# Each factorial computation is CPU-heavy
#
# Without multiprocessing:
#   Tasks run sequentially → very slow
#
# With multiprocessing:
#   Tasks run in parallel on multiple CPU cores → much faster


# ================= EXTRA NOTES =================
# 1. Each process has its own memory
#    → No shared memory by default
#
# 2. Not affected by GIL
#    → True parallel execution
#
# 3. Best for:
#    ✔ Heavy computations (math, ML, data processing)
#
# 4. Overhead:
#    → Creating processes is expensive
#    → Use only when tasks are large enough


# ================= WARNING =================
# Printing very large factorials (like 8000!) can:
# ❗ Slow down your program
# ❗ Flood your console
#
# Better approach:
# Print only length or summary instead of full number
#
# Example:
# len(str(result)) → number of digits