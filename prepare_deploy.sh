#!/bin/bash
# Deployment preparation script for Linux/Mac

echo "🚀 Preparing for Deployment..."

# Create .gitignore if doesn't exist
if [ ! -f .gitignore ]; then
    echo "Creating .gitignore..."
    cat > .gitignore << EOF
# Environment
.env
venv/
env/

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Reports
*_report.md
*.json

# Logs
*.log
EOF
fi

# Initialize git if not already
if [ ! -d .git ]; then
    echo "Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit: Trade Opportunities API"
fi

echo ""
echo "✅ Ready for GitHub!"
echo ""
echo "Next steps:"
echo "1. Create GitHub repo: https://github.com/new"
echo "2. Run these commands:"
echo ""
echo "   git remote add origin https://github.com/YOUR_USERNAME/trade-opportunities-api.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Share with recruiter:"
echo "   GitHub: https://github.com/YOUR_USERNAME/trade-opportunities-api"
echo ""
