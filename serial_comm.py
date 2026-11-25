import serial
import serial.tools.list_ports

class Serial_comm:
    def __init__(self, port=None, baudrate=9600, timeout=1):
        """
        Inicializa a comunicação serial
        
        Args:
            port (str, optional): Nome da porta serial (ex: 'COM3' ou '/dev/ttyUSB0'). 
                                 Se None, tentará auto-detectar. Default: None.
            baudrate (int, optional): Taxa de transmissão. Default: 9600.
            timeout (int, optional): Timeout em segundos. Default: 1.
        """
        self.serial_port = None
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        
        if port is None:
            self.port = self._auto_detect_port()
        
        self._connect()
    
    def _auto_detect_port(self):
        """Tenta auto-detectar a porta serial disponível"""
        ports = serial.tools.list_ports.comports()
        if not ports:
            raise Exception("Nenhuma porta serial encontrada!")
        if len(ports) > 1:
            print("Múltiplas portas encontradas. Usando a primeira.")
        return ports[0].device
    
    def _connect(self):
        """Conecta à porta serial"""
        try:
            self.serial_port = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout
            )
            print(f"Conectado à porta {self.port} com baudrate {self.baudrate}")
        except serial.SerialException as e:
            raise Exception(f"Erro ao conectar na porta {self.port}: {str(e)}")
    
    def send_command(self, command, encoding='utf-8', wait_response=False):
        """
        Envia um comando pela porta serial
        
        Args:
            command (str/bytes): Comando a ser enviado (string ou bytes)
            encoding (str, optional): Codificação para strings. Default: 'utf-8'
            wait_response (bool, optional): Se True, aguarda e retorna a resposta
            
        Returns:
            str/None: Resposta do dispositivo (se wait_response=True) ou None
        """
        if not self.serial_port or not self.serial_port.is_open:
            raise Exception("Porta serial não está aberta!")
        
        try:
            # Converte string para bytes se necessário
            if isinstance(command, str):
                command = command.encode(encoding)
            
            # Envia o comando
            self.serial_port.write(command)
            
            # Se necessário, aguarda e retorna a resposta
            if wait_response:
                response = self.serial_port.read_until()  # Lê até encontrar um timeout ou caractere de nova linha
                return response.decode(encoding).strip()
            
            return None
            
        except serial.SerialException as e:
            raise Exception(f"Erro na comunicação serial: {str(e)}")
    
    def close(self):
        """Fecha a conexão serial"""
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
            print("Conexão serial fechada")
    
    def __del__(self):
        """Destrutor - fecha a conexão quando o objeto é destruído"""
        self.close()