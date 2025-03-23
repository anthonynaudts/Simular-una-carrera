import time
import random
import tracemalloc
import threading
import ttkbootstrap as tb
from ttkbootstrap.constants import *

def ordenamientoBurbuja(lista):
    elementos = len(lista)
    for i in range(elementos):
        for j in range(0, elementos - i - 1):
            if lista[j] > lista[j + 1]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]

def quickSort(lista):
    if len(lista) <= 1:
        return lista
    division = lista[len(lista) // 2]
    menores = [elemento for elemento in lista if elemento < division]
    iguales = [elemento for elemento in lista if elemento == division]
    mayores = [elemento for elemento in lista if elemento > division]
    return quickSort(menores) + iguales + quickSort(mayores)

def metodoInsercion(lista):
    for i in range(1, len(lista)):
        numeroActual = lista[i]
        posicion = i - 1
        while posicion >= 0 and numeroActual < lista[posicion]:
            lista[posicion + 1] = lista[posicion]
            posicion -= 1
        lista[posicion + 1] = numeroActual

def busquedaSecuencial(lista, numero):
    for indice in range(len(lista)):
        if lista[indice] == numero:
            return indice
    return -1

def busquedaBinaria(lista, numero):
    izquierda, derecha = 0, len(lista) - 1
    while izquierda <= derecha:
        posicionCentral = (izquierda + derecha) // 2
        if lista[posicionCentral] == numero:
            return posicionCentral
        elif lista[posicionCentral] < numero:
            izquierda = posicionCentral + 1
        else:
            derecha = posicionCentral - 1
    return -1



def medirTiempoYMemoria(algoritmo, datos):
    tracemalloc.start()
    inicio = time.perf_counter()
    algoritmo(datos)
    fin = time.perf_counter()
    memoria = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    return fin - inicio, memoria

def ejecutarAlgoritmos():
    cantidadNumeros = int(cantidadNumerosVector.get())
    listaNumeros = [random.randint(0, 10000) for _ in range(cantidadNumeros)]
    numeroBuscar = listaNumeros[random.randint(0, cantidadNumeros - 1)]

    etiquetaEstadoBoton.config(text="Ejecutando...", foreground="yellow")
    botonIniciar.config(state=DISABLED)
    barraProgreso.start()
    ventana.update_idletasks()
    
    

    algoritmos = {
        "Búsqueda secuencial": lambda: medirTiempoYMemoria(lambda arr: busquedaSecuencial(arr, numeroBuscar), listaNumeros.copy()),
        "Búsqueda binaria": lambda: medirTiempoYMemoria(lambda arr: busquedaBinaria(arr, numeroBuscar), sorted(listaNumeros.copy())),
        "Ordenamiento burbuja": lambda: medirTiempoYMemoria(ordenamientoBurbuja, listaNumeros.copy()),
        "Quick sort": lambda: medirTiempoYMemoria(quickSort, listaNumeros.copy()),
        "Método de inserción": lambda: medirTiempoYMemoria(metodoInsercion, listaNumeros.copy())
    }
    
    resultados = {}
    hilos = []
    for nombre, funcion in algoritmos.items():
        hilo = threading.Thread(target=lambda n=nombre, f=funcion: resultados.update({n: f()}))
        hilos.append(hilo)
        hilo.start()
    
    for hilo in hilos:
        hilo.join()
    
    etiquetaEstadoBoton.config(text="Finalizado", foreground="lightgreen")
    botonIniciar.config(state=NORMAL)
    barraProgreso.stop()
    mostrarResultados(resultados)

def mostrarResultados(resultados):
    for widget in ventadaResultados.winfo_children():
        widget.destroy()

    if not resultados:
        return

    busquedas = {k: v for k, v in resultados.items() if k in ("Búsqueda secuencial", "Búsqueda binaria")}
    ordenamientos = {k: v for k, v in resultados.items() if k in ("Ordenamiento burbuja", "Quick sort", "Método de inserción")}


    masRapidaBusqueda = min(busquedas.items(), key=lambda x: x[1][0]) if busquedas else None
    masRapidoOrdenamiento = min(ordenamientos.items(), key=lambda x: x[1][0]) if ordenamientos else None

    def agregarSeccion(titulo, datos, masRapido):
        if not datos:
            return

        tb.Label(ventadaResultados, text=titulo, font=("Arial", 14, "bold"), bootstyle=SUCCESS).pack(pady=5)

        for nombre, (tiempo, memoria) in datos.items():
            color = "primary" if masRapido and nombre == masRapido[0] else "dark"

            card = tb.Frame(ventadaResultados, bootstyle=color, padding=10)
            card.pack(fill=X, padx=10, pady=5)

            tb.Label(card, text=nombre, font=("Arial", 12, "bold"), bootstyle=INVERSE).pack()
            tb.Label(card, text=f"Tiempo: {tiempo:.12f} s\nMemoria: {memoria / 1024:.6f} KB", font=("Arial", 10)).pack()

    agregarSeccion("Resultados búsqueda", busquedas, masRapidaBusqueda)
    agregarSeccion("Resultados ordenamiento", ordenamientos, masRapidoOrdenamiento)

    if masRapidaBusqueda and masRapidoOrdenamiento:
        texto_resultado = f"Algoritmos más rápidos\nBúsqueda: {masRapidaBusqueda[0]} | Ordanamiento: {masRapidoOrdenamiento[0]}"
    else:
        texto_resultado = masRapidaBusqueda[0] if masRapidaBusqueda else masRapidoOrdenamiento[0]

    etiquetaResultado.config(text=texto_resultado, foreground="lightgreen", anchor="center", justify="center")




ventana = tb.Window(themename="superhero")
ventana.title("Comparación de Algoritmos")
ventana.geometry("900x850")
ventana.resizable(False, False)


ventanaVista = tb.Frame(ventana, bootstyle=SECONDARY, padding=15)
ventanaVista.pack(pady=10, padx=20, fill=X)

tb.Label(ventanaVista, text="Cantidad de números:", font=("Arial", 12), bootstyle=INVERSE).pack(side=LEFT, padx=5)

cantidadNumerosVector = tb.Entry(ventanaVista, width=10, font=("Arial", 12))
cantidadNumerosVector.insert(0, "1000")
cantidadNumerosVector.pack(side=LEFT, padx=5)

botonIniciar = tb.Button(ventanaVista, text="▶ Ejecutar", command=ejecutarAlgoritmos, bootstyle=SUCCESS, padding=(10, 5))
botonIniciar.pack(side=LEFT, padx=10)

etiquetaEstadoBoton = tb.Label(ventanaVista, text="Listo", font=("Arial", 12, "bold"), foreground="lightgreen")
etiquetaEstadoBoton.pack(side=LEFT, padx=10)

barraProgreso = tb.Progressbar(ventana, mode="indeterminate", bootstyle=INFO)
barraProgreso.pack(pady=10, fill=X, padx=20)

ventadaResultados = tb.Frame(ventana, padding=15)
ventadaResultados.pack(pady=10, fill=BOTH, expand=True)

etiquetaResultado = tb.Label(ventana, text="Esperando ejecución...", font=("Arial", 14, "bold"), bootstyle=SUCCESS)
etiquetaResultado.pack(pady=10)

ventana.mainloop()
