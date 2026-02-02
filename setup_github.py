#!/usr/bin/env python3
"""
GitHub Repository Setup Script
==============================

Automates the process of setting up and pushing the Molecular Data Converter
project to GitHub.

Author: Bei Chen
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(cmd, description=""):
    """Run a command and return success status."""
    print(f"🔄 {description}")
    print(f"   Command: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            print(f"✅ Success: {description}")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Failed: {description}")
            if result.stderr.strip():
                print(f"   Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ Exception in {description}: {e}")
        return False

def setup_git_repository():
    """Initialize and configure git repository."""
    print("🚀 Setting up Git Repository for Molecular Data Converter")
    print("=" * 60)
    
    # Check current directory
    current_dir = Path.cwd()
    print(f"📁 Working directory: {current_dir}")
    
    # Initialize git repository
    if not (current_dir / ".git").exists():
        if not run_command("git init", "Initializing git repository"):
            return False
    else:
        print("✅ Git repository already initialized")
    
    # Configure git user
    run_command('git config user.name "Bei Chen"', "Setting git user name")
    run_command('git config user.email "beichen@example.com"', "Setting git user email")
    
    # Check git status
    run_command("git status", "Checking repository status")
    
    # Add all files
    if not run_command("git add .", "Adding files to staging area"):
        return False
    
    # Check what files were added
    run_command("git status", "Checking staged files")
    
    # Create initial commit
    commit_message = '''Initial commit: Molecular Data Converter by Bei Chen

- Complete Python toolkit for converting DCD/PSF files to readable formats
- Support for XYZ, CSV, and TXT output formats  
- 3D molecular visualization capabilities
- Interactive starter script for easy file conversion
- Comprehensive documentation and setup guides
- Windows batch file for one-click execution
- Sample H3O water simulation data included'''
    
    commit_cmd = f'git commit -m "{commit_message}"'
    if not run_command(commit_cmd, "Creating initial commit"):
        print("⚠️ Commit may have failed or no changes to commit")
    
    # Rename branch to main
    run_command("git branch -M main", "Renaming branch to main")
    
    # Add remote repository
    remote_url = "https://github.com/BeiChenD/Molecular-Data-Converter.git"
    remote_cmd = f"git remote add origin {remote_url}"
    if not run_command(remote_cmd, "Adding GitHub remote"):
        # Try to set the URL if remote already exists
        set_url_cmd = f"git remote set-url origin {remote_url}"
        run_command(set_url_cmd, "Setting GitHub remote URL")
    
    # Push to GitHub
    if not run_command("git push -u origin main", "Pushing to GitHub"):
        print("❌ Failed to push to GitHub")
        print("🔑 You may need to:")
        print("   1. Create the repository on GitHub first")
        print("   2. Set up authentication (GitHub token or SSH keys)")
        print("   3. Check your internet connection")
        return False
    
    print("\n🎉 SUCCESS! Repository pushed to GitHub!")
    print(f"🔗 Visit: {remote_url}")
    return True

def create_github_workflow():
    """Create GitHub Actions workflow for testing."""
    workflow_dir = Path(".github/workflows")
    workflow_dir.mkdir(parents=True, exist_ok=True)
    
    workflow_content = """name: Test Molecular Data Converter

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', '3.11']

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Test imports
      run: |
        python -c "import MDAnalysis; print('MDAnalysis imported successfully')"
        python -c "from convert_molecular_data import MolecularDataConverter; print('MolecularDataConverter imported successfully')"
    
    - name: Test quick convert (if sample data exists)
      run: |
        if [ -f "H3O_ws.psf" ] && [ -f "H3O_ws_short.dcd" ]; then
          python quick_convert.py
        else
          echo "Sample data not found, skipping conversion test"
        fi
"""
    
    workflow_file = workflow_dir / "test.yml"
    with open(workflow_file, 'w') as f:
        f.write(workflow_content)
    
    print(f"✅ Created GitHub Actions workflow: {workflow_file}")

def main():
    """Main function."""
    print("🧬 GitHub Repository Setup - Molecular Data Converter")
    print("Author: Bei Chen")
    print("=" * 60)
    
    # Create GitHub workflow
    create_github_workflow()
    
    # Setup and push repository
    if setup_git_repository():
        print("\n📋 Repository Contents:")
        run_command("git ls-files", "Listing tracked files")
        
        print("\n🔗 Next Steps:")
        print("   1. Visit https://github.com/BeiChenD/Molecular-Data-Converter")
        print("   2. Add a description to your repository")
        print("   3. Consider adding topics/tags for discoverability")
        print("   4. Share with the research community!")
        
    else:
        print("\n❌ Repository setup failed. Please check the errors above.")
        print("\n🔧 Manual Steps:")
        print("   1. Ensure Git is installed and in PATH")
        print("   2. Create repository on GitHub first")
        print("   3. Set up authentication (GitHub CLI or SSH keys)")
        print("   4. Try running the git commands manually")

if __name__ == "__main__":
    main()
