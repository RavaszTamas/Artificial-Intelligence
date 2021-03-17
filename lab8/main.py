
import numpy as np
import matplotlib as mpl
from sklearn.model_selection import train_test_split
from repository import Repository
from controller import Controller
from ui import Console


        
if __name__ == "__main__":
    
    repository = Repository()
    controller = Controller(repository)
    console = Console(controller)
    console.run()
    
