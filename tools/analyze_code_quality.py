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
        self.report_content = []

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
