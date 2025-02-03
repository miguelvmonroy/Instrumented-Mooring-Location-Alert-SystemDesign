import serial
import time
import sys
import select
import configRX

# ... (mantén las constantes y funciones anteriores iguales)

def main():
    """Función principal sin dependencia de root."""
    configure_p2p_mode()
    print("Modo lista/transmitir activado. Presiona:")
    print("q - Salir | t - Enviar mensaje manual")
    
    try:
        while True:
            # Escuchar mensajes
            if not listen_for_messages(LISTEN_TIMEOUT):
                print(f"Timeout: No hay mensajes en {LISTEN_TIMEOUT}ms")
            
            # Verificar entrada de usuario sin keyboard
            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                line = sys.stdin.readline().strip().lower()
                if line == 't':
                    mensaje = input("Ingrese mensaje en hex (ej: 686f6c61): ")
                    response = send_at_command(f"AT+PSEND={mensaje}", 
                                             configRX.PORT, configRX.BAUDRATE)
                    print(f"Respuesta TX: {response}")
                elif line == 'q':
                    print("Saliendo...")
                    break
                
            time.sleep(DELAY_BETWEEN_CHECKS)
            
    except KeyboardInterrupt:
        print("Interrupción manual")
    except Exception as e:
        print(f"Error crítico: {e}")
    finally:
        print("Operación finalizada")