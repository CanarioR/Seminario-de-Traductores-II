from tabulate import tabulate

PALABRAS_RESERVADAS = {"if", "while", "return", "else", "int", "float"}
OPERADORES_DOBLES = {"==", "!=", "<=", ">=", "&&", "||"}
OPERADORES_SIMPLES = {'+', '-', '*', '/', '=', '<', '>', '!', '(', ')', '{', '}', ';'}

# Estados del autómata léxico
ESTADO_INICIAL = 0
ESTADO_IDENTIFICADOR = 1
ESTADO_ENTERO = 2
ESTADO_PUNTO = 3
ESTADO_REAL = 4
ESTADO_ERROR_REAL = 5
ESTADO_OPERADOR = 6

# Tabla LR(1)
idReglas = [2, 2]  
lonReglas = [3, 1]  

tablaLR = {
    (0, "IDENTIFICADOR"): "d2",
    (0, "E"): "1",
    (2, "OPERADOR"): "d3",
    (2, "FIN_DE_CADENA"): "r2",
    (3, "IDENTIFICADOR"): "d2",
    (3, "E"): "4",
    (4, "OPERADOR"): "d3",
    (4, "FIN_DE_CADENA"): "r1",  
    (1, "FIN_DE_CADENA"): "r0",  
}

def analizador_lexico(entrada):
    tokens = []
    token_actual = ""
    estado = ESTADO_INICIAL
    i = 0
    longitud = len(entrada)

    while i < longitud:
        c = entrada[i]

        if estado == ESTADO_INICIAL:
            if c.isalpha() or c == '_':  
                estado = ESTADO_IDENTIFICADOR
                token_actual += c
            elif c.isdigit():  
                estado = ESTADO_ENTERO
                token_actual += c
            elif c == '.':  
                estado = ESTADO_ERROR_REAL
                token_actual += c
            elif c in OPERADORES_SIMPLES:  
                estado = ESTADO_OPERADOR
                token_actual += c
            elif c.isspace():  
                pass  
            else:  
                tokens.append({"tipo": "DESCONOCIDO", "valor": c})

        elif estado == ESTADO_IDENTIFICADOR:
            if c.isalnum() or c == '_':
                token_actual += c
            else:
                if token_actual in PALABRAS_RESERVADAS:
                    tokens.append({"tipo": "PALABRA_RESERVADA", "valor": token_actual})
                else:
                    tokens.append({"tipo": "IDENTIFICADOR", "valor": token_actual})
                token_actual = ""
                estado = ESTADO_INICIAL
                i -= 1  

        elif estado == ESTADO_ENTERO:
            if c.isdigit():
                token_actual += c
            elif c == '.':  
                estado = ESTADO_PUNTO
                token_actual += c
            else:
                tokens.append({"tipo": "ENTERO", "valor": token_actual})
                token_actual = ""
                estado = ESTADO_INICIAL
                i -= 1  

        elif estado == ESTADO_PUNTO:
            if c.isdigit():  
                estado = ESTADO_REAL
                token_actual += c
            else:  
                estado = ESTADO_ERROR_REAL
                token_actual += c  

        elif estado == ESTADO_REAL:
            if c.isdigit():
                token_actual += c
            else:
                tokens.append({"tipo": "REAL", "valor": token_actual})
                token_actual = ""
                estado = ESTADO_INICIAL
                i -= 1  

        elif estado == ESTADO_ERROR_REAL:
            if c.isspace() or c in OPERADORES_SIMPLES or i == longitud - 1:
                tokens.append({"tipo": "ERROR_REAL", "valor": token_actual})
                token_actual = ""
                estado = ESTADO_INICIAL
                i -= 1  
            else:
                token_actual += c  

        elif estado == ESTADO_OPERADOR:
            if token_actual + c in OPERADORES_DOBLES:
                token_actual += c
                tokens.append({"tipo": "OPERADOR", "valor": token_actual})
                token_actual = ""
            else:
                tokens.append({"tipo": "OPERADOR", "valor": token_actual})
                token_actual = ""
                i -= 1  
            estado = ESTADO_INICIAL

        i += 1

    if token_actual:
        if estado == ESTADO_IDENTIFICADOR:
            if token_actual in PALABRAS_RESERVADAS:
                tokens.append({"tipo": "PALABRA_RESERVADA", "valor": token_actual})
            else:
                tokens.append({"tipo": "IDENTIFICADOR", "valor": token_actual})
        elif estado == ESTADO_ENTERO:
            tokens.append({"tipo": "ENTERO", "valor": token_actual})
        elif estado == ESTADO_REAL:
            tokens.append({"tipo": "REAL", "valor": token_actual})
        elif estado == ESTADO_ERROR_REAL:
            tokens.append({"tipo": "ERROR", "valor": token_actual})
        elif estado == ESTADO_OPERADOR:
            tokens.append({"tipo": "OPERADOR", "valor": token_actual})
        else:
            tokens.append({"tipo": "DESCONOCIDO", "valor": token_actual})

    tokens.append({"tipo": "FIN_DE_CADENA", "valor": "$"})

    return tokens

def analizador_sintactico(tokens):
    tabla_proceso = []  #almacenar filas
    pila = [(0, "$")]
    i = 0
    
    while i < len(tokens):
        estado_actual = pila[-1][0]  # Último estado en la pila
        simbolo_actual = tokens[i]['tipo']  # Token actual
        entrada_restante = " ".join([t["valor"] for t in tokens[i:]])
        
        if (estado_actual, simbolo_actual) not in tablaLR:
            print(f"Error de sintaxis en: {simbolo_actual}")
            return
        
        accion = tablaLR[(estado_actual, simbolo_actual)]
        
        # Agregar a la tabla antes de modificar la pila
        tabla_proceso.append([" ".join([f"{s}" for s in pila]), entrada_restante, accion])
        
        if accion.startswith('d'):  # Desplazamiento
            nuevo_estado = int(accion[1:])
            pila.append((nuevo_estado, simbolo_actual))
            i += 1
        elif accion == "r0":  # Aceptación
            tabla_proceso.append([" ".join([f"{s}" for s in pila]), entrada_restante, "Aceptación"])
            print(tabulate(tabla_proceso, headers=["Pila", "Entrada", "Acción"], tablefmt="grid"))
            return
        elif accion.startswith('r'):  # Reducción
            num_regla = int(accion[1:])
            longitud = lonReglas[num_regla - 1]
            
            for _ in range(longitud):
                pila.pop()
            
            estado_anterior = pila[-1][0]
            if (estado_anterior, "E") not in tablaLR:
                print(f"Error: No hay transición definida para el estado {estado_anterior} y el símbolo E")
                return
            
            nuevo_estado = int(tablaLR[(estado_anterior, "E")])
            pila.append((nuevo_estado, "E"))
    
    print("Error: Entrada incompleta")
    print(tabulate(tabla_proceso, headers=["Pila", "Entrada", "Acción"], tablefmt="grid"))

if __name__ == "__main__":
    entrada = input("\nIntroduce una cadena: ")
    tokens = analizador_lexico(entrada)

    print("\nTokens identificados:")
    print(tabulate(tokens, headers="keys", tablefmt="grid"))

    analizador_sintactico(tokens)
