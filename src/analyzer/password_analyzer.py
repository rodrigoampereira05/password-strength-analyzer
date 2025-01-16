from typing import Dict, Tuple, List, Optional
from .advanced_analyzer import AdvancedPasswordAnalyzer

class PasswordAnalyzer:
    """
    Main class for analyzing password strength and security
    Provides methods to check various password criteria and generate security reports    
    """

    def __init__(self):
        # Minimum requirements for a password
        self.min_length = 8
        self.min_uppercase = 1
        self.min_lowercase = 1
        self.min_numbers = 1
        self.min_special_chars = 1

        # List of special characters considered valid
        self.special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        self.advanced_analyzer = AdvancedPasswordAnalyzer()

    def check_length(self, password: str) -> Tuple[bool, int, str]:
        """
        Check if password meets minimum length requirements.
        """
        length = len(password)
        passed = length >= self.min_length

        # Calculate score: 1 point per 2 characters, max 5 points
        score = min(length // 2, 5)

        # Generate feedback message
        message = (
            f"Good length ({length} characters)" if passed
            else f"Password should be at least {self.min_length} characters long"
        )

        return passed, score, message

    def check_complexity(self, password: str) -> Dict[str, any]:
        """
        Analyze password complexity checking for different character types.
        """
        counts = {
            "uppercase": sum(1 for c in password if c.isupper()),
            "lowercase": sum(1 for c in password if c.islower()),
            "numbers": sum(1 for c in password if c.isdigit()),
            "special": sum(1 for c in password if c in self.special_chars)
        }

        passed = {
            "uppercase": counts["uppercase"] >= self.min_uppercase,
            "lowercase": counts["lowercase"] >= self.min_lowercase,
            "numbers": counts["numbers"] >= self.min_numbers,
            "special": counts["special"] >= self.min_special_chars
        }

        feedback = []
        if not passed["uppercase"]:
            feedback.append(f"Add at least {self.min_uppercase} uppercase letter(s)")
        if not passed["lowercase"]:
            feedback.append(f"Add at least {self.min_lowercase} lowercase letter(s)")
        if not passed["numbers"]:
            feedback.append(f"Add at least {self.min_numbers} number(s)")
        if not passed["special"]:
            feedback.append(f"Add at least {self.min_special_chars} special character(s)")

        score = sum(passed.values())

        return {
            "counts": counts,
            "passed": passed,
            "score": score,
            "feedback": feedback
        }

    def analyze_password(self, password: str) -> Dict[str, any]:
        """
        Perform complete password analysis.
        """
        # Get basic analysis
        length_passed, length_score, length_feedback = self.check_length(password)
        complexity_analysis = self.check_complexity(password)

        # Get advanced analysis
        advanced_results = self.advanced_analyzer.analyze(password)

        # Calculate total score
        total_score = length_score + complexity_analysis["score"]
    
        # Adjust score if password is common
        if advanced_results["is_common"]:
            total_score = max(total_score - 2, 0)

        # Determine strength
        strength = "Weak"
        if total_score >= 8:
            strength = "Strong"
        elif total_score >= 6:
            strength = "Moderate"

        # Combine all feedbacks
        feedback = []
        if not length_passed:
            feedback.append(length_feedback)
        # Add advanced feedback first
        feedback.extend(advanced_results["feedback"])
        # Then add complexity feedback
        feedback.extend(complexity_analysis["feedback"])

        return {
            "score": total_score,
            "strength": strength,
            "feedback": feedback,
            "is_common": advanced_results["is_common"],
            "keyboard_patterns": advanced_results["keyboard_patterns"],
            "details": {
                "length_score": length_score,
                "complexity_score": complexity_analysis["score"],
                "character_counts": complexity_analysis["counts"]
            }
        }