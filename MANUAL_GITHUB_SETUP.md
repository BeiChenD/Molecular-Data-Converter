# Manual GitHub Setup Instructions

## Bei Chen - Molecular Data Converter

If the automated setup script doesn't work, follow these manual steps:

### Step 1: Ensure Git is Installed
```powershell
git --version
```
If not installed, download from: https://git-scm.com/

### Step 2: Initialize Repository
```powershell
cd "Y:\CompSci Studies\MDAnalysisData"
git init
```

### Step 3: Configure Git
```powershell
git config user.name "Bei Chen"
git config user.email "your-email@example.com"
```

### Step 4: Add Files
```powershell
git add .
git status
```

### Step 5: Create Initial Commit
```powershell
git commit -m "Initial commit: Molecular Data Converter by Bei Chen

- Complete Python toolkit for converting DCD/PSF files to readable formats
- Support for XYZ, CSV, and TXT output formats  
- 3D molecular visualization capabilities
- Interactive starter script for easy file conversion
- Comprehensive documentation and setup guides
- Windows batch file for one-click execution
- Sample H3O water simulation data included"
```

### Step 6: Set Up Remote Repository
```powershell
git branch -M main
git remote add origin https://github.com/BeiChenD/Molecular-Data-Converter.git
```

### Step 7: Push to GitHub
```powershell
git push -u origin main
```

### Authentication Setup

#### Option 1: GitHub CLI (Recommended)
```powershell
# Install GitHub CLI from https://cli.github.com/
gh auth login
gh repo create BeiChenD/Molecular-Data-Converter --public
git push -u origin main
```

#### Option 2: Personal Access Token
1. Go to GitHub Settings > Developer settings > Personal access tokens
2. Generate new token with repo permissions
3. Use token as password when pushing

#### Option 3: SSH Key
1. Generate SSH key: `ssh-keygen -t ed25519 -C "your-email@example.com"`
2. Add key to GitHub: Settings > SSH and GPG keys
3. Change remote URL: `git remote set-url origin git@github.com:BeiChenD/Molecular-Data-Converter.git`

### Verification
After successful push, verify at:
https://github.com/BeiChenD/Molecular-Data-Converter

### Files That Should Be Pushed:
- ✅ convert_molecular_data.py
- ✅ start_here.py  
- ✅ quick_convert.py
- ✅ START.bat
- ✅ README.md
- ✅ LICENSE
- ✅ CHANGELOG.md
- ✅ requirements.txt
- ✅ GET_STARTED.md
- ✅ HOW_TO_START.md
- ✅ Sample data files (H3O_ws.psf, H3O_ws_short.dcd)
- ✅ .gitignore
- ✅ .github/workflows/test.yml

### Troubleshooting

**Error: "repository not found"**
- Ensure repository exists on GitHub
- Check repository name spelling
- Verify authentication

**Error: "failed to push"** 
- Check internet connection
- Verify GitHub credentials
- Try: `git push origin main --force-with-lease`

**Error: "permission denied"**
- Set up authentication (see options above)
- Check repository permissions

---
*Manual setup guide for Molecular Data Converter - Bei Chen*
