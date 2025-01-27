import re

#Patrones para los tokens
PATRON_IDENTIFICADOR = r"^[a-zA-Z][a-zA-Z0-9]*$"
PATRON_NUMERO_REAL = r"^\d+\.\d+$"
PATRON_NUMERO_ENTERO = r"^\d+$"

#Función para identificar el token de la cadena
def identificar_token(token):
    if re.match(PATRON_IDENTIFICADOR, token):
        return "IDENTIFICADOR"
    elif re.match(PATRON_NUMERO_REAL, token):
        return "NUMERO_REAL"
    elif re.match(PATRON_NUMERO_ENTERO, token):
        return "ENTERO"
    else:
        return "ERROR"

#Función para analizar los tokens de la cadena
def analizador_lexico(entrada):
    tokens = entrada.split()
    resultado = []
    for token in tokens:
        tipo = identificar_token(token)
        resultado.append({"tipo": tipo, "valor": token})
    return resultado

#Main
if __name__ == "__main__":
    entrada = input("Introduce la cadena de texto a analizar: ")
    tokens = analizador_lexico(entrada)
    print("Tokens identificados:")
    for token in tokens:
        print(f"Tipo: {token['tipo']}, Valor: {token['valor']}")