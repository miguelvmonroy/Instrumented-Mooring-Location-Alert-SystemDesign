####################################################################
#LIBRERIAS##

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from shapely.geometry import Point
import numpy as np
from PIL import Image, ImageTk
import time
import serial

####################################################################

# Definición de colores como variables
CFimpares = "white"
#Frames: 1,3,5,7
CFpares = "lightblue"
#Frames: 2,4,6,8
####################################################################


####################################################################

variablex1_1 = 200
variabley1_2 = 3
variablex2_3 = 50
variabley2_4 = 10

####################################################################

#Definiones 
def outer_func(parameter, label):
    def inner_func():
        print(f"{label} {parameter.get()}")
    return inner_func

# Función para crear el buffer alrededor de un punto
def create_buffer(point, radius):
    return point.buffer(radius)

####################################################################

# Configuración del puerto serial
SERIAL_PORT = "COM4"  # Cambia esto al puerto donde esté conectado tu ESP32C3
BAUD_RATE = 9600

# Inicializa el puerto serial
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Espera a que se inicialice la conexión serial
except serial.SerialException as e:
    print(f"Error al abrir el puerto serial: {e}")
    ser = None
####################################################################

def encender_led():
    if ser:
        ser.write(b'ON\n')  # Enviar comando 'ON' al microcontrolador
        print("Comando enviado: ON")

def apagar_led():
    if ser:
        ser.write(b'OFF\n') # Enviar comando 'OFF' al microcontrolador
        print("Comando enviado: OFF")










####################################################################

start_time = time.time()

# Crear la ventana principal
root = tk.Tk()
root.title("IMLAS- Instrumented Mooring Location Alert System")

# Dimensiones del Frame
frame_width =  400
frame_height = 400
banner_width = 380  # Ancho del banner
banner_height = 50  # Alto del banner

# Crear un Frame para el banner y colocarlo en la parte superior de la ventana
banner_frame = tk.Frame(root, width=banner_width, height=banner_height, bg="#ebe9eb")
banner_frame.pack(side="top", fill="x")

# Cargar la imagen del banner
banner_path = r"C:\Users\migue\OneDrive\Desktop\VSCode\Py\Tk\proyecto\banner.jpg"  # Ruta a la imagen del banner
try:
    banner_image = Image.open(banner_path)
    # Redimensionar la imagen del banner
    banner_image = banner_image.resize((banner_width, banner_height), Image.LANCZOS)
    banner_photo = ImageTk.PhotoImage(banner_image)

    # Crear un Label para mostrar el banner alineado a la izquierda en el Frame
    banner_label = tk.Label(banner_frame, image=banner_photo, anchor= "w") # Anchor 'w' alinea a la izquierda
    banner_label.image = banner_photo  # Mantener una referencia a la imagen
    banner_label.pack(side="left") #Colocar el banner a la izquierda
except FileNotFoundError:
    print(f"Error: No se pudo encontrar la imagen en la ruta: {banner_path}")

# Crear un Notebook (pestañas)
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# Crear la primera pestaña
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="Tab 1")

# Configurar que los frames se expandan en la primera pestaña
tab1.grid_rowconfigure(0, weight=1)  # Fila 0 tendrá un peso, permitiendo que crezca
tab1.grid_rowconfigure(1, weight=1)
tab1.grid_columnconfigure(0, weight=1)
tab1.grid_columnconfigure(1, weight=1)
tab1.grid_columnconfigure(2, weight=1)
tab1.grid_columnconfigure(3, weight=1)

# Crear y configurar los frames manualmente en la primera pestaña
frame1 = tk.Frame(tab1, bg=CFimpares, borderwidth=2, relief="solid")
frame1.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

# Hacer que el frame1 expanda en ambas direcciones
tab1.grid_rowconfigure(0, weight=1)
tab1.grid_columnconfigure(0, weight=1)

# Título en negrita
titulo1 = tk.Label(frame1, text="Ubicación del barco al anclaje", bg="lightblue", font=("Arial", 12, "bold"))
titulo1.pack(anchor='nw', padx=5, pady=5)  # Justificado a la izquierda en la parte superior

# Crear el frame adicional debajo del título
frame1_1 = tk.Frame(frame1, bg="gray", borderwidth=2, relief="solid")
frame1_1.pack(padx=5, pady=5, fill='x')  # Llenar horizontalmente

# Puedes agregar contenido al frame1_1 si es necesario
label_frame1_1 = tk.Label(frame1_1, text="", bg="gray", fg="white")
label_frame1_1.pack(padx=5, pady=5)

# Crear la figura de Matplotlib y el eje
fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.set_xlim(-5, 15)
ax.set_ylim(-5, 15)
ax.set_title("Movimiento de dos puntos con buffers circulares")

# Integrar la figura de Matplotlib en el Frame de Tkinter
canvas = FigureCanvasTkAgg(fig, master=frame1_1)
canvas.get_tk_widget().pack(fill="both", expand=True)


# Variables iniciales para la animación
x1 = variablex1_1
y1 = variabley1_2
x2 = variablex2_3
y2 = variabley2_4

buffer_radius = 1
steps = 20

# Función de animación
def animate():
    global x1, y1, x2, y2
    for step in range(steps):
        # Calcular los nuevos límites basados en las variables
        margin = 6  # Margen adicional para que no queden exactamente al borde
        min_x = min(variablex1_1, variablex2_3) - margin
        max_x = max(variablex1_1, variablex2_3) + margin
        min_y = min(variabley1_2, variabley2_4) - margin
        max_y = max(variabley1_2, variabley2_4) + margin

        # Limpiar el gráfico anterior
        ax.clear()
        ax.set_xlim(min_x, max_x)
        ax.set_ylim(min_y, max_y)
        ax.set_title("Movimiento de dos puntos con buffers circulares")

        # Crear puntos y buffers
        point1 = Point(x1, y1)
        point2 = Point(x2, y2)
        buffer1 = create_buffer(point1, buffer_radius)
        buffer2 = create_buffer(point2, buffer_radius)

        # Dibujar buffers
        buffer1_patch = plt.Polygon(np.array(buffer1.exterior.coords), color='blue', alpha=0.5)
        buffer2_patch = plt.Polygon(np.array(buffer2.exterior.coords), color='red', alpha=0.5)
        ax.add_patch(buffer1_patch)
        ax.add_patch(buffer2_patch)

        # Dibujar puntos y etiquetas
        ax.plot(*point1.xy, 'bo')
        ax.plot(*point2.xy, 'ro')
        ax.text(x1 + 0.3, y1 + 0.3, "Punto Azul", fontsize=9, ha='center', color='blue')
        ax.text(x2 + 0.3, y2 + 0.3, "Punto Rojo", fontsize=9, ha='center', color='red')

        # Actualizar posiciones de los puntos
        x1 += (x2 - x1) / steps
        y1 += (y2 - y1) / steps

        # Dibujar en el Canvas
        canvas.draw()
        root.update()  # Actualizar la interfaz para cada frame


# Llamar a la función de animación al cargar la interfaz
root.after(100, animate)

# Crear los demás frames en la primera pestaña
frame2 = tk.Frame(tab1, bg=CFpares, borderwidth=2, relief="solid")
frame2.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

titulo2 = tk.Label(frame2, text="LED", bg="lightblue", font=("Arial", 12, "bold"))
titulo2.pack(anchor='nw', padx=5, pady=5)

# Crear un subtítulo en frame2
subtitulo2 = tk.Label(frame2, text="Vin", bg="lightblue", font=("Arial", 10))
subtitulo2.pack(anchor='nw', padx=5, pady=(5, 0))  # Justificado a la izquierda en la parte superior

boton2 = tk.Button(frame2, text="Botón 2", bg="blue", fg="white")
boton2.pack(expand=True)

frame3 = tk.Frame(tab1, bg=CFimpares, borderwidth=2, relief="solid")
frame3.grid(row=0, column=2, padx=5, pady=5, sticky='nsew')

titulo3 = tk.Label(frame3, text="Título 3", bg="lightblue", font=("Arial", 12, "bold"))
titulo3.pack(anchor='nw', padx=5, pady=5)

boton3 = tk.Button(frame3, text="Botón 3", bg="blue", fg="white")
boton3.pack(expand=True)

frame4 = tk.Frame(tab1, bg=CFpares, borderwidth=2, relief="solid")
frame4.grid(row=0, column=3, padx=5, pady=5, sticky='nsew')

titulo4 = tk.Label(frame4, text="Título 4", bg="lightblue", font=("Arial", 12, "bold"))
titulo4.pack(anchor='nw', padx=5, pady=5)

boton4 = tk.Button(frame4, text="Botón 4", bg="blue", fg="white")
boton4.pack(expand=True)

frame5 = tk.Frame(tab1, bg=CFimpares, borderwidth=2, relief="solid")
frame5.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

# Título principal en frame5
titulo5 = tk.Label(frame5, text="GPS", bg="lightblue", font=("Arial", 12, "bold"))
titulo5.pack(anchor='nw', padx=5, pady=5)

# Subtítulo para las coordenadas1
subtitulo5_1 = tk.Label(frame5, text="Coordenadas1", bg="lightblue", font=("Arial", 10))
subtitulo5_1.pack(anchor='nw', padx=5, pady=(5, 0))  # Justificado a la izquierda en la parte superior

# Widgets para ingresar la latitud
entry_string_lat_1 = tk.StringVar(value='19.18')
frame_lat_1 = tk.Frame(frame5)  # Crear un frame para alinear la entrada y el botón
frame_lat_1.pack(anchor='nw', padx=5, pady=5, fill='x')

entry_lat_1 = ttk.Entry(frame_lat_1, textvariable=entry_string_lat_1)
entry_lat_1.pack(side='left')  # Posicionar el entry en el frame_lat

button_lat_1 = ttk.Button(frame_lat_1, text='Ingresar Latitud 1', command=outer_func(entry_string_lat_1, 'Latitud:'))
button_lat_1.pack(side='left', padx=10)

# Widgets para ingresar la longitud
entry_string_lon_1 = tk.StringVar(value='-91.8405')
frame_lon_1 = tk.Frame(frame5)  # Crear un frame para alinear la entrada y el botón
frame_lon_1.pack(anchor='nw', padx=5, pady=5, fill='x')

entry_lon_1 = ttk.Entry(frame_lon_1, textvariable=entry_string_lon_1)
entry_lon_1.pack(side='left')  # Posicionar el entry en el frame_lon

button_lon_1 = ttk.Button(frame_lon_1, text='Ingresar Longitud 1', command=outer_func(entry_string_lon_1, 'Longitud:'))
button_lon_1.pack(side='left', padx=10)

# Subtítulo para las coordenadas2
subtitulo5_2 = tk.Label(frame5, text="Coordenadas2", bg="lightskyblue", font=("Arial", 10))
subtitulo5_2.pack(anchor='nw', padx=5, pady=(5, 0))  # Justificado a la izquierda en la parte superior

# Widgets para ingresar la latitud
entry_string_lat_2 = tk.StringVar(value='7.15')
frame_lat_2 = tk.Frame(frame5)  # Crear un frame para alinear la entrada y el botón
frame_lat_2.pack(anchor='nw', padx=5, pady=5, fill='x')

entry_lat_2 = ttk.Entry(frame_lat_2, textvariable=entry_string_lat_2)
entry_lat_2.pack(side='left')  # Posicionar el entry en el frame_lat

button_lat_2 = ttk.Button(frame_lat_2, text='Ingresar Latitud 2', command=outer_func(entry_string_lat_2, 'Latitud:'))
button_lat_2.pack(side='left', padx=10)

# Widgets para ingresar la longitud
entry_string_lon_2 = tk.StringVar(value='81.82')
frame_lon_2 = tk.Frame(frame5)  # Crear un frame para alinear la entrada y el botón
frame_lon_2.pack(anchor='nw', padx=5, pady=5, fill='x')

entry_lon_2 = ttk.Entry(frame_lon_2, textvariable=entry_string_lon_2)
entry_lon_2.pack(side='left')  # Posicionar el entry en el frame_lon

button_lon_2 = ttk.Button(frame_lon_2, text='Ingresar Longitud 2', command=outer_func(entry_string_lon_2, 'Longitud:'))
button_lon_2.pack(side='left', padx=10)

### Crear un subtítulo en frame5
subtitulo5_1 = tk.Label(frame5, text="Temp del  GPS", bg="lightblue", font=("Arial", 10))
subtitulo5_1.pack(anchor='nw', padx=5, pady=(0, 10))  # Justificado a la izquierda en la parte superior

frame6 = tk.Frame(tab1, bg=CFpares, borderwidth=2, relief="solid")
frame6.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

titulo6 = tk.Label(frame6, text="Acelerómetro", bg="lightblue", font=("Arial", 12, "bold"))
titulo6.pack(anchor='nw', padx=5, pady=5)

# Crear un subtítulo en frame6
subtitulo6 = tk.Label(frame6, text="Serial", bg="lightblue", font=("Arial", 10))
subtitulo6.pack(anchor='nw', padx=5, pady=(5, 0))  # Justificado a la izquierda en la parte superior>

boton6 = tk.Button(frame6, text="Botón 6", bg="blue", fg="white")
boton6.pack(expand=True)

frame7 = tk.Frame(tab1, bg=CFimpares, borderwidth=2, relief="solid")
frame7.grid(row=1, column=2, padx=5, pady=5, sticky='nsew')

titulo7 = tk.Label(frame7, text="Título 7", bg="lightblue", font=("Arial", 12, "bold"))
titulo7.pack(anchor='nw', padx=5, pady=5)

boton7 = tk.Button(frame7, text="Botón 7", bg="blue", fg="white")
boton7.pack(expand=True)

frame8 = tk.Frame(tab1, bg=CFpares, borderwidth=2, relief="solid")
frame8.grid(row=1, column=3, padx=5, pady=5, sticky='nsew')

titulo8 = tk.Label(frame8, text="Título 8", bg="lightblue", font=("Arial", 12, "bold"))
titulo8.pack(anchor='nw', padx=5, pady=5)

boton8 = tk.Button(frame8, text="Botón 8", bg="blue", fg="white")
boton8.pack(expand=True)

# Crear la segunda pestaña
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="Tab 2")

# Crear y centrar un botón en la segunda pestaña
boton_tab2 = tk.Button(tab2, text="Botón Centrador", bg="green", fg="white")
boton_tab2.pack(expand=True)  # Centrar el botón en la pestaña

#Tiempo de ejecuccion.
print(f"Tiempo de ejecución: {time.time() - start_time} segundos")

# Ejecutar el bucle principal de la aplicación
root.mainloop()
