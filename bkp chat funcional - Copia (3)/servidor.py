from socket import socket,AF_INET,SOCK_STREAM
from threading import Thread
import time

#Variaveis que compoe a chave publica recebida
q2=0
g2=0
h2=0
public_k2=0
powe2=0

#q1 = tcp.recv(1024)  # q
#g1 = tcp.recv(1024)  # g
#h1 = tcp.recv(1024)  # h
#public_k1 = tcp.recv(1024)  # public_k
#powe1 = tcp.recv(1024)  # powe

######################################################Funcoes para tratar o conteudo das mensagens#######################

#1 ENVIO trata a mensagem transformando seu conteudo de inteiro para string
def pre_proc(en_msg1):
 string = []
 for i in range(0, len(en_msg1)):
  string.append(str(en_msg1[i]))
 msg_pro = "-".join(string)  # msg processada para envio
 return msg_pro

#2 RECEBIMENTO trata a mensagem transformando seu conteudo de string para inteiro
def pos_pro(msg_ci):
 processo = msg_ci.split("-")
 inteiro = []
 for i in range(0, len(processo)):
  inteiro.append(int(processo[i]))

 return inteiro

################ Algoritmo ELGAMAL #####################

import random
from math import pow

a = random.randint(2, 10)

def gcd(a, b):
 if a < b:
  return gcd(b, a)
 elif a % b == 0:
  return b;
 else:
  return gcd(b, a % b)

 # Generating large random numbers


def gen_key(q):
 key = random.randint(pow(10, 20), q)
 while gcd(q, key) != 1:
  key = random.randint(pow(10, 20), q)

 return key


# Modular exponentiation
def power(a, b, c):
 x = 1
 y = a

 while b > 0:
  if b % 2 == 0:
   x = (x * y) % c;
  y = (y * y) % c
  b = int(b / 2)

 return x % c

# Asymmetric encryption
def encrypt(msg, q, h, chave_p, forca):
 en_msg = []

 k = chave_p  # public key
 s = power(h, k, q)
 p = forca

 for i in range(0, len(msg)):
  en_msg.append(msg[i])

 for i in range(0, len(en_msg)):
  en_msg[i] = s * ord(en_msg[i])

 return en_msg  # , p

def decrypt(en_msg, p, key, q):
 dr_msg = []
 h = power(p, key, q)
 for i in range(0, len(en_msg)):
  dr_msg.append(chr(int(en_msg[i] / h)))

 return dr_msg

########### START NA CRIAÇÃO DAS CHAVES   ######################


q = random.randint(pow(10, 20), pow(10, 50))
g = random.randint(2, q)

######### Privada criação da CHAVE PRIVADA ########
easy = random.randint(pow(10, 20), pow(10, 50))
key = gen_key(easy)  # Private
#######

h = power(g, key, q)
public_k = gen_key(q)  # Public key for sender
powe = power(g, public_k, q)
##########################

# Classe para manipular o socket
class Send:
 def __init__(self): #Inicializa a classe
  self.__msg=''
  self.new=True
  self.con=None
 def put(self,msg): #Envia  a mensagem no formato de string
  self.__msg=msg
  if self.con != None:
   #envia um mensagem atraves de uma conexão socket
   self.con.send(str.encode(self.__msg))
   #self.co.send(str.encode(self.__msg))

 def get(self):
  return self.__msg
 def loop(self):#mantem o ciclo de verificação dessa classe
  return self.new
 
#função esperar - Thread
def esperar(tcp,send,host='',port=5000):
 origem=(host,port)
 #cria um vinculo
 tcp.bind(origem)
 #deixa em espera
 tcp.listen(1) # nº de usuários suportados na conexao no servidor

 while True:
  #aceita um conexão
  con,cliente=tcp.accept()

  print('Cliente ',cliente,' conectado!')

  #atribui a conexão ao servidor
  send.con=con

  #############recebo 5 partes da chave apos iniciar a conexao ########
  time.sleep(10)
  rec_chav = tcp.recv(1024)
  armazena_chavep(tratar_rec_chave_p(rec_chav))

  while True:

   msg = tcp.recv(1024)
   if not msg:
    break
   print(str(msg, 'utf-8'))

   msg_rc = pos_pro(msg)
   dr_msg = decrypt(msg_rc, powe, key, q)
   dmsg = ''.join(dr_msg)
   print("Decrypted Message full :", dmsg);
   print(str(msg, 'utf-8'))



#cria um socket
tcp=socket(AF_INET,SOCK_STREAM)
send=Send()
#cria um Thread e usa a função esperar com dois argumentos
processo=Thread(target=esperar,args=(tcp,send))
processo.start()

print('Iniciando o servidor de chat!')
print('Aguarde alguém conectar!')


def envia_chave_pub(msg_form): #envia chave
 time.sleep(7)
 send.put(msg_form)

def tratar_env_chave_p(): #trata chave para o envio na msg
 string = []
 string.append(str(q))
 string.append(str(g))
 string.append(str(h))
 string.append(str(public_k))
 string.append(str(powe))
 msg_proc = "-".join(string)  # msg processada para envio
 return msg_proc

def tratar_rec_chave_p(chavp): #trata a chave recebida para utilizar nos calculos
 inteiros = []
 processo = chavp.split("-")
 for i in range(0, len(processo)):
  inteiros.append(int(processo[i]))

 return inteiros

def armazena_chavep(inteir):
 q2=inteir[0]
 g2=inteir[1]
 h2=inteir[2]
 public_k2=inteir[3]
 powe2=inteir[4]

 return q2,g2,h2,public_k2,powe2

#envia a chave
envia_chave_pub(tratar_env_chave_p())

msg=input()

while True:
  en_msg=encrypt(msg, q2,h2,public_k2, powe2)
  manda=pre_proc(en_msg)
  send.put(manda)
  msg=input()
  
processo.join()
tcp.close()
exit()