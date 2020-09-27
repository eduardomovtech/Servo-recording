from PySimpleGUI import PySimpleGUI as sg
import serial
import time
import serial.tools.list_ports
import os

##seleção de portas serial
def get_ports():

    ports = serial.tools.list_ports.comports()
    
    return ports

def findArduino(portsFound):
    
    commPort = 'None'
    numConnection = len(portsFound)
    
    for i in range(0,numConnection):
        port = foundPorts[i]
        strPort = str(port)
        
        if 'Arduino' in strPort: 
            splitPort = strPort.split(' ')
            commPort = (splitPort[0])
        elif 'Genuino' in strPort: 
            splitPort = strPort.split(' ')
            commPort = (splitPort[0])    

    return commPort
            
                    
foundPorts = get_ports()        
connectPort = findArduino(foundPorts)

numPoints = 5
dataList = [0]*numPoints

def getValues():
    
    ser.write(b'g')
    arduinoData = ser.readline().decode('ascii')

    return arduinoData

layout = [
    [sg.Slider(range=(0, 200), orientation='h', size=(50, 20), default_value=0, disable_number_display=True,
    tick_interval=25, enable_events=True, key='valor', resolution=1)],
    [sg.Slider(range=(0, 200), orientation='h', size=(50, 20), default_value=0, disable_number_display=True,
    tick_interval=25, enable_events=True, key='valor2', resolution=1)],
    [sg.Text('',size =(50,2),key='saida')],
    #[sg.Output(size =(5,1), key='valor_s1')],
    [sg.Output(size =(5,1), key='valor_s1'),sg.Output(size =(5,1), key='valor_s2')],
    [sg.Button(('Gravar'), key='gravar'),
     sg.Button(('Executar'), key='execute'),
     sg.Button(('Remover'), key='remover') ],
    [sg.Output(size =(20,10), key='saida2')]
    ]

window = sg.Window('Controle de servo', icon='icone.ico').Layout(layout)

if connectPort != 'None':
    ser = serial.Serial(connectPort, baudrate = 115200, timeout=1)
    sg.Output = print('aguarde')
    #time.sleep(1)
    sg.Output = print('conected to',connectPort)
    time.sleep(1)
event, values = window.read() 
sg.popup('Title',
         'The results of the window.',
         'The button clicked was "{}"'.format(event),
         'The values are', values)
while True:
    event, values = window.read() 
  
    if event == sg.WIN_CLOSED:      
        break

    cara = (int(values['valor']))
    cara2 = (int(values['valor2']))+201

    if event == 'valor':
        ser.write(str(cara).encode("UTF-8"))
        ser.write (b'\n')
        
    if event == 'valor2':
        ser.write(str(cara2).encode("UTF-8"))
        ser.write (b'\n')
    if event == 'gravar':
        sg.Output = print("")
        sg.Output = print("gravando em 3..")
        time.sleep(1)
        sg.Output = print("gravando em 2..")
        time.sleep(1)
        sg.Output = print("gravando em 1..")
        time.sleep(1)
        sg.Output = print("gravando...")

        f= open("gravado.txt","a+")
        for i in range(0,1000):
            event, values = window.read(timeout=0)
            cara = (int(values['valor']))
            cara2 = (int(values['valor2']))+201
            ser.write(str(cara).encode("UTF-8"))
            ser.write (b'\n')
            f.write(str(cara))
            f.write('\n')
            cara = (int(values['valor']))
            cara2 = (int(values['valor2']))+201    
            ser.write(str(cara2).encode("UTF-8"))
            ser.write (b'\n')
            f.write(str(cara2))
            f.write('\n')
            sg.Output = print(int(i/10))
            window['valor_s1'].update(cara)
            window['valor_s2'].update(cara2)
        window.Element('saida2').Update("pronto")
        f.close()

    if event == 'execute':
        
        if os.path.exists("gravado.txt"):
            window.Element('saida2').Update('Executando!')
            sg.Output = print('')
            f= open("gravado.txt","r")
            if f.mode == 'r':
                 
                f1=f.readlines()
                for x in f1:
                    
                    #sg.Output = print('')
                    sg.Output = print(str(x))                    
                    ser.write(str(x).encode("UTF-8"))
                    time.sleep(0.0025)

            window.Element('saida2').Update("Finalizado!")        
            f.close() 
        else:
            window.Element('saida2').Update("Grave um Arquivo!")
    if event == 'remover':
        if os.path.exists("gravado.txt"):
            os.remove("gravado.txt")
            window.Element('saida2').Update("Removido")
        else:
            window.Element('saida2').Update("Sem arquivo!")    

    window['valor_s1'].update(cara)
    window['valor_s2'].update(cara2)

    window.Element('saida').Update(cara)





