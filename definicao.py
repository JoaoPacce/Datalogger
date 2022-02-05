import sqlite3

def valida(limite_inferior, limite_superior):
    """
   -> Verificar se tem coerencia nos dados inseridos
    :param limite_inferior: Valor de medição minímo do conversor
    :param limite_superior: Valor de medição maxímo do conversor
    """
    while True:
        if limite_inferior > limite_superior:
            print('Limites inválidos, digite novamente')
            limite_inferior = float(input('Digite o limite inferior'))
            limite_superior = float(input('Digite o limite superior'))
        else:
            break
    return limite_inferior, limite_superior


def escala(limite_inferior, limite_superior):
    """
    ->Validar os dados e descobrir a escala total
    :param limite_inferior: Valor minímo do conversor
    :param limite_superior: Valor maxímo do conversor
    :return: retorna a escala total do conversor e quanto vale  1 bits convertido
    """
    total = abs(limite_superior - limite_inferior)
    return total


def equivalente(escala_total,tipo_conversor):
    """
    ->Descobrir o valor equivalente de um único bit
    :param tipo_conversor: Tipo do conversor
    :param escala_total: Escala total do conversor
    :return: Retorna o valor equivalente a um bit
    """
    if tipo_conversor == 1 or tipo_conversor == 2:
        valor_1_bit = escala_total / 32768
        return valor_1_bit
    elif tipo_conversor == 3:
        valor_1_bit = escala_total / 26214
        #valor_1_bit = escala_total / 65535/2
        return valor_1_bit

def conversão(limite_inferior, valor_1_bit, valor_medido, tipo_conversor):
    """
    ->Converter valores medidos
    :param tipo_conversor: O tipo de conversor utilizado, tensão ou corrente(0-20mA / 4-20mA)
    :param limite_inferior: Valor minímo do conversor
    :param valor_1_bit: Valor equivalente a um bits do conversor
    :param valor_medido: Valor vindo do conversor
    :return: Valor já convertido
    """
    if tipo_conversor == 1 or tipo_conversor == 2:
        valor_convertido = valor_medido * valor_1_bit
        valor_real = limite_inferior + valor_convertido
    elif tipo_conversor == 3:
        if valor_medido <= 6553:
            return 'Conversor desconectado'
        elif valor_medido > 6553:
            valor_certo = (valor_medido - 6553)  # Faz a diferença e calcular o valor correspondente real
            valor_convertido = valor_certo * valor_1_bit
            valor_real = limite_inferior + valor_convertido
    return valor_real

def valor_real():
    return valor_real

def conversor(tipo_conversor):
    """
    -> Tipo de conversor que o usuario diz que vai usar
    :param tipo_conversor:
    :return: (número de identificação, tipo de sensor)
    """
    while True:
        if tipo_conversor == 1:
            return 1, 'Sensor tipo tensão'
            break
        elif tipo_conversor == 2:
            return 2, 'Sensor tipo corrente (0-20mA)'
            break
        elif tipo_conversor == 3:
            return 3, 'Sensor tipo corrente (4-20mA)'
            break
        else:
            print('Dado invalido, favor inserir uma das opções abaixo')
            tipo_conversor = int(input('''Digite o número correspondete ao sensor utilizado
            [1] Tensão
            [2] Corrente (0-20mA)
            [3] Corrente (4-20mA)
            Sensor corresponde ao número: '''))


# BACKUP DO BANCO DE DADOS
    # -> FAZER VERIFICAÇÃO DE NOME VÁLIDO 
def backup(self):
    file_name = input('Digite o nome do arquivo de backup: ')
    file_name = file_name + '.sql'
    with io.open(file_name, 'w') as f:
        for linha in self.conn.iterdump():
            f.write('%f\n' % linha)
    # VERIFICAR SE DEU CERTO
    print('Backup realizado com sucesso!')
    print('Salvo como: %s' % file_name)

def arquivo():
    """
    -> Pedir para salvar no mesmo arquivo ou criar um novo
    :param teste: Resposta do usuario
    :return: retorna o nome do novo banco de dados 
    """
    # CRIA UM NOVO ARQUIVO .db
    # CONFIGURA O SQLITE
    conn = sqlite3.connect('datalogger.db')
    cursor = conn.cursor()
    
    while True:
        novo = str(input('Deseja criar uma nova tabela? [S/N]: '))
        
        if novo in 'Ss':
            nome_tabela = str(input('Digite o nome da tabela: '))
            dados = nome_tabela
            continuar = input('Alerta: caso exista uma tabela com esse mesmo nome, a anterior sera apagada. Continuar? [S/N]: ')
            
            if continuar in 'Ss':
                cursor.execute("DROP TABLE IF EXISTS "+dados)
                cursor.execute("CREATE TABLE "+dados+"(id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,"
                               "dia TINYINT, mes TINYINT, ano SMALLINT, hora TINYINT,"
                               "minuto TINYINT, segundo TINYINT, dado FLOAT)")    
                break
            else:
                break
            
        elif novo in 'Nn':
            print('Alerta: caso a tabela não exista o programa resultará em erro')
            nome_tabela = str(input('Digite o nome da tabela: '))
            dados = nome_tabela
            break
        
        else:
            print('Resposta Inválida!')
            
    return nome_tabela
    
    
    
