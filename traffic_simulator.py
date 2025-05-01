import requests
import random
import time
from fake_useragent import UserAgent
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize fake user agent generator
ua = UserAgent()

# List of sample referers to simulate different traffic sources
REFERERS = [
    "https://www.google.com",
    "https://www.bing.com",
    "https://www.yahoo.com",
    "https://www.facebook.com",
    "https://www.twitter.com"
]

def simulate_visit(url):
    try:
        # Generate random user agent
        user_agent = ua.random
        
        # Generate random headers
        headers = {
            "User-Agent": user_agent,
            "Referer": random.choice(REFERERS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive"
        }

        # Simulate IP spoofing with X-Forwarded-For (note: this doesn't change actual IP)
        headers["X-Forwarded-For"] = f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

        # Send GET request
        response = requests.get(url, headers=headers, timeout=5)
        
        # Log the result
        logging.info(f"Visit sent - Status: {response.status_code}, User-Agent: {user_agent}")
        
        return response.status_code
    except Exception as e:
        logging.error(f"Error during visit: {str(e)}")
        return None

def main():
    # Prompt for website URL
    url = input("Please enter the website URL to test: ").strip()
    
    # Validate URL
    if not url.startswith("http"):
        logging.error("Invalid URL. Please include http:// or https://")
        return
    
    # Number of visits to simulate (adjust for testing, e.g., 100 for demo)
    num_visits = 100
    delay = 1  # Delay between visits in seconds to avoid overwhelming the server

    logging.info(f"Starting simulation of {num_visits} visits to {url}")
    
    for i in range(num_visits):
        status = simulate_visit(url)
        if status:
            logging.info(f"Visit {i+1}/{num_visits} completed with status {status}")
        else:
            logging.warning(f"Visit {i+1}/{num_visits} failed")
        
        # Random delay to mimic human behavior
        time.sleep(random.uniform(delay, delay + 0.5))
    
    logging.info("Simulation completed")

if __name__ == "__main__":
    main()
