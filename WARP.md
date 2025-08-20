# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Repository Overview

This is a static website for Creative Excellence Tutoring, containing archived HTML pages from web.archive.org. The site provides information about personalized after-school tutoring services. The repository includes the main website files and Python utility scripts for maintenance.

## Development Commands

### Local Development
```bash
# Start local development server
npm start
# OR
npm run serve
# OR
npm run dev
# OR
npm run preview

# Alternative direct Python server (if Node.js not available)
python -m http.server 8000
# OR
python3 -m http.server 8000
```

### Build & Deployment
```bash
# Build the project (currently just echoes status)
npm run build

# Deploy (configure with your hosting provider)
npm run deploy

# Clean build artifacts
npm run clean
```

### Link Management & Validation
```bash
# Check all links in HTML files for broken references
python check_links.py

# Extract and categorize all links from index.html
python extract_links.py

# Fix common broken links and template variables
python fix_links.py
```

### Testing & Quality
```bash
# Run tests
npm test

# Lint HTML files
npm run lint
```

## Architecture & Code Structure

### Website Structure
- **Static HTML Pages**: Individual pages for different sections (index, contact, FAQ, etc.)
- **Archived Content**: Pages contain `download_date` metadata indicating they were archived from web.archive.org
- **jQuery-based**: Uses jQuery 3.3.1 for DOM manipulation and interactions
- **CSS Framework**: Appears to use utility-first CSS with responsive design principles

### Key Components
- `index.html` - Main landing page
- `contact.html` - Contact information and forms
- `faq.html` - Frequently asked questions
- `college-counseling-admissions-support.html` - Specialized service page
- `legal-policies.html` - Legal and policy information
- `privacy-policy.html` - Privacy policy
- `meet-the-team.html` - Team information page
- `news.html` - News and updates

### Python Utility Scripts
- **`check_links.py`**: Validates links across HTML files, identifies broken references
- **`extract_links.py`**: Extracts and categorizes all href attributes from HTML files into internal, external, email, JavaScript, and anchor links
- **`fix_links.py`**: Automatically fixes common broken links including:
  - Template variables (`{{src}}`, `${post.link}`)
  - Malformed email and phone links
  - JavaScript void links

### Deployment Configuration
- **Netlify**: Configured for Netlify deployment with `netlify.toml`
- **Static Hosting**: Designed for static file hosting environments
- **No Build Process**: Simple static files with no complex build pipeline

## Development Guidelines

### HTML Development
- All HTML files use UTF-8 encoding
- jQuery 3.3.1 is embedded inline for faster loading
- Responsive design with mobile-first approach
- SEO optimized with proper meta tags and descriptions

### Link Management
- Use relative paths for internal navigation
- Ensure all href attributes are properly formatted
- Run `python fix_links.py` after making link changes
- Validate with `python check_links.py` before deployment

### Content Updates
- Update individual HTML files directly
- Maintain consistent styling and structure across pages
- Preserve canonical URLs and meta descriptions for SEO

### Testing Workflow
1. Make changes to HTML files
2. Run local development server to preview
3. Execute link checking scripts to validate
4. Test responsive design on multiple devices
5. Deploy to staging (Netlify) for final review

## Special Considerations

### Archived Content
- This site contains archived content from web.archive.org
- Original URLs and canonical links reference `creativeexcellencetutoring.com`
- Some template variables and broken links are expected in archived content

### Link Maintenance
- The utility scripts are specifically designed to handle common issues in archived web content
- Regular link checking is recommended due to the nature of archived content
- Template variables should be replaced with actual values when updating content

### SEO & Performance
- Inline jQuery reduces HTTP requests but increases HTML file size
- Each page has specific meta titles and descriptions optimized for tutoring services
- Favicon is embedded as base64 data URI

### Browser Compatibility
- jQuery 3.3.1 provides broad browser compatibility
- Responsive design works across modern browsers
- No complex JavaScript frameworks - simple and reliable
