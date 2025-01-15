import argparse
from src.analyzer.password_analyzer import PasswordAnalyzer
from colorama import init, Fore, Style
import sys

def get_strength_color(strength: str) -> str:
    """Return color based on password strength"""
    colors = {
        "Weak": Fore.RED,
        "Moderate": Fore.YELLOW,
        "Strong": Fore.GREEN
    }
    return colors.get(strength, Fore.WHITE)

def main():
    """
    Main function to handle command line interface
    """
    # Initialize colorama
    init()

    # Create argument parser
    parser = argparse.ArgumentParser(
        description="Password Strength Analyzer - Check how secure your password is"
    )

    # Add arguments
    parser.add_argument(
        "password",
        help="Password to analyze"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed analysis"
    )

    # Parse arguments
    args = parser.parse_args()

    # Create analyzer and analyze password
    analyzer = PasswordAnalyzer()
    result = analyzer.analyze_password(args.password)

    # Get color based on strength
    strength_color = get_strength_color(result['strength'])

    # Print results
    print(f"\n{Fore.CYAN}Password Analysis Results:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}-------------------------{Style.RESET_ALL}")
    print(f"Strength: {strength_color}{result['strength']}{Style.RESET_ALL}")
    print(f"Score: {strength_color}{result['score']:.1f}/10{Style.RESET_ALL}")

    if result['feedback']:
        print(f"\n{Fore.CYAN}Suggestions for improvement:{Style.RESET_ALL}")
        for feedback in result['feedback']:
            print(f"{Fore.YELLOW}- {feedback}{Style.RESET_ALL}")

    if args.verbose:
        print(f"\n{Fore.CYAN}Detailed Analysis:{Style.RESET_ALL}")
        print(f"Length Score: {result['details']['length_score']}/5")
        print(f"Complexity Score: {result['details']['complexity_score']}/5")
        
        print(f"\n{Fore.CYAN}Character Counts:{Style.RESET_ALL}")
        for char_type, count in result['details']['character_counts'].items():
            if count > 0:
                print(f"{Fore.GREEN}- {char_type.capitalize()}: {count}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}- {char_type.capitalize()}: {count}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()

#To test
#python main.py "Senha123" -v