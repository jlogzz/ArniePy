from codegen.ast import Node
import sys

def p_programa(p):
    '''programa : PROGRAM bloque ENDPROGRAM
    | PROGRAM bloque funciones ENDPROGRAM
    | PROGRAM global bloque funciones ENDPROGRAM'''
    if len(p) == 4:
        p[0] = Node('programa', p[2])
    elif len(p) == 5:
        p[0] = Node('programa', p[2], p[4])
    else:
        p[0] = Node('programa', p[2], p[3], p[5])

def p_funciones(p):
    '''funciones : func funciones
    | voidfunc funciones
    | empty'''
    if len(p) == 3:
        p[0] = Node('funcion_list', p[1], p[2])

def p_vars(p):
    '''vars : VAR vars_list ENDVAR'''
    p[0] = Node('vars', p[2])

def p_global(p):
    '''global : GLOBAL vars_list ENDGLOBAL'''
    p[0] = Node('global', p[2])

def p_vars_list(p):
    '''vars_list : vars_declaration vars_list
    | vars_declaration
    | empty'''
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
    | hash
    | VOID'''
    p[0] = Node('tipo', p[1])

def p_bloque(p):
    '''bloque : estatuto_list'''
    if len(p) > 2:
        p[0] = Node('bloque', p[1])
        
def p_estatuto_list(p):
    '''estatuto_list : estatuto estatuto_list
    | estatuto
    | empty'''

def p_estatuto(p):
    '''estatuto : asignacion
    | condicion
    | escritura
    | lectura
    | while
    | for
    | vars'''
    p[0] = Node('estatuto', p[1])

def p_asignacion(p):
    '''asignacion : identifier EQUAL expresion'''
    p[0] = Node('asignacion', p[1], p[3])

def p_escritura(p):
    '''escritura : PRINT escritura_vars'''
    p[0] = Node('escritura', p[2])

def p_escritura_vars(p):
    '''escritura_vars : expresion COMMA escritura_vars
    | expresion'''
    if len(p) > 2:
        p[0] = Node('escritura_vars', p[1], p[2])
    else:
        p[0] = Node('escritura_vars', p[1])

def p_lectura(p):
    '''lectura : READ identifier'''
    p[0] = Node('lectura', p[2])

def p_condicion(p):
    '''condicion : IF expresion estatuto_list elseif ENDIF
    | IF expresion estatuto_list elseif ELSE estatuto_list ENDIF
    | IF expresion estatuto_list ELSE estatuto_list ENDIF
    | IF expresion estatuto_list ENDIF'''
    if len(p) == 5:
        p[0] = Node('if', p[2], p[3])
    elif len(p) == 6:
        p[0] = Node('if', p[2], p[3], p[4])
    elif len(p) == 7:
        p[0] = Node('if', p[2], p[3], p[5])
    else:
        p[0] = Node('if', p[2], p[3], p[4], p[6])

def p_elseif(p):
    '''elseif : ELSEIF expresion estatuto_list'''
    p[0] = Node('if', p[2], p[3])

def p_while(p):
    '''while : WHILE expresion estatuto_list ENDWHILE'''
    p[0] = Node('while', p[2], p[3])

def p_for(p):
    '''for : FOR int estatuto_list ENDFOR'''
    p[0] = Node('for', p[2], p[3])

def p_expresion(p):
    '''expresion : termino
    | expresion and_or termino'''
    if len(p) == 2:
        p[0] = Node('op', p[1])
    else:
        p[0] = Node('op', p[2], p[1], p[3])
        
def p_termino(p):
    '''termino : factor
    | termino sign factor'''
    if len(p) == 2:
        p[0] = Node('op', p[1])
    else:
        p[0] = Node('op', p[2], p[1], p[3])
        
def p_factor(p):
    '''factor : elemento
    | factor psign elemento'''
    if len(p) == 2:
        p[0] = Node('op', p[1])
    else:
        p[0] = Node('op', p[2], p[1], p[3])

def p_sign(p):
    '''sign : LTHAN
    | GTHAN
    | EQUALTO
    | GTHANEQ
    | LTHANEQ
    | NOTEQUAL
    | PLUS
    | MINUS'''
    p[0] = Node('sign', p[1])
    
def p_psign(p):
    '''psign : MULTI
    | DIVIDE'''
    p[0] = Node('psign', p[1])
    
def p_and_or(p):
    '''and_or : AND
    | OR'''
    p[0] = Node('and_or', p[1])

def p_elemento(p):
    '''elemento : identifier
    | int
    | float
    | string
    | LPARENTHESES expresion RPARENTHESES
    | llamarfun'''
    if len(p) == 2:
        p[0] = Node("elemento", p[1])
    else:
        p[0] = Node("elemento", p[2])

def p_func(p):
    '''func : funchead bloque RETURN identifier ENDMETHOD'''
    p[0] = Node('funcion', p[1], p[2], p[4])

def p_voidfunc(p):
    '''voidfunc : prochead bloque ENDMETHOD'''
    p[0] = Node('procedure', p[1], p[2])
    
def p_prochead(p):
    '''prochead : METHOD VOID identifier parameter_list
    | METHOD VOID identifier'''
    if len(p) == 4:
	    p[0] = Node("procedure_head",p[3])
    else:
        p[0] = Node("procedure_head",p[3],p[4])

def p_funchead(p):
    '''funchead : METHOD tipo identifier parameter_list
    | METHOD tipo identifier'''
    if len(p) == 4:
        p[0] = Node("funcion_head",p[2], p[3])
    else:
        p[0] = Node("funcion_head",p[2], p[3], p[4])

def p_parameter_list(p):
    '''parameter_list : parameter
    | parameter COMMA parameter_list'''
    if len(p) == 4:
        p[0] = Node("parameter_list", p[1], p[3])
    else:
        p[0] = p[1]

def p_parameter(p):
    '''parameter : tipo identifier
    | tipo referencia'''
    p[0] = Node('parameter', p[1], p[2])

def p_llamarfun(p):
    '''llamarfun : CALLMETHOD identifier funparams
    | CALLMETHOD identifier'''
    if len(p) > 3:
        p[0] = Node('llamarfun', p[2], p[3])
    else:
        p[0] = Node('llamarfun', p[2])

def p_funparams(p):
    '''funparams : expresion
    | expresion COMMA funparams'''
    if len(p) > 2:
        p[0] = Node('funparams', p[1], p[3])
    else:
        p[0] = Node('funparams', p[1])

def p_empty(p):
  '''empty : '''
  
def p_identifier(p):
    '''identifier : IDENTIFIER'''
    p[0] = Node('identifier', str(p[1]).lower())
    
def p_referencia(p):
    '''referencia : REFERENCIA'''
    p[0] = Node('referencia', str(p[1]).lower())

def p_int(p):
    '''int : INT'''
    p[0] = p[1]

def p_float(p):
    '''float : FLOAT'''
    p[0] = p[1]

def p_bool(p):
    '''bool : BOOL'''
    p[0] = p[1]
    
def p_string(p):
    '''string : STRING'''
    p[0] = p[1]

def p_hash(p):
    '''hash : HASH'''
    p[0] = p[1]

# Error rule for syntax errors
def p_error(p):
	print ("Syntax error in input, in line",p.lineno)
	sys.exit()
