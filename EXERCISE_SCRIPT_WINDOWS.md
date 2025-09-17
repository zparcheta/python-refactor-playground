# 🎯 Exercise Script: Code Quality (Windows)
## *Step-by-Step Guide for Students*

**📝 Instructions: Execute each command in order, one by one. Wait for each command to complete before running the next one.**

---

## 📋 **PHASE 1: SETUP**

### Step 1: Verify Installation
```cmd
run.bat help
```
*Or with PowerShell:*
```powershell
.\run.ps1 help
```

### Step 2: Install Dependencies
```cmd
run.bat install
```
*Or with PowerShell:*
```powershell
.\run.ps1 install
```

### Step 3: Check Project Structure
```cmd
dir
```
*Or with PowerShell:*
```powershell
Get-ChildItem
```

---

## 🔍 **PHASE 2: INITIAL ANALYSIS**

### Step 4: Record Initial Benchmark
```cmd
run.bat benchmark-initial
```
*Or with PowerShell:*
```powershell
.\run.ps1 benchmark-initial
```

### Step 5: See Generated Files
```cmd
dir *report*.txt issues_to_fix*.txt benchmark_results.json
```
*Or with PowerShell:*
```powershell
Get-ChildItem *report*.txt, issues_to_fix*.txt, benchmark_results.json
```

### Step 6: View Fixable Issues (MOST IMPORTANT)
```cmd
type issues_to_fix_*.txt
```
*Or with PowerShell:*
```powershell
Get-Content issues_to_fix_*.txt
```

### Step 7: View Benchmark Data
```cmd
python tools/benchmark_code_quality.py --report
```

---

## ⚡ **PHASE 3: AUTO-FIXER**

### Step 8: Fix All Issues Automatically
```cmd
run.bat fix
```
*Or with PowerShell:*
```powershell
.\run.ps1 fix
```

### Step 9: See What Files Were Modified
```cmd
git status
```

### Step 10: Verify Code Still Works
```cmd
run.bat test
```
*Or with PowerShell:*
```powershell
.\run.ps1 test
```

---

## 📊 **PHASE 4: COMPARISON**

### Step 11: Record Post-Fix Benchmark
```cmd
run.bat benchmark-post-autofix
```
*Or with PowerShell:*
```powershell
.\run.ps1 benchmark-post-autofix
```

### Step 12: Compare Results
```cmd
run.bat benchmark-compare
```
*Or with PowerShell:*
```powershell
.\run.ps1 benchmark-compare
```

### Step 13: Generate Detailed Report
```cmd
run.bat benchmark-report
```
*Or with PowerShell:*
```powershell
.\run.ps1 benchmark-report
```

---

## 🤖 **PHASE 5: AI AGENT**

### Step 14: See Remaining Errors
```cmd
type issues_to_fix_*.txt
```
*Or with PowerShell:*
```powershell
Get-Content issues_to_fix_*.txt
```

### Step 15: Use AI Agent
**💬 Copy and paste this prompt in your AI agent:**

```
Analyze the files in this project and fix the remaining code quality issues 
that automated tools cannot fix. Focus on:
1. Type errors (MyPy issues)
2. Logic improvements
3. Performance optimizations
4. Code structure improvements

Explain each change you make and why it improves the code.
```

### Step 16: Test After AI Changes
```cmd
run.bat test
```
*Or with PowerShell:*
```powershell
.\run.ps1 test
```

---

## 📈 **PHASE 6: FINAL ANALYSIS**

### Step 17: Record Final Benchmark
```cmd
run.bat benchmark-post-ai
```
*Or with PowerShell:*
```powershell
.\run.ps1 benchmark-post-ai
```

### Step 18: Final Comparison
```cmd
run.bat benchmark-compare
```
*Or with PowerShell:*
```powershell
.\run.ps1 benchmark-compare
```

### Step 19: Final Report
```cmd
run.bat benchmark-report
```
*Or with PowerShell:*
```powershell
.\run.ps1 benchmark-report
```

### Step 20: Reflection
**🤔 Answer these questions:**

1. **What percentage of errors were fixed automatically?**
   - Answer: ___ (check benchmark report)

2. **What types of errors were most difficult to fix?**
   - Answer: ___

3. **Which tool did you find most useful?**
   - Answer: ___

4. **How would you change your development process after this?**
   - Answer: ___

---

## 🆘 **TROUBLESHOOTING**

### If a command fails:
```cmd
REM Check if dependencies are installed
pip list | findstr "black ruff mypy bandit"

REM Reinstall if needed
run.bat install
```
*Or with PowerShell:*
```powershell
# Check if dependencies are installed
pip list | Select-String "black|ruff|mypy|bandit"

# Reinstall if needed
.\run.ps1 install
```

### If tests fail:
```cmd
REM See specific errors
run.bat test-verbose

REM Verify code works
python main.py
```
*Or with PowerShell:*
```powershell
# See specific errors
.\run.ps1 test-verbose

# Verify code works
python main.py
```

### If you get confused:
- **Go back to the previous step** and make sure it completed successfully
- **Check the output** of each command for error messages
- **Ask for help** if you're stuck

### Windows-Specific Issues:

#### PowerShell Execution Policy
If you get execution policy errors with PowerShell:
```powershell
# Check current policy
Get-ExecutionPolicy

# Set policy for current user (if needed)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Python Not Found
If Python is not recognized:
1. Install Python from https://python.org
2. Make sure to check "Add Python to PATH" during installation
3. Restart Command Prompt/PowerShell after installation

#### Long Path Issues
If you encounter path length issues:
```cmd
REM Enable long paths (Windows 10+)
git config --global core.longpaths true
```

---

## 🏆 **SUCCESS CRITERIA**

### ✅ **Exercise Completed Successfully if:**
- [ ] Reduced at least 70% of initial errors
- [ ] Understand what each tool does
- [ ] Can explain the difference between auto-fixer and AI
- [ ] Applied at least 3 changes suggested by AI
- [ ] Code still works after all changes

### 🎯 **Learning Objectives Achieved:**
- [ ] Know code quality tools
- [ ] Can automate repetitive tasks
- [ ] Know when to use AI vs automated tools
- [ ] Have a workflow to improve code

---

## 🖥️ **Windows-Specific Notes**

### Command Prompt vs PowerShell
- **Command Prompt**: Use `run.bat` commands
- **PowerShell**: Use `.\run.ps1` commands (recommended for better error handling)

### File Paths
- Windows uses backslashes (`\`) in paths
- Use quotes around paths with spaces: `"C:\Program Files\Python\python.exe"`

### Environment Variables
- Python path should be in `PATH` environment variable
- Check with: `echo %PATH%` (CMD) or `$env:PATH` (PowerShell)

---

**Congratulations on completing the exercise! 🎉**

*Remember: Code quality is a continuous process, not a destination.*
