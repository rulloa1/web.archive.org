#!/usr/bin/env python3
"""
Link checker script to verify all internal links in HTML files.
"""

import os
import re
import urllib.parse
from pathlib import Path

def find_internal_links(html_content):
    """Find all internal links in HTML content"""
    # Find all href attributes
    href_pattern = r'href=["\']([^"\']*)["\']'
    links = re.findall(href_pattern, html_content, re.IGNORECASE)
    
    internal_links = []
    for link in links:
        # Skip external links, email, tel, and anchors
        if (link.startswith('http://') or 
            link.startswith('https://') or 
            link.startswith('mailto:') or 
            link.startswith('tel:') or
            link.startswith('#') or
            link.startswith('javascript:') or
            link.startswith('data:') or
            not link.strip()):
            continue
        
        # Remove query parameters and anchors for file checking
        parsed = urllib.parse.urlparse(link)
        clean_path = parsed.path
        
        internal_links.append({
            'original': link,
            'path': clean_path,
            'has_anchor': bool(parsed.fragment),
            'anchor': parsed.fragment
        })
    
    return internal_links

def check_file_exists(base_dir, link_path):
    """Check if a file exists for the given link path"""
    if not link_path or link_path == '/':
        # Root path should point to index.html
        return os.path.exists(os.path.join(base_dir, 'index.html'))
    
    # Remove leading slash
    if link_path.startswith('/'):
        link_path = link_path[1:]
    
    full_path = os.path.join(base_dir, link_path)
    
    # Check exact file
    if os.path.exists(full_path):
        return True
    
    # If no extension, try adding .html
    if '.' not in os.path.basename(link_path):
        html_path = full_path + '.html'
        if os.path.exists(html_path):
            return True
    
    # Check if it's a directory with index.html
    if os.path.isdir(full_path):
        index_path = os.path.join(full_path, 'index.html')
        if os.path.exists(index_path):
            return True
    
    return False

def main():
    base_dir = Path(__file__).parent
    html_files = list(base_dir.glob('*.html'))
    
    print(f"Checking links in {len(html_files)} HTML files...")
    print("=" * 60)
    
    all_good = True
    
    for html_file in html_files:
        print(f"\nChecking {html_file.name}:")
        
        try:
            with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            print(f"  ERROR: Could not read file: {e}")
            all_good = False
            continue
        
        links = find_internal_links(content)
        
        if not links:
            print("  No internal links found.")
            continue
        
        print(f"  Found {len(links)} internal links:")
        
        for link in links:
            exists = check_file_exists(base_dir, link['path'])
            status = "✓" if exists else "✗"
            print(f"    {status} {link['original']}")
            
            if not exists:
                print(f"      -> Target file not found: {link['path']}")
                all_good = False
    
    print("\n" + "=" * 60)
    if all_good:
        print("✓ All internal links are working!")
    else:
        print("✗ Some links are broken. Please fix them before deployment.")
    
    return 0 if all_good else 1

if __name__ == "__main__":
    exit(main())
