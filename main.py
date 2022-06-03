import os
import sys

from Colors import Colors
from Repository import Repository
from Simulation import Simulation
from SimulationBuilder import SimulationBuilder
from VeloSim import VeloSim

if __name__ == '__main__':

    AsciArt = r"""
                  ______ _                 _        _____ _                 _       _             
                  | ___ (_)               | |      /  ___(_)               | |     | |            
                  | |_/ /_  ___ _   _  ___| | ___  \ `--. _ _ __ ___  _   _| | __ _| |_ ___  _ __ 
                  | ___ \ |/ __| | | |/ __| |/ _ \  `--. \ | '_ ` _ \| | | | |/ _` | __/ _ \| '__|
                  | |_/ / | (__| |_| | (__| |  __/ /\__/ / | | | | | | |_| | | (_| | || (_) | |   
                  \____/|_|\___|\__, |\___|_|\___| \____/|_|_| |_| |_|\__,_|_|\__,_|\__\___/|_|   
                                 __/ |                                                            
                                |___/     
                  """
    print(Colors.HEADER + AsciArt + Colors.ENDC)
    if len(sys.argv) > 1:
        if sys.argv[1] == '-s':
            if os.path.exists("Resources/Data/Stations.json") and os.path.exists(
                    "Resources/Data/Users.json") and os.path.exists("Resources/Data/Transporters.json"):
                repo = Repository()
                repo.load()
                sim = Simulation(30, 12)
                sim.start()
            else:
                builder = SimulationBuilder()
                builder.createsimulation()
                sim = Simulation(30, 12)
                sim.start()
    else:
        velo_sim = VeloSim()
        velo_sim.start()
