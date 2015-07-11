import board
import time

def main():
    while True:
        time.sleep(1)
        board.simulation_step()

if __name__ == '__main__':
    main()