from socket import *
import sys

#AF_INET = IPv4
#SOCK_STREAM = TCP
serverSocket = socket(AF_INET, SOCK_STREAM) 

serverSocket.bind(('', 6789)) #Associa o socket à porta 6789 (definida na atividade)
serverSocket.listen(1) #Faz o servidor começar a ouvir conexões, porém o número 1 indica a fila máxima de conexões pendentes

while True:
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept() #Aceita a conexão do cliente

    try:
        message = connectionSocket.recv(1024).decode() #Vai receber oss primeiros 1024 bytes da requisição e transformar eles em string

        filename = message.split()[1] #Divide por espaços
        f = open(filename[1:]) #Remove a barra inicial e abre o arquivo requisitado
        outputdata = f.read() #Lê o conteúdo do arquivo e guarda numa string

        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode()) #Envia o texto escrito entre as aspas (\r\n\r\n separa o cabeçalho do corpo do arquivo)

        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode()) #Envia caractere por caractere

        connectionSocket.send("\r\n".encode()) #Finaliza o envio com uma quebra de linha

        connectionSocket.close() #Fecha a conexão com o cliente que estava usando o servidor 

    except IOError: #Para caso o arquivo não exista
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode()) #Envia o cabeçalho de erro
        connectionSocket.send("<h1>404 Not Found</h1>".encode()) #Envia uma página HTML simples

        connectionSocket.close() 

serverSocket.close() #Fecha o socket 
sys.exit() #Encerra o programa


