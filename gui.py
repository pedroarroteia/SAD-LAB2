import tkinter as tk
from idk import DataGenerator
import threading
import time
from time import sleep
from tkinter import *
import json
from tkinter import * 
from tkinter.ttk import *
from tkinter import scrolledtext

class SensorGUI:
    def __init__(self, dg, root, pa):
        self.porta_uart = pa
        self.data_generator = dg
        self.root = root

        self.PedroCachorro = True

        root.geometry("1400x1200")
        self.root.title("Central de Comando")

        # Criação dos widgets
        l1 = Label(self.root, text="Envio de Comandos:")
        l1.grid(row=0, column=0, sticky=W, pady=2)

        l2 = Label(self.root, text="Ativar/Desativar Canais de Amostragem:")
        l2.grid(row=1, column=0, sticky=W, pady=2)

        l3 = Label(self.root, text="AN0:")
        l3.grid(row=2, column=0, sticky=W, pady=2)

        self.an0_var = StringVar()
        values = {"ON": "1", "OFF": "2"}

        # Usar o Radiobutton do tkinter normal em vez do ttk
        R1 = Radiobutton(self.root, text="ON", variable=self.an0_var,value=1, command = self.amostrarAN0).grid(row=2, column=1, sticky=W, pady=2)
        R2 = Radiobutton(self.root, text="OFF", variable=self.an0_var,value=2, command = self.naoAmostrarAN0).grid(row=2, column=2, sticky=W, pady=2)
            
        l4 = Label(self.root, text="AN5:")
        l4.grid(row=3, column=0, sticky=W, pady=2)
            
        self.an4_var = StringVar()
        values = {"ON": "1", "OFF": "2"}

        # Usar o Radiobutton do tkinter normal em vez do ttk
        R3 = Radiobutton(self.root, text="ON", variable=self.an4_var,value=1, command = self.amostrarAN5).grid(row=3, column=1, sticky=W, pady=2)
        R4 = Radiobutton(self.root, text="OFF", variable=self.an4_var,value=2, command = self.naoAmostrarAN5).grid(row=3, column=2, sticky=W, pady=2)
        
        l5 = Label(self.root, text="AN4:")
        l5.grid(row=4, column=0, sticky=W, pady=2)
            
        self.an5_var = StringVar()
        values = {"ON": "1", "OFF": "2"}

        # Usar o Radiobutton do tkinter normal em vez do ttk
        R5 = Radiobutton(self.root, text="ON", variable=self.an5_var,value=1, command = self.amostrarAN4).grid(row=4, column=1, sticky=W, pady=2)
        R6 = Radiobutton(self.root, text="OFF", variable=self.an5_var,value=2, command = self.naoAmostrarAN4).grid(row=4, column=2, sticky=W, pady=2)      

        l6 = Label(self.root, text="D6:")
        l6.grid(row=5, column=0, sticky=W, pady=2)
            
        self.d6_var = StringVar()
        values = {"ON": "1", "OFF": "2"}

        # Usar o Radiobutton do tkinter normal em vez do ttk
        R7 = Radiobutton(self.root, text="ON", variable=self.d6_var,value=1, command = self.amostrarD6).grid(row=5, column=1, sticky=W, pady=2)
        R8 = Radiobutton(self.root, text="OFF", variable=self.d6_var,value=2, command = self.naoAmostrarD6).grid(row=5, column=2, sticky=W, pady=2)      
            
        l7 = Label(self.root, text="D7:")
        l7.grid(row=6, column=0, sticky=W, pady=2)
            
        self.d7_var = StringVar()
        values = {"ON": "1", "OFF": "2"}

        # Usar o Radiobutton do tkinter normal em vez do ttk
        R9 = Radiobutton(self.root, text="ON", variable=self.d7_var,value=1, command = self.amostrarD7).grid(row=6, column=1, sticky=W, pady=2)
        R10 = Radiobutton(self.root, text="OFF", variable=self.d7_var,value=2, command = self.naoAmostrarD7).grid(row=6, column=2, sticky=W, pady=2)
            
        l7 = Label(self.root, text="B7:")
        l7.grid(row=7, column=0, sticky=W, pady=2)
            
        self.b7_var = StringVar()
        values = {"ON": "1", "OFF": "2"}

        # Usar o Radiobutton do tkinter normal em vez do ttk
        R11 = Radiobutton(self.root, text="ON", variable=self.b7_var,value=1, command = self.amostrarB7).grid(row=7, column=1, sticky=W, pady=2)
        R12 = Radiobutton(self.root, text="OFF", variable=self.b7_var,value=2, command = self.naoAmostrarB7).grid(row=7, column=2, sticky=W, pady=2)           

        l7 = Label(self.root, text=" ")
        l7.grid(row=8, column=0, sticky=W, pady=2)
        
        l7 = Label(self.root, text="Configurar Período de Amostragem:")
        l7.grid(row=9, column=0, sticky=W, pady=2)

        self.command_entryAN0 = tk.Entry(self.root, width=30)
        self.command_entryAN0.grid(row=10, column=1, sticky=W, pady=2)

        self.send_button = tk.Button(self.root, text="Submeter para AN0", command=self.freqAmostragemAN0_comando)
        self.send_button.grid(row=10, column=0, sticky=W, pady=2)

        self.command_entryAN4 = tk.Entry(self.root, width=30)
        self.command_entryAN4.grid(row=11, column=1, sticky=W, pady=2)

        self.send_button = tk.Button(self.root, text="Submeter para AN4", command=self.freqAmostragemAN4_comando)
        self.send_button.grid(row=11, column=0, sticky=W, pady=2)

        self.command_entryAN5 = tk.Entry(self.root, width=30)
        self.command_entryAN5.grid(row=12, column=1, sticky=W, pady=2)

        self.send_button = tk.Button(self.root, text="Submeter para AN5", command=self.freqAmostragemAN5_comando)
        self.send_button.grid(row=12, column=0, sticky=W, pady=2)

        self.command_entryD6 = tk.Entry(self.root, width=30)
        self.command_entryD6.grid(row=13, column=1, sticky=W, pady=2)

        self.send_button = tk.Button(self.root, text="Submeter para D6", command=self.freqAmostragemD6_comando)
        self.send_button.grid(row=13, column=0, sticky=W, pady=2)

        self.command_entryD7 = tk.Entry(self.root, width=30)
        self.command_entryD7.grid(row=14, column=1, sticky=W, pady=2)

        self.send_button = tk.Button(self.root, text="Submeter para D7", command=self.freqAmostragemD7_comando)
        self.send_button.grid(row=14, column=0, sticky=W, pady=2)

        self.command_entryB7 = tk.Entry(self.root, width=30)
        self.command_entryB7.grid(row=15, column=1, sticky=W, pady=2)

        self.send_button = tk.Button(self.root, text="Submeter para B7", command=self.freqAmostragemB7_comando)
        self.send_button.grid(row=15, column=0, sticky=W, pady=2)

        l7 = Label(self.root, text=" ")
        l7.grid(row=16, column=0, sticky=W, pady=2)

        l7 = Label(self.root, text="Configurar Número de Amostras:")
        l7.grid(row=17, column=0, sticky=W, pady=2)

        self.command_entryNumAN0 = tk.Entry(self.root, width=30)
        self.command_entryNumAN0.grid(row=18, column=1, sticky=W, pady=2)

        self.send_button = tk.Button(self.root, text="Submeter para AN0", command=self.numAmostragemAN0_comando)
        self.send_button.grid(row=18, column=0, sticky=W, pady=2)

        self.command_entryNumAN4 = tk.Entry(self.root, width=30)
        self.command_entryNumAN4.grid(row=19, column=1, sticky=W, pady=2)

        self.send_button = tk.Button(self.root, text="Submeter para AN4", command=self.numAmostragemAN4_comando)
        self.send_button.grid(row=19, column=0, sticky=W, pady=2)

        self.command_entryNumAN5 = tk.Entry(self.root, width=30)
        self.command_entryNumAN5.grid(row=20, column=1, sticky=W, pady=2)

        self.send_button = tk.Button(self.root, text="Submeter para AN5", command=self.numAmostragemAN5_comando)
        self.send_button.grid(row=20, column=0, sticky=W, pady=2)

        self.command_entryNumD6 = tk.Entry(self.root, width=30)
        self.command_entryNumD6.grid(row=21, column=1, sticky=W, pady=2)

        self.send_button = tk.Button(self.root, text="Submeter para D6", command=self.numAmostragemD6_comando)
        self.send_button.grid(row=21, column=0, sticky=W, pady=2)

        self.command_entryNumD7 = tk.Entry(self.root, width=30)
        self.command_entryNumD7.grid(row=22, column=1, sticky=W, pady=2)

        self.send_button = tk.Button(self.root, text="Submeter para D7", command=self.numAmostragemD7_comando)
        self.send_button.grid(row=22, column=0, sticky=W, pady=2)

        self.command_entryNumB7 = tk.Entry(self.root, width=30)
        self.command_entryNumB7.grid(row=23, column=1, sticky=W, pady=2)

        self.send_button = tk.Button(self.root, text="Submeter para B7", command=self.numAmostragemB7_comando)
        self.send_button.grid(row=23, column=0, sticky=W, pady=2)

        l7 = Label(self.root, text=" ")
        l7.grid(row=24, column=0, sticky=W, pady=2)

        l8 = Label(self.root, text="Configuração do Canal Bidirecional")
        l8.grid(row=25, column=0, sticky=W, pady=2)
            
        self.biChannel_var = StringVar()
        values = {"OUTPUT": "1", "INPUT": "2"}

        # Usar o Radiobutton do tkinter normal em vez do ttk
        R13 = Radiobutton(self.root, text="OUTPUT", variable=self.biChannel_var,value=1, command = self.outputB7).grid(row=25, column=1, sticky=W, pady=2)
        R14 = Radiobutton(self.root, text="INPUT", variable=self.biChannel_var,value=2, command = self.inputB7).grid(row=25, column=2, sticky=W, pady=2) 

        l10 = Button(self.root, text="Acionar LED(Só em Output)", command = self.actvLed) #so funciona em modo OUTPUT
        l10.grid(row=26, column=0, sticky=W, pady=2)

        l11 = Label(self.root, text=" ")
        l11.grid(row=27, column=0, sticky=W, pady=2)

        l12 = Label(self.root, text="Configuração do Canal Virtual(2 Bits)")
        l12.grid(row=28, column=0, sticky=W, pady=2)

        self.virChannel_var = StringVar()
        values = {"ON": "1", "OFF": "2"}

        # Usar o Radiobutton do tkinter normal em vez do ttk
        R15 = Radiobutton(self.root, text="ON", variable=self.virChannel_var,value=1, command = self.actVirtual).grid(row=28, column=1, sticky=W, pady=2)
        R16 = Radiobutton(self.root, text="OFF", variable=self.virChannel_var,value=2, command = self.dctVirtual).grid(row=28, column=2, sticky=W, pady=2) 
            
        l13 = Label(self.root, text="Configuração do Evento Alerta")
        l13.grid(row=29, column=0, sticky=W, pady=2)

        self.alerEvent_var = StringVar()
        values = {"1": "1", "2": "2","3": "3"}

        # Usar o Radiobutton do tkinter normal em vez do ttk
        R20 = Radiobutton(self.root, text="0", variable=self.alerEvent_var,value=1, command = self.alertEv0).grid(row=29, column=1, sticky=W, pady=2)
        R17 = Radiobutton(self.root, text="1", variable=self.alerEvent_var,value=1, command = self.alertEv1).grid(row=29, column=2, sticky=W, pady=2)
        R18 = Radiobutton(self.root, text="2", variable=self.alerEvent_var,value=2, command = self.alertEv2).grid(row=29, column=3, sticky=W, pady=2) 
        R19 = Radiobutton(self.root, text="3", variable=self.alerEvent_var,value=3, command = self.alertEv3).grid(row=29, column=4, sticky=W, pady=2) 
        

        l14 = Label(self.root, text=" ")
        l14.grid(row=30, column=0, sticky=W, pady=2)

        l17 = Button(self.root, text="I2C", command = self.i2c) 
        l17.grid(row=31, column=0, sticky=W, pady=2)

        self.output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=8, width=75)
        self.output_text.grid(row=1, column=4)

        l7 = Label(self.root, text=" ")
        l7.grid(row=0, column=2, sticky=W, pady=2)

        self.output_label = tk.Label(self.root, text="Output Amostragem:")
        self.output_label.grid(row=0, column=3, pady=2) #exprimenta tirar o sticky e reduzir a largura da imagem ou em vez de W meter um E
        
        self.status_label = tk.Label(root, text="Status: N/A")
        self.status_label.grid(row=2, column=5, sticky=W, pady=2)
        self.sensor1_label = tk.Label(root, text="Sensor 1: N/A")
        self.sensor1_label.grid(row=3, column=5, sticky=W, pady=2)
        self.sensor2_label = tk.Label(root, text="Sensor 2: N/A")
        self.sensor2_label.grid(row=4, column=5, sticky=W, pady=2)
        self.timestamp_label = tk.Label(root, text="Timestamp: N/A")
        self.timestamp_label.grid(row=5, column=5, sticky=W, pady=2)

        #l20 = Button(self.root, text="QUIT", command = root.destroy) 
        #l20.grid(row=2, column=6, sticky=W, pady=2)

        #devia se meter um output para o I"C se nao não da para ver, de qq forma é so descomentar "

    def atualizar_valores(self, dados):
    
        if 'Status' in dados:
            self.status_label.config(text=f"Status: {dados['Status']}")
        if 'sensor1' in dados:
            self.sensor1_label.config(text=f"Sensor 1: {dados['sensor1']}")
        if 'sensor2' in dados:
            self.sensor2_label.config(text=f"Sensor 2: {dados['sensor2']}")
        if 'timestamp' in dados:
            self.timestamp_label.config(text=f"Timestamp: {dados['timestamp']}")
    
        if 'timestamp' in dados:
            self.output_text.insert(tk.END,f"Timestamp: {dados['timestamp']}")
         
        if 'Status' in dados:
            self.output_text.insert(tk.END, f"Status: {dados['Status']}")
           
            
        if 'sensor1' in dados:
            self.output_text.insert(tk.END, f"Sensor 1: {dados['sensor1']}")
                      
        if 'sensor2' in dados:
            self.output_text.insert(tk.END, f"Sensor 2: {dados['sensor2']}")

        if 'AN0' in dados:
            self.output_text.insert(tk.END,f"AN0: {dados['AN0']}")
         
        if 'AN4' in dados:
            self.output_text.insert(tk.END, f"AN4: {dados['AN4']}")        
            
        if 'AN5' in dados:
            self.output_text.insert(tk.END, f"AN5: {dados['AN5']}")
                     
        if 'D6' in dados:
            self.output_text.insert(tk.END, f"D6: {dados['D6']}")

        if 'D7' in dados:
            self.output_text.insert(tk.END, f"D7: {dados['D7']}")

        if 'B7' in dados:
            self.output_text.insert(tk.END, f"B7: {dados['B7']}")
             
        self.output_text.yview(tk.END)
         
        
    def amostrarAN0(self):
        cmd = "{\"analogAmostragem\":[0,1]}"
        self.porta_uart.write(cmd.encode())

    def naoAmostrarAN0(self):
        cmd = "{\"analogAmostragem\":[0,0]}"
        self.porta_uart.write(cmd.encode())

    def amostrarAN4(self):
        cmd = "{\"analogAmostragem\":[4,1]}"
        self.porta_uart.write(cmd.encode())

    def naoAmostrarAN4(self):
        cmd = "{\"analogAmostragem\":[4,0]}"
        self.porta_uart.write(cmd.encode())

    def amostrarAN5(self):
        cmd = "{\"analogAmostragem\":[5,1]}"
        self.porta_uart.write(cmd.encode())

    def naoAmostrarAN5(self):
        cmd = "{\"analogAmostragem\":[5,0]}"
        self.porta_uart.write(cmd.encode())

    def amostrarD6(self):
        cmd = "{\"DigitalAmostragem\":[6,1]}"
        self.porta_uart.write(cmd.encode())

    def naoAmostrarD6(self):
        cmd = "{\"DigitalAmostragem\":[6,0]}"
        self.porta_uart.write(cmd.encode())

    def amostrarD7(self):
        cmd = "{\"DigitalAmostragem\":[7,1]}"
        self.porta_uart.write(cmd.encode())

    def naoAmostrarD7(self):
        cmd = "{\"DigitalAmostragem\":[7,0]}"
        self.porta_uart.write(cmd.encode())

    def amostrarB7(self):
        cmd = "{\"DigitalAmostragem\":[1,1]}"
        self.porta_uart.write(cmd.encode())

    def naoAmostrarB7(self):
        cmd = "{\"DigitalAmostragem\":[1,0]}"
        self.porta_uart.write(cmd.encode())

    def freqAmostragemAN0_comando(self):
        comando = self.command_entryAN0.get()
        cmd = "{\"freqAmostragem\":[0,"+comando+"]}"
        self.porta_uart.write(cmd.encode())

    def freqAmostragemAN4_comando(self):
        comando = self.command_entryAN4.get()
        cmd = "{\"freqAmostragem\":[4,"+comando+"]}"
        self.porta_uart.write(cmd.encode())

    def freqAmostragemAN5_comando(self):
        comando = self.command_entryAN5.get()
        cmd = "{\"freqAmostragem\":[5,"+comando+"]}"
        self.porta_uart.write(cmd.encode())

    def freqAmostragemD6_comando(self):
        comando = self.command_entryD6.get()
        cmd = "{\"DigitalFreq\":[6,"+comando+"]}"
        self.porta_uart.write(cmd.encode())

    def freqAmostragemD7_comando(self):
        comando = self.command_entryD7.get()
        cmd = "{\"DigitalFreq\":[7,"+comando+"]}"
        self.porta_uart.write(cmd.encode())

    def freqAmostragemB7_comando(self):
        comando = self.command_entryB7.get()
        cmd = "{\"DigitalFreq\":[1,"+comando+"]}"
        self.porta_uart.write(cmd.encode())

    def numAmostragemAN0_comando(self):
        comando = self.command_entryNumAN0.get()
        cmd = "{\"numAmostragem\":[0,"+comando+"]}"
        self.porta_uart.write(cmd.encode())

    def numAmostragemAN4_comando(self):
        comando = self.command_entryNumAN4.get()
        cmd = "{\"numAmostragem\":[4,"+comando+"]}"
        self.porta_uart.write(cmd.encode())

    def numAmostragemAN5_comando(self):
        comando = self.command_entryNumAN5.get()
        cmd = "{\"numAmostragem\":[5,"+comando+"]}"
        self.porta_uart.write(cmd.encode())

    def numAmostragemD6_comando(self):
        comando = self.command_entryNumD6.get()
        cmd = "{\"DigitalNum\":[6,"+comando+"]}"
        self.porta_uart.write(cmd.encode())

    def numAmostragemD7_comando(self):
        comando = self.command_entryNumD7.get()
        cmd = "{\"DigitalNum\":[7,"+comando+"]}"
        self.porta_uart.write(cmd.encode())

    def numAmostragemB7_comando(self):
        comando = self.command_entryNumB7.get()
        cmd = "{\"DigitalNum\":[1,"+comando+"]}"
        self.porta_uart.write(cmd.encode())

    def inputB7(self):
        cmd = "{\"Bidirecional\":[1,1]}"
        self.porta_uart.write(cmd.encode())

    def outputB7(self):
        cmd = "{\"Bidirecional\":[1,0]}"
        self.porta_uart.write(cmd.encode())

    def actvLed(self):
        cmd = "{\"BidirecionalActive\":[1]}"
        self.porta_uart.write(cmd.encode())

    def actVirtual(self):
        cmd = "{\"virtual\":[0]}"
        self.porta_uart.write(cmd.encode())

    def dctVirtual(self):
        cmd = "{\"virtual\":[1]}"
        self.porta_uart.write(cmd.encode())

    def alertEv0(self):
        cmd = "{\"alertEvent\":[0]}"
        self.porta_uart.write(cmd.encode())

    def alertEv1(self):
        cmd = "{\"alertEvent\":[1]}"
        self.porta_uart.write(cmd.encode())

    def alertEv2(self):
        cmd = "{\"alertEvent\":[2]}"
        self.porta_uart.write(cmd.encode())

    def alertEv3(self):
        cmd = "{\"alertEvent\":[3]}"
        self.porta_uart.write(cmd.encode())
       
    def i2c(self):
        cmd = "{\"I2C\":[3]}"
        self.porta_uart.write(cmd.encode())
    
    def stop(self):
        
        self.PedroCachorro = False
        #self.root.quit()
        #self.root.destroy()

    def iniciar_gui(self):
        while self.PedroCachorro:
            
            while True:
                valor = self.data_generator.return_listener()
                if valor != -1:
                    break
                if(self.PedroCachorro == False):
                        break
            if(self.PedroCachorro == False):
                        break
            time2 = self.data_generator.gerar_dados_ficticios()
            if self.root:
                self.root.after(0, self.atualizar_valores, valor)

            time.sleep(15)