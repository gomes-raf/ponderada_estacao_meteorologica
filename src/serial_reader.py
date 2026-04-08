import serial, json, requests, time, sys

PORTA = 'COM5' # Windows: COM3 / Linux: /dev/ttyUSB0
BAUD = 9600
URL = 'http://localhost:5000/leituras'

def ler_serial():
    sys.stdout.reconfigure(line_buffering=True)
    print(f'Tentando abrir porta {PORTA} a {BAUD} bauds...', flush=True)
    try:
        with serial.Serial(PORTA, BAUD, timeout=1) as ser:
            print(f'Porta {PORTA} aberta. Aguardando dados do Arduino...', flush=True)
            while True:
                linha = ser.readline().decode('utf-8', errors='replace').strip()
                if not linha:
                    continue
                print(f'Linha recebida: {linha}', flush=True)
                try:
                    dados = json.loads(linha)
                    try:
                        response = requests.post(URL, json=dados, timeout=3)
                        if response.ok:
                            print(f'Enviado: {dados}', flush=True)
                        else:
                            print(f'Falha HTTP {response.status_code}: {response.text}', flush=True)
                    except requests.exceptions.ConnectionError:
                        print(f'Erro: nao foi possivel conectar a {URL}. Verifique se o Flask esta rodando.', flush=True)
                    except requests.exceptions.Timeout:
                        print('Erro: timeout ao enviar dados para o servidor.', flush=True)
                except json.JSONDecodeError:
                    print(f'Linha invalida (nao eh JSON): {linha}', flush=True)
                except Exception as e:
                    print(f'Erro ao processar linha: {e}', flush=True)
    except serial.SerialException as e:
        print(f'Erro ao abrir a porta {PORTA}: {e}', flush=True)
        print('Feche o Serial Monitor/IDE se ele estiver usando a mesma porta e tente novamente.', flush=True)
    except KeyboardInterrupt:
        print('\nLeitura interrompida pelo usuario.', flush=True)

if __name__ == '__main__':
    ler_serial()