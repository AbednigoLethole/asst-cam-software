"""Configuration set for tests."""

from component_managers.astt_comp_manager import ASTTComponentManager
import pytest


@pytest.fixture(scope="module")
def cm_manager_connected_to_antnn():
    """Estabilish connection and return the antenna node"""

    # testing ASTT Token

    cm = ASTTComponentManager()
    cm.connect_to_network()
    cm.connect_to_plc_node()
    return cm
