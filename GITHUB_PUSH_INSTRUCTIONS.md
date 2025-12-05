# Instructions for Pushing to GitHub

Since Git is not currently installed on your system, here are the steps to push your code to GitHub:

## Step 1: Install Git

### Option A: Download Git for Windows
1. Go to https://git-scm.com/download/win
2. Download and install Git for Windows
3. During installation, choose "Git from the command line and also from 3rd-party software"
4. Restart your terminal/PowerShell after installation

### Option B: Use GitHub Desktop (Easier)
1. Download GitHub Desktop from https://desktop.github.com/
2. Install and sign in with your GitHub account
3. Use the GUI to push your code

## Step 2: Initialize Git Repository

Open PowerShell in your project directory and run:

```powershell
# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: YouTube to MP3 Downloader v2.0.0"
```

## Step 3: Connect to GitHub

```powershell
# Add remote repository (replace with your actual repo URL)
git remote add origin https://github.com/sallonikaG4/ytdownloader.git

# Verify remote
git remote -v
```

## Step 4: Push to GitHub

```powershell
# Push to main branch
git branch -M main
git push -u origin main
```

If you're prompted for credentials:
- **Username**: Your GitHub username
- **Password**: Use a Personal Access Token (not your GitHub password)
  - Go to GitHub Settings > Developer settings > Personal access tokens
  - Generate a new token with `repo` permissions
  - Use that token as your password

## Alternative: Using GitHub Desktop

1. **Open GitHub Desktop**
2. **File > Add Local Repository**
3. **Browse to your project folder**: `C:\Users\polyt\OneDrive\Companies\Tech Solutions\Webdesign Works\Youtube`
4. **Click "Publish repository"**
5. **Select the repository**: `sallonikaG4/ytdownloader`
6. **Click "Publish Repository"**

## Files Ready to Push

All files are ready:
- ✅ `README.md` - Comprehensive documentation
- ✅ `LICENSE` - GPL 3.0 License
- ✅ All source code files
- ✅ Windows build files
- ✅ macOS build files
- ✅ Documentation files

## After Pushing

Once pushed, your repository will have:
- Complete source code
- Installation instructions
- Build instructions for both platforms
- GPL 3.0 License
- Comprehensive README

## Next Steps

After pushing:
1. Create a **Release** on GitHub with the built installers
2. Add screenshots to the README (optional)
3. Set up GitHub Actions for automatic builds (optional)

## Need Help?

If you encounter issues:
- Check GitHub's documentation: https://docs.github.com/en/get-started
- For authentication issues, see: https://docs.github.com/en/authentication

