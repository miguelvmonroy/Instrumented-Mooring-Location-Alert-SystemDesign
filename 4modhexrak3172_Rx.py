import serial
import time
import configRX

def setup_module():
    """Configura inicialmente el módulo en modo receptor P2P."""
    try:
        with serial.Serial(configRX.PORT, configRX.BAUDRATE, timeout=1) as ser:
            commands = [
                "AT+PRECV=0",    # Deshabilitar recepción temporalmente
                "AT+NWM=0",      # Configurar el módulo en modo normal (no LoRaWAN)
                "AT+P2P=915000000:7:0:1:8:14",  # Configurar parámetros P2P (ajustado)
                "AT+PRECV=65534" # Habilitar recepción continua
            ]
            for cmd in commands:
                ser.write(f"{cmd}\r\n".encode())
                time.sleep(1)  # Esperar para asegurar la respuesta
                response = ser.read_all().decode().strip()
                print(f"Enviado: {cmd} | Respuesta: {response}")
                if "ERROR" in response:
                    print(f"Error en comando: {cmd}")
                    break
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