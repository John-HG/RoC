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
    #realizamso lo mismo que en el metodo anteriro pero agremamos una linea mas               
    _, g = db()                                         
    g.remove_node(error)                                #en esta linea removemos el nodo si es que el robot detecta 
                                                        #algun tipo de obstaculo   
    astar = list(nx.astar_path(g,source=star,target=stop, weight='destino'))           
                                                        #en este caso al eliminar el nodo se realiza la busqueda sin el 
                                                        #retornamos la lista 
                    
    return astar                                        

def direccion_distancica(lista):
    x = None
    data, g = db()                  
    for i in range(len(lista)-1):                       #obtener el numero de nodos de la lista
        origen = lista[i]                               #de la lista obtenemos el origen "virtual" por que siempre cambia 
        destino = lista[i+1]                            #de la lista obtenemos el destino "virtual"
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
        print("La distancia de {} a {} es {} y hacia {} \n".format(origen, destino, metros, lado))

#confirmamos la existencia del nodo en la db
def cofirmarnodo(nodo):
    data, _ = db()                              #obtenemos el db de la funcion db()
    confirm = data[data["origen"] == nodo]      #vemos si los nodos estan dentro del db
    c = len(confirm.index)                      #
    if c == 0:                                  #obtenemos si esta dentro 
        return False                            
    else:
        return True

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
        direccion_distancica(lis)
        mensaje= "Nodos Correctos"
        return mensaje
    else:
        mensaje = "Uno o mas nodos no estan en el db"
        

def verificacion(punto):
    espera = 10
    data, g = db()
    todos_los_nodos= g.nodes()
    t = time.time()  # ingresamos el tiempo base
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)#abrimos la camara
    #font = cv2.FONT_HERSHEY_PLAIN   // por si queremos mostrar algun mensaje en la pantalla de la camara
    #qr = [] #es un un arreglo vaicio el cual ya a contener la salida de la funcion
    estado = True #es la llave para el ciclo while creo que se puede cambiar y solamente poner while true y poner breaks
    time.sleep(1)
    while estado:
        n = time.time() #obtenemos el tiempo
        _, frame = cap.read() #creamos la variable frame la cual nos va a dar la lectura de la camara
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
        cv2.imshow("Frame", frame)
        if (n== t + espera) or (n>= t + espera): #aquie se genera la cuenta
            estado = False
        #else:
        #    print("{}".format(n-t)) # imprime el tiempo que va pasando
        key = cv2.waitKey(3) & 0xff
        if key == False:
            break
    cap.release()
    cv2.destroyAllWindows()

    if len(qr) != 0: # aqui manda el estado y el qr
        if qr == punto:
            return True, qr #si qr es igual al punto que mandamos envia un true y el punto
        else:
            return False, qr # si no manda un falso pero si lee algo y ese algo lo manda
    else:
        return False, None  # si no lee nada manda un falso y una lista vacia



           