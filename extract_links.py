#!/usr/bin/env python3
"""
Link Extractor for HTML Files
Extracts all href attributes from HTML files and categorizes them.
"""

import re
import urllib.parse
from pathlib import Path

def extract_links_from_html(file_path):
    """Extract all href attributes from an HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

    # Find all href attributes using regex
    href_pattern = r'href=["\']([^"\']+)["\']'
    matches = re.findall(href_pattern, content, re.IGNORECASE)
    
    return matches

def categorize_links(links):
    """Categorize links into internal, external, and other types"""
    internal_links = []
    external_links = []
    email_links = []
    javascript_links = []
    anchor_links = []
    other_links = []
    
    for link in links:
        link = link.strip()
        if not link:
            continue
            
        if link.startswith('mailto:'):
            email_links.append(link)
        elif link.startswith('javascript:'):
            javascript_links.append(link)
        elif link.startswith('#'):
            anchor_links.append(link)
        elif link.startswith('http://') or link.startswith('https://'):
            external_links.append(link)
        elif link.startswith('//'):
            external_links.append('https:' + link)
        elif link.startswith('/') or not '://' in link:
            # Relative or root-relative links
            internal_links.append(link)
        else:
            other_links.append(link)
    
    return {
        'internal': internal_links,
        'external': external_links,
        'email': email_links,
        'javascript': javascript_links,
        'anchor': anchor_links,
        'other': other_links
    }

def print_results(categorized_links):
    """Print the categorized links"""
    for category, links in categorized_links.items():
        if links:
            print(f"\n{category.upper()} LINKS ({len(links)}):")
            print("-" * 40)
            for i, link in enumerate(sorted(set(links)), 1):
                print(f"{i:3d}. {link}")

def main():
    file_path = Path("index.html")
    
    if not file_path.exists():
        print(f"File {file_path} not found!")
        return
    
    print(f"Extracting links from {file_path}...")
    links = extract_links_from_html(file_path)
    
    if not links:
        print("No links found in the file.")
        return
    
    print(f"Found {len(links)} total href attributes")
    
    categorized = categorize_links(links)
    print_results(categorized)
    
    # Summary
    total_unique = sum(len(set(links)) for links in categorized.values())
    print(f"\nSUMMARY:")
    print(f"Total href attributes found: {len(links)}")
    print(f"Unique links: {total_unique}")
    
    for category, links in categorized.items():
        unique_count = len(set(links))
        if unique_count > 0:
            print(f"{category.capitalize()}: {unique_count} unique links")

if __name__ == "__main__":
    main()
