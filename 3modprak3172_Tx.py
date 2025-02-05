import serial
import time
import keyboard  # Biblioteca para detectar teclas presionadas
import configTX

#####################################################################
# Función para manejar retardos en milisegundos
def delay_ms(milliseconds):
    seconds = milliseconds / 1000.0  # Convertir a segundos
    time.sleep(seconds)

# Configuración del retardo
delay_before = 1000  # Retardo antes del mensaje (en ms)   
delay_between = 500  # Retardo entre cada envío (en ms)

# Mensaje a enviar (en hexadecimal)
message = "082f6c66206d756e6300"

# Retardo antes de enviar el primer mensaje
print(f"Esperando {delay_before} ms antes de iniciar el envío...")
delay_ms(delay_before)


def send_at_command(command):
    """Envía un comando AT al módulo y devuelve la respuesta."""
    try:
        with serial.Serial(configTX.PORT, configTX.BAUDRATE, timeout=5) as ser:
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
    print("Configurando módulo como transmisor P2P...")

    # Configurar el módulo en modo P2P
    send_at_command("AT+NWM=0")  # Cambiar a modo P2P
    send_at_command("AT+P2P=915000000,7,0,1,8,14")  # Parámetros ajustados
    
    print("Presiona 'q' en cualquier momento para salir del ciclo de envío.")
    
    try:
        # Enviar mensajes en un bucle continuo
        i = 1
        while True:
            if keyboard.is_pressed('q'):  # Verificar si se presiona la tecla 'q'
                print("Deteniendo el envío de mensajes...")
                break

            print(f"Envío {i}: Enviando mensaje: {message}")
            response = send_at_command(f"AT+PSEND={message}")
            print(f"Respuesta al envío {i}: {response}")
            
            print(f"Esperando {delay_between} ms antes del próximo envío...")
            delay_ms(delay_between)
            i += 1  # Incrementar contador
    except KeyboardInterrupt:
        print("Interrupción manual detectada. Saliendo...")
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        print("Operación completada.")