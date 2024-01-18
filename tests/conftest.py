"""Configuration set for tests."""
import pytest

from component_managers.astt_comp_manager import ASTTComponentManager


@pytest.fixture(scope="module")
def comp_manager_connected_to_antenna():
    """Estabilish connection and return the antenna node"""
    cm = ASTTComponentManager()
    cm.connect_to_network()
    cm.connect_to_plc_node()
    return cm
