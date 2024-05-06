from Visual import Visual
from DataVisual import DataVisual
from Generational import Generational

if __name__ == "__main__":
    generational = Generational()
    dataVisual = DataVisual()
    visual = Visual(dataVisual, generational)