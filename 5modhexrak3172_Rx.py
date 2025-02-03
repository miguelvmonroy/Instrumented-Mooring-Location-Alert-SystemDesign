import serial
import time
import keyboard  # Nueva biblioteca para detectar teclas
import configRX  

# Constantes de configuración
DELAY_BETWEEN_CHECKS = 1  # Retardo entre ciclos (segundos)
LISTEN_TIMEOUT = 2000     # Tiempo de espera para recepción (ms)
RESPONSE_MESSAGE = "61636b"  # "ack" en hexadecimal

def send_at_command(command, port, baudrate, timeout=5):
    """Envía comando AT y devuelve respuesta (con puerto ya abierto)."""
    try:
        ser = serial.Serial(port, baudrate, timeout=timeout)
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write((command + '\r\n').encode())
        time.sleep(0.5)
        response = ser.read_all().decode(errors='ignore')
        ser.close()
        return response.strip() or "Sin respuesta"
    except Exception as e:
        return f"Error: {e}"

def process_rx_event(response):
    """Procesa evento de recepción y envía ACK automático."""
    try:
        if "+EVT:RXP2P" in response:
            parts = response.split(":")
            if len(parts) >= 4:
                hex_data = parts[-1].strip()
                text = bytes.fromhex(hex_data).decode('utf-8', errors='replace')
                print(f"Mensaje recibido: {text}")
                
                # Enviar ACK automático
                send_at_command(f"AT+PSEND={RESPONSE_MESSAGE}", 
                              configRX.PORT, configRX.BAUDRATE)
                print("ACK enviado")
                return True
        return False
    except Exception as e:
        print(f"Error procesando: {e}")
        return False

def configure_p2p_mode():
    """Configura módulo en modo P2P bidireccional."""
    print("Configurando módulo P2P...")
    send_at_command("AT+NWM=0", configRX.PORT, configRX.BAUDRATE)
    send_at_command("AT+P2P=915000000,7,125,1,14,8", configRX.PORT, configRX.BAUDRATE)

def listen_for_messages(timeout):
    """Escucha mensajes con timeout y envía ACK."""
    try:
        start_time = time.time()
        with serial.Serial(configRX.PORT, configRX.BAUDRATE, timeout=1) as ser:
            while (time.time() - start_time) * 1000 < timeout:
                if ser.in_waiting > 0:
                    data = ser.read_all().decode(errors='ignore')
                    if process_rx_event(data):
                        return True  # Mensaje recibido y ACK enviado
                time.sleep(0.1)
        return False  # Timeout
    except Exception as e:
        print(f"Error escuchando: {e}")
        return False

def main():
    """Función principal con modo bidireccional."""
    configure_p2p_mode()
    print("Modo lista/transmitir activado. Presiona:")
    print("q - Salir | t - Enviar mensaje manual")
    
    try:
        while True:
            # Escuchar mensajes con timeout
            if not listen_for_messages(LISTEN_TIMEOUT):
                print(f"Timeout: No hay mensajes en {LISTEN_TIMEOUT}ms")
            
            # Verificar si se presiona 't' para transmitir
            if keyboard.is_pressed('t'):
                mensaje = input("Ingrese mensaje en hex (ej: 686f6c61): ")
                response = send_at_command(f"AT+PSEND={mensaje}", 
                                         configRX.PORT, configRX.BAUDRATE)
                print(f"Respuesta TX: {response}")
            
            # Verificar salida
            if keyboard.is_pressed('q'):
                print("Saliendo...")
                break
                
            time.sleep(DELAY_BETWEEN_CHECKS)
            
    except KeyboardInterrupt:
        print("Interrupción manual")
    except Exception as e:
        print(f"Error crítico: {e}")
    finally:
        print("Operación finalizada")

if __name__ == "__main__":
    main()