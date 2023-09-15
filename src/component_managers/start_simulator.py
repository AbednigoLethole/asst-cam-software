import subprocess

green   = "\033[0;32m"
yellow  = "\033[0;33m"

class SimulatorManager:
    def __init__(self):
        self.start_virtual_can = "./startVirtualCANInterface.sh"
        #self.docker_load = "docker load -i ubuntu_canopen.tar"
        self.docker_run = "docker run -it --network=host ubuntu_canopen bash -c 'cd simulator && ./slave && exec bash'"
        
    def start_can_interface(self):
        print(yellow)
        # Start the Virtual CAN Interface
        subprocess.run(self.start_virtual_can, shell=True, check=True)
        print("CANopen interface has started.")
        
    def run_contaier_and_startup_simulator(self):
        print(green)
        # Run the Docker container and start simulator 
        #subprocess.run(self.docker_load, shell=True, check=True)

        subprocess.run(self.docker_run, shell=True, check=True)

if __name__ == "__main__":

    simulator_manager = SimulatorManager()
    simulator_manager.start_can_interface()
    simulator_manager.run_contaier_and_startup_simulator()