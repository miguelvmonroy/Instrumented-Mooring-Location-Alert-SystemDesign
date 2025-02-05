import serial
import time
import keyboard  # Biblioteca para detectar teclas presionadas
import configTX  # Archivo de configuración con PORT y BAUDRATE

#####################################################################
# Función para manejar retardos en milisegundos
def delay_ms(milliseconds):
    time.sleep(milliseconds / 1000.0)

# Configuración de tiempos
delay_before = 1000  # Retardo antes del primer mensaje (ms)
delay_between = 2000  # Retardo entre envíos (ms)

# Mensaje a enviar (en hexadecimal)
message = "082f6c66206d756e6300"

# Retardo inicial
print(f"Esperando {delay_before} ms antes de iniciar el envío...")
delay_ms(delay_before)

def send_at_command(command):
    """Envía un comando AT y devuelve la respuesta."""
    try:
        with serial.Serial(configTX.PORT, configTX.BAUDRATE, timeout=5) as ser:
            ser.reset_input_buffer()  
            ser.reset_output_buffer()  
            print(f"Enviando comando: {command}")
            ser.write((command + '\r\n').encode())  
            time.sleep(1)  
            response = ser.read_all().decode(errors='ignore')  
            return response.strip() or "Sin respuesta"
    except serial.SerialException as e:
        return f"Error de conexión: {e}"
    except Exception as e:
        return f"Error: {e}"

def wait_for_ready():
    """Espera hasta que el módulo esté listo para una nueva transmisión."""
    while True:
        response = send_at_command("AT+PRECV=0")  
        if "OK" in response:
            break
        print("Módulo ocupado, esperando...")
        time.sleep(1)

if __name__ == "__main__":
    print("Configurando módulo como transmisor P2P...")

    # Configurar módulo en modo P2P
    send_at_command("AT+NWM=0")  
    send_at_command("AT+P2P=915000000,7,125,1,14,8")  

    print("Presiona 'q' para salir del ciclo de envío.")

    try:
        i = 1
        while True:
            if keyboard.is_pressed('q'):  
                print("Deteniendo el envío de mensajes...")
                break

            wait_for_ready()  # Esperar a que el módulo esté listo
            
            print(f"Envío {i}: Enviando mensaje: {message}")
            response = send_at_command(f"AT+PSEND={message}")
            print(f"Respuesta al envío {i}: {response}")

            print(f"Esperando {delay_between} ms antes del próximo envío...")
            delay_ms(delay_between)
            i += 1  
    except KeyboardInterrupt:
        print("Interrupción manual detectada. Saliendo...")
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        print("Operación completada.")
