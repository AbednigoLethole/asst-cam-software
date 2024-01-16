"""Configuration set for tests."""
import pytest

from component_managers.astt_comp_manager import ASTTComponentManager


@pytest.fixture
def antenna_comp_manager():
    """Returns an instance of antenna comp manager"""
    cm = ASTTComponentManager()
    return cm


@pytest.fixture
def antenna_node(antenna_comp_manager):
    """Estabilish connection and return the atenna node"""
    antenna_comp_manager.connect_to_network()
    node2 = antenna_comp_manager.connect_to_plc_node()
    return node2
