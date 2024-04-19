from Visual import Visual
from DataVisual import DataVisual
from Generational import Generational
import pickle

if __name__ == "__main__":
    generational = Generational()
    #dataVisual = DataVisual()
    #visual = Visual(dataVisual, generational)
    with open('test2.pkl', 'rb') as file:
        generational.nodes = pickle.load(file)
    generational.runModel()