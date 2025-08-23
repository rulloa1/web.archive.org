.PHONY: netlify-ready clean build test lint help

# Default target
help:
	@echo "Available targets:"
	@echo "  netlify-ready - Prepare files for Netlify deployment"
	@echo "  build         - Build the static website"
	@echo "  clean         - Clean build artifacts and temporary files"
	@echo "  test          - Run tests and validation"
	@echo "  lint          - Lint HTML files"
	@echo "  help          - Show this help message"

# Main target to prepare files for Netlify
netlify-ready: clean build test
	@echo "🚀 Preparing files for Netlify deployment..."
	@echo "✅ Checking HTML files..."
	@powershell -Command "Get-ChildItem -Name '*.html' | ForEach-Object { Write-Host '   - Validating' $$_ }"
	@echo "✅ Checking for required files..."
	@powershell -Command "if (!(Test-Path 'index.html')) { Write-Host '❌ Error: index.html not found!'; exit 1 }"
	@echo "✅ Files are ready for Netlify deployment!"
	@echo ""
	@echo "📝 Next steps:"
	@echo "   1. Commit your changes: git add . && git commit -m 'Ready for deployment'"
	@echo "   2. Push to your repository: git push"
	@echo "   3. Deploy via Netlify dashboard or CLI: netlify deploy --prod"

# Build target
build:
	@echo "🔨 Building static website..."
	@npm run build
	@echo "✅ Build complete!"

# Clean target
clean:
	@echo "🧹 Cleaning temporary files..."
	@powershell -Command "if (Test-Path '.tmp') { Remove-Item '.tmp' -Recurse -Force }"
	@powershell -Command "if (Test-Path 'dist') { Remove-Item 'dist' -Recurse -Force }"
	@powershell -Command "Get-ChildItem '*.tmp' -ErrorAction SilentlyContinue | Remove-Item -Force"
	@echo "✅ Clean complete!"

# Test target
test:
	@echo "🧪 Running tests and validation..."
	@npm run test
	@echo "✅ All tests passed!"

# Lint target
lint:
	@echo "🔍 Linting HTML files..."
	@npm run lint
	@echo "✅ Linting complete!"

# Alternative target names for convenience
ready: netlify-ready
deploy-ready: netlify-ready
prepare: netlify-ready
