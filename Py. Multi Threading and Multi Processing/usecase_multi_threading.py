# ================= REAL-WORLD MULTITHREADING EXAMPLE =================
# Scenario: Web Scraping (I/O-bound task)

# ---------------- WHY MULTITHREADING HERE ----------------
# Web scraping involves sending requests to websites and waiting
# for responses. This waiting time makes it an I/O-bound task.
#
# Multithreading helps by:
# ✔ Fetching multiple web pages at the same time
# ✔ Reducing total waiting time
# ✔ Improving performance

# ------------------------------------------------------------

# Import threading module → used to create multiple threads
import threading

# Import requests → used to send HTTP requests to websites
import requests

# Import BeautifulSoup → used to parse HTML content
from bs4 import BeautifulSoup


# ---------------- URL LIST ----------------
# List of websites to scrape
urls = [
    'https://www.langchain.com/langsmith/observability',
    'https://www.langchain.com/blog',
    'https://www.langchain.com/langsmith/deployment'
]

# ---------------- FUNCTION ----------------
# Function to fetch content from a given URL
def fetch_content(url):
    
    # Send HTTP GET request to the URL
    response = requests.get(url)
    
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Print length of extracted text
    print(f'Fetched {len(soup.text)} characters from {url}')


# ---------------- THREAD LIST ----------------
# This list will store all thread objects
threads = []


# ---------------- CREATE & START THREADS ----------------
# Loop through each URL
for url in urls:
    
    # Create a thread
    # target=fetch_content → function to execute
    # args=(url,) → pass URL as argument (tuple required)
    thread = threading.Thread(target=fetch_content, args=(url,))
    
    # Store thread in list
    threads.append(thread)
    
    # Start thread → begins execution immediately
    thread.start()


# ---------------- WAIT FOR ALL THREADS ----------------
# Ensure main program waits until all threads finish
for thread in threads:
    thread.join()


# ---------------- FINAL MESSAGE ----------------
# This runs only after all threads complete
print("All web pages fetched")