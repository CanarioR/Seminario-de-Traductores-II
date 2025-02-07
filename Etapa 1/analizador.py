# Definición de las palabras reservadas
PALABRAS_RESERVADAS = {"if", "while", "return", "else", "int", "float"}

# Función para identificar un identificador
def es_identificador(token):
    if token[0].isalpha():
        return all(c.isalnum() or c == "_" for c in token)
    return False

# Función para identificar un número entero
def es_entero(token):
    return token.isdigit()

# Función para identificar un número real válido
def es_real(token):
    if '.' in token:
        partes = token.split('.')
        if len(partes) == 2 and partes[0].isdigit() and partes[1].isdigit():
            return True
    return False

# Función para determinar si un token es inválido (como "12." o ".5")
def es_error_real(token):
    return token.count('.') == 1 and (token.startswith('.') or token.endswith('.'))

# Función para identificar operadores y símbolos
def es_operador_adicion(token):
    return token in {'+', '-'}

def es_operador_multiplicacion(token):
    return token in {'*', '/'}

def es_operador_asignacion(token):
    return token == '='

def es_operador_relacional(token):
    return token in {'<', '>', '<=', '>=', '!=', '=='}

def es_operador_and(token):
    return token == '&&'

def es_operador_or(token):
    return token == '||'

def es_operador_not(token):
    return token == '!'

def es_parentesis(token):
    return token in {'(', ')'}

def es_llave(token):
    return token in {'{', '}'}

def es_punto_coma(token):
    return token == ';'

def es_palabra_reservada(token):
    return token in PALABRAS_RESERVADAS

# Función para identificar el tipo de token
def identificar_token(token):
    if es_palabra_reservada(token):
        return "PALABRA_RESERVADA"
    elif es_identificador(token):
        return "IDENTIFICADOR"
    elif es_real(token):
        return "REAL"
    elif es_entero(token):
        return "ENTERO"
    elif es_error_real(token):  # Detectar casos como "12." o ".5" como error
        return "ERROR_EN_NO_REAL"
    elif es_operador_adicion(token):
        return "OPERADOR_ADICION"
    elif es_operador_multiplicacion(token):
        return "OPERADOR_MULTIPLICACION"
    elif es_operador_asignacion(token):
        return "OPERADOR_ASIGNACION"
    elif es_operador_relacional(token):
        return "OPERADOR_RELACIONAL"
    elif es_operador_and(token):
        return "OPERADOR_AND"
    elif es_operador_or(token):
        return "OPERADOR_OR"
    elif es_operador_not(token):
        return "OPERADOR_NOT"
    elif es_parentesis(token):
        return "PARENTESIS"
    elif es_llave(token):
        return "LLAVE"
    elif es_punto_coma(token):
        return "PUNTO_COMA"
    else:
        return "ERROR"

# Función para separar correctamente los tokens
def analizador_lexico(entrada):
    tokens = []
    token_actual = ""
    i = 0
    longitud = len(entrada)
    
    while i < longitud:
        c = entrada[i]
        
        # Si es un espacio, finaliza el token actual
        if c.isspace():
            if token_actual:
                tokens.append(token_actual)
                token_actual = ""
        
        # Si es un operador o símbolo, finaliza el token anterior y agrega el operador
        elif c in {'+', '-', '*', '/', '=', '<', '>', '!', '(', ')', '{', '}', ';'}:
            if token_actual:
                tokens.append(token_actual)
                token_actual = ""
            
            # Manejar operadores dobles (==, !=, <=, >=, &&, ||)
            if i + 1 < longitud and entrada[i:i+2] in {'==', '!=', '<=', '>=', '&&', '||'}:
                tokens.append(entrada[i:i+2])
                i += 1  # Saltar el siguiente carácter
            else:
                tokens.append(c)
        
        # Manejo especial para números reales (verificar si el punto es parte de un número)
        elif c == '.':
            if token_actual.isdigit() and i + 1 < longitud and entrada[i + 1].isdigit():
                token_actual += c  # Si el anterior era un número y el siguiente también, es un número real
            else:
                if token_actual:
                    tokens.append(token_actual)
                token_actual = c  # Guardar el punto temporalmente en caso de error
        
        # Si es un carácter alfanumérico o un guion bajo (para identificadores)
        elif c.isalnum() or c == '_':
            token_actual += c
        
        # Si encontramos un carácter inesperado, lo agregamos como token desconocido
        else:
            if token_actual:
                tokens.append(token_actual)
                token_actual = ""
            tokens.append(c)
        
        i += 1

    # Añadir el último token que pueda haber quedado
    if token_actual:
        tokens.append(token_actual)
    
    resultado = []
    for token in tokens:
        tipo = identificar_token(token)
        resultado.append({"tipo": tipo, "valor": token})
    
    return resultado

# Ejemplo de uso
if __name__ == "__main__":
    print("Analizador Léxico con Autómatas - Introduce cadenas de texto para analizar.")
    print("Escribe 'salir' para terminar.")
    while True:
        entrada = input("\nIntroduce una cadena: ")
        if entrada.lower() == "salir":
            print("Saliendo del programa...")
            break
        tokens = analizador_lexico(entrada)
        print("Tokens identificados:")
        for token in tokens:
            print(f"Tipo: {token['tipo']}, Valor: {token['valor']}")
g