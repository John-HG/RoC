import sys
from PySide2.QtWidgets import (QApplication, QDialog, QWidget, QRadioButton, QLineEdit, QPushButton,
                               QMessageBox,QFrame,QVBoxLayout, QStackedWidget)
from Roc import Ui_Dialog
import metodos

class Roc (QDialog):
    def __init__(self):
        super(Roc, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.stackedWidget.setCurrentIndex(0)                        #inicializamos en la primera pagina
        self.ui.entrar.clicked.connect(self.menuprincipal)
        self.ui.mover_r.clicked.connect(self.configurar_viaje)          #nos manda al menu 
        self.lista = [self.ui.nodo_A, self.ui.nodo_B, self.ui.nodo_C, self.ui.nodo_D, self.ui.nodo_E,
                        self.ui.nodo_F, self.ui.nodo_G, self.ui.nodo_H, self.ui.nodo_I]
        self.ui.boton_inicio.clicked.connect(self.setear_incio)
        self.ui.boton_fin.clicked.connect(self.setear_fin)
        self.ui.confirmar_n.clicked.connect(self.confirmar_nodos)
        self.ui.clear.clicked.connect(self.limpieza)
    
    ###metodos de movimiento
    

    def menuprincipal(self):                                            #menu elegir mover robot o ver herramienta  
        self.ui.stackedWidget.setCurrentIndex(1)                        #nos mueve al menu principal 

    def configurar_viaje(self):                                         #menu de configurar viaje 
        self.ui.stackedWidget.setCurrentIndex(2)
        self.ui.back.clicked.connect(self.menuprincipal)
        self.ui.confirmar_n.clicked.connect(self.viaje)               #si se presiona se va a menu de viaje

    
    def viaje(self):                                                    #menu de vieje      
        self.ui.stackedWidget.setCurrentIndex(3)                        
        self.ui.irconfimov.clicked.connect(self.configurar_viaje)       #si se presiona se va a configurar viaje 


    ####metodos de confirmar viaje 
    def setear_incio(self):   #aqui se agrega el nodo a inicio
        for self.x in self.lista:                           #se recorre la lista que tiene todos los radiobutton asignados
            if self.x.isChecked() == True:                  #si algun nodo se selecciono 
                print(self.x.text())                        #se imprime el parametro text() del radioButton
                self.ui.opc_inicio.setText(self.x.text())   #y se asigna al lineEdit                 

    def setear_fin(self):
        for self.x in self.lista:                           #se recorre la lista que tiene todos los radiobutton asignados
            if self.x.isChecked() == True:                  #si algun nodo se selecciono 
                print(self.x.text())                        #se imprime el parametro text() del radioButton
                self.ui.opc_fin.setText(self.x.text())      #y se asigna al lineEdit
    
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = Roc()
    myapp.show()
    sys.exit(app.exec_())