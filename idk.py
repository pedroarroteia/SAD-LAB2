import time
from tkinter import messagebox
import csv
import os
import xml.etree.ElementTree as ET
import requests
import json


class DataGenerator:
    def __init__(self,pa):
        self.csvAux = None

        self.listeners = []
        self.PedroCachorro = True
        self.idleee = 1
        self.porta_uart = pa

    def add_listener(self, listener):
        self.listeners.append(listener)
        self.idleee=0

    def return_listener(self):

        if(self.idleee==0):
            return self.listeners[-1]
        else:
            return -1

    def start_generating(self):
        # Configuração da porta UART (no Windows, use COM5 em vez de /dev/ttyUSB0)
        dados1 = None

        # Nome do arquivo CSV
        csv_filename = 'dados_recebidos.csv'
        
        # Verifica se o arquivo já existe
        file_exists = os.path.isfile(csv_filename)

        with open(csv_filename, mode='a', newline='')  as csvfile:

            fieldnames = ['timestamp', 'Status', 'sensor1', 'sensor2', 'AN0', 'AN4','AN5', 'D6', 'D7', 'B7']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Escreve o cabeçalho apenas se o arquivo for novo
            if not file_exists:
                writer.writeheader()
            #try:
            time.sleep(1)
            while self.PedroCachorro:
                while(1):

                    dados1 = self.porta_uart.readline().strip()
                    if(dados1 != b''):
                        break
                    if(self.PedroCachorro == False):
                        break
                if(self.PedroCachorro == False):
                    break

                time1 = self.gerar_dados_ficticios()

                dados_str = dados1.decode('latin-1')

                dados_json = json.loads(dados_str) 

                dados_json.__setitem__('timestamp', time1)

                self.add_listener(dados_json)

                
                a = self.convert_to_xml(dados_json)
                self.send_to_server(a)

                dados_csv = dados_json.copy()

                if(not('timestamp'in dados_csv)):
                    dados_csv['timestamp'] = '-999'
                if(not('Status'in dados_csv)):
                    dados_csv['Status'] = -999
                if(not('sensor1'in dados_csv)):
                    dados_csv['sensor1'] = -999
                if(not('sensor2'in dados_csv)):
                    dados_csv['sensor2'] = -999
                if(not('AN0'in dados_csv)):
                    dados_csv['AN0'] = -999
                if(not('AN4'in dados_csv)):
                    dados_csv['AN4'] = -999
                if(not('AN5'in dados_csv)):
                    dados_csv['AN5'] = -999
                if(not('D6'in dados_csv)):
                    dados_csv['D6'] = -999
                if(not('D7'in dados_csv)):
                    dados_csv['D7'] = -999
                if(not('B7'in dados_csv)):
                    dados_csv['B7'] = -999

                # Escreve os dados no arquivo CSV
                writer.writerow({
                    'timestamp': dados_csv['timestamp'],
                    'Status': dados_csv['Status'],
                    'sensor1': dados_csv['sensor1'],
                    'sensor2': dados_csv['sensor2'],
                    'AN0': dados_csv['AN0'],
                    'AN4': dados_csv['AN4'],
                    'AN5': dados_csv['AN5'],
                    'D6': dados_csv['D6'],
                    'D7': dados_csv['D7'],
                    'B7': dados_csv['B7']
                })              

    def stop(self):
        self.PedroCachorro = False
    
    def gerar_dados_ficticios(self):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        millis = int(round(time.time() * 1000)) % 1000
        timestamp = f"{current_time}.{millis:03d}"

        return timestamp

    def convert_to_xml(self, dados):
        root = ET.Element("data")
        if('timestamp'in dados):
            ET.SubElement(root, "timestamp").text = dados["timestamp"]
        if('Status'in dados):
            ET.SubElement(root, "Status").text = str(dados["Status"])
        if('sensor1'in dados):
            ET.SubElement(root, "sensor1").text = str(dados["sensor1"])
        if('sensor2'in dados):
            ET.SubElement(root, "sensor2").text = str(dados["sensor2"])
        if('AN0'in dados):
            ET.SubElement(root, "AN0").text = str(dados["AN0"])
        if('AN4'in dados):
            ET.SubElement(root, "AN4").text = str(dados["AN4"])
        if('AN5'in dados):
            ET.SubElement(root, "AN5").text = str(dados["AN5"])
        if('D6'in dados):
            ET.SubElement(root, "D6").text = str(dados["D6"])
        if('D7'in dados):
            ET.SubElement(root, "D7").text = str(dados["D7"])
        if('B7'in dados):
            ET.SubElement(root, "B7").text = str(dados["B7"])
        return ET.tostring(root, encoding='unicode')

    def send_to_server(self, xml_data):
        url = "http://193.136.120.133/~sad/"
        headers = {'Content-Type': 'application/xml'}
        try:
            response = requests.post(url, data=xml_data, headers=headers)
            response.raise_for_status()
            #print(f"Dados enviados com sucesso: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Erro ao enviar dados para o servidor: {e}")



