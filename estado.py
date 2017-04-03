class Estado():
	def __init__(self, nome, inicial = False, aceitacao = False):
		self.nome = nome
		self.inicial = inicial
		self.aceitacao = aceitacao
		self.transicoes = {}