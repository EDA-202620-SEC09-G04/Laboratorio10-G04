import sys
import threading

from App import view as view


# Main function
def main():
    view.main()


# Main function call to run the program
if __name__ == '__main__':
    threading.stack_size(67108864)
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=main)
    thread.start()
