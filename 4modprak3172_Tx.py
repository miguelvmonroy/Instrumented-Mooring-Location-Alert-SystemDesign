import serial
import time
import keyboard  # Biblioteca para detectar teclas presionadas
import configTX

def delay_ms(milliseconds):
    time.sleep(milliseconds / 1000.0)  # Convertir a segundos y esperar

def send_at_command(command):
    try:
        with serial.Serial(configTX.PORT, configTX.BAUDRATE, timeout=5) as ser:
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            ser.write((command + '\r\n').encode())
            time.sleep(1)
            return ser.read_all().decode(errors='ignore').strip() or "Sin respuesta"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    message = "066d6D66256d756e6300"
    delay_before, delay_between = 1000, 500
    
    print(f"Esperando {delay_before} ms antes de iniciar el envío...")
    delay_ms(delay_before)
    
    send_at_command("AT+NWM=0")
    send_at_command("AT+P2P=915000000,7,0,1,8,14")
    
    print("Presiona 'q' para detener el envío.")
    i = 1
    try:
        while True:
            if keyboard.is_pressed('q'):
                print("Deteniendo el envío...")
                break
            
            print(f"Envío {i}: {message}")
            response = send_at_command(f"AT+PSEND={message}")
            print(f"Respuesta {i}: {response}")
            
            delay_ms(delay_between)
            i += 1
    except KeyboardInterrupt:
        print("Interrupción manual detectada.")
    finally:
        print("Operación completada.")