from component_managers.start_simulator import SimulatorManager


def test_start_can_interface_unhappy_path():
    # Test against the unhappy path
    sm = SimulatorManager()
    result = sm.start_can_interface("123")
    assert result == 1
