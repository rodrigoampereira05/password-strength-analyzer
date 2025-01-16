import pytest
from src.analyzer.password_analyzer import PasswordAnalyzer

class TestPasswordAnalyzer:
    """
    Test suite for the PasswordAnalyzer class.
    Tests all main functionalities and edge cases.
    """

    @pytest.fixture
    def analyzer(self):
        """
        Fixture that provides a fresh PasswordAnalyzer instance for each test
        """
        return PasswordAnalyzer()

    def test_check_length_valid(self, analyzer):
        """Test password with valid length"""
        password = "password123"  # 11 characters
        passed, score, feedback = analyzer.check_length(password)
        assert passed is True
        assert score == 5  # Max score is 5
        assert "Good length" in feedback

    def test_check_length_invalid(self, analyzer):
        """Test password with invalid length"""
        password = "pass"  # 4 characters
        passed, score, feedback = analyzer.check_length(password)
        assert passed is False
        assert score == 2  # 4 characters = 2 points
        assert "should be at least" in feedback

    def test_check_complexity_strong(self, analyzer):
        """Test password with all complexity requirements"""
        password = "TestPass123!"
        result = analyzer.check_complexity(password)

        assert result["counts"]["uppercase"] >= analyzer.min_uppercase
        assert result["counts"]["lowercase"] >= analyzer.min_lowercase
        assert result["counts"]["numbers"] >= analyzer.min_numbers
        assert result["counts"]["special"] >= analyzer.min_special_chars
        assert len(result["feedback"]) == 0  # No feedback needed
        assert result["score"] == 4  # All criteria met

    def test_check_complexity_weak(self, analyzer):
        """Test password with missing complexity requirements"""
        password = "onlyletters"
        result = analyzer.check_complexity(password)

        assert result["counts"]["uppercase"] == 0
        assert result["counts"]["numbers"] == 0
        assert result["counts"]["special"] == 0
        assert len(result["feedback"]) > 0  # Should have feedback
        assert result["score"] < 4  # Not all criteria met

    def test_analyze_password_strong(self, analyzer):
        """Test complete analysis of a strong password"""
        password = "SecureP@ss123"
        result = analyzer.analyze_password(password)

        assert result["strength"] == "Strong"
        assert result["score"] >= 8
        assert len(result["feedback"]) == 0

    def test_analyze_password_weak(self, analyzer):
        """Test complete analysis of a weak password"""
        password = "weak"
        result = analyzer.analyze_password(password)  # Corrigido aqui

        assert result["strength"] == "Weak"
        assert result["score"] < 6
        assert len(result["feedback"]) > 0

    def test_empty_password(self, analyzer):
        """Test analysis of an empty password"""
        result = analyzer.analyze_password("")
        assert result["strength"] == "Weak"
        assert result["score"] == 0
        assert len(result["feedback"]) > 0

    def test_special_characters_only(self, analyzer):
        """Test password with only special characters"""
        password = "@#$%^&*"
        result = analyzer.analyze_password(password)
        assert "lowercase" in str(result["feedback"])
        assert "uppercase" in str(result["feedback"])
        assert "number(s)" in str(result["feedback"])

    def test_common_password(self, analyzer):
        """Test common password"""
        result = analyzer.analyze_password("password123")
        assert result["is_common"] is True
        assert "commonly used" in result["feedback"][0]
    
    def test_keyboard_pattern(self, analyzer):
        """Test password with a keyboard pattern"""
        result = analyzer.analyze_password("qwerty123")
        assert "qwerty" in result["keyboard_patterns"]
        assert "keyboard pattern" in result["feedback"][0]

    def test_strong_password(self, analyzer):
        """Test password with strong password criteria"""
        result = analyzer.analyze_password("K9$mP2#vL5")
        assert result["is_common"] is False
        assert len(result["keyboard_patterns"]) == 0
        assert len(result["feedback"]) == 0