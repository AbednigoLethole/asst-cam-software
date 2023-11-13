from subprocess import PIPE, Popen, run

green = "\033[0;32m"
yellow = "\033[0;33m"


class SimulatorManager:
    def __init__(self):
        self.start_virtual_can = (
            "sudo -S sh startVirtualCANInterface.sh"
        )
        # self.docker_load = "docker load -i ubuntu_canopen.tar"
        self.docker_run = (
            "docker run -d --network=host astt-cam-software bash -c "
            "'cd src/antenna_simulator && sh compileSlave.sh && ./slave '"
        )

    def start_can_interface(self, password):
        print(yellow)
        # Start the Virtual CAN Interface
        proc = Popen(
            (self.start_virtual_can).split(),
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
        )
        proc.communicate(password.encode())
        return proc.returncode

    def run_contaier_and_startup_simulator(self):
        print(green)
        # Run the Docker container and start simulator
        # subprocess.run(self.docker_load, shell=True, check=True)

        run(self.docker_run, shell=True, check=True)


if __name__ == "__main__":
    simulator_manager = SimulatorManager()
    simulator_manager.start_can_interface("Mabejela@99")
    simulator_manager.run_contaier_and_startup_simulator()
