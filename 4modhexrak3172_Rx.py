import serial
import time
import configRX

def send_at_command(ser, command):
    """Envía un comando AT y devuelve la respuesta."""
    try:
        ser.write((command + '\r\n').encode())
        time.sleep(1)  # Esperar respuesta
        response = ser.read_all().decode(errors='ignore').strip()
        print(f"Enviado: {command} | Respuesta: {response}")
        return response
    except Exception as e:
        print(f"Error al enviar el comando {command}: {e}")
        return None

def setup_module():
    """Configura el módulo en modo receptor P2P."""
    try:
        with serial.Serial(configRX.PORT, configRX.BAUDRATE, timeout=1) as ser:
            # Verificar estado del módulo
            response = send_at_command(ser, "AT+NWM?")
            if "LoRa P2P" in response:
                print("Modo LoRa P2P ya configurado.")
            else:
                # Comandos para configurar el módulo
                commands = [
                    "AT+PRECV=0",  # Deshabilitar recepción temporalmente
                    "AT+NWM=0",    # Modo normal (no LoRaWAN)
                    "AT+P2P=915000000,7,0,1,8,14",  # Configurar parámetros P2P
                    "AT+PRECV=65534" # Habilitar recepción continua
                ]
                for cmd in commands:
                    send_at_command(ser, cmd)
                
                print("Módulo configurado correctamente.")
    except Exception as e:
        print(f"Error en configuración: {e}")

def listen_for_events():
    """Escucha continuamente eventos del módulo."""
    try:
        with serial.Serial(configRX.PORT, configRX.BAUDRATE, timeout=None) as ser:
            buffer = ""
            while True:
                data = ser.read_all().decode(errors='ignore')
                if data:
                    buffer += data
                    while '\n' in buffer:
                        line, buffer = buffer.split('\n', 1)
                        line = line.strip()
                        if line:
                            process_rx_event(line)
                time.sleep(0.1)
    except Exception as e:
        print(f"Error en escucha: {e}")

def process_rx_event(line):
    """Procesa cada línea recibida."""
    if "+EVT:RXP2P" in line:
        parts = line.split(":")
        if len(parts) >= 4:
            hex_data = parts[-1].strip()
            print(f"Datos codificados: {hex_data}")
            try:
                text = bytes.fromhex(hex_data).decode('utf-8', errors='replace')
                print(f"Datos decodificados: {text}")
            except ValueError:
                print("Error en conversión HEX a texto")
    else:
        print(f"Evento recibido: {line}")

if __name__ == "__main__":
    print("Iniciando configuración...")
    setup_module()
    print("Escuchando eventos...")
    listen_for_events()
