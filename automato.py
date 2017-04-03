from estado import *

class Automato():
	def __init__(self, cadeia = ""):
		self.estados = {}
		self.simbolos = []
		self.direcaoLeitura = "d"
		self.fita = cadeia
		self.posicaoCabecote = 0
		self.estadoAtual = None

	def _imprimeConfiguracao(self):
		print("Dipositivo na configuração M = " + self.estadoAtual.nome, end=" X ") 
		print(self.fita[:self.posicaoCabecote], end=" X ")
		print(self.fita[self.posicaoCabecote], end=" X ")
		print(self.fita[self.posicaoCabecote + 1:], end="\n\n")

	def erroFaltaDeTransicao(self):
		print("Ocorreu um erro de falta de transição")

	def erroFimDaFita(self):
		print("O automato tentou recuar à esquerda do fim da fita, e portanto a máquina ficou bloqueada")

	def adicionaEstado(self, nomeEstado, estado):
		self.estados[nomeEstado] = estado
	
	def adicionaSimbolo(self, simbolo):
		self.simbolos.append(simbolo)

	def adicionaTransicao(self, origem, simbolo, destino):
		self.estados[origem].transicoes[simbolo] = destino

	def inicializa(self, cadeia, rastro = True):
		for estado in self.estados:
			if self.estados[estado].inicial:
				self.estadoAtual = self.estados[estado]
		self.fita = cadeia

	def movimentoCabecote(self, rastro):
		self.posicaoCabecote += 1
		if rastro:
			print("Cabeçote encontra-se na posição " + str(self.posicaoCabecote))
			self._imprimeConfiguracao()
		return ""

	def fimSimulacao(self):
		if self.estadoAtual.aceitacao:
			print("Dispositivo atingiu estado de aceitacao")
		else:
			print("Dispositivo nao atingiu estado de aceitacao")

		self._imprimeConfiguracao()

class AutomatoFinito(Automato):
	def __init__(self):
		super().__init__()
		self.direcaoLeitura = "d"

	def inicializa(self, cadeia, rastro = True):
		super().inicializa(cadeia, rastro)
		self.posicaoCabecote = 0
		if rastro:
			self._imprimeConfiguracao()

	def leSimbolo(self, rastro):
		simbolo = self.fita[self.posicaoCabecote]
		if simbolo == "#":
			return ['fim']
		else:
			try:
				nomeNovoEstado = self.estadoAtual.transicoes[simbolo][0]
			except KeyError:
				raise
			
			if rastro:
				print("A máquina consome o símbolo " + simbolo, end ="")
				print(" e vai do estado " + self.estadoAtual.nome, end="")
				print(" ao estado " + nomeNovoEstado)

			for estado in self.estados:
				if estado == nomeNovoEstado:
					self.estadoAtual = self.estados[estado]

			return [""]

class AutomatoDePilha(Automato):
	def __init__(self):
		super().__init__()
		self.direcaoLeitura = "d"
		self.pilha = []
		self.submaquinas = {}

	def inicializa(self, cadeia, posicaoCabecote = 0, rastro=True):
		super().inicializa(cadeia, rastro)
		self.posicaoCabecote = posicaoCabecote
		self.maquinaAtual = self
		if rastro:
			self._imprimeConfiguracao()

	def empilha(self, rastro, estado, submaquina):
		if rastro:
			print("------------------Chamada da submaquina " + submaquina + "------------------")
		self.maquinaAtual = self.maquinaAtual.submaquinas[submaquina]
		self.maquinaAtual.inicializa(self.fita, self.posicaoCabecote, False)
		self.pilha.append(estado)

	def desempilha(self, rastro):
		if rastro:
			print("------------------Retorno de submaquina------------------")
		self.maquinaAtual = self
		nomeNovoEstado = self.pilha.pop()
		for estado in self.maquinaAtual.estados:
			if estado == nomeNovoEstado:
				self.maquinaAtual.estadoAtual = self.maquinaAtual.estados[estado]

	def fimSimulacao(self):
		if self.maquinaAtual.estadoAtual.aceitacao and len(self.pilha) == 0:
			print("Dispositivo atingiu estado de aceitacao")
		else:
			print("Dispositivo nao atingiu estado de aceitacao")

		self._imprimeConfiguracao()

	def leSimbolo(self, rastro):
		simbolo = self.fita[self.posicaoCabecote]
		if simbolo == "#":
			return ['fim']
		else:
			try:
				nomeNovoEstado = self.maquinaAtual.estadoAtual.transicoes[simbolo][0]
			except KeyError:
				raise
			
			if "$" not in nomeNovoEstado:
				if rastro:
					print("A máquina consome o símbolo " + simbolo, end ="")
					print(" e vai do estado " + self.maquinaAtual.estadoAtual.nome, end="")
					print(" ao estado " + nomeNovoEstado)

				for estado in self.maquinaAtual.estados:
					if estado == nomeNovoEstado:
						self.maquinaAtual.estadoAtual = self.maquinaAtual.estados[estado]

				if self.maquinaAtual.estadoAtual.aceitacao and len(self.pilha) > 0:
					return["desempilha"]

				return [""]

			else:
				nomeNovoEstado = nomeNovoEstado.split("$")
				submaquina = nomeNovoEstado[0]
				nomeNovoEstado = nomeNovoEstado[1]

				if rastro:
					print("A máquina consome o símbolo " + simbolo, end ="")
					print(" e vai à máquina " + submaquina, end="")
					print(" empilhando o estado " + nomeNovoEstado)

				return ["empilha", nomeNovoEstado, submaquina]

class MaquinaDeTuring(Automato):
	def __init__(self):
		super().__init__()

	def inicializa(self, cadeia, rastro = True):
		super().inicializa(cadeia, rastro)
		self.posicaoCabecote = len(self.fita) - 1
		if rastro:
			self._imprimeConfiguracao()

	def movimentoCabecote(self, rastro):
		if self.direcaoLeitura == "d":
			self.posicaoCabecote += 1
			if self.posicaoCabecote == len(self.fita):
				self.fita = self.fita + "#"
		else:
			self.posicaoCabecote -= 1
			if self.posicaoCabecote == len(self.fita) -2 and self.fita[-1] == "#":
				self.fita = self.fita[:-1]
			if self.posicaoCabecote == -1:
				self.posicaoCabecote = 0
				return "bloqueia"	
		if rastro:
			print("Cabeçote encontra-se na posição " + str(self.posicaoCabecote))
			self._imprimeConfiguracao()
		return ""

	def escreveSimbolo(self, rastro, simbolo):
		self.fita = self.fita[:self.posicaoCabecote] + simbolo + self.fita[self.posicaoCabecote + 1:]
		if rastro:
			print("A máquina escreve o símbolo " + simbolo)
		self._imprimeConfiguracao()

	def leSimbolo(self, rastro):
		simbolo = self.fita[self.posicaoCabecote]
		try:
			novoEstado = self.estadoAtual.transicoes[simbolo]
		except KeyError:
			raise

		if rastro:
			print("A máquina consome o símbolo " + simbolo + " e vai do estado " + self.estadoAtual.nome + " ao estado " + novoEstado[0])

		for estado in self.estados:
			if estado == novoEstado[0]:
				self.estadoAtual = self.estados[estado]

		if novoEstado[0] == "h":
			if novoEstado[1] == "L":
				self.direcaoLeitura = "e"
				return ["mover","fim"]
			elif novoEstado[1] == "R":
				self.direcaoLeitura = "d"
				return ["mover","fim"]
			return ["fim"]

		if novoEstado[1] == "L":
			self.direcaoLeitura = "e"
			return ["mover"]
		elif novoEstado[1] == "R":
			self.direcaoLeitura = "d"
			return ["mover"]
		else:
			return ["escrever", novoEstado[1]]