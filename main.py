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
        self.timer.timeout.connect(self.ver_video)
        self.timer.start(30)
        self.t = time.time() ##################################
        self.espera = 30
    def ver_video(self):
        n = time.time() #############
        _,frame = self.cap.read()
        _,g = metodos.db()
        todos_los_nodos = g.nodes()
        qr = []
        #####################################
        decodedObjects = pyzbar.decode(frame) #aqui obtenemos el objeto qr el cual lo va a obtener de la imagen obtenida frame
        for obj in decodedObjects:
            (x, y, w, h) = obj.rect #obtenemos las coordenadas del objeto
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) #dibujamos un rectangulo en las coordenadas obtenidas
            barcodeData = obj.data.decode("utf-8") #obtenemos el mensaje que contine la imagen qr
            #cv2.putText(frame, str(barcodeData), (30, 30), font, 2, (255, 0, 0), 3)
            for i in todos_los_nodos: #recorre la variable i en la lista de nodos
                if barcodeData == i:
                    qr = barcodeData
                    estado = False
             #print("Type: " , obj.type)
        #////////////////////////////////aqui anterior//////////7##
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame,1)
        cuadro = QImage(frame,frame.shape[1],frame.shape[0],frame.strides[0],QImage.Format_RGB888)
        self.ui.imagen.setPixmap(QPixmap.fromImage(cuadro))
        ##/////////////////////////////////////////////////////////
        if (n== self.t + self.espera) or (n>= self.t + self.espera): #aquie se genera la cuenta
            estado = False
        #######################################
        
        if len(qr) != 0:
            if qr == "A":
                self.ui.line_progreso.setText(qr)
            



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