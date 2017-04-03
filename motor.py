from minHeap import *
from automato import *

class Motor():
	def __init__(self, rastro, listaEventos, dispositivo, cadeia):
		self.agora = 0
		self.rastro = rastro
		self.listaEventos = listaEventos
		self.automato = dispositivo
		self.cadeia = cadeia
		self.count = 0
								
	def inicia(self):
		fim = False
		while not fim:
			if self.listaEventos.is_empty():
				fim = True
			else:
				fim = self.processaEvento(self.listaEventos.serve())


	def processaEvento(self, evento):
		self.count += 1
		self.agora = evento[0]
		tipoEvento = evento[1]

		fim = False
		
		if tipoEvento == "partidaInicial":
			self.automato.inicializa(self.cadeia)

		elif tipoEvento == "leSimbolo":
			try:
				acao = self.automato.leSimbolo(self.rastro)
				if acao[0] == "fim":
					self.listaEventos.append([self.agora, "fimSimulacao"])
				elif acao[0] == "mover":
					self.listaEventos.append([self.agora, "movimentoCabecote"])
					if len(acao) > 1:
						if acao[1] == "fim":
							self.listaEventos.append([self.agora, "fimSimulacao"])
				elif acao[0] == "escrever":
					self.listaEventos.append([self.agora, "escreveSimbolo", acao[1]])
				elif acao[0] == "empilha":
					self.listaEventos.append([self.agora, "empilha", acao[1], acao[2]])
				elif acao[0] == "desempilha":
					self.listaEventos.append([self.agora, "desempilha"])
			except KeyError:
				self.listaEventos.append([self.agora, "erroFaltaDeTransicao"])

		elif tipoEvento == "empilha":
			self.automato.empilha(self.rastro, evento[2], evento[3])

		elif tipoEvento == "desempilha":
			self.automato.desempilha(self.rastro)

		elif tipoEvento == "escreveSimbolo":
			self.automato.escreveSimbolo(self.rastro, evento[2])
			self.listaEventos.append([self.agora, "leSimbolo"])

		elif tipoEvento == "movimentoCabecote":
			bloqueia = self.automato.movimentoCabecote(self.rastro)
			if bloqueia == "bloqueia":
				self.listaEventos.append([self.agora, "erroFimDaFita"])	
			elif type(self.automato) is MaquinaDeTuring:
				self.listaEventos.append([self.agora, "leSimbolo"])

		elif tipoEvento == "erroFaltaDeTransicao":
			self.automato.erroFaltaDeTransicao()
			self.listaEventos.append([self.agora, "fimSimulacao"])

		elif tipoEvento == "erroFimDaFita":
			self.automato.erroFimDaFita()
			self.listaEventos.append([self.agora, "fimSimulacao"])

		elif tipoEvento == "fimSimulacao":
			self.automato.fimSimulacao()
			self.geraRelatorio()
			fim = True

		else:
			raise TypeError("Tipo inválido de evento")
		
		return fim
	
	def geraRelatorio(self):
		print("Foram processados " + str(self.count) + " eventos, em " + str(self.agora) + " unidades de tempo.")