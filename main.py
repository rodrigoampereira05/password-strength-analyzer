"""
Password Strength Analyzer - Command Line Interface

This module provides a command-line interface for the password strength analyzer.
It features colored output, multiple analysis modes, and rich formatting.
"""

import argparse
import json
import sys
from typing import List, Dict
from pathlib import Path
from src.analyzer.password_analyzer import PasswordAnalyzer
from colorama import init, Fore, Style
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint

# Initialize rich console
console = Console()

def get_strength_color(strength: str) -> str:
    """Maps password strength levels to appropriate colors."""
    colors = {
        "Weak": Fore.RED,
        "Moderate": Fore.YELLOW,
        "Strong": Fore.GREEN
    }
    return colors.get(strength, Fore.WHITE)

def get_strength_emoji(strength: str) -> str:
    """Returns appropriate emoji for password strength."""
    emojis = {
        "Weak": "❌",
        "Moderate": "⚠️",
        "Strong": "✅"
    }
    return emojis.get(strength, "❓")

def analyze_multiple_passwords(passwords: List[str], analyzer: PasswordAnalyzer) -> List[Dict]:
    """Analyzes multiple passwords with a progress bar."""
    results = []
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True
    ) as progress:
        task = progress.add_task("[cyan]Analyzing passwords...", total=len(passwords))
        for password in passwords:
            result = analyzer.analyze_password(password)
            results.append({"password": password, "analysis": result})
            progress.advance(task)
    return results

def print_table_output(result: Dict, password: str):
    """Prints analysis results in a formatted table."""
    table = Table(title=f"Analysis Results for: {password}")
    
    table.add_column("Metric", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")
    
    strength_color = "red" if result["strength"] == "Weak" else "yellow" if result["strength"] == "Moderate" else "green"
    
    table.add_row("Strength", f"[{strength_color}]{result['strength']} {get_strength_emoji(result['strength'])}")
    table.add_row("Score", f"{result['score']:.1f}/10")
    
    # Character counts subtable
    counts = result["details"]["character_counts"]
    count_rows = []
    for char_type, count in counts.items():
        color = "green" if count > 0 else "red"
        count_rows.append(f"{char_type.capitalize()}: [{color}]{count}")
    
    table.add_row("Character Counts", "\n".join(count_rows))
    
    if result["feedback"]:
        table.add_row("Suggestions", "\n".join([f"• {f}" for f in result["feedback"]]))
    
    console.print(table)

def main():
    """Main function that handles the command-line interface."""
    init()  # Initialize colorama

    parser = argparse.ArgumentParser(
        description="Password Strength Analyzer - Check how secure your password is"
    )

    # Add arguments
    parser.add_argument(
        "password",
        nargs="*",
        help="Password(s) to analyze. Can provide multiple passwords."
    )
    
    parser.add_argument(
        "-f", "--file",
        type=Path,
        help="File containing passwords (one per line)"
    )
    
    parser.add_argument(
        "-j", "--json",
        action="store_true",
        help="Output results in JSON format"
    )
    
    parser.add_argument(
        "-s", "--silent",
        action="store_true",
        help="Show only basic results without formatting"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed analysis"
    )

    args = parser.parse_args()
    analyzer = PasswordAnalyzer()
    passwords = []

    # Collect passwords from arguments and/or file
    if args.file:
        try:
            with open(args.file, 'r') as f:
                passwords.extend([line.strip() for line in f if line.strip()])
        except Exception as e:
            console.print(f"[red]Error reading file: {e}")
            sys.exit(1)
    
    passwords.extend(args.password)

    if not passwords:
        parser.print_help()
        sys.exit(1)

    # Analyze passwords
    results = analyze_multiple_passwords(passwords, analyzer)

    # Output results
    if args.json:
        print(json.dumps(results, indent=2))
    elif args.silent:
        for result in results:
            print(f"{result['password']}: {result['analysis']['strength']} ({result['analysis']['score']:.1f}/10)")
    else:
        for result in results:
            print_table_output(result["analysis"], result["password"])
            print()

if __name__ == "__main__":
    main()