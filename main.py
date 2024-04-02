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
        #Metodos de configurar viaje se pusieron aqui por que si se ponen en el metodo de configurar hace un pin*!$e desmadre 
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
        self.ui.stackedWidget.setCurrentIndex(1)                                        #nos mueve al menu principal 
        self.ui.mover_r.clicked.connect(self.configurar_viaje)                          #nos manda a hoja 2

    #hoja 2 configurar viaje 
    def configurar_viaje(self):                                                         #menu de configurar viaje 
        self.ui.stackedWidget.setCurrentIndex(2)
        self.ui.back.clicked.connect(self.menuprincipal)
        self.ui.opc_inicio.clear()
        self.ui.opc_fin.clear()
        self.cap.release()
        #self.ui.confirmar_n.clicked.connect(self.viaje)                                #nos manda a hoja 3 viaje

    #hoja 3 viaje
    def viaje(self):                                                                    #menu de viaje     
        #time.sleep(3)
        self.ui.stackedWidget.setCurrentIndex(3)                        
        self.ui.irconfimov.clicked.connect(self.configurar_viaje)                       #si se presiona se va a configurar viaje
        self.mover(self.elinicio,self.elfin,None)
        msgb = QMessageBox.question(self,"ooo",
                                    "Se llego al final",
                                    QMessageBox.Yes| QMessageBox.No)
        if msgb == QMessageBox.Yes:
            self.menuprincipal()
        else:
            self.configurar_viaje()

    ####metodos de confirmar viaje 
    def setear_incio(self):                                                             #aqui se agrega el nodo a inicio
        for x in self.lista:                                                            #se recorre la lista que tiene todos los radiobutton asignados
            if x.isChecked() == True:                                                   #si algun nodo se selecciono 
                #print(x.text())                                                        #se imprime el parametro text() del radioButton
                self.ui.opc_inicio.setText(x.text())                                    #y se asigna al lineEdit                 

    def setear_fin(self):
        for x in self.lista:                                                            #se recorre la lista que tiene todos los radiobutton asignados
            if x.isChecked() == True:                                                   #si algun nodo se selecciono 
                #print(x.text())                                                        #se imprime el parametro text() del radioButton
                self.ui.opc_fin.setText(x.text())                                       #y se asigna al lineEdit
    
    def limpieza(self):                                                                 #se limpian los lineEdit de inicio y fin 
        self.ui.opc_inicio.clear()
        self.ui.opc_fin.clear()   

    def confirmar_nodos(self):                                                          #se confirman los nodos con un messageBox
        self.elinicio = self.ui.opc_inicio.text()
        self.elfin = self.ui.opc_fin.text()
        if not self.elinicio or not self.elfin:
            #print("ningun elemento ")
            msgb = QMessageBox()
            msgb.setText("Necesita completar el inicio y el fin ")
            msgb.exec_()
        elif self.elinicio == self.elfin :
            msgb = QMessageBox()
            msgb.setText("Nodos iguales")
            msgb.exec_()
        else:
            mensaje = metodos.mensaje_nodo(self.elinicio,self.elfin)
            msgb = QMessageBox()
            msgb.setText("{}".format(mensaje))
            msgb.exec_()
            self.viaje()                                                                #nos manda a viaje
    ######Metodos de viaje 
    def setup_camera(self,f):                                                           #abre la camara y verifca los nodos
        self.cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        self.timer = QTimer()
        self.timer.start(30)
        espera = 15
        _, g = metodos.db()
        todos_los_nodos = g.nodes()
        t = time.time()                                                                 # ingresamos el tiempo base
        qr = []                                                                         #es un un arreglo vacio el cual ya va a contener la salida de la funcion
        estado = True                                                                   #es la llave para el ciclo while creo que se puede cambiar y solamente poner while true y poner breaks
        time.sleep(1)
        while estado:
            n = time.time()                                                             #obtenemos el tiempo
            _, frame = self.cap.read()                                                  #creamos la variable frame la cual nos va a dar la lectura de la camara
            decodedObjects = pyzbar.decode(frame)                                       #aqui obtenemos el objeto qr el cual lo va a obtener de la imagen obtenida frame
            for obj in decodedObjects:
                (x, y, w, h) = obj.rect                                                 #obtenemos las coordenadas del objeto
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)            #dibujamos un rectangulo en las coordenadas obtenidas
                barcodeData = obj.data.decode("utf-8")                                  #obtenemos el mensaje que contine la imagen qr
                for i in todos_los_nodos:                                               #recorre la variable i en la lista de nodos
                    if barcodeData == i:
                        qr = barcodeData
                        estado = False
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)                               #esto es lo que tenemos que hacer 
            frame = cv2.flip(frame,1)                                                   #para mostrarlo
            imagen = QImage(frame,frame.shape[1], frame.shape[0],frame.strides[0], QImage.Format_RGB888)
            self.ui.imagen.setPixmap(QPixmap.fromImage(imagen))
            if (n== t + espera) or (n>= t + espera):                                    #aqui se genera la cuenta
                estado = False
            key = cv2.waitKey(3) & 0xff                                                 #¡¡muy importante, este key es necesario
            if key == False:                                                                            #para que funcione esta parte!!
                break
        self.cap.release()
        self.ui.imagen.setPixmap(QPixmap.fromImage("C:/Users/Enrique Manuel/Desktop/multiventanas/fondos/saitama.png"))
        self.timer.stop()
        if len(qr) != 0:                                                            # aqui manda el estado y el qr
            if qr == f:
                return True,qr
                
            else:
                return False,qr
        else:
            return False, None

    def mover(self, inicio, fin,nodo_malo):                                             #realiza la logica del movimiento
        if nodo_malo == None:
            lista = metodos.busqueda(inicio,fin)
            listaS = " ".join(lista)
        else:
            lista = metodos.busqueda_error(inicio,fin,nodo_malo)
            listaS = " ".join(lista)
        self.ui.lista_nodos.setText(listaS)
        print(lista)
        n = len(lista)
        c = 1
        for i in lista:
            respuesta,nodo = self.setup_camera(i)
            if respuesta == True and nodo == i:
                if nodo == fin:
                    y= "se verifico el ultimo nodo {} \n llegamos".format(nodo) 
                    print(y)
                    self.ui.verificacion.setText(y)
                    break
                else:
                    x = "Se verifico {}".format(i)
                    self.ui.verificacion.setText(x)
                    mensaje,y = metodos.direccion(i,lista[c])
                    self.ui.direccion.setText(mensaje)
                    print(mensaje)
                    metodos.comunicacion_arduino(str(y))
                    c += 1
            elif respuesta == False and nodo == None:
                x= "No se encontro nodo  {}".format(i)
                self.ui.verificacion.setText(x)
                print(x)
                print("i-1{}  fin{} error {}".format(lista[-2],fin,i))
                self.mover(lista[-2], fin, i)
                break
            else:
                x= "Nodo incorrecto {}".format(nodo)
                self.ui.verificacion.setText(x)
                print(x)
                self.ui.direccion.clear()
                self.mover(nodo,fin,None)        #####
                break
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = Roc()
    myapp.show()
    sys.exit(app.exec_())