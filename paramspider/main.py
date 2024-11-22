#!/usr/bin/env python3
import argparse
import os
import sys
import time
import requests
from urllib.parse import unquote, urlparse, parse_qs, urlencode
import logging
from core import requester, extractor, save_it

# Inisialisasi
start_time = time.time()

def clean_url(url, extensions, placeholder):
    """
    Clean the URL by removing redundant port information for HTTP and HTTPS URLs.
    Args:
        url (str): The URL to clean.
        extensions (list): List of extensions to ignore.
        placeholder (str): The placeholder for query parameters.
    Returns:
        str: Cleaned URL.
    """
    parsed_url = urlparse(url)
    path = parsed_url.path

    # Ignore URLs with certain extensions
    if any(path.endswith(ext) for ext in extensions):
        return None
    
    # Replace query parameters with placeholder
    query_params = parse_qs(parsed_url.query)
    cleaned_params = {key: placeholder for key in query_params}
    cleaned_query = urlencode(cleaned_params, doseq=True)
    cleaned_url = parsed_url._replace(query=cleaned_query).geturl()

    return cleaned_url

def fetch_urls(domain, extensions, proxy, placeholder):
    """
    Fetch and clean URLs related to a specific domain from the Wayback Machine.
    Args:
        domain (str): The domain name to fetch URLs for.
        extensions (list): List of file extensions to ignore.
        proxy (str): The proxy address for requests.
        placeholder (str): The string to use as a placeholder for query parameters.
    Returns:
        list: List of cleaned URLs.
    """
    wayback_uri = f"https://web.archive.org/cdx/search/cdx?url={domain}/*&output=txt&collapse=urlkey&fl=original&page=/"
    response = requester.connector(wayback_uri, proxy)
    if not response:
        return []
    
    response = unquote(response)
    urls = response.splitlines()

    # Filter and clean URLs
    cleaned_urls = []
    for url in urls:
        cleaned_url = clean_url(url, extensions, placeholder)
        if cleaned_url:
            cleaned_urls.append(cleaned_url)

    return cleaned_urls

def main():
    if os.name == 'nt':
        os.system('cls')

    banner = """\u001b[36m

         ___                               _    __       
        / _ \___ ________ ___ _  ___ ___  (_)__/ /__ ____
       / ___/ _ `/ __/ _ `/  ' \(_-</ _ \/ / _  / -_) __/
      /_/   \_,_/_/  \_,_/_/_/_/___/ .__/_/\_,_/\__/_/   
                                  /_/     \u001b[0m               

                           \u001b[32m - coded with <3 by Devansh Batham\u001b[0m 
    """
    print(banner)

    parser = argparse.ArgumentParser(description='ParamSpider a parameter discovery suite')
    parser.add_argument('-d', '--domain', help='Domain name of the target [ex : hackerone.com]', required=True)
    parser.add_argument('-s', '--subs', help='Set False for no subs [ex : --subs False]', default=True)
    parser.add_argument('-l', '--level', help='For nested parameters [ex : --level high]')
    parser.add_argument('-e', '--exclude', help='Extensions to exclude [ex --exclude php,aspx]')
    parser.add_argument('-o', '--output', help='Output file name [by default it is \'domain.txt\']')
    parser.add_argument('-p', '--placeholder', help='The string to add as a placeholder after the parameter name.', default="FUZZ")
    parser.add_argument('--proxy', help='Set the proxy address for web requests.', default=None)
    parser.add_argument('-q', '--quiet', help='Do not print the results to the screen', action='store_true')
    parser.add_argument('-r', '--retries', help='Specify number of retries for 4xx and 5xx errors', default=3)
    args = parser.parse_args()

    # Set URL for Wayback Machine
    if args.subs:
        url = f"https://web.archive.org/cdx/search/cdx?url=*.{args.domain}/*&output=txt&fl=original&collapse=urlkey&page=/"
    else:
        url = f"https://web.archive.org/cdx/search/cdx?url={args.domain}/*&output=txt&fl=original&collapse=urlkey&page=/"
    
    retries = 0
    while retries <= int(args.retries):
        response = requester.connector(url, args.proxy)
        if response:
            break
        retries += 1

    if not response:
        print("[!] Failed to fetch URLs after multiple retries.")
        return

    # Exclude unwanted extensions
    black_list = []
    if args.exclude:
        black_list = args.exclude.split(",") if "," in args.exclude else [args.exclude]
        black_list = [f".{ext}" for ext in black_list]

    # Fetch and clean URLs
    extensions = black_list
    cleaned_urls = fetch_urls(args.domain, extensions, args.proxy, args.placeholder)

    # Save output
    save_it.save_func(cleaned_urls, args.output, args.domain)

    # Output results
    if not args.quiet:
        print("\u001b[32;1m")
        print('\n'.join(cleaned_urls))
        print("\u001b[0m")

    print(f"\n[+] Total unique URLs found: {len(cleaned_urls)}")
    if args.output:
        print(f"[+] Output saved here: {args.output}")
    else:
        print(f"[+] Output saved here: output/{args.domain}.txt")
    print(f"\n[!] Total execution time: {time.time() - start_time:.2f}s")

if __name__ == "__main__":
    main()
