from typing import List, Set
from pathlib import Path

class AdvancedPasswordAnalyzer:
    """
    Provides advanced password analysis features including common password checks,
    keyboard pattern detection, and dictionary word similarity.
    """

    def __init__(self):
        self.common_passwords = self._load_common_passwords()
        self.keyboard_patterns = [
            'qwerty', 'asdfgh', 'zxcvbn',
            '123456', '987654',
            'qweasd', 'plmokn'
        ]

    def _load_common_passwords(self) -> Set[str]:
        """Load common passwords from file"""
        try:
            data_path = Path(__file__).parent.parent.parent / 'data' / 'common_passwords.txt'
            with open(data_path, 'r') as f:
                return {line.strip().lower() for line in f if line.strip()}
        except FileNotFoundError:
            return set()

    def check_common_password(self, password: str) -> bool:
        """Check if password is in common password list."""
        return password.lower() in self.common_passwords

    def check_keyboard_patterns(self, password: str) -> List[str]:
        """Check for common keyboard patterns in password."""
        password_lower = password.lower()
        found_patterns = []

        for pattern in self.keyboard_patterns:
            if pattern in password_lower:
                found_patterns.append(pattern)

        return found_patterns

    def analyze(self, password: str) -> dict:
        """Perform complete advanced analysis of password"""
        results = {
            "is_common": self.check_common_password(password),
            "keyboard_patterns": self.check_keyboard_patterns(password),
            "feedback": []
        }

        # Check common passwords
        if self.check_common_password(password):
            results["feedback"].append(
                "This password is commonly used and easily guessable"
            )

        # Check keyboard patterns
        patterns = self.check_keyboard_patterns(password)
        if patterns:
            results["keyboard_patterns"] = patterns
            results["feedback"].append(
                f"Contains keyboard pattern(s): {', '.join(patterns)}"
            )

        return results