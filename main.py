from gui import SensorGUI
from idk import DataGenerator
import threading
import signal
import tkinter as tk
from tkinter import *
import serial


def main():
    porta_uart = serial.Serial('COM4', baudrate=19200, timeout=0.01)

    root = tk.Tk()
    data_generator1 = DataGenerator(porta_uart)
    data_generator = threading.Thread(target=data_generator1.start_generating)
    data_generator.start()
    
    sensor_gui1 = SensorGUI(data_generator1, root, porta_uart)
    sensor_gui = threading.Thread(target=sensor_gui1.iniciar_gui) 
    sensor_gui.start()  
    Button(root, text="Quit", command=root.destroy).grid(row=2, column=6, sticky=W, pady=2)

    root.mainloop()
    sensor_gui1.stop() 

    data_generator1.stop()


if __name__ == "__main__":
    main()
