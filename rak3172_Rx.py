import serial
import time

# Configuración del puerto y velocidad
PORT = 'COM5'  # Cambia según tu puerto detectado
BAUDRATE = 115200  # Velocidad predeterminada del módulo

def send_at_command(command):
    """Envía un comando AT al módulo y devuelve la respuesta."""
    try:
        with serial.Serial(PORT, BAUDRATE, timeout=5) as ser:
            ser.reset_input_buffer()  # Limpia el buffer de entrada
            ser.reset_output_buffer()  # Limpia el buffer de salida
            print(f"Enviando comando: {command}")
            ser.write((command + '\r\n').encode())  # Enviar comando
            time.sleep(1)  # Espera respuesta
            response = ser.read_all().decode(errors='ignore')  # Leer respuesta
            return response.strip() or "Sin respuesta"
    except serial.SerialException as e:
        return f"Error de conexión: {e}"
    except Exception as e:
        return f"Error: {e}"

# Codigo para el modulo receptor
if __name__ == "__main__":
    print("Configurando modulo como receptor P2P...")

# Configurar el modo en modo P2P    
send_at_command("AT+NWM=0") # Cambiar a modo P2P


send_at_command("AT+P2P=915000000,7,125,1,14,8")  
# Ejemplo Frecuencia 915 MHz, SF=7, BW=125kHz, CRC=ON, TxPower=14 dBm

#Parámetros del comando:

# Frecuencia: 915000000 (915 MHz, ajusta según tu región: 868 MHz en Europa, 915 MHz en América).
# SF (Spreading Factor): 7 (equilibrio entre alcance y velocidad).
# BW (Bandwidth): 125 (ancho de banda en kHz).
# CRC: 1 para habilitar el chequeo de errores (recomendado).
# Potencia de Transmisión: 14 dBm.
# Paquete: 8 bytes como tamaño máximo del paquete.

# Activar recepcion de datos
print("Esperando mensaje del transmisor...")
response = send_at_command("AT+PRECV=65535") #Modo Continuo para recibir mensajes
print(f"Datos recibidos: {response}")

response = send_at_command("AT+VER=?") #Modo Continuo para recibir mensajes
print(f"Version del firmware: {response}")

