import re


def tokenizar_codigo_fonte(codigo_fonte):
    tokens = []
    
    padrao_espaco_branco = re.compile(r'\s+')
    padrao_identificador = re.compile(r'[a-zA-Z_]\w*')
    padrao_keyword = re.compile(r'\b(int|char|long|short|float|double|void|if|else|for|while|do|break|continue|struct|switch|case|default|return|printf)\b')
    padrao_operadores = re.compile(r'(\+\+|--|\+=|-=|\*=|/=|%=|==|!=|<=|>=|&&|\|\||[;+\-*/%.,<>&|!^=~])')
    padrao_inteiros = re.compile(r'\d+')
    padrao_textual = re.compile(r'\".*?\"')
    padrao_ponto_flutuante = re.compile(r'(\d+\.\d+)')
    padrao_delimitador = re.compile(r"\[|\]|\(|\)|\{|\}|\;|\,|\:")
    
    posicao = 0
    while posicao < len(codigo_fonte):
        # Nesse trecho de codigo ele verifica se é um espaço em branco, caso seja ele só pula para a proxima parte do codigo
        match_espaco_branco = padrao_espaco_branco.match(codigo_fonte, posicao)
        if match_espaco_branco:
            posicao = match_espaco_branco.end()
            continue

        match_identificador = padrao_identificador.match(codigo_fonte, posicao)
        if match_identificador:
            identificador = match_identificador.group()
            match_keyword = padrao_keyword.match(codigo_fonte, posicao)
            if match_keyword:
                tokens.append(('Keyword', match_keyword.group()))
                posicao = match_keyword.end()
            else:
                tokens.append(('Identificador', identificador))
                posicao += len(identificador)
            continue

        match_textual = padrao_textual.match(codigo_fonte, posicao)
        if match_textual:
            tokens.append(('Textual', match_textual.group()))
            posicao += len(match_textual.group())
            continue

        match_delimitador = padrao_delimitador.match(codigo_fonte, posicao)
        if match_delimitador:
            tokens.append(('Delimitador', match_delimitador.group()))
            posicao += len(match_delimitador.group())
            continue
        
        match_operadores = padrao_operadores.match(codigo_fonte, posicao)
        if match_operadores:
            tokens.append(('Operadores', match_operadores.group()))
            posicao += len(match_operadores.group())
            continue

        match_ponto_flutuante = padrao_ponto_flutuante.match(codigo_fonte, posicao)
        if match_ponto_flutuante:
            tokens.append(('Ponto Flutuante', match_ponto_flutuante.group()))
            posicao += len(match_ponto_flutuante.group())
            continue

        match_inteiros = padrao_inteiros.match(codigo_fonte, posicao)
        if match_inteiros:
            tokens.append(('Inteiro', match_inteiros.group()))
            posicao += len(match_inteiros.group())
            continue

        raise RuntimeError(f'Token não identificado na posição => {posicao} {codigo_fonte[posicao]}')
    
    return tokens

if __name__ == '__main__':
    with open('testes/teste3.c', 'r') as file:
        input = file.read()
        input = re.sub('//.*', ' ', input)  
        input = re.sub('(/\*(.|\n)*?\*/)', ' ', input)  
        tokens = tokenizar_codigo_fonte(input)
        for token in tokens:
            print(token)
