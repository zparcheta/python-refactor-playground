# 🎯 Exercise Script: Code Quality
## *Step-by-Step Guide for Students*

---

## 📋 **Environment Setup**

### 1. Verify everything is installed:
```bash
# Verify project is configured
make help

# Install dependencies if needed
make install
```

### 2. Verify project structure:
```bash
# See the structure
ls -la

# See main files
ls src/ tests/ tools/
```

---

## 🔍 **PHASE 1: INITIAL ANALYSIS**

### Step 1.1: Record Initial Benchmark
```bash
# Record initial benchmark (automatically runs analysis)
make benchmark-initial
```

### Step 1.2: Review Results
```bash
# See generated files
ls -la *report*.txt issues_to_fix*.txt benchmark_results.json

# See complete report (optional, it's long)
head -50 code_quality_report_*.txt

# See fixable issues (MOST IMPORTANT)
cat issues_to_fix_*.txt
```

### Step 1.3: View Benchmark Data
**📝 The benchmark tool automatically records all metrics:**

```bash
# View benchmark data
python tools/benchmark_code_quality.py --report
```

**The benchmark tool automatically captures:**
- Ruff Linting errors
- Black Format issues  
- Flake8 Style issues
- MyPy Type errors
- Vulture Dead Code issues
- Bandit Security issues
- **TOTAL ERRORS**

---

## ⚡ **PHASE 2: AUTO-FIXER**

### Step 2.1: Fix Automatically
```bash
# Option A: All at once (faster)
make fix

# Option B: Step by step (more educational)
python3 -m black .
python3 -m isort .
python3 -m ruff check . --fix
```

### Step 2.2: Observe Changes
```bash
# See what files were modified
git status

# See an example of changes (optional)
git diff src/cinema/movie.py
```

### Step 2.3: Verify it Works
```bash
# Run tests to ensure we didn't break anything
make test
```

---

## 📊 **PHASE 3: COMPARISON**

### Step 3.1: Record Post-Fix Benchmark
```bash
# Record post-autofix benchmark
make benchmark-post-autofix
```

### Step 3.2: Compare Results Automatically
**📝 The benchmark tool automatically compares results:**

```bash
# Compare all stages with a nice table
make benchmark-compare
```

**This automatically shows:**
- Before and after numbers for each tool
- Improvement percentages
- Total errors fixed
- Visual comparison table

### Step 3.3: View Detailed Report
```bash
# Generate comprehensive report
make benchmark-report
```

**The benchmark tool automatically calculates:**
- Improvement percentages for each metric
- Total errors fixed
- Stage-by-stage comparisons
- Overall improvement summary

---

## 🤖 **PHASE 4: AI AGENT**

### Step 4.1: Identify Remaining Errors
```bash
# See what errors remained
cat issues_to_fix_*.txt
```

### Step 4.2: Use AI Agent
**💬 Copy and paste these prompts in your AI agent:**

#### For type errors:
```
Analyze the file [filename.py] and fix the type errors 
that appear in the MyPy analysis. Explain each change you make.
```

#### For logic errors:
```
Review the file [filename.py] and improve the logic of functions 
that have problems. Explain why each change improves the code.
```

#### For optimization:
```
Optimize the file [filename.py] to improve performance 
and readability. Explain each optimization.
```

### Step 4.3: Apply Changes
1. **Review** the agent's suggestions
2. **Apply** the changes you consider correct
3. **Test** that the code still works:
   ```bash
   make test
   ```

---

## 📈 **PHASE 5: FINAL ANALYSIS**

### Step 5.1: Record Final Benchmark
```bash
# Record post-AI benchmark
make benchmark-post-ai
```

### Step 5.2: Complete Comparison
**📝 The benchmark tool automatically generates the complete comparison:**

```bash
# Generate final comprehensive report
make benchmark-report
```

**This automatically shows:**
- Complete phase-by-phase comparison
- Total improvement percentages
- Errors fixed at each stage
- Professional benchmark report

### Step 5.3: View Final Comparison Table
```bash
# Show final comparison table
make benchmark-compare
```

### Step 5.4: Reflection
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

## 🎯 **USEFUL COMMANDS DURING THE EXERCISE**

### Check project status:
```bash
make help          # See all available commands
make test          # Run tests
make lint          # Check quality
make format        # Format code
```

### Benchmarking commands:
```bash
make benchmark-initial      # Record initial state
make benchmark-post-autofix # Record after auto-fixer
make benchmark-post-ai      # Record after AI
make benchmark-compare      # Compare all stages
make benchmark-report       # Generate full report
make benchmark-full         # Run complete workflow
```

### See generated files:
```bash
ls -la *report*.txt     # See reports
ls -la issues_to_fix*.txt  # See fixable issues
ls -la benchmark_results.json  # See benchmark data
ls -la backup_before_fixes/  # See backups
```

### Compare changes:
```bash
git status         # See modified files
git diff           # See detailed changes
```

---

## 🆘 **TROUBLESHOOTING**

### If analysis fails:
```bash
# Check dependencies
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

### If AI agent doesn't respond well:
- **Be specific** in your prompts
- **Include the complete file** or specific function
- **Ask for explanations** of each change
- **Try different approaches** if it doesn't work

---

## 📚 **ADDITIONAL RESOURCES**

### Tool documentation:
- [Black](https://black.readthedocs.io/) - Formatter
- [Ruff](https://docs.astral.sh/ruff/) - Linter
- [MyPy](https://mypy.readthedocs.io/) - Type checker
- [Bandit](https://bandit.readthedocs.io/) - Security analysis

### Makefile commands:
```bash
make help          # See help
make install       # Install dependencies
make test          # Run tests
make lint          # Check quality
make format        # Format code
make analyze       # Complete analysis
make fix           # Auto-fixer
make clean         # Clean temporary files
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

**Congratulations on completing the exercise! 🎉**

*Remember: Code quality is a continuous process, not a destination.*
