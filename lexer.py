import ply.lex as lex

# List of reserved word that are going to be added to the tokens
reserved = {
  'ILied' : 'FALSE',
  'NoProblemo' : 'TRUE',
  'ItsShowtime' : 'PROGRAM',
  'YouHaveBeenTerminated' : 'ENDPROGRAM',
  'WhoAreYou' : 'VAR',
  'YouAreNotYouYouAreMe' : 'ENDVAR',
  'WhoIsYourDaddy' : 'GLOBAL',
  'AndWhatDoesHeDo' : 'ENDGLOBAL',
  'ComeAndGetMe' : 'READ',
  'TalkToTheHand' : 'PRINT',
  'BecauseImGoingToSayPlease' : 'IF',
  'IHaveAfewMoreQuestions' : 'ELSEIF',
  'NoItsNotTrue' : 'ELSE',
  'YouHaveNoRespectForLogic' : 'ENDIF',
  'STICK_AROUND' : 'WHILE',
  'Chill' : 'ENDWHILE',
  'NiceNightForAWalk' : 'FOR',
  'GetToTheChopper' : 'ENDFOR',
  'ListenToMeVeryCarefully' : 'METHOD',
  'HastaLaVistaBaby' : 'ENDMETHOD',
  'DoMeAFavor' : 'CALLMETHOD',
  'IllBeBack' : 'RETURN',
  'void' : 'VOID',
  'int' : 'INT',
  'float' : 'FLOAT',
  'bool' : 'BOOL',
  'HeyChristmasTree' : 'HASH',
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
  'STRING',
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
t_STRING     = r'\".*\"'
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
