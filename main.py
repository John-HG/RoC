import sys
import cv2
import time
import pyzbar.pyzbar as pyzbar
from PySide2.QtWidgets import (QApplication, QDialog, QWidget, QRadioButton, QLineEdit, QPushButton,
                               QMessageBox,QFrame,QVBoxLayout, QStackedWidget)
from PySide2.QtGui import(QImage,QPixmap)
from PySide2.QtCore import(QTimer,QSize)

from Roc import Ui_Dialog
import metodos



class Roc (QDialog):
    def __init__(self):
        super(Roc, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.lista = [self.ui.nodo_A, self.ui.nodo_B, self.ui.nodo_C, self.ui.nodo_D, self.ui.nodo_E,
                        self.ui.nodo_F, self.ui.nodo_G, self.ui.nodo_H, self.ui.nodo_I]
        #Metodos de configurar viaje se pusieron aqui por que si se ponen el el metodo de configurara hace un pinche desmadre 
        self.ui.confirmar_n.clicked.connect(self.confirmar_nodos)
        self.ui.btn_clear.clicked.connect(self.limpieza)
        self.ui.boton_inicio.clicked.connect(self.setear_incio)
        self.ui.boton_fin.clicked.connect(self.setear_fin)
        
        
        #hoja 0 Login                
        self.ui.stackedWidget.setCurrentIndex(0)                        #inicializamos en la primera pagina
        self.ui.entrar.clicked.connect(self.menuprincipal)
        #hoja 3 viaje
        self.ui.imagen.setScaledContents(True)
    
    # hoja 1 menu elegir mover robot o ver herramienta 
    def menuprincipal(self):                                            
        self.ui.stackedWidget.setCurrentIndex(1)                        #nos mueve al menu principal 
        self.ui.mover_r.clicked.connect(self.configurar_viaje)          #nos manda a hoja 2

    #hoja 2 configurar viaje 
    def configurar_viaje(self):                                         #menu de configurar viaje 
        self.ui.stackedWidget.setCurrentIndex(2)
        self.ui.back.clicked.connect(self.menuprincipal)

        #self.ui.confirmar_n.clicked.connect(self.viaje)               #snos manda a hoja 3  viaje

    #hoja 3 vieje
    def viaje(self):                                                    #menu de vieje     
        time.sleep(3)
        self.ui.stackedWidget.setCurrentIndex(3)                        
        self.ui.irconfimov.clicked.connect(self.configurar_viaje)       #si se presiona se va a configurar viaje 
        self.setup_camera()
        #self.ui.show.clicked.connect(self.setup_camera)
        self.ui.stop_record.clicked.connect(self.stop_camera)

    ####metodos de confirmar viaje 
    def setear_incio(self):   #aqui se agrega el nodo a inicio
        for x in self.lista:                           #se recorre la lista que tiene todos los radiobutton asignados
            if x.isChecked() == True:                  #si algun nodo se selecciono 
                print(x.text())                        #se imprime el parametro text() del radioButton
                self.ui.opc_inicio.setText(x.text())   #y se asigna al lineEdit                 

    def setear_fin(self):
        for x in self.lista:                           #se recorre la lista que tiene todos los radiobutton asignados
            if x.isChecked() == True:                  #si algun nodo se selecciono 
                print(x.text())                        #se imprime el parametro text() del radioButton
                self.ui.opc_fin.setText(x.text())      #y se asigna al lineEdit
    
    def limpieza(self):
        self.ui.opc_inicio.clear()
        self.ui.opc_fin.clear()   

    def confirmar_nodos(self):
        elinicio = self.ui.opc_inicio.text()
        elfin = self.ui.opc_fin.text()
        if not elinicio or not elfin:
            #print("ningun elemento ")
            msgb = QMessageBox()
            msgb.setText("Necesita completar el inicio y el fin ")
            msgb.exec_()
        elif elinicio == elfin :
            msgb = QMessageBox()
            msgb.setText("Nodos iguales")
            msgb.exec_()
        else:
            mensaje = metodos.mensaje_nodo(elinicio,elfin)
            msgb = QMessageBox()
            msgb.setText("{}".format(mensaje))
            msgb.exec_()
            self.viaje()
    ######Metodos de viaje 
    def setup_camera(self):
        self.cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        self.timer = QTimer()
        self.timer.timeout.connect(self.ver_video(self.ui.opc_inicio.text()))
        self.timer.start(30)
        self.t = time.time() ##################################
        self.espera = 30
    def ver_video(self,f):
        espera = 10
        #data, g = db()
        todos_los_nodos= ["A","B"]#g.nodes()
        t = time.time()  # ingresamos el tiempo base
        qr = [] #es un un arreglo vaicio el cual ya a contener la salida de la funcion
        estado = True #es la llave para el ciclo while creo que se puede cambiar y solamente poner while true y poner breaks
        time.sleep(1)
        while estado:
            n = time.time() #obtenemos el tiempo
            _, frame = self.cap.read() #creamos la variable frame la cual nos va a dar la lectura de la camara
            decodedObjects = pyzbar.decode(frame) #aqui obtenemos el objeto qr el cual lo va a obtener de la imagen obtenida frame
            for obj in decodedObjects:
                (x, y, w, h) = obj.rect #obtenemos las coordenadas del objeto
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) #dibujamos un rectangulo en las coordenadas obtenidas
                barcodeData = obj.data.decode("utf-8") #obtenemos el mensaje que contine la imagen qr
                for i in todos_los_nodos: #recorre la variable i en la lista de nodos
                    if barcodeData == i:
                        qr = barcodeData
                        estado = False
                #print("Type: " , obj.type)
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            frame = cv2.flip(frame,1)
            imagen = QImage(frame,frame.shape[1], frame.shape[0],frame.strides[0], QImage.Format_RGB888)
            self.ui.imagen.setPixmap(QPixmap.fromImage(imagen))
            if (n== t + espera) or (n>= t + espera): #aquie se genera la cuenta
                estado = False
            #else:
            #    print("{}".format(n-t)) # imprime el tiempo que va pasando
            key = cv2.waitKey(3) & 0xff
            if key == False:
                break
        self.cap.release()
        cv2.destroyAllWindows()

        if len(qr) != 0: # aqui manda el estado y el qr
            if qr == f:
                self.ui.line_progreso.setText("Nodo verificado {}".format(qr))
                #return True, qr #si qr es igual al punto que mandamos envia un true y el punto
            else:
                self.ui.line_progreso.setText("Nodo incorrecto se detecta el nodo {}".format(qr))
                #return False, qr # si no manda un falso pero si lee algo y ese algo lo manda
        else:
            self.ui.line_progreso.setText("No de detecto ningun nodo")
            #return False, None  # si no lee nada manda un falso y una lista vacia
            



    def stop_camera(self):
        self.cap.release()
        self.ui.imagen.setPixmap(QPixmap.fromImage("C:/Users/Enrique Manuel/Desktop/multiventanas/fondos/saitama.png"))
        self.timer.stop()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = Roc()
    myapp.show()
    sys.exit(app.exec_())