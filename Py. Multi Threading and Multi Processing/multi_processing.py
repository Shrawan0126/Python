# ================= MULTIPROCESSING EXAMPLE =================
# This program demonstrates how to use multiprocessing in Python
# to run multiple tasks in parallel using separate processes.

# ---------------- WHEN TO USE MULTIPROCESSING ----------------
# 1. CPU-bound tasks:
#    Tasks that require heavy computation (e.g., calculations, data processing)
#
# 2. Parallel execution:
#    When you want to use multiple CPU cores to improve performance

# ------------------------------------------------------------

# Import multiprocessing module → used to create and manage processes
import multiprocessing  

# Import time module → used for delays and measuring execution time
import time


# ---------------- FUNCTION 1 ----------------
# This function calculates and prints squares of numbers
def square_number():
    # Loop runs 5 times (0 to 4)
    for i in range(5):
        
        # Simulate delay (represents computation or waiting)
        time.sleep(1)
        
        # Print square of the number
        print(f"Square: {i*i}")


# ---------------- FUNCTION 2 ----------------
# This function calculates and prints cubes of numbers
def cube_number():
    # Loop runs 5 times (0 to 4)
    for i in range(5):
        
        # Simulate delay
        time.sleep(1)
        
        # Print cube of the number
        print(f"Cube: {i*i*i}")


# ---------------- MAIN BLOCK ----------------
# IMPORTANT:
# This condition ensures that the code inside runs only when
# the script is executed directly (not when imported)
#
# This is REQUIRED in multiprocessing (especially on Windows/macOS)
# to prevent infinite process creation.
if __name__ == "__main__":

    # ---------------- PROCESS CREATION ----------------
    # Create process p1 to run square_number()
    p1 = multiprocessing.Process(target=square_number)

    # Create process p2 to run cube_number()
    p2 = multiprocessing.Process(target=cube_number)

    # NOTE:
    # Processes are created but NOT started yet


    # ---------------- START TIMER ----------------
    # Record start time to measure performance
    t = time.time()


    # ---------------- START PROCESSES ----------------
    # Start process p1 → runs square_number() in a separate process
    p1.start()

    # Start process p2 → runs cube_number() in another separate process
    p2.start()

    # IMPORTANT:
    # These processes run in TRUE PARALLEL (on multiple CPU cores if available)


    # ---------------- WAIT FOR PROCESSES ----------------
    # Wait until p1 completes execution
    p1.join()

    # Wait until p2 completes execution
    p2.join()

    # Without join():
    # Main program may finish before child processes complete


    # ---------------- CALCULATE TOTAL TIME ----------------
    finished_time = time.time() - t


    # ---------------- PRINT RESULT ----------------
    print(f"Total Time Taken: {finished_time}")


# ================= IMPORTANT UNDERSTANDING =================
# Each function takes approximately:
#   5 iterations × 1 second = ~5 seconds
#
# Without multiprocessing (sequential execution):
#   Total time ≈ 10 seconds
#
# With multiprocessing (parallel execution):
#   Total time ≈ ~5 seconds
#
# This shows performance improvement using multiple CPU cores.


# ================= EXTRA NOTES =================
# 1. Each process has its OWN memory space
#    → No shared memory by default
#
# 2. No GIL limitation:
#    → True parallel execution is possible
#
# 3. Best for CPU-heavy tasks
#
# 4. Slightly heavier than threads:
#    → More memory usage
#    → Higher overhead