""" Tests for the generation of mode & states enums"""

import unittest

from src.component_managers.astt_comp_manager import (
    ASTTComponentManager,
)


class TestStatesModesGeneratiom(unittest.TestCase):

    def setUp(self):
        self.manager = ASTTComponentManager()

    def test_generated_mode_with_valid_input(self):
        """
        Use a valid value to test the creation of the mode.
        """
        generated_enum = self.manager.gen_mode_state_enums("Mode", 1)
        assert generated_enum.name == "POINT"

    def test_generated_mode_with_invalid_input(self):
        """
        Use an invalid value to test the creation of the mode.
        """
        generated_enum = self.manager.gen_mode_state_enums("Mode", 6)
        assert generated_enum is None

    def test_generated_func_state_with_valid_input(self):
        """
        Use a valid value to test the creation of the func state.
        """
        generated_enum = self.manager.gen_mode_state_enums(
            "FuncState", 0
        )
        assert generated_enum.name == "BRAKED"

    def test_generated_func_state_invalid_input(self):
        """
        Use an invalid value to test the creation of the func state.
        """
        generated_enum = self.manager.gen_mode_state_enums(
            "FuncState", 10
        )
        assert generated_enum is None

    def test_generated_stow_state_with_valid_input(self):
        """
        Use a valid value to test the creation of the stow state.
        """
        generated_enum = self.manager.gen_mode_state_enums(
            "StowPinState", 4
        )
        assert (
            generated_enum.name
            == "ENGAGED_NOT_RELEASED_NOT_STOW_WINDOW"
        )

    def test_generated_stow_state_invalid_input(self):
        """
        Use an invalid value to test the creation of the stow state.
        """
        generated_enum = self.manager.gen_mode_state_enums(
            "StowPinState", 13
        )
        assert generated_enum is None


if __name__ == "__main__":
    unittest.main()
