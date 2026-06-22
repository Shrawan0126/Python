# ================= MULTITHREADING EXAMPLE =================
# This program demonstrates how to use multithreading in Python
# to run multiple tasks concurrently (at the same time).

# ---------------- WHEN TO USE MULTITHREADING ----------------
# 1. I/O-bound tasks:
#    Tasks that spend most of their time waiting (e.g., file reading,
#    network requests, database calls, sleep delays, etc.)
#
# 2. Concurrent execution:
#    When you want to improve performance by doing multiple tasks together
#    instead of one after another.

# ------------------------------------------------------------

# Import threading module → used to create and manage threads
import threading  

# Import time module → used for delays and measuring execution time
import time


# ---------------- FUNCTION 1 ----------------
# This function prints numbers from 0 to 4
def print_number():
    # Loop runs 5 times (0,1,2,3,4)
    for i in range(5):
        
        # Simulate an I/O delay (like waiting for a file or API response)
        # The thread will "sleep" for 2 seconds
        time.sleep(2)
        
        # Print the current number
        print(f"Number:{i}")


# ---------------- FUNCTION 2 ----------------
# This function prints letters from 'a' to 'd'
def print_letter():
    # Loop through each character in the string "abcd"
    for letter in "abcd":
        
        # Again simulate an I/O delay of 2 seconds
        time.sleep(2)
        
        # Print the current letter
        print(f"Letter: {letter}")


# ---------------- THREAD CREATION ----------------
# Create thread t1
# target=print_number means this thread will execute print_number() function
t1 = threading.Thread(target=print_number)

# Create thread t2
# target=print_letter means this thread will execute print_letter() function
t2 = threading.Thread(target=print_letter)

# NOTE:
# At this point, threads are CREATED but NOT STARTED yet.


# ---------------- START TIMER ----------------
# Store the current time before starting threads
# This helps us measure total execution time
t = time.time()


# ---------------- START THREADS ----------------
# Start thread t1 → begins execution of print_number()
t1.start()

# Start thread t2 → begins execution of print_letter()
t2.start()

# IMPORTANT:
# Both threads now run CONCURRENTLY (in parallel-like behavior)
# Output will be mixed/interleaved (not strictly ordered)


# ---------------- WAIT FOR THREADS ----------------
# join() ensures that the main program waits until t1 finishes
t1.join()

# join() ensures that the main program waits until t2 finishes
t2.join()

# Without join():
# The main program may finish early before threads complete execution


# ---------------- CALCULATE TOTAL TIME ----------------
# Get total execution time by subtracting start time from current time
finished_time = time.time() - t


# ---------------- PRINT RESULT ----------------
# Print how long the program took to execute
print(f"Total Time Taken: {finished_time}")


# ================= IMPORTANT UNDERSTANDING =================
# Each function takes approximately:
#   5 iterations × 2 seconds = ~10 seconds
#
# If executed WITHOUT threading (sequentially):
#   Total time ≈ 20 seconds
#
# With threading (concurrent execution):
#   Total time ≈ 10 seconds
#
# This shows performance improvement for I/O-bound tasks.


# ================= EXTRA NOTES =================
# 1. Python has something called GIL (Global Interpreter Lock)
#    → It prevents true parallel execution for CPU-heavy tasks
#
# 2. Multithreading is BEST for:
#    ✔ I/O-bound tasks (waiting operations)
#
# 3. Multithreading is NOT ideal for:
#    ✖ CPU-bound tasks (heavy computations)
#
# 4. For CPU-bound tasks, use:
#    → multiprocessing module instead