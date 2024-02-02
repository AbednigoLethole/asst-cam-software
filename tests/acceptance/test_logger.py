"""Tests for the logging system"""
import os


def test_logs_are_cleared(cm_manager_connected_to_antnn):
    """Tests clear_all_logs function"""
    # It is expected that logs are written immediately
    cm_manager_connected_to_antnn.clear_all_logs()
    file_name = "app_dev.log"
    absolute_path = os.path.abspath(file_name)
    # when the file is cleared, the size becomes zero
    assert os.path.getsize(absolute_path) == 0
