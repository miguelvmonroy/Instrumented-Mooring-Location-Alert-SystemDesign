import serial
import time
import keyboard  

def delay_ms(milliseconds):
    time.sleep(milliseconds / 1000.0)

delay_before = 1000  
delay_between = 500  

message = "3c33203c33203c33203c3320204d696775656c20616d612061204772657474656c2020203c33203c33203c33203c33"

PORT = 'COM8'  
BAUDRATE = 115200  

def send_at_command(ser, command, timeout=2):
    try:
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        print(f"Enviando comando: {command}")
        ser.write((command + '\r\n').encode())  
        time.sleep(0.1)  
        response = ser.read_until().decode(errors='ignore').strip()  
        print(f"Respuesta: {response}")
        return response
    except Exception as e:
        return f"Error: {e}"

def configurar_modulo(ser):
    print("Configurando módulo como transmisor P2P...")

    if "OK" not in send_at_command(ser, "AT+NWM=0"):
        print("Error al configurar el modo P2P")
        return False

    version = send_at_command(ser, "AT+VER=?")
    print(f"Versión del firmware: {version}")

    configuraciones_p2p = [
        "AT+P2P=915000000:7:0:0:8:14",
        "AT+P2P=915000000:7:125:0:8:14",
        "AT+P2P=915000000:7:0:1:8:14",
        "AT+P2P=915000000:7:125:1:8:14"
    ]

    for config in configuraciones_p2p:
        response = send_at_command(ser, config)
        if "OK" in response:
            print(f"Configuración P2P establecida: {config}")
            break
    else:
        print("No se pudo configurar P2P. Verifica los parámetros o el firmware.")
        return False

    if "OK" not in send_at_command(ser, "AT+PRECV=0"):
        print("Error al desactivar la recepción")
        return False

    print("Módulo configurado correctamente.")
    return True

def enviar_mensajes(ser):
    print("Presiona 'q' en cualquier momento para salir del ciclo de envío.")

    i = 1
    try:
        while True:
            if keyboard.is_pressed('q'):
                print("Deteniendo el envío de mensajes...")
                break

            print(f"Envío {i}: {message}")
            response = send_at_command(ser, f"AT+PSEND={message}")
            
            if "OK" not in response:
                print("Error en el envío del mensaje.")
            
            delay_ms(delay_between)
            i += 1
    except KeyboardInterrupt:
        print("Interrupción manual detectada. Saliendo...")

if __name__ == "__main__":
    print(f"Esperando {delay_before} ms antes de iniciar el envío...")
    delay_ms(delay_before)

    try:
        with serial.Serial(PORT, BAUDRATE, timeout=5) as ser:
            if configurar_modulo(ser):
                enviar_mensajes(ser)
    except serial.SerialException as e:
        print(f"Error al abrir el puerto serie: {e}")
    finally:
        print("Operación completada.")
