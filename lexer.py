import ply.lex as lex

# List of reserved word that are going to be added to the tokens
reserved = {
  'falso' : 'FALSE',
  'verdadero' : 'TRUE',
  'inicioPrograma' : 'PROGRAM',
  'finPrograma' : 'ENDPROGRAM',
  'inicioVariablesLocales' : 'VAR',
  'finVariablesLocales' : 'ENDVAR',
  'inicioVariablesGlobales' : 'GLOBAL',
  'finVariablesGlobales' : 'ENDGLOBAL',
  'leer' : 'READ',
  'imprimir' : 'PRINT',
  'inicioSi' : 'IF',
  'sinoEsto' : 'ELSEIF',
  'sino' : 'ELSE',
  'finSi' : 'ENDIF',
  'inicioMientras' : 'WHILE',
  'finMientras' : 'ENDWHILE',
  'inicioRepetir' : 'FOR',
  'finRepetir' : 'ENDFOR',
  'inicioFuncion' : 'METHOD',
  'finFuncion' : 'ENDMETHOD',
  'llamarFuncion' : 'CALLMETHOD',
  'regresa' : 'RETURN',
  'void' : 'VOID',
  'int' : 'INT',
  'string' : 'STRING',
  'float' : 'FLOAT',
  'bool' : 'BOOL',
  'hash' : 'HASH',
}

# List of token names. This is always required
tokens = [
  'IDENTIFIER',
  'PLUS',
  'MINUS',
  'MULTI',
  'DIVIDE',
  'LPARENTHESES',
  'RPARENTHESES',
  'CTEINT',
  'CTEFLOAT',
  'CTESTRING',
  'EQUAL',
  'EQUALTO',
  'GTHAN',
  'GTHANEQ',
  'LTHAN',
  'LTHANEQ',
  'NOTEQUAL',
  'COMMA',
  'OR',
  'AND',
  'REFERENCIA',
  'VALOR'
] + list(reserved.values())


    # Regular expression rules for simple tokens
t_CTEINT     = r'[\+-]?\d+'
t_CTEFLOAT   = r'[\+-]?\d+\.\d+'
t_CTESTRING     = r'\".*\"'
t_PLUS       = r'\+'
t_MINUS      = r'-'
t_MULTI      = r'\*'
t_DIVIDE     = r'/'
t_LPARENTHESES    = r'\('
t_RPARENTHESES    = r'\)'
t_EQUAL      = r'='
t_EQUALTO    = r'=='
t_GTHAN      = r'>'
t_GTHANEQ    = r'>='
t_LTHAN      = r'<'
t_LTHANEQ    = r'<='
t_NOTEQUAL   = r'!='
t_COMMA      = r'\,'
t_OR         = r'\|\|'
t_AND        = r'&&'
t_ignore     = ' \t'

    # A regular expression rule with some action code
def t_IDENTIFIER(t):
  r'[a-zA-Z][a-zA-Z0-9]*'
  t.type = reserved.get(t.value, 'IDENTIFIER')
  return t

    # A regular expression rule with some action code
def t_REFERENCIA(t):
  r'&[a-zA-Z][a-zA-Z0-9]*'
  t.type = reserved.get(t.value, 'REFERENCIA')
  return t

    # A regular expression rule with some action code
def t_VALOR(t):
  r'\*[a-zA-Z][a-zA-Z0-9]*'
  t.type = reserved.get(t.value, 'VALOR')
  return t


    # Define a rule so we can track line numbers
def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)

    # Error handling rule
def t_error(t):
  print("Caracter ilegal '", t.value[0], "' linea: ", t.lexer.lineno)
  t.lexer.skip(1)

    # Build the lexer from my environment and return it
lex.lex()
