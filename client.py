import requests

def fetch_url_content(url, proxy=None):
    """
    Fetch content from the specified URL with optional proxy.
    :param url: URL to fetch content from.
    :param proxy: Optional proxy setting.
    :return: Response object or None.
    """
    try:
        if proxy:
            response = requests.get(url, proxies={"http": proxy, "https": proxy})
        else:
            response = requests.get(url)
        response.raise_for_status()  # Check if request was successful
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None
