# Estação Meteorológica IoT

Sistema completo para monitoramento de condições ambientais usando Arduino e interface web Flask.

## Funcionalidades

- Leitura de temperatura e umidade via sensor DHT11
- Interface web responsiva com painel de controle
- API REST completa para CRUD de leituras
- Gráfico de variação temporal das medições
- Histórico completo com paginação
- Comunicação serial Arduino ↔ Python ↔ Web

## Arquitetura do Sistema

Este projeto segue a mesma estrutura proposta no barema, com três camadas bem definidas:

- **Dispositivo (Hardware)**: Arduino Uno + sensores DHT11 (temperatura e umidade) e, opcionalmente, BMP280 (pressão). O Arduino realiza a leitura dos sensores e envia os dados via porta serial USB.
- **Servidor (Backend)**: Python + Flask + SQLite. O backend recebe leituras via API REST, armazena os dados no banco e expõe endpoints para consulta e gerenciamento.
- **Interface (Frontend)**: HTML + CSS + JavaScript + Jinja2. A interface exibe as leituras, permite edição/exclusão e mostra o gráfico temporal.

Essa abordagem foi escolhida para manter o fluxo de dados alinhado ao especificado: Arduino → Porta Serial USB → Script Python (leitura serial) → API Flask (POST) → SQLite (persistência) → Interface Web (GET). Dessa forma, seguimos exatamente a mesma arquitetura proposta e garantimos separação clara entre hardware, backend e frontend.

## Hardware Necessário

### Componentes

- Arduino Uno (ou compatível)
- Sensor DHT11 (temperatura e umidade)
- Cabo USB para conexão Arduino ↔ Computador
- Jumpers para conexões
- Protoboard (opcional)

### Conexão do Sensor DHT11

```
Arduino Uno          DHT11
-----------          -----
   5V   ------------>  VCC
   GND  ------------>  GND
   A1   ------------>  DATA
```

**Atenção:**

- Use resistor pull-up de 10kΩ entre DATA e VCC se necessário
- Verifique a pinagem do seu sensor DHT11 (alguns têm ordem diferente)
- Pino de dados conectado ao pino digital 2 do Arduino

### Adição do Sensor BMP280 (Pressão - Opcional)

Para adicionar medição de pressão atmosférica:

```
Arduino Uno          BMP280
-----------          ------
   3.3V   ------------>  VCC
   GND  ------------>  GND
   A4   ------------>  SDA
   A5   ------------>  SCL
```

**Bibliotecas necessárias no Arduino IDE:**

- Adafruit_BMP280
- Adafruit_Sensor

## Instalação e Configuração

### Pré-requisitos

- Python 3.8 ou superior
- Arduino IDE
- Git

### 1. Clone o Repositório

```bash
git clone <url-do-repositorio>
cd ponderada_estacao_meteorologica
```

### 2. Instale as Dependências Python

```bash
cd src
pip install flask requests pyserial
```

### 3. Configure o Banco de Dados

O banco SQLite será criado automaticamente na primeira execução.

### 4. Carregue o Sketch no Arduino

1. Abra o Arduino IDE
2. Instale a biblioteca DHT:
   - Sketch → Incluir Biblioteca → Gerenciar Bibliotecas
   - Procure por "DHT sensor library" e instale
3. Abra o arquivo `arduino/estacao.ino`
4. Selecione a placa correta: Ferramentas → Placa → Arduino Uno
5. Selecione a porta correta: Ferramentas → Porta
6. Carregue o sketch: Sketch → Carregar (Ctrl+U)

## Execução

### 1. Inicie o Servidor Web

```bash
cd src
python app.py
```

O servidor estará disponível em: http://localhost:5000

### 2. Inicie a Leitura Serial (em outro terminal)

```bash
cd src
python serial_reader.py
```

### 3. Acesse a Interface Web

Abra seu navegador e vá para: http://localhost:5000

## Como Usar

### Interface Web

1. **Página Inicial (/)**: Visualize as últimas leituras e adicione novas manualmente
2. **Histórico (/historico)**: Veja todas as leituras em tabela + gráfico temporal
3. **Edição**: Clique em "Editar" em qualquer leitura para corrigir valores

### API REST

Base URL: http://localhost:5000

#### Endpoints Disponíveis:

- `GET /leituras` - Lista todas as leituras
- `GET /leituras/{id}` - Obtém leitura específica
- `POST /leituras` - Cria nova leitura
- `PUT /leituras/{id}` - Atualiza leitura
- `DELETE /leituras/{id}` - Remove leitura

#### Exemplo de uso da API:

```bash
# Criar leitura
curl -X POST http://localhost:5000/leituras \
  -H "Content-Type: application/json" \
  -d '{"temperatura": 25.5, "umidade": 60.0, "pressao": 1013.2}'

# Listar leituras
curl http://localhost:5000/leituras
```

## Configuração Avançada

### Porta Serial

Por padrão, o sistema usa `COM5`. Para alterar:

1. Abra `src/serial_reader.py`
2. Modifique a linha: `PORTA = 'COM5'` para sua porta

### Intervalo de Leitura

Para alterar o intervalo de envio do Arduino:

1. Abra `arduino/estacao.ino`
2. Modifique `delay(5000)` (valor em milissegundos)

### Banco de Dados

O arquivo `schema.sql` contém a estrutura da tabela. Para recriar:

```bash
cd src
rm database.db  # Remove o banco atual
python -c "from database import init_db; init_db()"
```

## Solução de Problemas

### Erro: "ModuleNotFoundError: No module named 'serial'"

```bash
pip install pyserial
```

### Erro: "could not open port 'COM5'"

- Feche o Serial Monitor do Arduino IDE
- Verifique se a porta está correta no Gerenciador de Dispositivos
- Reinicie o Arduino

### Erro: "SerialException: device reports readiness to read but returned no data"

- Verifique as conexões do sensor DHT11
- Certifique-se que o sensor está alimentado corretamente
- Teste com outro sensor se possível

### Gráfico não aparece

- Verifique se há dados no banco
- Abra o console do navegador (F12) para erros JavaScript
- Certifique-se que Chart.js está carregando

### Arduino não envia dados

- Abra o Serial Monitor (9600 baud) para verificar se o Arduino está enviando JSON
- Verifique se o sensor DHT11 está conectado corretamente
- Teste com valores fixos no código do Arduino

## Estrutura do Projeto

```
src/
├── app.py                 # Servidor Flask principal
├── database.py            # Funções CRUD do SQLite
├── serial_reader.py       # Leitor serial Arduino
├── schema.sql            # Estrutura do banco
├── arduino/
│   └── estacao.ino       # Sketch Arduino
├── templates/            # Templates Jinja2
│   ├── base.html
│   ├── index.html
│   ├── historico.html
│   └── editar.html
├── static/               # Arquivos estáticos
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
└── README.md
```
