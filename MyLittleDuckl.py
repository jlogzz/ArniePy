import ply.lex as lex

# List of reserved word that are going to be added to the tokens
reserved = {
  'program' : 'PROGRAM',
  'var' : 'VAR',
  'print' : 'PRINT',
  'if' : 'IF',
  'else' : 'ELSE',
  'int' : 'INT', 
  'float' : 'FLOAT',
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
  'LBRACE',
  'RBRACE',
  'CTEINT',
  'CTEFLOAT',
  'STRING',
  'EQUAL',
  'GTHAN',
  'LTHAN',
  'NOTEQUAL',
  'COMMA',
  'COLON',
  'SEMICOLON'
] + list(reserved.values())


    # Regular expression rules for simple tokens
t_CTEINT    = r'[\+-]?\d+'
t_CTEFLOAT  = r'[\+-]?\d+\.\d+'
t_STRING    = r'\'.*\''
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_MULTI     = r'\*'
t_DIVIDE    = r'/'
t_LPARENTHESES    = r'\('
t_RPARENTHESES    = r'\)'
t_LBRACE    = r'\{'
t_RBRACE    = r'\}'
t_EQUAL     = r'='
t_GTHAN     = r'>'
t_LTHAN     = r'<'
t_NOTEQUAL    = r'<>'
t_COMMA     = r'\,'
t_COLON     = r':'
t_SEMICOLON = r';'
t_ignore    = ' \t'

    # A regular expression rule with some action code
def t_IDENTIFIER(t):
  r'[a-zA-Z][a-zA-Z0-9]*'
  t.type = reserved.get(t.value, 'IDENTIFIER')
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