import serial
import time
import keyboard  # Biblioteca para detectar teclas presionadas

# Configuración del puerto serie
PORT = 'COM8'  # Ajusta según el puerto correcto
BAUDRATE = 115200  

# Función para enviar comandos AT
def send_at_command(command, timeout=2):
    """Envía un comando AT al módulo y devuelve la respuesta."""
    try:
        with serial.Serial(PORT, BAUDRATE, timeout=timeout) as ser:
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            print(f"Enviando comando: {command}")
            ser.write((command + '\r\n').encode())  
            time.sleep(0.5)
            response = ser.read_all().decode(errors='ignore')
            return response.strip() or "Sin respuesta"
    except serial.SerialException as e:
        return f"Error de conexión: {e}"
    except Exception as e:
        return f"Error inesperado: {e}"

# Configuración inicial
print("Configurando módulo como transmisor P2P...")
send_at_command("AT+NWM=0")  
send_at_command("AT+P2P=915000000,7,125,1,14,8")  

print("Presiona 'q' para salir del ciclo de envío.")

# Envío en bucle
i = 1
try:
    while True:
        if keyboard.is_pressed('q'):
            print("Deteniendo el envío de mensajes...")
            break

        message = "486f6c61206d756e6410"  # Mensaje en hexadecimal
        print(f"Envío {i}: Enviando mensaje {message}")
        response = send_at_command(f"AT+PSEND={message}")

        if "+EVT:TXP2P DONE" in response:
            print(f"Mensaje {i} enviado con éxito.")
        else:
            print(f"Error en el envío {i}: {response}")

        time.sleep(0.5)
        i += 1
except KeyboardInterrupt:
    print("Interrupción manual detectada. Saliendo...")
finally:
    print("Operación finalizada.")
