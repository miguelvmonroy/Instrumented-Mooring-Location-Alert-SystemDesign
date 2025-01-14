import serial
import time

# Configuración del puerto y velocidad
PORT = 'COM9'  # Cambia según tu puerto detectado
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

if __name__ == "__main__":
    print("Iniciando prueba del RAK3172...")
    
    # Probar comando AT
    response = send_at_command("AT")
    print(f"Respuesta a AT: {response}")
    if "OK" not in response:
        print("No se obtuvo OK. Revisar conexión o configuración.")
        exit()
   
response = send_at_command("AT+NWM?")
print(f"Respuesta a AT+NWM?: {response}")

response = send_at_command("AT+NWM=0")
print(f"Respuesta a AT+NWM?: {response}")

send_at_command("AT+P2P=915000000,7,125,1,14,8")  
# Ejemplo Frecuencia 915 MHz, SF=7, BW=125kHz, CRC=ON, TxPower=10 dBm

#Parámetros del comando:

# Frecuencia: 915000000 (915 MHz, ajusta según tu región: 868 MHz en Europa, 915 MHz en América).
# SF (Spreading Factor): 7 (equilibrio entre alcance y velocidad).
# BW (Bandwidth): 125 (ancho de banda en kHz).
# CRC: 1 para habilitar el chequeo de errores (recomendado).
# Potencia de Transmisión: 14 dBm.
# Paquete: 8 bytes como tamaño máximo del paquete.


 # Enviar datos
print("Enviando mensaje...")
response = send_at_command("AT+P2PSEND=Hola, P2P!")# Envía el mensaje "Hola"
print(f"Respuesta a envío: {response}")


# Recibir datos
print("Esperando mensaje...")
response = send_at_command("AT+P2PRECV")
print(f"Datos recibidos: {response}")

