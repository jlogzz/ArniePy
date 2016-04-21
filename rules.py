from codegen.ast import Node
import sys

def p_programa(p):
    '''programa : PROGRAM bloque ENDPROGRAM
    | PROGRAM bloque ENDPROGRAM funciones
    | global PROGRAM bloque ENDPROGRAM funciones'''
    if len(p) == 4:
        p[0] = Node('programa', p[2])
    elif len(p) == 5:
        p[0] = Node('programa', p[2], p[4])
    else:
        p[0] = Node('programa', p[1], p[3], p[5])

def p_identifier(p):
    '''identifier : IDENTIFIER'''
    p[0] = Node('identifier', str(p[1]).lower())

def p_int(p):
    '''int : INT'''

def p_float(p):
    '''float : FLOAT'''

def p_bool(p):
    '''bool : BOOL'''

def p_hash(p):
    '''hash : HASH'''

def p_funciones(p):
    '''funciones : func funciones
    | voidfunc funciones
    | empty'''
    if len(p) == 3:
        p[0] = Node('funciones', p[1], p[2])

def p_vars(p):
    '''vars : VAR vars_list ENDVAR'''
    p[0] = Node('vars', p[2])

def p_global(p):
    '''global : GLOBAL vars_list ENDGLOBAL'''
    p[0] = Node('global', p[2])

def p_vars_list(p):
    '''vars_list : vars_declaration vars_list
    | vars_declaration'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node('vars_list', p[1], p[2])
    
def p_vars_declaration(p):
    '''vars_declaration : tipo identifier'''
    p[0] = Node('vars_declaration', p[1], p[2])

def p_tipo(p):
  '''tipo : int
      | float
      | string
      | bool
      | hash'''
      p[0] = Node('tipo', p[1])

def p_bloque(p):
    '''bloque : empty
    | estatuto bloque'''
    if len(p) > 2:
        p[0] = Node('bloque', p[1], p[2])

def p_estatuto(p):
    '''estatuto : asignacion
    | condicion
    | escritura
    | lectura
    | while
    | for
    | vars
    | empty'''
    p[0] = Node('estatuto', p[1])

def p_asignacion(p):
    '''asignacion : IDENTIFIER EQUAL expresion'''
    p[0] = Node('asignacion', p[3])

def p_escritura(p):
    '''escritura : PRINT escritura1'''
    p[0] = Node('escritura', p[2])

def p_escritura1(p):
    '''escritura1 : expresion escritura2'''
    p[0] = Node('escritura1', p[1], p[2])

def p_escritura2(p):
    '''escritura2 : empty
    | COMMA escritura1'''
    if len(p) > 2:
        p[0] = p[2]

def p_lectura(p):
    '''lectura : READ IDENTIFIER'''
    p[0] = Node('lectura', p[2])

def p_condicion(p):
    '''condicion : IF expresion bloque condicion1 ENDIF
    | IF expresion bloque condicion1 ELSE bloque ENDIF'''
    if len(p) == 6:
        p[0] = Node('condicion', p[2], p[3], p[4])
    else:
        p[0] = Node('condicion', p[2], p[3], p[4], p[6])

def p_condicion1(p):
    '''condicion1 : empty
    | ELSEIF expresion bloque condicion1'''
    if len(p) > 2:
        p[0] = Node('condicion1', p[2], p[3], p[4])

def p_while(p):
    '''while : WHILE expresion bloque ENDWHILE'''
    p[0] = Node('while', p[2], p[3])

def p_for(p):
    '''for : FOR CTEINT bloque ENDFOR'''
    p[0] = Node('for', p[3])

def p_expresion(p):
    '''expresion : exp
    | exp expresion1 exp'''
    if len(p) == 2:
        p[0] = Node('expresion', p[1])
    else:
        p[0] = Node('expresion', p[1], p[2])



def p_expresion1(p):
    '''expresion1 : LTHAN
    | GTHAN
    | EQUALTO
    | GTHANEQ
    | LTHANEQ
    | NOTEQUAL
    | AND
    | OR'''
    p[0] = Node('expresion1', p[1])

def p_exp(p):
    '''exp : termino exp1'''
    p[0] = Node('exp', p[1], p[2])

def p_exp1(p):
    '''exp1 : empty
      | PLUS termino exp1
      | MINUS termino exp1'''
      if len(p) > 2:
          p[0] = Node('exp1', p[2], p[3])

def p_termino(p):
    '''termino : factor termino1'''
    p[0] = Node('termino', p[1], p[2])

def p_termino1(p):
    '''termino1 : empty
    | MULTI termino
    | DIVIDE termino'''
    if len(p) > 2:
        p[0] = p[2]

def p_factor(p):
    '''factor : LPARENTHESES expresion RPARENTHESES
    | factor1 varcte'''
    if len(p) == 3:
        p[0] = Node('factor', p[1], p[2])
    else:
        p[0] = Node('factor', p[2])

def p_factor1(p):
    ''' factor1 : empty
    | MULTI
    | DIVIDE'''
    p[0] = p[1]

def p_varcte(p):
    '''varcte : IDENTIFIER
    | CTEINT
    | CTEFLOAT
    | STRING
    | TRUE
    | FALSE
    | llamarfun'''
    p[0] = Node('varcte', p[1])

def p_func(p):
    '''func : METHOD tipo IDENTIFIER func1 bloque RETURN IDENTIFIER ENDMETHOD'''
    p[0] = Node('func', p[2], p[4], p[5])

def p_voidfunc(p):
    '''voidfunc : METHOD VOID identifier func1 bloque ENDMETHOD'''
    p[0] = Node('voidfunc', p[4], p[5])

def p_func1(p):
    '''func1 : tipo func2
    | tipo func2 COMMA func1
    | empty'''
    if len(p) == 3:
        p[0] = Node('func1', p[1], p[2])
    elif len(p) == 5:
        p[0] = Node('func1', p[1], p[2], p[4])


def p_func2(p):
    '''func2 : identifier
    | referencia
    | valor'''
    p[0] = p[1]

def p_llamarfun(p):
    '''llamarfun : CALLMETHOD identifier funparams'''
    p[0] = Node('llamarfun', p[2], p[3])

def p_funparams(p):
    '''funparams : expresion
    | expresion COMMA funparams
    | empty'''
    if len(p) > 2:
        p[0] = Node('funparams', p[1], p[3])
    else:
        p[0] = Node('funparams', p[1])

def p_empty(p):
  '''empty : '''

# Error rule for syntax errors
def p_error(p):
    print("Error de tipo: ", p.value,"  linea: ", p.lineno)
    err = 0
