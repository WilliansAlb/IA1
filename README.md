# REPOSITORIO PARA INTELIGENCIA ARTIFICIAL 1
## PRÁCTICA 1 - CleanPractice
#### Problem
Una aspiradora inteligente vive en un mundo simple, dos cuadros A y B. La aspiradora puede percibir en que cuadro se encuentra. También puede percibir si el cuadro está sucio.

Puede elegir si se mueve a la derecha o izquierda, aspirar suciedad o no hacer nada.

Implemente un programa que represente a la aspiradora y su mundo. Y que el usuario pueda *ensuciar algún cuadrante* para que la aspiradora lo limpie.

Cree dos formas de comportamiento para la aspiradora: estúpida o inteligente

### Version 1
#### Tools
* Python 3.2.1
* Python Libraries: 
	- tkinter
	- threading
	- time
	- sys

#### How to run
1. Open a console on directory that contains *main.py*
2. Run the command, sending the mode for the vacuum cleaner (**1** if is not stupid)

```
python main.py [isCleaned]
```

3. Click over the square for dirtying and see what the vacuum do.

#### Modes

##### Stupid
The vacuum cleaner choose randomly between *clean*, *move* or *doing nothing*.

##### Intelligence
The vacuum cleaner checks if the square it is located in is not already clean for *clean* it, then *move* it to the another square.

### Version 2
#### Changes
Added a model for clean, this model waits 2 seconds in every square before changing position. For more information about the model, is already added the file _model.txt_ that contains all the information.

#### How to run
1. Open a console on directory _CleanPractice/v2_ that contains *main.py*
2. Run the command

```
python main.py
```

3. Click over the square for dirtying and see what the vacuum do.

## PRÁCTICA 2 - VendingPractice
### Tools
* Python 3.2.1
* Python Libraries: 
	- tkinter
	- threading
	- time
	- sys

### Problem
Modelar una máquina expendedora de refrescos como un agente reactivo simple. Este agente solo tiene un sensor que percibe cuando se ingresa una moneda o cuando se selecciona alguno de los 3 refrescos disponibles.

### How to run
1. Open a console on directory _VendingPractice_ that contains *main.py*
2. Run the command

```
python main.py
```

3. Click over the space for insert coin or an option of soda. Additional, is added a click area for get the sodas.