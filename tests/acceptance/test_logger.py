"""Tests for the logging system."""

import os


def test_logs_are_cleared(cm_manager_connected_to_antnn):
    """Test if clear_all_logs gets logged."""
    # It is expected that logs are written immediately
    cm_manager_connected_to_antnn.clear_all_logs()
    file_name = "app_dev.log"
    absolute_path = os.path.abspath(file_name)
    # When the file is cleared, the size becomes zero
    assert os.path.getsize(absolute_path) == 0
