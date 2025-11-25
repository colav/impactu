"""
Test for the fixed authenticate_cvlac function to ensure proper browser cleanup.
"""

import unittest
from unittest.mock import patch, MagicMock, call
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the fixed function
from cvlac_auth_fix import authenticate_cvlac_fixed, _robust_browser_cleanup, _alternative_browser_cleanup


class TestAuthenticateCvlacFix(unittest.TestCase):
    """Test cases for the fixed authenticate_cvlac function."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.valid_params = {
            'nacionalidad': 'Colombiana',
            'nombres': 'Test User',
            'documento_identificacion': '12345678',
            'password': 'testpass123'
        }
    
    def test_input_validation(self):
        """Test that input validation works correctly."""
        # Test missing required fields
        result = authenticate_cvlac_fixed('', '', '', '')
        self.assertEqual(result['status'], 'error')
        self.assertIn('required', result['message'])
        
        # Test missing pais_nacimiento for foreign nationality
        result = authenticate_cvlac_fixed('Extranjero - otra', 'Test', '123', 'pass')
        self.assertEqual(result['status'], 'error')
        self.assertIn('pais_nacimiento is required', result['message'])
    
    @patch('time.sleep')
    def test_robust_browser_cleanup_retries(self, mock_sleep):
        """Test that robust cleanup retries when kill_browser fails."""
        with patch('cvlac_auth_fix.kill_browser') as mock_kill_browser:
            # Make kill_browser fail twice, then succeed
            mock_kill_browser.side_effect = [Exception("Kill failed"), Exception("Kill failed again"), None]
            
            # Call the cleanup function
            _robust_browser_cleanup(max_attempts=3, delay_between_attempts=0.1)
            
            # Verify it was called 3 times
            self.assertEqual(mock_kill_browser.call_count, 3)
            
            # Verify sleep was called between attempts
            self.assertEqual(mock_sleep.call_count, 2)
    
    @patch('cvlac_auth_fix._alternative_browser_cleanup')
    def test_robust_cleanup_calls_alternative_on_failure(self, mock_alternative_cleanup):
        """Test that alternative cleanup is called when all standard attempts fail."""
        with patch('cvlac_auth_fix.kill_browser') as mock_kill_browser:
            # Make kill_browser always fail
            mock_kill_browser.side_effect = Exception("Always fails")
            
            # Call the cleanup function
            _robust_browser_cleanup(max_attempts=2, delay_between_attempts=0.0)
            
            # Verify alternative cleanup was called
            mock_alternative_cleanup.assert_called_once()
    
    @patch('platform.system')
    @patch('subprocess.run')
    def test_alternative_cleanup_linux(self, mock_subprocess, mock_platform):
        """Test alternative cleanup on Linux systems."""
        mock_platform.return_value = "Linux"
        mock_subprocess.return_value = MagicMock()
        
        # Call alternative cleanup
        _alternative_browser_cleanup()
        
        # Verify subprocess was called for both chrome and chromedriver
        expected_calls = [
            call(["pkill", "-f", "chrome"], check=False, capture_output=True),
            call(["pkill", "-f", "chromedriver"], check=False, capture_output=True)
        ]
        mock_subprocess.assert_has_calls(expected_calls)
    
    @patch('platform.system')
    @patch('subprocess.run')
    def test_alternative_cleanup_windows(self, mock_subprocess, mock_platform):
        """Test alternative cleanup on Windows systems."""
        mock_platform.return_value = "Windows"
        mock_subprocess.return_value = MagicMock()
        
        # Call alternative cleanup
        _alternative_browser_cleanup()
        
        # Verify subprocess was called for both chrome and chromedriver
        expected_calls = [
            call(["taskkill", "/F", "/IM", "chrome.exe"], check=False, capture_output=True),
            call(["taskkill", "/F", "/IM", "chromedriver.exe"], check=False, capture_output=True)
        ]
        mock_subprocess.assert_has_calls(expected_calls)

if __name__ == '__main__':
    # Run the tests
    unittest.main()