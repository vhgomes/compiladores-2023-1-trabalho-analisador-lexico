import re


def tokenizar_codigo_fonte(codigo_fonte):
    tokens = []
    
    padrao_espaco_branco = re.compile(r'\s+')
    padrao_identificador = re.compile(r'[a-zA-Z_]\w*')
    padrao_keyword = re.compile(r'\b(int|char|long|short|float|double|void|if|else|for|while|do|break|continue|struct|switch|case|default|return|printf)\b')
    padrao_operadores = re.compile(r'(\+\+|--|\+=|-=|\*=|/=|%=|==|!=|<=|>=|&&|\|\||[;+\-*/%.,<>&|!^=~(){}])')
    padrao_inteiros = re.compile(r'\d+')
    
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
        
        match_operadores = padrao_operadores.match(codigo_fonte, posicao)
        if match_operadores:
            tokens.append(('Operadores', match_operadores.group()))
            posicao += len(match_operadores.group())
            continue
        
        match_inteiros = padrao_inteiros.match(codigo_fonte, posicao)
        if match_inteiros:
            tokens.append(('Inteiro', match_inteiros.group()))
            posicao += len(match_inteiros.group())
            continue
        
        raise RuntimeError(f'Token não identificado na posição => {posicao}')
    
    return tokens


if __name__ == '__main__':
    with open('testes/teste1.c', 'r') as file:
        input = file.read()
        tokens = tokenizar_codigo_fonte(input)
        for token in tokens:
            print(token)