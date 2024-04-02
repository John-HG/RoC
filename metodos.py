import networkx as nx 
import pandas as pd 
import cv2 
import pyzbar.pyzbar as pyzbar
import time
import serial

#Creamos el data y el grafo con el que vamos a trabajar 
def db():
    data = pd.read_csv("C:/Users/Enrique Manuel/Desktop/multiventanas/base_datos.csv")        #lee la base de datos 
    g = nx.Graph()                              #creamos el grafo 
    for row in data.iterrows():                 #Agregamos los nodos 
        g.add_edge(row[1]["origen"],            #por medio de edges lo que nos permite dar origen y destino
                   row[1]["destino"],           #destino
                   large = row[1]["distancia"],    #agregamos pesos con la distancia 
                   way = row[1]["direccion"])   #ademas de la direccion en donde esta 
    return data,g                               #retornamos el csv y el grafo que creamos
   
#generamos una busqueda 
def busqueda(star, stop):
    _,g = db()                                          #cargamos el grafo
    astar = list(nx.astar_path(g, source=star, target=stop, weight="destino"))      #utilizamos el metodo de busqueda astar de la libreria nx
                                                        #necesita origen destino y el peso que se una para -> 
                                                        #->obtener el mejor camino 
    return astar                                        #retornamos una lista que se genera del metodo  
# busqueda con error 
def busqueda_error(star, stop, error):
    #realizamos lo mismo que en el metodo anterior pero agregamos una linea mas               
    _, g = db()                                         
    g.remove_node(error)                                #en esta linea removemos el nodo si es que el robot detecta 
                                                        #algun tipo de obstaculo   
    astar = list(nx.astar_path(g,source=star,target=stop, weight='destino'))           
                                                        #en este caso al eliminar el nodo se realiza la busqueda sin el 
                                                        #retornamos la lista 
                    
    return astar                                        

#confirmamos la existencia del nodo en la db
def cofirmarnodo(nodo):
    data, _ = db()                              #obtenemos el db de la funcion db()
    confirm = data[data["origen"] == nodo]      #vemos si los nodos estan dentro del db
    c = len(confirm.index)                      #
    if c == 0:                                  #obtenemos si esta dentro 
        return False                            
    else:
        return True

#mandamos el mensaje de confirmacion 
def mensaje_nodo(o,d):
    lista =[]
    for i in(o,d):
        respuesta=cofirmarnodo(i)
        if respuesta == False:
            estado = False
            lista.append(estado)
        else:
            estado = True
            lista.append(estado)
    print(lista)
    if lista[0]== True and lista[1] == True:
        lis = busqueda(o,d)
        #direccion_distancica(lis)
        mensaje= "Nodos Correctos"
        return mensaje
    else:
        mensaje = "Uno o mas nodos no estan en el db"
           
#obtenemos la direccion 
def direccion(origen,destino):
    x = None
    data, g = db()                  
    datos = data[(data["origen"] == origen) & (data["destino"] == destino)] #comparamos en el db que el inicio y el fin son los deseados
    di = datos["direccion"]                         #obtenemos la direccion de ese inicio y fin 
    metros = g[origen][destino]["large"]            #obtenemos la distancia de el grafo entre destino y origen
    for i in di:                    
        x = i #x.append(i)
    if x == 1:
        lado = x#"derecha"
    elif x == 2:
        lado = x#"arriba"
    elif x == 3:
        lado = x#"izquierda"
    elif x == 4:
        lado = x #"abajo"
    y = "La distancia de {} a {} es {} y hacia {} \n".format(origen, destino, metros, lado)
    return y,x

def comunicacion_arduino(nodo):
    arduino = serial.Serial("COM4", 9600)
    time.sleep(2)
    arduino.write(nodo.encode())
    time.sleep(.5)
    arduino.close()



#y = direccion("A","B")