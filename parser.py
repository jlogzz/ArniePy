import sys, os
from subprocess import Popen, PIPE

from ply import yacc,lex

from lexer import *
from rules import *
from semantic import *
from maquinavirtual import *

def get_input(file=False):
  if file:
    f = open(file,"r")
    data = f.read()
    f.close()
  else:
    data = ""
    while True:
      try:
        data += raw_input() + "\n"
      except:
        break
  return data

def main(options={},filename=False):
	logger = yacc.NullLogger()
	yacc.yacc(debug = logger, errorlog= logger)
	filename = sys.argv[1]
	
	data = get_input(filename)
	ast =  yacc.parse(data,lexer = lex.lex(nowarn=1))	
	
	try:
		check(ast)
	except Exception as e:
		print ("Error: ", e)
		sys.exit()
		
	m = maquinaVirtual(get_funciones(),get_cuads(),get_gInt(),get_gFloat(),get_gString(),get_lInt(),get_lFloat(),get_lString())
	m.execute()
	
if __name__ == '__main__':
	main()