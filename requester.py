import requests
import time
from urllib.parse import urlparse

def connector(url, proxy=None, retries=3):
    """
    Connect to a URL and retry on failure.
    :param url: URL to connect to.
    :param proxy: Optional proxy setting.
    :param retries: Number of retries on failure.
    :return: Response content or False if failed.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for _ in range(retries):
        try:
            if proxy:
                response = requests.get(url, headers=headers, proxies={"http": proxy, "https": proxy}, timeout=10)
            else:
                response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                return response.text, False
            else:
                print(f"Failed to retrieve {url}. Status Code: {response.status_code}")
                time.sleep(2)
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            time.sleep(2)
    
    return False, True
