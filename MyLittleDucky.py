# Yacc example

import ply.yacc as yacc
import MyLittleDuckl
#import sys 
# Get the token map from the lexer.  This is required.
from MyLittleDuckl import tokens

def p_programa(p): 
    '''programa : PROGRAM IDENTIFIER SEMICOLON vars bloque
    | PROGRAM IDENTIFIER SEMICOLON bloque'''

def p_vars(p):
    '''vars : VAR vars1'''

def p_vars1(p):
    '''vars1 : IDENTIFIER vars2 COLON tipo SEMICOLON vars1
    | IDENTIFIER vars2 COLON tipo SEMICOLON'''

def p_vars2(p):
    '''vars2 : empty
    | COMMA IDENTIFIER vars2'''

def p_tipo(p):
  '''tipo : INT
      | FLOAT'''

def p_bloque(p):
    '''bloque : LBRACE bloque1 RBRACE'''

def p_bloque1(p):
    '''bloque1 : empty
    | estatuto bloque1'''

def p_estatuto(p):
    '''estatuto : asignacion
    | condicion 
    | escritura'''

def p_asignacion(p):
    '''asignacion : IDENTIFIER EQUAL expresion SEMICOLON'''

def p_escritura(p):
    '''escritura : PRINT LPARENTHESES escritura1 RPARENTHESES SEMICOLON'''

def p_escritura1(p):
    '''escritura1 : expresion escritura2
    | STRING escritura2'''

def p_escritura2(p):
    '''escritura2 : empty
    | COMMA escritura1'''

def p_condicion(p):
    '''condicion : IF LPARENTHESES expresion RPARENTHESES bloque SEMICOLON
    | IF LPARENTHESES expresion RPARENTHESES bloque ELSE bloque SEMICOLON'''

def p_expresion(p):
    '''expresion : exp
    | exp LTHAN exp
    | exp GTHAN exp
    | exp NOTEQUAL exp '''

def p_exp(p):
    '''exp : termino exp1'''

def p_exp1(p):
    '''exp1 : empty
      | PLUS termino exp1
      | MINUS termino exp1'''

def p_termino(p):
    '''termino : factor termino1'''

def p_termino1(p):
    '''termino1 : empty
    | MULTI factor termino1
    | DIVIDE factor termino1'''

def p_factor(p):
    '''factor : LPARENTHESES expresion RPARENTHESES
    | factor1 varcte'''

def p_factor1(p):
    ''' factor1 : empty
    | PLUS
    | MINUS'''

def p_varcte(p):
    '''varcte : IDENTIFIER
    | CTEINT
    | CTEFLOAT'''

def p_empty(p):
  '''empty : '''

# Error rule for syntax errors
def p_error(p):
    print("Error de tipo: ", p.value,"  linea: ", p.lineno)
    global err
    err = 0

# Build the parser
yacc.yacc()

err = 1

while True:
  try:
    nombre = input("Nombre del archivo? (Teclee 'S' para salir) ")
    if nombre == 'S':
      break
    fil = open(nombre, "r")
    s = fil.readlines()
    e = ""
    for line in s:
      e += line
    yacc.parse(e)

    if err:
      print("No hay ningun error, buen programa (Y)!")

  except EOFError:
    print("Error! No se pudo abrir el archivo!")
    break;
