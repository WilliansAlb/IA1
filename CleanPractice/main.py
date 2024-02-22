from Square import Square
from Threads import UserThread, VacuumThread
from Vacuum import Vacuum
import sys

def main():
    isStupid = True if sys.argv[1] == 1 else False
    squareA = Square('A')
    squareB = Square('B')
    user_thread = UserThread(squareA, squareB)
    vacuum = Vacuum(locationSquare=squareA,isStupid=isStupid)
    vacuum_thread = VacuumThread(user_thread, squareA, squareB, vacuum)
    user_thread.start()
    vacuum_thread.start()
    user_thread.join()
    vacuum_thread.join()

main()