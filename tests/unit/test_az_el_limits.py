"""Tests for AZ/EL limits"""

import unittest

from src.component_managers.astt_comp_manager import ASTTComponentManager


class TestAzElLimits(unittest.TestCase):
    def setUp(self):
        """Initialize the cm for reuse"""
        self.cm = ASTTComponentManager()

    def test_az_in_range(self):
        """Test with input in range of [-127,127]"""
        self.assertTrue(self.cm.is_az_allowed(45.0))

    def test_az_out_of_range(self):
        """Test with input out of range of [-127,127]"""
        self.assertFalse(self.cm.is_az_allowed(-128.0))

    def test_el_in_range(self):
        """Test with input in range of [-15,92]"""
        self.assertTrue(self.cm.is_el_allowed(-2.0))

    def test_el_out_of_range(self):
        """Test with input out of range of [-15,92]"""
        self.assertFalse(self.cm.is_el_allowed(95.0))


if __name__ == "__main__":
    unittest.main()
