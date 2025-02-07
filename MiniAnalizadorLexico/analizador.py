def es_identificador(token):
    estado = 0
    for c in token:
        if estado == 0:  # Estado inicial
            if c.isalpha() or c == '_':  # Primera letra o guion bajo
                estado = 1
            else:
                return False
        elif estado == 1:  # Estado válido
            if c.isalnum() or c == '_':  # Letras, números o guion bajo
                estado = 1
            else:
                return False
    return estado == 1

def es_numero_real(token):
    estado = 0
    for c in token:
        if estado == 0:  # Estado inicial
            if c.isdigit():  # Primer dígito
                estado = 1
            else:
                return False
        elif estado == 1:  # Estado después de dígitos iniciales
            if c.isdigit():  # Más dígitos antes del punto
                estado = 1
            elif c == '.':  # Se encontró el punto decimal
                estado = 2
            else:
                return False
        elif estado == 2:  # Después del punto decimal, debe haber al menos un dígito
            if c.isdigit():
                estado = 3
            else:
                return False
        elif estado == 3:  # Dígitos después del punto decimal
            if c.isdigit():
                estado = 3
            else:
                return False
    return estado == 3  # Solo es válido si termina en estado 3

def es_operador_adicion(token):
    return token in {'+', '-'}

def identificar_token(token):
    if es_identificador(token):
        return "IDENTIFICADOR"
    elif es_numero_real(token):
        return "NUMERO_REAL"
    elif es_operador_adicion(token):
        return "OPERADOR_ADICION"
    else:
        return "ERROR"

def analizador_lexico(entrada):
    tokens = entrada.split()
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
