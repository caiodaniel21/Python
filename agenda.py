from agenda_modulos import pede_nome, pede_aniversario, pede_telefone, pede_email, pede_nome_arquivo, mostra_dados, confirmar


agenda = []
alterada = False


def pesquisa(nome):
    mnome = nome.lower()
    for p, e in enumerate(agenda):
        if e[0].lower() == mnome:
            return p
    return None

def novo():
    global alterada
    nome = pede_nome()
    if pesquisa(nome) is not None:
        print ('Esse nome já existe, tente outro!')
    else:
        telefone = pede_telefone()
        aniversario = pede_aniversario()
        email = pede_email()
        agenda.append([nome, telefone, aniversario, email])
        alterada = True

def altera():
    global alterada
    nome = pede_nome()
    p = pesquisa(nome)
    if p is not None:
        contato = agenda[p]
        print ('Encontrado!')
        print (mostra_dados(*contato))
        if confirmar('alterar') == 'S':
            novo_nome = pede_nome()
            novo_telefone = pede_telefone()
            novo_aniversario = pede_aniversario()
            novo_email = pede_email()
            agenda[p] = [novo_nome, novo_telefone, novo_aniversario, novo_email]
            alterada = True
    else:
        print ('Nome não encontrado!')
    
def apaga():
    global alterada
    p = pesquisa(pede_nome())
    if p is not None:
        print ('Encontrado!')
        if confirmar('apagar') == 'S':
            del agenda[p]
            alterada = True
    else:
        print ('Nome não encontrado!')

def lista():
    print ('\nAgenda\n------')
    for e in agenda:
        print (mostra_dados(*e))
    print ('\n------\n')
    print (f'Tamanho da agenda: {len(agenda)} contatos')
    print ('\n------')

def ler():
    global alterada, agenda
    if alterada:
        print ('Existem itens na lista que ainda não foram salvos!')
        if confirmar('gravar') == 'S':
            gravar()
    nome_arquivo = pede_nome_arquivo()
    with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
        agenda = []
        for l in arquivo.readlines():
            nome, telefone, aniversario, email = l.strip().split('#')
            agenda.append[nome, telefone, aniversario, email]
            alterada = False

def gravar():
    global alterada
    if not alterada:
        print ('Não existem itens para ser salvos.')
        if confirmar('gravar') == 'N':
            return
    nome_arquivo = pede_nome_arquivo()
    with open(nome_arquivo, 'w', encoding='utf=8') as arquivo:
        for e in agenda:
            arquivo.write(f'{e[0]}#{e[1]}#{e[2]}#{e[3]}\n')
            alterada = False

def ordena():
    global alterada
    agenda.sort()
    alterada = True

def valida_faixa_inteiro(pergunta, min, max):
    try:
        valor = int(input(pergunta))
        if min <= valor <= max:
            return valor
    except ValueError:
        print (f'Digite um número inteiro entre {min} e {max}')

def menu():
    print ('''
    1 - Novo
    2 - Altera
    3 - Apaga
    4 - Lista
    5 - Ler
    6 - Gravar
    7 - Ordena
    0 - Sair
''')
    return valida_faixa_inteiro('Escolha uma opção: ', 0, 7)

try:
    while True:
        op = menu()
        if op == 0:
            break
        elif op == 1:
            novo()
        elif op == 2:
            altera()
        elif op == 3:
            apaga()
        elif op == 4:
            lista()
        elif op == 5:
            ler()
        elif op == 6:
            gravar()
        elif op == 7:
            ordena()
except Exception as e:
    print (f'Ocorreu um erro: \n{e}')
