from Square import Square
from Threads import UserThread, VacuumThread
from Vacuum import Vacuum

def main():
    squareA = Square('A')
    squareB = Square('B')
    user_thread = UserThread(squareA, squareB)
    vacuum = Vacuum(locationSquare=squareA,isStupid=True)
    vacuum_thread = VacuumThread(user_thread, squareA, squareB, vacuum)
    user_thread.start()
    vacuum_thread.start()
    user_thread.join()
    vacuum_thread.join()

def on_button_click():
    print("Button clicked!")

main()