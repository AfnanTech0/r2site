import requests
import random
import time
from fake_useragent import UserAgent
import logging
from urllib.parse import urlparse

# Setup detailed logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize fake user agent generator
ua = UserAgent()

# Expanded list of referers to simulate diverse traffic sources
REFERERS = [
    "https://www.google.com/search?q=test",
    "https://www.bing.com/search?q=test",
    "https://www.yahoo.com",
    "https://www.facebook.com",
    "https://www.twitter.com",
    "https://www.linkedin.com",
    "https://www.reddit.com",
    "https://www.instagram.com"
]

# Common browser accept headers for realism
ACCEPT_HEADERS = [
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
]

def simulate_visit(url, session):
    try:
        # Generate random user agent
        user_agent = ua.random

        # Randomize headers to mimic real browsers
        headers = {
            "User-Agent": user_agent,
            "Referer": random.choice(REFERERS),
            "Accept": random.choice(ACCEPT_HEADERS),
            "Accept-Language": random.choice(["en-US,en;q=0.9", "en-GB,en;q=0.8", "fr-FR,fr;q=0.9", "de-DE,de;q=0.8"]),
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0"
        }

        # Simulate IP spoofing with X-Forwarded-For
        headers["X-Forwarded-For"] = f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

        # Log headers for debugging
        logging.debug(f"Request headers: {headers}")

        # Send GET request using session for cookie persistence
        response = session.get(url, headers=headers, timeout=10, allow_redirects=True)

        # Log response details
        logging.info(f"Visit sent - Status: {response.status_code}, URL: {response.url}")
        logging.debug(f"Response headers: {response.headers}")

        # Check for common anti-bot indicators
        if "cf-ray" in response.headers or "cloudflare" in response.text.lower():
            logging.warning("Cloudflare protection detected")
        if response.status_code == 403:
            logging.warning("403 Forbidden - Possible anti-bot or IP block")
        elif response.status_code == 429:
            logging.warning("429 Too Many Requests - Rate limiting detected")

        return response.status_code
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {str(e)}")
        return None

def main():
    # Prompt for website URL
    url = input("Please enter the website URL to test: ").strip()

    # Validate URL
    if not url.startswith(("http://", "https://")):
        logging.error("Invalid URL. Please include http:// or https://")
        return

    # Prompt for number of visits
    try:
        num_visits_input = input("Please enter the number of visits to simulate (default 1000): ").strip()
        num_visits = int(num_visits_input) if num_visits_input else 1000
        if num_visits <= 0:
            logging.error("Number of visits must be positive")
            return
        if num_visits > 10000:
            logging.warning("High visit counts (>10,000) may overload your server, trigger anti-bot protections, or violate hosting terms. Proceed with caution.")
    except ValueError:
        logging.error("Invalid input. Please enter a number")
        return

    # Extract domain for logging
    domain = urlparse(url).netloc
    logging.info(f"Testing website: {domain} with {num_visits} visits")

    # Minimum and maximum delay between visits
    min_delay = 1
    max_delay = 3

    # Create a session to persist cookies and mimic a real browser
    session = requests.Session()

    logging.info(f"Starting simulation of {num_visits} visits to {url}")

    for i in range(num_visits):
        status = simulate_visit(url, session)
        if status:
            logging.info(f"Visit {i+1}/{num_visits} completed with status {status}")
        else:
            logging.warning(f"Visit {i+1}/{num_visits} failed")

        # Random delay to mimic human behavior
        time.sleep(random.uniform(min_delay, max_delay))

    logging.info("Simulation completed")
    session.close()

if __name__ == "__main__":
    main()
