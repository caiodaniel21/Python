import sys
import pickle
from functools import total_ordering

def nulo_ou_vazio(texto):
    return texto is None or not texto.strip()
    
def valida_faixa_inteiro(pergunta, min, max, padrao=None):
    while True:
        try:
            entrada = input(pergunta)
            if nulo_ou_vazio(entrada) and padrao is not None:
                entrada = padrao
            valor = int(entrada)
            if min <= valor <= max:
                return valor
        except ValueError:
            print (f'Valor inválido, o valor deve estar entre {min} e {max}')

def valida_faixa_inteiro_branco(pergunta, min, max):
    while True:
        try:
            entrada = input(pergunta)
            if nulo_ou_vazio(entrada):
                return None
            valor = int(entrada)
            if min <= valor <= max:
                return valor
        except ValueError:
            print (f'Valor inválido, o valor deve estar entre {min} e {max}')

class ListaUnica:
    def __init__(self, elem_class):
        self.lista = []
        self.elem_class = elem_class

    def __len__(self):
        return len(self.lista)
    
    def __iter__(self):
        return iter(self.lista)
    
    def __getitem__(self, p):
        return self.lista[p]
    
    def indiceValido(self, i):
        return i >= 0 and i < len(self.lista)
    
    def adiciona(self, elem):
        if self.pesquisa(elem) == -1:
            self.lista.append(elem)

    def remove(self, elem):
        self.lista.remove(elem)

    def pesquisa(self, elem):
        self.verifica_tipo(elem)
        try:
            return self.lista.index(elem)
        except ValueError:
            return -1
        
    def verifica_tipo(self, elem):
        if not isinstance(elem, self.elem_class):
            raise TypeError('Tipo inválido!')

    def ordena(self, chave=None):
        self.lista.sort(key=chave)

@total_ordering
class Nome:
    def __init__(self, nome):
        self.nome = nome
    
    def __str__(self):
        return self.nome
    
    def __repr__(self):
        return f'<Classe {type(self).__name__} 0x {id(self):x} Nome: {self.__nome} Chave: {self.__chave}>'
    
    def __eq__(self, outro):
        return self.nome == outro.nome
    
    def __lt__(self, outro):
        return self.nome < outro.nome
   
    @property
    def nome(self):
        return self.__nome
    
    @nome.setter
    def nome(self, valor):
        if nulo_ou_vazio(valor):
            raise ValueError('O valor não pode ser nulo nem em branco!')
        self.__nome = valor
        self.__chave = Nome.CriaChave(valor)

    @property
    def chave(self):
        return self.__chave
    
    @staticmethod
    def CriaChave(nome):
        return nome.strip().lower()

@total_ordering
class TipoTelefone:
    def __init__(self, tipo):
        self.tipo = tipo
    
    def __str__(self):
        return f'({self.tipo})'
    
    def __eq__(self, outro):
        if outro is None:
            return False
        return self.tipo == outro.tipo
    
    def __lt__(self, outro):
        return self.tipo < outro.tipo
    
class Telefone:
    def __init__(self, numero, tipo=None):
        self.numero = numero
        self.tipo = tipo

    def __str__(self):
        if self.tipo is not None:
            tipo = self.tipo
        else:
            tipo = ''
        return f'{self.numero} {tipo}'

    def __eq__(self, outro):
        return self.numero == outro.numero and(
            (self.tipo == outro.tipo) or (
                self.tipo is None or outro.tipo is None))
    
    @property
    def numero(self):
        return self.__numero
    
    @numero.setter
    def numero(self, valor):
        if nulo_ou_vazio(valor):
            raise ValueError('O valor não pode ser None ou em branco')
        self.__numero = valor
    
class Telefones(ListaUnica):
    def __init__(self):
        super().__init__(Telefone)

class TiposTelefones(ListaUnica):
    def __init__(self):
        super().__init__(TipoTelefone)

class DadoAgenda:
    def __init__(self, nome):
        self.nome = nome
        self.telefones = Telefones()
    
    @property
    def nome (self):
        return self.__nome
    
    @nome.setter
    def nome(self, valor):
        if not isinstance(valor, Nome):
            raise ValueError('O valor não pode ser nulo ou estar vazio')
        self.__nome = valor

    def pesquisaTelefone(self, telefone):
        posicao = self.telefones.pesquisa(Telefone(telefone))
        if posicao == -1:
            return None
        else:
            return self.telefones[posicao]
        
class Agenda(ListaUnica):
    def __init__(self):
        super().__init__(DadoAgenda)
        self.tiposTelefone = TiposTelefones()
    
    def adicionaTipo(self, tipo):
        self.tiposTelefone.adiciona(TipoTelefone(tipo))

    def pesquisaNome(self, nome):
        if isinstance(nome, str):
            nome = Nome(nome)
        for dados in self.lista:
            if dados.nome == nome:
                return dados
            else:
                return None
    def ordena(self):
        super().ordena(lambda dado: str(dado.nome))

class Menu:
    def __init__(self):
        self.opcoes = [['Sair', None]]
    
    def adicionarOpcao(self, nome, funcao):
        self.opcoes.append([nome, funcao])

    def exibe(self):
        print ('====')
        print ('Menu')
        print ('====\n')
        for i, opcao in enumerate(self.opcoes):
            print (f'<{i}> - {opcao[0]}')
        print ()
    
    def execute(self):
        while True:
            try:
                self.exibe()
                escolha = valida_faixa_inteiro('Escolha uma opção: ', 0, len(self.opcoes) - 1)
                if escolha == 0:
                    break
                self.opcoes[escolha][1]()
            except Exception as e:
                print (f'[ OCORREU UM ERRO NO MENU DAS FUNÇÕES ]\n{e}')
    
class appAgenda:
    @staticmethod
    def pede_nome():
        return input('Nome: ')

    @staticmethod
    def pede_telefone():
        return input('Telefone: ')
    
    @staticmethod
    def mostra_dados(dados):
        print (f'Nome: {dados.nome}')
        for telefone in dados.telefones:
            print (f'Telefone: {telefone}')
        print ()
    
    @staticmethod
    def mostra_dados_telefone(dados):
        print (f'Nome: {dados.nome}')
        for i, telefone in enumerate(dados.telefones):
            print (f'{i} - Telefone: {telefone}')
        print ()

    @staticmethod
    def pede_nome_arquivo():
        return input('Nome do arquivo: ')
    
    def __init__(self):
        self.agenda = Agenda()
        self.agenda.adicionaTipo('Celular')
        self.agenda.adicionaTipo('Residência')
        self.agenda.adicionaTipo('Trabalho')
        self.agenda.adicionaTipo('Fax')
        self.menu = Menu()
        self.menu.adicionarOpcao('Novo', self.novo)
        self.menu.adicionarOpcao('Altera', self.altera)
        self.menu.adicionarOpcao('Apagar', self.apaga)
        self.menu.adicionarOpcao('Lista', self.lista)
        self.menu.adicionarOpcao('Ler', self.ler)
        self.menu.adicionarOpcao('Gravar', self.grava)
        self.menu.adicionarOpcao('Ordena', self.ordena)

    def pede_tipo_telefone(self, padrao=None):
        for i, tipo in enumerate(self.agenda.tiposTelefone):
            print (f'{i} - {tipo}', end=None)
        t = valida_faixa_inteiro('Tipo: ', 0, len(self.agenda.tiposTelefone) - 1, padrao)
        return self.agenda.tiposTelefone[t]
    
    def pesquisa(self, nome):
        dado = self.agenda.pesquisaNome(nome)
        return dado
    
    def novo(self):
        novo = appAgenda.pede_nome()
        if nulo_ou_vazio(novo):
            return None
        nome = Nome(novo)
        if self.pesquisa(nome) is not None:
            print ('O nome já existe')
            return
        registro = DadoAgenda(nome)
        self.menu_telefones(registro)
        self.agenda.adiciona(registro)

    def apaga(self):
        if len(self.agenda) == 0:
            print ('Agenda vazia, nada a apagar')
            return
        nome = appAgenda.pede_nome()
        if nulo_ou_vazio(nome):
            return
        p = self.pesquisa(nome)
        if p is not None:
            self.agenda.remove(p)
            print (f'Apagado, agora a agenda possui {len(self.agenda)} registros')
        else:
            print ('Nome não encontrado')
    
    def altera(self):
        if len(self.agenda) == 0:
            print ('Agenda vazia, nada a alterar')
        nome = appAgenda.pede_nome()
        if nulo_ou_vazio(nome):
            return
        p = self.pesquisa(nome)
        if p is not None:
            print ('\nEncontrado\n')
            appAgenda.mostra_dados(p)
            print ('Digite enter caso não queira alterar o nome')
            novo = appAgenda.pede_nome()
            if not nulo_ou_vazio(novo):
                p.nome = Nome(novo)
            self.menu_telefones(p)
        else:
            print ('Nome não encontrado')
    
    def menu_telefones(self, dados):
        while True:
            print ('\nEditando telefones\n')
            appAgenda.mostra_dados_telefone(dados)
            if len(dados.telefones) > 0:
                print ('\n[A] - alterar\n[D] - apagar\n', end='')
            print ('[N] - novo\n[S] - sair\n')
            op = input('Escolha uma operação: ')
            op = op.lower()
            if op not in ['a', 'd', 'n', 's']:
                print ('Operação inválida. Digite A, D, N ou S.')
                continue
            if op == 'a' and len(dados.telefones) > 0:
                self.altera_telefones(dados)
            elif op == 'd' and len(dados.telefones) > 0:
                self.apaga_telefone(dados)
            elif op == 'n':
                self.novo_telefone(dados)
            elif op == 's':
                break

    def novo_telefone(self, dados):
        telefone = appAgenda.pede_telefone()
        if nulo_ou_vazio(telefone):
            return None
        if dados.pesquisaTelefone(telefone) is not None:
            print ('Esse telefone já existe')
        tipo = self.pede_tipo_telefone()
        dados.telefones.adiciona(Telefone(telefone, tipo))
    
    def apaga_telefone(self, dados):
        t = valida_faixa_inteiro_branco(
            'Digite o índice do número que deseja apagar, deixe em branco para sair: ', 0, len(dados.telefones) - 1)
        if t is None:
            return
        dados.telefones.remove(dados.telefones[t])
    
    def altera_telefones(self, dados):
        t = valida_faixa_inteiro_branco(
            'Digite o índice do número que deseja alterar, deixe em branco para sair: ', 0, len(dados.telefones) - 1)
        if t is None:
            return
        telefone = dados.telefones[t]
        print (f'Telefone: {telefone}')
        print ('Digite enter caso não queira altera o número.')
        novo_telefone = appAgenda.pede_telefone()
        if not nulo_ou_vazio(novo_telefone):
            telefone.numero = novo_telefone
        print ('Digite enter caso não queira alterar o tipo')
        telefone.tipo = self.pede_tipo_telefone(self.agenda.tiposTelefone.pesquisa(telefone.tipo))
    
    def lista(self):
        print ('\nAgenda')
        print ('-' * 30)
        for e in self.agenda:
            appAgenda.mostra_dados(e)
        print ('-' * 30)

    def ler(self, nome_arquivo=None):
        if nome_arquivo is None:
            nome_arquivo = appAgenda.pede_nome_arquivo()
        if nulo_ou_vazio(nome_arquivo):
            return
        with open(nome_arquivo, 'rb') as arquivo:
            self.agenda = pickle.load(arquivo)
        self.ultimo_nome = nome_arquivo

    def ordena(self):
        self.agenda.ordena()
        print ('\nAgenda ordenada\n')
    
    def grava(self):
        if self.ultimo_nome is not None:
            print (f'Último nome utilizado foi "{self.ultimo_nome}"')
            print ('Digite enter caso queira utilizar o mesmo nome')
        nome_arquivo = appAgenda.pede_nome_arquivo()
        if nulo_ou_vazio(nome_arquivo):
            nome_arquivo = self.ultimo_nome
        else:
            return
        with open(nome_arquivo, 'wb') as arquivo:
            pickle.dump(self.agenda, arquivo)
    
    def execute(self):
        self.menu.execute()

if __name__ == '__main__':
    app = appAgenda()
    if len(sys.argv) > 1:
        app.ler(sys.argv[1])
    app.execute()
        
