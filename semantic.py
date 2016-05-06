types = ['int','float','string','bool','void']

class Any(object):
    def __eq__(self, o):
        return True
    def __ne__(self, o):
        return False

class Context(object):
    """docstring for Context"""
    def __init__(self, name=None):
        self.variables = {}
        self.var_count = {}
        self.var_dir = {}
        self.name = name

    def has_var(self, name):
        return name in self.variables

    def get_var(self, name):
        return self.variables[name]
        
    def get_dir(self, name):
        return self.var_dir[name]

    def set_var(self,name,typ,dir):
        self.variables[name] = typ
        self.var_count[name] = 0
        self.var_dir[name] = dir
        
contexts = []

functions = {}
functions_dir = {}
functions_param = {}
functions_param_dir = {}
functions_var = {}

pilaO = [] #Pila de operandos

pOper = [] #Pila de operadores

pTipos = [] #Pila de tipos de los operadores

pSaltos = [] #Pila de saltos para los condicionales y los ciclos

pReturn = [] #Pila de returns

cuadruplos = [] #Lista de cuadruplos

memGlobalEntero = -1 #Contador para memoria virtual de variables globales enteras
memGlobalDecimal = 4999 #Contador para memoria virtual de variables globales decimales
memGlobalTexto = 9999 #Contador para memoria virtual de variables globales texto
memLocalEntero = 14999 #Contador para memoria virtual de variables locales y temporales enteras
memLocalDecimal = 24999 #Contador para memoria virtual de variables locales y temporales decimales
memLocalTexto = 34999 #Contador para memoria virtual de variables locales y temporales texto

globalFlag = 1

functionFlag = 0

def get_funciones():
    return dirProcs

def get_cuads():
    return cuadruplos
 
def get_gInt():
    return memGlobalEntero

def get_gFloat():
    return memGlobalDecimal
    
def get_gString():
    return memGlobalTexto

def get_lInt():
    return memLocalEntero

def get_lFloat():
    return memLocalDecimal
    
def get_lString():
    return memLocalTexto

def pop():
    count = contexts[-1].var_count
    for v in count:
        if count[v] == 0:
            print ("Warning: variable", v, "was declared, but not used.")
    contexts.pop()

def check_if_function(var):
    if var.lower() in functions and not if_function_name(var.lower()):
        raise Exception("A function called %s already exists") % var

def is_function_name(var):
    for i in contexts[::-1]:
        if i.name == var:
            return True
    return False

def has_var(varn):
    var = varn.lower()
    check_if_function(var)
    for c in contexts[::-1]:
        if c.has_var(var):
            return True
    return False

def get_var(varn):
    var = varn.lower()
    for c in contexts[::-1]:
        if c.has_var(var):
            c.var_count[var] += 1
            return c.get_var(var)
    raise Exception( "Variable "+var+" is referenced before assignment")
    
def get_dir(varn):
    var = varn.lower()
    for c in contexts[::-1]:
        if c.has_var(var):
            c.var_count[var] += 1
            return c.get_dir(var)
    raise Exception( "Variable "+var+" is referenced before assignment")

def set_var(varn,typ):
    direccion = None
    global memGlobalDecimal
    global memGlobalEntero
    global memGlobalTexto
    global memLocalDecimal
    global memLocalEntero
    global memLocalTexto
    global cuadruplos
    
    var = varn.lower()
    check_if_function(var)
    now = contexts[-1]
    glob = contexts[0]
    if now.has_var(var):
        raise Exception( "Variable "+var+" already defined")
    elif glob.has_var(var):
        raise Exception( "Variable "+var+" already globally defined")
    else:
        if globalFlag == 1:
            if typ.lower() == "int":
                memGlobalEntero += 1
                direccion = memGlobalEntero
                val = '0'
            elif typ.lower() == "float":
                memGlobalDecimal += 1
                direccion = memGlobalDecimal
                val = '0.0'
            else:
                memGlobalTexto += 1
                direccion = memGlobalTexto
                val = ""
        else:
            if typ.lower() == "int":
                memLocalEntero += 1
                direccion = memLocalEntero
                val = '0'
            elif typ.lower() == "float":
                memLocalDecimal += 1
                direccion = memLocalDecimal
                val = '0.0'
            else:
                memLocalTexto += 1
                direccion = memLocalTexto
                val = ""
        cuadruplos.append(['=',val,typ.lower(),direccion])
        now.set_var(var,typ.lower(),direccion)
        return direccion

def get_params(node):
    global pilaO
    if node.type == "parameter":
        ret = check(node.args[0])
        return [ret]
    else:
        l = []
        for i in node.args:
            l.extend(get_params(i))
        return l

def flatten(n):
    if not is_node(n): return [n]
    if not n.type.endswith("_list"):
        return [n]
    else:
        l = []
        for i in n.args:
            l.extend(flatten(i))
        return l

def is_node(n):
    return hasattr(n,"type")
    
def printCuads():
    print(cuadruplos)
    
def getCuads():
    return cuadruplos

def printMem():
        print("")
        print("Global")
        print("memGlobalEntero:",memGlobalEntero)
        print("memGlobalDecimal:",memGlobalDecimal)
        print("memGlobalTexto:",memGlobalTexto)
        print("Local")
        print("memLocalEntero:",memLocalEntero)
        print("memLocalDecimal:",memLocalDecimal)
        print("memLocalTexto:",memLocalTexto)
        print("")
    

def check(node):
    global functionFlag
    global globalFlag
    global memLocalEntero
    global memLocalDecimal
    global memLocalTexto
    
    if not is_node(node):
        if hasattr(node,"__iter__") and type(node) != type(""):
            for i in node:
                check(i)
        else:
            return node
    else:
        if node.type in ['identifier']:
            return node.args[0]

        elif node.type in ['vars_list','estatuto_list','funcion_list']:
            return check(node.args)
            
        elif node.type in ['global']:
            check(node.args)

        elif node.type in ["bloque","programa"]:
            if node.type == "programa":
                cuadruplos.append(['goto',None,None,None])
            if node.type == "bloque" and functionFlag == 0:
                cont = len(cuadruplos)
                cuadruplos[0][3] = cont
            if node.type == "bloque" and globalFlag:
                globalFlag = 0
            contexts.append(Context())
            check(node.args)
            pop()
            if node.type == "programa":
                cuadruplos.append(['end',None,None,None])

        elif node.type == "vars_declaration":
            var_type = node.args[0].args[0]
            var_name = node.args[1].args[0]
            set_var(var_name, var_type)

        elif node.type in ['funcion','procedure']:
            functionFlag = 1
            globalFlag = 0
            head = node.args[0]
            if node.type == "procedure":
                name = head.args[0].args[0].lower()
            else:
                name = head.args[1].args[0].lower()
                
            check_if_function(name)


            if node.type == "procedure":
                rettype = 'void'
                
                if len(head.args) == 1:
                    args = []
                else:
                    args = flatten(head.args[1])
                    args = map(lambda x: (x.args[1].args[0],x.args[0].args[0]), args)
            else:
                rettype = head.args[0].args[0].lower()
                
                if len(head.args) == 2:
                    args = []
                else:
                    args = flatten(head.args[2])
                    args = map(lambda x: (x.args[1].args[0],x.args[0].args[0]), args)

            functions[name] = (rettype,list(args))
            
            

            contexts.append(Context(name))
            for i in functions[name][1]:
                functions_param_dir[name] = {i[0]:set_var(i[0],i[1])}
            functions_dir[name] = len(cuadruplos)
            functions_param[name] = len(functions[name][1])
            check(node.args[1])
            
            pop()
            functionFlag = 0

        elif node.type in ["llamarfun"]:
            fname = node.args[0].args[0].lower()
            if fname not in functions:
                raise Exception( "Function "+fname+" is not defined")
                
            cuadruplos.append(['era',None,None,'1'])
            if len(node.args) > 1:
                args = get_params(node.args[1])
            else:
                args = []
            rettype,vargs = functions[fname]

            if len(args) != len(list(vargs)):
                raise Exception( "Function "+fname+" is expecting "+str(len(vargs))+" parameters and got "+str(len(args)))
            else:
                for i in range(len(vargs)):
                    if vargs[i][1] != args[i]:
                        raise Exception( "Parameter "+str(i+1)+" passed to function "+fname+" should be of type "+vargs[i][1]+" and not "+args[i])
                    dirParam = functions_param_dir[fname][vargs[i][0]]
                    typ = pTipos.pop()
                    cuadruplos.append(['param',pilaO.pop(),typ,dirParam])
            cuadruplos.append(['gosub',fname,None,functions_dir[fname]])
            return rettype
        
        elif node.type == "retorno":
            functype = functions[contexts[-2].name][0]
            ret = node.args[0].args[0]
            ret = check(node.args[0])
            if functype != ret:
                raise Exception("La funcion debe de regresar el mismo tipo que espera la funcion")
            retval = pilaO.pop()
            pTipos.pop()
            pReturn.append(retval)
            cuadruplos.append(['return',None,None,retval])
            
        elif node.type == "asignacion":
            varn = check(node.args[0]).lower()
            if is_function_name(varn):
                vartype = functions[varn][0]
            else:
                if not has_var(varn):
                    raise Exception( "Variable "+varn+" not declared" )
                pilaO.append(get_dir(varn))
                pTipos.append(get_var(varn))
                pOper.append('=')
                vartype = get_var(varn)
            assgntype = check(node.args[1])
            

            if vartype != assgntype:
                raise Exception( "Variable "+varn+" if of type "+vartype+" and does not support "+assgntype)
            
            oper = pOper.pop()
            if node.args[1].args[0].type == "llamarfun":
                oDer = pReturn.pop()
                typ = assgntype
            else:
                oDer = pilaO.pop()
                typ = pTipos.pop()    
            oIzq = pilaO.pop()
            pTipos.pop()
            #Genera cuadruplo de asignacion
            cuadruplos.append([oper,oDer,typ,oIzq])
            
            
        elif node.type == "and_or":
            op = node.args[0].args[0]
            pOper.append(op)
            for i in range(1,2):
                a = check(node.args[i])
                if a != "boolean":
                    raise Exception( op+" requires a boolean. Got "+a+" instead.")

        elif node.type == "op":
            op = node.args[0].args[0]
            vt1 = check(node.args[1])
            vt2 = check(node.args[2])
            pOper.append(op)

            if vt1 != vt2:
                raise Exception( "Arguments of operation '"+op+"' must be of the same type. Got "+vt1+" and "+vt2+".")

            if op == '/':
                if vt1 != 'float':
                    raise Exception( "Operation "+op+" requires reals.")
                    
            oper = pOper.pop()
            oDer = pilaO.pop()
            pTipos.pop()
            oIzq = pilaO.pop()
            pTipos.pop()
            
            if op in ['==','<=','>=','>','<','!=']:
                memLocalEntero += 1
                auxDir = memLocalEntero
                res = 'bool'
            else:
                if vt1 == "int":
                    memLocalEntero += 1
                    auxDir = memLocalEntero
                    res = "int"
                elif vt1 == "float":
                    memLocalDecimal += 1
                    auxDir = memLocalDecimal
                    res = "float"
                elif vt1 == "string":
                    memLocalTexto += 1
                    auxDir = memLocalTexto
                    res = "string"
            
            cuadruplos.append([oper,oIzq,oDer,auxDir])
            pilaO.append(auxDir)
            pTipos.append(res)
            
            if op in ['==','<=','>=','>','<','!=']:
                return 'boolean'
            else:
                return vt1

        elif node.type in ['if','while']:
            c = 0
            t = check(node.args[c])
            if t != 'boolean':
                raise Exception( node.type+" condition requires a boolean. Got "+t+" instead.")
            
            aux = pTipos.pop()
            if node.type == "while":
                pSaltos.append(len(cuadruplos))
            resultado = pilaO.pop()
            cuadruplos.append(['gotof',resultado,None,None])
            if node.type == "while":
                pSaltos.append(len(cuadruplos)-1)
            else:
                pSaltos.append(len(cuadruplos))
           
                
            # check body
            check(node.args[1])
            if node.type == "while":
                falso = pSaltos.pop()
                retorno = pSaltos.pop()-1
                cuadruplos.append(['goto',None,None,retorno])
                cuadruplos[falso][3] = len(cuadruplos)
            else:
                cuadruplos.append(['goto',None,None,None])
                falso = pSaltos.pop()
                cuadruplos[falso-1][3] = len(cuadruplos) 
                pSaltos.append(len(cuadruplos)-1)
            
            #check else/elseif
            if len(node.args) > 2:
                check(node.args[2])
                fin = pSaltos.pop()
                cuadruplos[fin][3] = len(cuadruplos)
                pSaltos.append(len(cuadruplos)-1)            
            #check else when elseif
            if len(node.args) == 4:
                check(node.args[3])
                fin = pSaltos.pop()
                cuadruplos[fin][3] = len(cuadruplos)
        elif node.type == "for":
            if node.args[0].args[0].type == "int":
                check(node.args[1])
            elif node.args[0].args[0].type == "identifier":
                if get_var(node.args[0].args[0].args[0]) == "int":
                    check(node.args[1])
                else:
                    raise Exception("Repetir requiere un int como valor en lugar de "+get_var(node.args[0].args[0].args[0]))
            else:
                raise Exception("Repetir requiere un int como valor en lugar de "+node.args[0].args[0].type)

        elif node.type == "elemento":
            if node.args[0].type == 'identifier':
                pilaO.append(get_dir(node.args[0].args[0]))
                pTipos.append(get_var(node.args[0].args[0]))
                return get_var(node.args[0].args[0])
            elif node.args[0].type == 'llamarfun':
                return check(node.args[0])
            else:
                if node.args[0].type in types:
                    pilaO.append(node.args[0].args[0])
                    pTipos.append(node.args[0].type)
                    if node.args[0].type == "int":
                        memLocalEntero += 1
                        auxDir = memLocalEntero
                    elif node.args[0].type == "float":
                        memLocalDecimal += 1
                        auxDir = memLocalDecimal
                    else:
                        memLocalTexto += 1
                        auxDir = memLocalTexto
                    #pilaO.append(auxDir)
                    return node.args[0].type
                else:
                    return check(node.args[0])
        
        elif node.type == "escritura":
            check(node.args[0])
            
        
        elif node.type == "escritura_vars":
            if len(node.args) > 1:
                check(node.args[1])
            check(node.args[0])
            typ = None
            if node.args[0].args[0].type == "identifier":
                typ = "identifier"
            
            if node.args[0].args[0].type == "llamarfun":
                value = pReturn.pop()
                typ = "identifier"
            else:
                value = pilaO.pop()
                typ = pTipos.pop()
            cuadruplos.append(['imprimir',None,typ,value])
        
        elif node.type == "lectura":
            check(node.args[0])
            return get_var(node.args[0].args[0])

        else:
            print ("semantic missing:", node.type)
            
