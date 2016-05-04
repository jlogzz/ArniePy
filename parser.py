# Yacc example

import ply.yacc as yacc
import lexer
#import sys
# Get the token map from the lexer.  This is required.
from lexer import tokens
from rules import *


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
    ast =  yacc.parse(data,lexer = lex.lex(nowarn=1))

    try:
      check(ast)
    except Exception, e:
      print "Error: %s" % e
      sys.exit()

    if err:
      print("No hay ningun error, buen programa (Y)!")

  except EOFError:
    print("Error! No se pudo abrir el archivo!")
    break;
