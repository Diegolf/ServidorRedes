# coding: utf-8

''' ServidorHTTP '''
import socket
import re
import os
import threading

class ServidorHTTP:

	# Constantes 
	EXTENSAO = {'jpg' : 'image/jpg', 
				'jpeg' : 'image/jpeg', 
				'png' : 'image/png', 
				'html' : 'text/html',
				'anyOther' : 'application/octetstream'}

	ERROR_HTML = '''HTTP/1.1 404
	Content-Type: text/html

	ERROR 404 NOT FOUND'''

	HEADER_HTML = '''HTTP/1.1 200 OK'''

	def __init__(self,ip = "127.0.0.1",porta = 8888):
		''' 	Construtor da classe
			Recebe como parâmetro o ip e a porta no qual o servidor vai operar 
			Inicia o servidor um servidor local na porta 8888 caso nenhum parâmetro seja passado'''

		# Socket TCP
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		
		# Tenta definir o socket para i ip e a porta informados
		try:
			self.s.bind((ip,porta))
		except:
			return

	def __servidorHTTP__(self,con):
		''' Trata a requisição do cliente '''
		# Recebe 1024 Bytes de dados
		dados = con.recv(1024)	

		# Termina a leitura caso o cliente feche a conexão
		if not dados:
			con.close()

		# Utiliza expressão regular para separar a página requisitada do cabeçalho
		requisicao = re.findall(r"(?<=GET )[^ ]+(?= )",dados)		

		# Remove o caractere '/' da requisiçãol
		requisicao = re.sub(r"^/","",requisicao[0])
		requisicao = re.sub(r'%20'," ",requisicao)
	
		# Utiliza expressão regular para separar a extensão da requisição
		extensao = re.findall(r"(?<=\.).+(?=$)",requisicao)

		# Não tem extensão, ex: 127.0.0.1/folder1/folder2
		if not extensao:
		
			# Verifica se a requisição é um diretório válido
			if (os.path.isdir('./'+requisicao)):
		
				# Inicia a variável resposta com a constante HEADER_HTML
				resposta = self.HEADER_HTML
		
				# Concatena o cabeçalho da resposta HTML com o formato da resposta
				resposta += "\nContent-type: "+ self.EXTENSAO['html']
		
				# Armazena uma lista com os diretórios e arquivos do diretório atual
				dirAtual = os.listdir('./'+requisicao)

				paginaHtml = "<html>\n\t<head></head>\n\t<body>\n"

				# Inicia uma variável do tipo str
				if '/' in requisicao:
					paginaHtml += '\t\t<a href="{0}/.">..</a><br>\n'.format(re.sub(r"/.*$","",requisicao))
				elif re.search(r'\w+',requisicao):
					paginaHtml += '\t\t<a href=".">..</a><br>\n'
		
				#  Concatena a variável paginaHtml com cada diretório e arquivo do 
				# diretório atual, em forma de link.
				print
				for dirA in dirAtual:
					paginaHtml += "\t\t<a href=\"{1}/{0}\">{0}</a><br>\n".format(dirA,requisicao)
				
				paginaHtml += "\t</body>\n</html>"

				# Concatena a variável resposta com o tamanho da página html resposta
				resposta += "\nContent-Lenght: " + str(len(paginaHtml)) + "\n\n"
				resposta += paginaHtml
			else:
		
				# Se não for um diretório válido retorna uma página default com uma resposta 404 
				resposta = self.ERROR_HTML
		
			# Envia a resposta ao cliente
			con.send(resposta)
		
			# Fecha a conexão com o cliente
			con.close()
		
			# Termina a funcção
			return
		# if not extensao

		# Armazena na varíavel extensao um str, removido da lista anterior
		extensao = extensao[-1]

		# Verifica se é uma extensão conhecida (pertencente ao dicionário EXTENSAO desta classe)
		try:
			self.EXTENSAO[extensao]
		except:
			extensao = "anyOther"

		# Resposta com uma página HTML
		try:			
			# Inicia a variável
			indexHtml = ""

			# Abre o arquivo html
			with open(requisicao) as i:
				# Armazena o conteúdo do arquivo em uma variável
				indexHtml += i.read()
			# Inicia a variável com o header default
			resposta = self.HEADER_HTML

			# Concatena a variável com o tipo do arquivo da resposta
			resposta += "\nContent-Type: " + self.EXTENSAO[extensao]

			# Concatena a variável com o tamanho do arquivo da resposta
			resposta += "\nContent-Length: " + str(len(indexHtml)) + "\n\n"
			
			# Concatena a resposta com a página hmtl
			resposta += indexHtml

			# Envia a resposta ao cliente
			con.send(resposta)
		except:
			# Envia uma página default com uma resposta 404
			con.send(self.ERROR_HTML)

		# Fecha a conexão com o cliente
		con.close()
	# __servidorHTTP__()

	def iniciarServidor(self):
		''' Inicia o servidor http '''

		while True:
			self.s.listen(1)

			# Exibe uma mensagem no console/prompt
			print "Aguardando conexão...\n"

			con, info_cli = self.s.accept()

			#  Utiliza uma thread para tratar a conexão com o cliente, assim deixando o servidor
			# livre para realizar conexões com outros clientes
			t1 = threading.Thread(target=self.__servidorHTTP__, args=[con])
			
			# Inicia a thread
			t1.start()

		# Termina a conexão com o cliente
		con.close()
		
	# iniciarServidor()
# class ServidorHTTP

#from servidorHTTP import ServidorHTTP
#se = ServidorHTTP()
#se.iniciarServidor()