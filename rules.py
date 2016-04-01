from codegen.ast import Node
import sys

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTI', 'DIVIDE'),
    ('left', 'EQUALTO', 'NOTEQUAL', 'LTHANEQ','LTHAN','GTHAN','GTHANEQ'),
    ('left', 'OR', 'AND'),
)

def p_programa(p):
    '''programa : PROGRAM bloque ENDPROGRAM
    | global PROGRAM bloque ENDPROGRAM
    | PROGRAM bloque ENDPROGRAM funciones
    | global PROGRAM bloque ENDPROGRAM funciones'''

def p_funciones(p):
    '''funciones : func funciones
    | voidfunc funciones
    | empty'''

def p_vars(p):
    '''vars : VAR vars1 ENDVAR'''

def p_global(p):
    '''global : GLOBAL vars1 ENDGLOBAL'''

def p_vars1(p):
    '''vars1 : tipo IDENTIFIER vars2'''

def p_vars2(p):
    '''vars2 : empty
    | COMMA IDENTIFIER vars2'''

def p_tipo(p):
  '''tipo : INT
      | FLOAT
      | STRING
      | BOOL
      | HASH'''

def p_bloque(p):
    '''bloque : empty
    | estatuto bloque'''

def p_estatuto(p):
    '''estatuto : asignacion
    | condicion
    | escritura
    | lectura
    | while
    | for
    | vars
    | empty'''

def p_asignacion(p):
    '''asignacion : IDENTIFIER EQUAL expresion'''

def p_escritura(p):
    '''escritura : PRINT escritura1'''

def p_escritura1(p):
    '''escritura1 : expresion escritura2'''

def p_escritura2(p):
    '''escritura2 : empty
    | COMMA escritura1'''

def p_lectura(p):
    '''lectura : READ IDENTIFIER'''

def p_condicion(p):
    '''condicion : IF expresion bloque condicion1 ENDIF
    | IF expresion bloque condicion1 ELSE bloque ENDIF'''

def p_condicion1(p):
    '''condicion1 : empty
    | ELSEIF expresion bloque condicion1'''

def p_while(p):
    '''while : WHILE expresion bloque ENDWHILE'''

def p_for(p):
    '''for : FOR CTEINT bloque ENDFOR'''

def p_expresion(p):
    '''expresion : exp
    | exp expresion1 exp'''

def p_expresion1(p):
    '''expresion1 : LTHAN
    | GTHAN
    | EQUALTO
    | GTHANEQ
    | LTHANEQ
    | NOTEQUAL
    | AND
    | OR'''

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
    | MULTI
    | DIVIDE'''

def p_varcte(p):
    '''varcte : IDENTIFIER
    | CTEINT
    | CTEFLOAT
    | TRUE
    | FALSE
    | llamarfun'''

def p_func(p):
    '''func : METHOD tipo IDENTIFIER func1 bloque RETURN IDENTIFIER ENDMETHOD'''

def p_voidfunc(p):
    '''voidfunc : METHOD VOID IDENTIFIER func1 bloque ENDMETHOD'''

def p_func1(p):
    '''func1 : tipo func2
    | tipo func2 COMMA func1
    | empty'''

def p_func2(p):
    '''func2 : IDENTIFIER
    | REFERENCIA
    | VALOR'''

def p_llamarfun(p):
    '''llamarfun : CALLMETHOD IDENTIFIER llamarfun1'''

def p_llamarfun1(p):
    '''llamarfun1 : expresion
    | expresion COMMA llamarfun1
    | empty'''

def p_empty(p):
  '''empty : '''

# Error rule for syntax errors
def p_error(p):
    print("Error de tipo: ", p.value,"  linea: ", p.lineno)
    global err
    err = 0
