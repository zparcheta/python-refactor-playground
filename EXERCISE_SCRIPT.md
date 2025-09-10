# 🎯 Exercise Script: Code Quality
## *Step-by-Step Guide for Students*

**📝 Instructions: Execute each command in order, one by one. Wait for each command to complete before running the next one.**

---

## 📋 **PHASE 1: SETUP**

### Step 1: Verify Installation
```bash
make help
```

### Step 2: Install Dependencies
```bash
make install
```

### Step 3: Check Project Structure
```bash
ls -la
```

---

## 🔍 **PHASE 2: INITIAL ANALYSIS**

### Step 4: Record Initial Benchmark
```bash
make benchmark-initial
```

### Step 5: See Generated Files
```bash
ls -la *report*.txt issues_to_fix*.txt benchmark_results.json
```

### Step 6: View Fixable Issues (MOST IMPORTANT)
```bash
cat issues_to_fix_*.txt
```

### Step 7: View Benchmark Data
```bash
python tools/benchmark_code_quality.py --report
```

---

## ⚡ **PHASE 3: AUTO-FIXER**

### Step 8: Fix All Issues Automatically
```bash
make fix
```

### Step 9: See What Files Were Modified
```bash
git status
```

### Step 10: Verify Code Still Works
```bash
make test
```

---

## 📊 **PHASE 4: COMPARISON**

### Step 11: Record Post-Fix Benchmark
```bash
make benchmark-post-autofix
```

### Step 12: Compare Results
```bash
make benchmark-compare
```

### Step 13: Generate Detailed Report
```bash
make benchmark-report
```

---

## 🤖 **PHASE 5: AI AGENT**

### Step 14: See Remaining Errors
```bash
cat issues_to_fix_*.txt
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
```bash
make test
```

---

## 📈 **PHASE 6: FINAL ANALYSIS**

### Step 17: Record Final Benchmark
```bash
make benchmark-post-ai
```

### Step 18: Final Comparison
```bash
make benchmark-compare
```

### Step 19: Final Report
```bash
make benchmark-report
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
```bash
# Check if dependencies are installed
pip list | grep -E "(black|ruff|mypy|bandit)"

# Reinstall if needed
make install
```

### If tests fail:
```bash
# See specific errors
make test-verbose

# Verify code works
python main.py
```

### If you get confused:
- **Go back to the previous step** and make sure it completed successfully
- **Check the output** of each command for error messages
- **Ask for help** if you're stuck

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

**Congratulations on completing the exercise! 🎉**

*Remember: Code quality is a continuous process, not a destination.*
