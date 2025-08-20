#!/usr/bin/env python3
"""
Script to fix common broken links and template variables in HTML files.
"""

import os
import re
from pathlib import Path

def fix_html_file(file_path):
    """Fix common issues in an HTML file"""
    print(f"Processing {file_path.name}...")
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        print(f"  ERROR: Could not read file: {e}")
        return False
    
    original_content = content
    changes_made = []
    
    # Fix template variables and broken links
    fixes = [
        # Template variables that should be removed or replaced
        (r'href=["\']{{src}}["\']', 'href="#"', "Template variable {{src}}"),
        (r'href=["\']\$\{post\.link\}["\']', 'href="#"', "Template variable ${post.link}"),
        (r'href=["\']\$\{post\.link\} target=["\']', 'href="#" target="', "Malformed template variable"),
        (r'href=["\']\$\{post\.link\}\s+target=', 'href="#" target=', "Malformed template variable with space"),
        
        # Fix malformed email and phone links
        (r'href=["\']nullinfo@creativeexcellencetutoring\.com["\']', 'href="mailto:info@creativeexcellencetutoring.com"', "Fix email link"),
        (r'href=["\']null\+17134916004["\']', 'href="tel:+17134916004"', "Fix phone link"),
        (r'href=["\']nullvoid\(0\);["\']', 'href="javascript:void(0);"', "Fix JavaScript void link"),
    ]
    
    for pattern, replacement, description in fixes:
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            changes_made.append(description)
    
    # Write back if changes were made
    if changes_made:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✓ Fixed: {', '.join(changes_made)}")
            return True
        except Exception as e:
            print(f"  ERROR: Could not write file: {e}")
            return False
    else:
        print("  No changes needed.")
        return True

def main():
    base_dir = Path(__file__).parent
    html_files = list(base_dir.glob('*.html'))
    
    print(f"Fixing links in {len(html_files)} HTML files...")
    print("=" * 60)
    
    success_count = 0
    
    for html_file in html_files:
        if fix_html_file(html_file):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"Successfully processed {success_count}/{len(html_files)} files.")
    
    if success_count == len(html_files):
        print("✓ All files processed successfully!")
        print("\nRun check_links.py again to verify all links are now working.")
    else:
        print("✗ Some files had errors. Please check the output above.")
    
    return 0 if success_count == len(html_files) else 1

if __name__ == "__main__":
    exit(main())
