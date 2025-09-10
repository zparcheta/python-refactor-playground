#!/usr/bin/env python3
"""
Code Quality Benchmarking Tool
==============================

This tool automatically runs code quality analysis at different stages
and compares the results to show improvements over time.

Usage:
    python tools/benchmark_code_quality.py --stage initial
    python tools/benchmark_code_quality.py --stage post-autofix
    python tools/benchmark_code_quality.py --stage post-ai
    python tools/benchmark_code_quality.py --compare
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict


class CodeQualityBenchmark:
    def __init__(self, project_dir: str = "."):
        self.project_dir = Path(project_dir)
        self.benchmark_file = self.project_dir / "benchmark_results.json"
        self.results = self.load_benchmark_data()

    def load_benchmark_data(self) -> Dict:
        """Load existing benchmark data or create new structure."""
        if self.benchmark_file.exists():
            try:
                with open(self.benchmark_file) as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass

        return {
            "project": "Cinema Ticket Management System",
            "created": datetime.now().isoformat(),
            "stages": {},
        }

    def save_benchmark_data(self):
        """Save benchmark data to file."""
        with open(self.benchmark_file, "w") as f:
            json.dump(self.results, f, indent=2)

    def run_analysis(self) -> Dict[str, int]:
        """Run code quality analysis and extract metrics."""
        print("🔍 Running code quality analysis...")

        try:
            # Run the analysis
            result = subprocess.run(
                ["python", "tools/analyze_code_quality.py"],
                capture_output=True,
                text=True,
                cwd=self.project_dir,
                timeout=300,  # 5 minutes timeout
            )

            if result.returncode != 0:
                print(f"❌ Analysis failed: {result.stderr}")
                return {}

            # Extract metrics from output
            metrics = self.extract_metrics_from_output(result.stdout)
            return metrics

        except subprocess.TimeoutExpired:
            print("⏰ Analysis timed out")
            return {}
        except Exception as e:
            print(f"❌ Error running analysis: {e}")
            return {}

    def extract_metrics_from_output(self, output: str) -> Dict[str, int]:
        """Extract error counts from analysis output."""
        metrics = {}

        # Look for specific patterns in the output
        lines = output.split("\n")

        for line in lines:
            # Ruff errors
            if "RUFF:" in line and "issues" in line:
                try:
                    count = int(line.split()[1])
                    metrics["ruff_errors"] = count
                except (ValueError, IndexError):
                    pass

            # Black formatting issues
            elif "BLACK:" in line and "formatting issues" in line:
                try:
                    count = int(line.split()[1])
                    metrics["black_issues"] = count
                except (ValueError, IndexError):
                    pass

            # Flake8 issues
            elif "FLAKE8:" in line and "issues" in line:
                try:
                    count = int(line.split()[1])
                    metrics["flake8_issues"] = count
                except (ValueError, IndexError):
                    pass

            # MyPy errors
            elif "MYPY:" in line and "type errors" in line:
                try:
                    count = int(line.split()[1])
                    metrics["mypy_errors"] = count
                except (ValueError, IndexError):
                    pass

            # Vulture dead code
            elif "VULTURE:" in line and "dead code issues" in line:
                try:
                    count = int(line.split()[1])
                    metrics["vulture_issues"] = count
                except (ValueError, IndexError):
                    pass

            # Bandit security issues
            elif "BANDIT:" in line and "security issues" in line:
                try:
                    count = int(line.split()[1])
                    metrics["bandit_issues"] = count
                except (ValueError, IndexError):
                    pass

        return metrics

    def record_stage(self, stage_name: str, description: str = ""):
        """Record metrics for a specific stage."""
        print(f"📊 Recording stage: {stage_name}")

        metrics = self.run_analysis()

        if not metrics:
            print("❌ No metrics collected")
            return False

        # Calculate total errors
        total_errors = sum(metrics.values())
        metrics["total_errors"] = total_errors

        # Record the stage
        self.results["stages"][stage_name] = {
            "timestamp": datetime.now().isoformat(),
            "description": description,
            "metrics": metrics,
        }

        self.save_benchmark_data()

        print(f"✅ Stage '{stage_name}' recorded with {total_errors} total errors")
        return True

    def compare_stages(self) -> Dict:
        """Compare all recorded stages."""
        if len(self.results["stages"]) < 2:
            print("❌ Need at least 2 stages to compare")
            return {}

        stages = list(self.results["stages"].keys())
        comparison = {"stages_compared": stages, "improvements": {}, "summary": {}}

        # Compare each stage with the previous one
        for i in range(1, len(stages)):
            current_stage = stages[i]
            previous_stage = stages[i - 1]

            current_metrics = self.results["stages"][current_stage]["metrics"]
            previous_metrics = self.results["stages"][previous_stage]["metrics"]

            improvement = self.calculate_improvement(previous_metrics, current_metrics)
            comparison["improvements"][
                f"{previous_stage}_to_{current_stage}"
            ] = improvement

        # Calculate overall improvement
        if len(stages) >= 2:
            initial_metrics = self.results["stages"][stages[0]]["metrics"]
            final_metrics = self.results["stages"][stages[-1]]["metrics"]

            overall_improvement = self.calculate_improvement(
                initial_metrics, final_metrics
            )
            comparison["summary"]["overall_improvement"] = overall_improvement

        return comparison

    def calculate_improvement(
        self, before: Dict[str, int], after: Dict[str, int]
    ) -> Dict:
        """Calculate improvement between two sets of metrics."""
        improvement = {}

        for metric in before:
            if metric in after:
                before_val = before[metric]
                after_val = after[metric]

                if before_val > 0:
                    percentage = ((before_val - after_val) / before_val) * 100
                else:
                    percentage = 0

                improvement[metric] = {
                    "before": before_val,
                    "after": after_val,
                    "improvement": before_val - after_val,
                    "percentage": round(percentage, 2),
                }

        return improvement

    def generate_report(self) -> str:
        """Generate a comprehensive benchmark report."""
        if not self.results["stages"]:
            return "No benchmark data available."

        report = []
        report.append("🏆 CODE QUALITY BENCHMARK REPORT")
        report.append("=" * 50)
        report.append(f"Project: {self.results['project']}")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")

        # Show all stages
        report.append("📊 STAGES RECORDED:")
        report.append("-" * 30)

        for stage_name, stage_data in self.results["stages"].items():
            timestamp = datetime.fromisoformat(stage_data["timestamp"])
            metrics = stage_data["metrics"]
            total = metrics.get("total_errors", 0)

            report.append(f"• {stage_name.upper()}")
            report.append(f"  Time: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            report.append(f"  Total Errors: {total}")

            if stage_data["description"]:
                report.append(f"  Description: {stage_data['description']}")
            report.append("")

        # Show comparisons
        comparison = self.compare_stages()
        if comparison:
            report.append("📈 IMPROVEMENTS:")
            report.append("-" * 30)

            for comparison_name, improvement_data in comparison["improvements"].items():
                report.append(f"• {comparison_name.replace('_', ' ').title()}")

                for metric, data in improvement_data.items():
                    if metric != "total_errors":
                        continue

                    before = data["before"]
                    after = data["after"]
                    percentage = data["percentage"]

                    report.append(f"  Total Errors: {before} → {after}")
                    report.append(f"  Improvement: {percentage}%")
                    report.append("")

            # Overall summary
            if "overall_improvement" in comparison["summary"]:
                overall = comparison["summary"]["overall_improvement"]
                if "total_errors" in overall:
                    data = overall["total_errors"]
                    report.append("🎯 OVERALL SUMMARY:")
                    report.append("-" * 30)
                    report.append(f"Initial Errors: {data['before']}")
                    report.append(f"Final Errors: {data['after']}")
                    report.append(f"Total Improvement: {data['percentage']}%")
                    report.append(f"Errors Fixed: {data['improvement']}")

        return "\n".join(report)

    def print_comparison_table(self):
        """Print a nice comparison table."""
        if len(self.results["stages"]) < 2:
            print("❌ Need at least 2 stages to compare")
            return

        stages = list(self.results["stages"].keys())

        print("\n📊 BENCHMARK COMPARISON TABLE")
        print("=" * 80)

        # Header
        header = f"{'Metric':<20}"
        for stage in stages:
            header += f"{stage.upper():<15}"
        header += f"{'IMPROVEMENT':<15}"
        print(header)
        print("-" * 80)

        # Get all metrics
        all_metrics = set()
        for stage_data in self.results["stages"].values():
            all_metrics.update(stage_data["metrics"].keys())

        # Sort metrics with total_errors first
        sorted_metrics = ["total_errors"] + sorted(
            [m for m in all_metrics if m != "total_errors"]
        )

        for metric in sorted_metrics:
            if metric == "total_errors":
                metric_display = "TOTAL ERRORS"
            else:
                metric_display = metric.replace("_", " ").upper()

            row = f"{metric_display:<20}"

            # Get values for each stage
            values = []
            for stage in stages:
                value = self.results["stages"][stage]["metrics"].get(metric, 0)
                values.append(value)
                row += f"{value:<15}"

            # Calculate improvement
            if len(values) >= 2:
                initial = values[0]
                final = values[-1]
                if initial > 0:
                    improvement = ((initial - final) / initial) * 100
                    row += f"{improvement:.1f}%"
                else:
                    row += "0.0%"
            else:
                row += "N/A"

            print(row)

        print("-" * 80)


def main():
    parser = argparse.ArgumentParser(description="Code Quality Benchmarking Tool")
    parser.add_argument(
        "--stage",
        choices=["initial", "post-autofix", "post-ai"],
        help="Record metrics for a specific stage",
    )
    parser.add_argument("--description", default="", help="Description for the stage")
    parser.add_argument(
        "--compare", action="store_true", help="Compare all recorded stages"
    )
    parser.add_argument(
        "--report", action="store_true", help="Generate comprehensive report"
    )
    parser.add_argument("--table", action="store_true", help="Show comparison table")
    parser.add_argument(
        "--project-dir", default=".", help="Project directory (default: current)"
    )

    args = parser.parse_args()

    benchmark = CodeQualityBenchmark(args.project_dir)

    if args.stage:
        description = args.description or f"Stage: {args.stage}"
        success = benchmark.record_stage(args.stage, description)
        if success:
            print(f"✅ Stage '{args.stage}' recorded successfully")
        else:
            print(f"❌ Failed to record stage '{args.stage}'")
            sys.exit(1)

    if args.compare or args.report or args.table:
        if args.report:
            report = benchmark.generate_report()
            print(report)

        if args.table:
            benchmark.print_comparison_table()

        if args.compare and not args.report and not args.table:
            comparison = benchmark.compare_stages()
            if comparison:
                print(
                    "📊 Comparison completed. Use --report or --table for detailed output."
                )
            else:
                print("❌ No comparison data available")

    if not any([args.stage, args.compare, args.report, args.table]):
        parser.print_help()


if __name__ == "__main__":
    main()
