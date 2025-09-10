#!/usr/bin/env python3
"""
Code Quality Analysis Script - Single Report
============================================

This script runs multiple code quality analysis tools and generates
a single comprehensive report file.

Usage:
    python analyze_code_quality.py
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path


class CodeQualityAnalyzer:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.report_file = f"code_quality_report_{self.timestamp}.txt"
        self.fixes_file = f"issues_to_fix_{self.timestamp}.txt"
        self.report_content = []
        self.fixable_issues = []

    def add_to_report(self, section_name, content, description=""):
        """Add content to the report."""
        self.report_content.append(f"\n{'='*20} {section_name.upper()} {'='*20}")
        if description:
            # Wrap description to max 80 characters
            wrapped_desc = self.wrap_text(description, 80)
            self.report_content.append(f"\nDESCRIPTION: {wrapped_desc}")
            self.report_content.append("")
        self.report_content.append(content)

    def wrap_text(self, text, max_length):
        """Wrap text to specified maximum length."""
        if len(text) <= max_length:
            return text

        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            if len(current_line + " " + word) <= max_length:
                if current_line:
                    current_line += " " + word
                else:
                    current_line = word
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return "\n".join(lines)

    def run_command(self, command, tool_name):
        """Run a command and add results to report."""
        try:
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True, timeout=30
            )

            content = f"Command: {command}\n"
            content += f"Return code: {result.returncode}\n"
            content += f"Timestamp: {datetime.now()}\n\n"

            if result.stdout:
                # Count issues and files affected
                lines = result.stdout.splitlines()
                issue_count = len(
                    [
                        line
                        for line in lines
                        if line.strip()
                        and not line.startswith("---")
                        and not line.startswith("+++")
                        and not line.startswith("@@")
                    ]
                )

                # Count unique files affected
                files_affected = set()
                for line in lines:
                    if (
                        line.startswith("./")
                        or line.startswith("src/")
                        or line.startswith("cinema_manager.py")
                        or line.startswith("main.py")
                        or line.startswith("movie.py")
                        or line.startswith("ticket.py")
                    ):
                        if ":" in line:
                            file_name = line.split(":")[0]
                            files_affected.add(file_name)

                content += "SUMMARY:\n"
                content += f"- Total issues found: {issue_count}\n"
                content += f"- Files affected: {len(files_affected)}\n"
                if files_affected:
                    content += f"- Files: {', '.join(sorted(files_affected))}\n"

                # Special handling for coverage report
                if tool_name == "COVERAGE REPORT":
                    for line in lines:
                        if "TOTAL" in line and "%" in line:
                            parts = line.split()
                            for part in parts:
                                if part.endswith("%"):
                                    content += f"- Coverage: {part}\n"
                                    break

                content += "\n"

            if result.stderr and result.returncode != 0:
                content += f"ERRORS: {result.stderr[:200]}...\n\n"

            # Get description for the tool
            description = self.get_tool_description(tool_name)
            self.add_to_report(tool_name, content, description)
            
            # Detect fixable issues from this tool's output
            self.detect_fixable_issues(tool_name, result)

            return result

        except subprocess.TimeoutExpired:
            description = self.get_tool_description(tool_name)
            self.add_to_report(tool_name, f"Command timed out: {command}", description)
            return None
        except Exception as e:
            description = self.get_tool_description(tool_name)
            self.add_to_report(tool_name, f"Error: {e}", description)
            return None

    def get_tool_description(self, tool_name):
        """Get description of what each tool does."""
        descriptions = {
            "CYCLOMATIC COMPLEXITY": "Measures code complexity by counting decision points. "
            + "Higher complexity = harder to maintain.",
            "MAINTAINABILITY INDEX": "Calculates how easy it is to maintain code (0-100 scale). "
            + "Higher = more maintainable.",
            "RAW METRICS": "Basic code metrics: lines of code, comments, functions, classes.",
            "RUFF LINTING": "Fast Python linter that checks for code style issues and bugs.",
            "BLACK FORMATTING": "Code formatter that enforces consistent Python code style.",
            "ISORT IMPORTS": "Sorts and organizes Python import statements according to PEP8.",
            "PYLINT": "Comprehensive Python code analyzer that checks for errors and "
            + "enforces coding standards.",
            "FLAKE8": "Python style guide checker that combines pycodestyle, pyflakes, "
            + "and mccabe complexity checker.",
            "MYPY TYPE CHECKING": "Static type checker that finds type errors and enforces "
            + "type annotations in Python code.",
            "BANDIT SECURITY": "Security linter that scans Python code for common security "
            + "vulnerabilities.",
            "SAFETY DEPENDENCIES": "Checks for known security vulnerabilities in Python "
            + "dependencies and packages.",
            "PIP-AUDIT": "Audits Python packages for known security vulnerabilities using "
            + "the Python Packaging Advisory Database.",
            "DEPTRY DEPENDENCIES": "Finds unused dependencies, missing dependencies, and "
            + "transitive dependencies in Python projects.",
            "VULTURE DEAD CODE": "Finds unused code (dead code) like unused variables, "
            + "functions, classes, and imports.",
            "SCALENE PERFORMANCE": "High-performance CPU and memory profiler for Python code "
            + "to identify bottlenecks.",
            "COVERAGE RUN": "Runs the application and tracks which lines of code are "
            + "executed during testing.",
            "COVERAGE REPORT": "Shows test coverage statistics - what percentage of code "
            + "is tested by unit tests.",
        }
        return descriptions.get(tool_name, "Code quality analysis tool.")

    def analyze_complexity(self):
        """Analyze code complexity using radon."""
        print("COMPLEXITY METRICS:")

        # Cyclomatic complexity
        result = self.run_command(
            "python3 -m radon cc -s -a .", "CYCLOMATIC COMPLEXITY"
        )
        if result and result.stdout:
            print(result.stdout)
        else:
            print("RADON: Tool not available")

        # Maintainability index
        result = self.run_command("python3 -m radon mi -s .", "MAINTAINABILITY INDEX")
        if result and result.stdout:
            print(result.stdout)

        # Raw metrics
        result = self.run_command("python3 -m radon raw -s .", "RAW METRICS")
        if result and result.stdout:
            print(result.stdout)

    def analyze_linting(self):
        """Analyze code style and linting issues."""
        print("\nLINTING ISSUES:")

        # Ruff linting
        result = self.run_command("python3 -m ruff check .", "RUFF LINTING")
        if result and result.stdout:
            issues_count = len(result.stdout.splitlines())
            print(f"RUFF: {issues_count} issues")
            print(result.stdout)

        # Black formatting check
        result = self.run_command(
            "python3 -m black --check --diff .", "BLACK FORMATTING"
        )
        if result and result.stdout:
            issues_count = len(result.stdout.splitlines())
            print(f"BLACK: {issues_count} formatting issues")
            print(result.stdout)

        # isort import sorting check
        result = self.run_command(
            "python3 -m isort --check-only --diff .", "ISORT IMPORTS"
        )
        if result and result.stdout:
            issues_count = len(result.stdout.splitlines())
            print(f"ISORT: {issues_count} import issues")
            print(result.stdout)

        # Pylint analysis
        result = self.run_command("python3 -m pylint src/ tests/ main.py", "PYLINT")
        if result and result.stdout:
            issues_count = len(result.stdout.splitlines())
            print(f"PYLINT: {issues_count} issues")
            print(result.stdout)

        # Flake8 analysis
        result = self.run_command("python3 -m flake8 .", "FLAKE8")
        if result and result.stdout:
            issues_count = len(result.stdout.splitlines())
            print(f"FLAKE8: {issues_count} issues")
            print(result.stdout)

    def analyze_types(self):
        """Analyze type checking issues."""
        print("\nTYPE ERRORS:")

        # MyPy type checking
        result = self.run_command("python3 -m mypy .", "MYPY TYPE CHECKING")
        if result and result.stdout:
            issues_count = len(result.stdout.splitlines())
            print(f"MYPY: {issues_count} type errors")
            print(result.stdout)

    def analyze_security(self):
        """Analyze security vulnerabilities."""
        print("\nSECURITY ISSUES:")

        # Bandit security analysis
        result = self.run_command("python3 -m bandit -r .", "BANDIT SECURITY")
        if result and result.stdout:
            issues_count = len(result.stdout.splitlines())
            print(f"BANDIT: {issues_count} security issues")
            print(result.stdout)

        # Safety dependency vulnerabilities
        result = self.run_command("python3 -m safety scan", "SAFETY DEPENDENCIES")
        if result and result.stdout:
            issues_count = len(result.stdout.splitlines())
            print(f"SAFETY: {issues_count} dependency issues")
            print(result.stdout)

        # pip-audit
        result = self.run_command("python3 -m pip_audit", "PIP-AUDIT")
        if result and result.stdout:
            issues_count = len(result.stdout.splitlines())
            print(f"PIP-AUDIT: {issues_count} vulnerabilities")
            print(result.stdout)

    def analyze_dependencies(self):
        """Analyze dependency issues."""
        print("\nDEPENDENCY ISSUES:")

        # Deptry dependency analysis
        result = self.run_command("python3 -m deptry .", "DEPTRY DEPENDENCIES")
        if result and result.stdout:
            issues_count = len(result.stdout.splitlines())
            print(f"DEPTRY: {issues_count} dependency issues")
            print(result.stdout)

        # Vulture dead code analysis
        result = self.run_command("python3 -m vulture .", "VULTURE DEAD CODE")
        if result and result.stdout:
            issues_count = len(result.stdout.splitlines())
            print(f"VULTURE: {issues_count} dead code issues")
            print(result.stdout)

    def analyze_performance(self):
        """Analyze performance bottlenecks."""
        print("\nPERFORMANCE METRICS:")

        # Scalene performance profiler
        try:
            result = self.run_command(
                "timeout 10s python3 -m scalene main.py || true", "SCALENE PERFORMANCE"
            )
            if result and result.stdout:
                print("SCALENE: Performance profiling completed")
                print(result.stdout)
        except:
            print("SCALENE: Profiling interrupted")

    def analyze_coverage(self):
        """Analyze test coverage."""
        print("\nTEST COVERAGE:")

        # Coverage analysis
        self.run_command(
            "python3 -m coverage run --source=src tests/test_cinema.py", "COVERAGE RUN"
        )

        result = self.run_command("python3 -m coverage report", "COVERAGE REPORT")
        if result and result.stdout:
            print("COVERAGE REPORT:")
            print(result.stdout)

            # Extract coverage percentage from the report
            lines = result.stdout.splitlines()
            for line in lines:
                if "TOTAL" in line and "%" in line:
                    # Extract percentage from line like "TOTAL                       407    210    48%"
                    parts = line.split()
                    for part in parts:
                        if part.endswith("%"):
                            coverage_pct = part
                            print(f"COVERAGE: {coverage_pct}")
                            break

    def save_report(self):
        """Save the complete report to a single file."""
        with open(self.report_file, "w", encoding="utf-8") as f:
            f.write("CODE QUALITY ANALYSIS REPORT\n")
            f.write("=" * 50 + "\n")
            f.write("Project: Cinema Ticket Management System\n")
            f.write(f"Analysis Date: {datetime.now()}\n")
            f.write(f"Report File: {self.report_file}\n")
            f.write("\n")
            f.write("This report contains comprehensive code quality metrics\n")
            f.write("for educational refactoring purposes.\n")

            for content in self.report_content:
                f.write(content)

        print(f"\nREPORT SAVED: {self.report_file}")

    def add_fixable_issue(self, tool_name, issue_type, description, fix_command):
        """Add a fixable issue to the list."""
        self.fixable_issues.append({
            'tool': tool_name,
            'type': issue_type,
            'description': description,
            'fix_command': fix_command
        })

    def detect_fixable_issues(self, tool_name, result):
        """Detect fixable issues from tool output."""
        if not result or not result.stdout:
            return

        output = result.stdout
        
        # Capture ALL output for each tool - students need to see everything
        if tool_name == "RUFF":
            if output.strip():
                self.add_fixable_issue(
                    "ruff",
                    "linting",
                    f"Ruff found issues (see full output below)",
                    "ruff check --fix ."
                )
                # Store full output for detailed display
                self.add_fixable_issue(
                    "ruff",
                    "detailed_output",
                    f"FULL RUFF OUTPUT:\n{output[:2000]}...",  # Limit to 2000 chars
                    "ruff check --fix ."
                )

        elif tool_name == "BLACK":
            if output.strip():
                self.add_fixable_issue(
                    "black",
                    "formatting",
                    f"Black found formatting issues (see full output below)",
                    "black ."
                )
                self.add_fixable_issue(
                    "black",
                    "detailed_output",
                    f"FULL BLACK OUTPUT:\n{output[:2000]}...",
                    "black ."
                )

        elif tool_name == "ISORT":
            if output.strip():
                self.add_fixable_issue(
                    "isort",
                    "import_sorting",
                    f"Isort found import issues (see full output below)",
                    "isort ."
                )
                self.add_fixable_issue(
                    "isort",
                    "detailed_output",
                    f"FULL ISORT OUTPUT:\n{output[:2000]}...",
                    "isort ."
                )

        elif tool_name == "PYLINT":
            if output.strip():
                # Count issues for summary
                lines = output.split('\n')
                issue_count = 0
                for line in lines:
                    if ": " in line and any(code in line for code in ["C0", "R0", "W0"]):
                        issue_count += 1
                
                self.add_fixable_issue(
                    "pylint",
                    "code_quality",
                    f"Pylint found {issue_count} code quality issues (see full output below)",
                    "pylint --disable=all --enable=C,R,W src/ tests/ main.py"
                )
                self.add_fixable_issue(
                    "pylint",
                    "detailed_output",
                    f"FULL PYLINT OUTPUT:\n{output[:2000]}...",
                    "pylint --disable=all --enable=C,R,W src/ tests/ main.py"
                )

        elif tool_name == "FLAKE8":
            if output.strip():
                # Count issues for summary - count lines that contain error codes (E, W, F followed by numbers)
                import re
                issue_count = len(re.findall(r'[EWF]\d+', output))
                
                self.add_fixable_issue(
                    "flake8",
                    "style",
                    f"Flake8 found {issue_count} style and syntax issues (see full output below)",
                    "flake8 --select=E,W,F src/ tests/ main.py"
                )
                self.add_fixable_issue(
                    "flake8",
                    "detailed_output",
                    f"FULL FLAKE8 OUTPUT:\n{output[:2000]}...",
                    "flake8 --select=E,W,F src/ tests/ main.py"
                )

        elif tool_name == "MYPY":
            if output.strip():
                # Count errors for summary
                import re
                error_count = len(re.findall(r"error:", output))
                
                self.add_fixable_issue(
                    "mypy",
                    "type_checking",
                    f"MyPy found {error_count} type checking errors (see full output below)",
                    "mypy src/ tests/ main.py"
                )
                self.add_fixable_issue(
                    "mypy",
                    "detailed_output",
                    f"FULL MYPY OUTPUT:\n{output[:2000]}...",
                    "mypy src/ tests/ main.py"
                )

        elif tool_name == "VULTURE":
            if output.strip():
                # Count unused items for summary
                lines = output.split('\n')
                unused_count = 0
                for line in lines:
                    if "unused" in line.lower() and ":" in line:
                        unused_count += 1
                
                self.add_fixable_issue(
                    "vulture",
                    "dead_code",
                    f"Vulture found {unused_count} unused code issues (see full output below)",
                    "vulture src/ tests/ main.py --min-confidence 60"
                )
                self.add_fixable_issue(
                    "vulture",
                    "detailed_output",
                    f"FULL VULTURE OUTPUT:\n{output[:2000]}...",
                    "vulture src/ tests/ main.py --min-confidence 60"
                )

    def save_fixable_issues(self):
        """Save fixable issues to a separate file."""
        if not self.fixable_issues:
            print("No fixable issues detected.")
            return

        with open(self.fixes_file, "w", encoding="utf-8") as f:
            f.write("ISSUES TO FIX - AUTOMATED TOOLS CAN HELP\n")
            f.write("=" * 50 + "\n")
            f.write("This file contains issues that can be automatically fixed\n")
            f.write("using various Python code quality tools.\n")
            f.write(f"Generated: {datetime.now()}\n\n")
            
            f.write("EDUCATIONAL NOTES FOR STUDENTS:\n")
            f.write("-" * 30 + "\n")
            f.write("These tools can automatically fix many common code quality issues.\n")
            f.write("Learning to use them effectively is a key skill for Python developers.\n\n")
            
            # Group by tool
            tools = {}
            for issue in self.fixable_issues:
                tool = issue['tool']
                if tool not in tools:
                    tools[tool] = []
                tools[tool].append(issue)
            
            for tool, issues in tools.items():
                # Separate summary and detailed issues
                summary_issues = [i for i in issues if i['type'] != 'detailed_output']
                detailed_issues = [i for i in issues if i['type'] == 'detailed_output']
                
                f.write(f"\n{tool.upper()} ISSUES ({len(summary_issues)} found):\n")
                f.write("-" * 20 + "\n")
                
                # Show summary issues
                for issue in summary_issues:
                    f.write(f"• {issue['description']}\n")
                
                # Show detailed output if available
                for issue in detailed_issues:
                    f.write(f"\n{issue['description']}\n")
                
                # Add fix command for this tool
                if summary_issues:
                    fix_cmd = summary_issues[0]['fix_command']
                    f.write(f"\nFix command: {fix_cmd}\n")
                    f.write(f"Alternative: make fix-{tool.lower()}\n")
            
            f.write("\n" + "=" * 50 + "\n")
            f.write("QUICK FIX OPTIONS:\n")
            f.write("=" * 50 + "\n")
            f.write("1. Fix all automatically: make fix\n")
            f.write("2. Fix specific tool: make fix-<tool>\n")
            f.write("3. Run individual commands above\n")
            f.write("4. Use auto_code_fixer_libraries_only.py\n\n")
            
            f.write("LEARNING OBJECTIVES:\n")
            f.write("-" * 20 + "\n")
            f.write("• Understand what each tool can fix automatically\n")
            f.write("• Learn when to use automated vs manual fixes\n")
            f.write("• Practice using professional development tools\n")
            f.write("• Compare before/after code quality metrics\n")

        print(f"\nFIXABLE ISSUES SAVED: {self.fixes_file}")
        print(f"Found {len(self.fixable_issues)} fixable issues")

    def run_full_analysis(self):
        """Run the complete code quality analysis."""
        print("CODE QUALITY ANALYSIS")
        print(f"Report: {self.report_file}")
        print(f"Time: {self.timestamp}")

        # Run all analyses
        self.analyze_complexity()
        self.analyze_linting()
        self.analyze_types()
        self.analyze_security()
        self.analyze_dependencies()
        self.analyze_performance()
        self.analyze_coverage()

        # Save single report
        self.save_report()
        
        # Save fixable issues
        self.save_fixable_issues()


def main():
    """Main function to run the code quality analysis."""
    print("CODE QUALITY ANALYSIS TOOL")
    print("Analyzing cinema ticket system...")

    # Check if we're in the right directory
    if not Path("main.py").exists():
        print("ERROR: main.py not found")
        sys.exit(1)

    analyzer = CodeQualityAnalyzer()

    try:
        analyzer.run_full_analysis()
    except KeyboardInterrupt:
        print("\nAnalysis interrupted")
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
