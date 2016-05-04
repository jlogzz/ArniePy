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
        self.name = name

    def has_var(self, name):
        return name in self.variables

    def get_var(self, name):
        return self.variables[name]

    def set_var(self,name,typ):
        self.variables[name] = typ
        self.var_count[name] = 0
        
contexts = []
functions = {}

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

def set_var(varn,typ):
    var = varn.lower()
    check_if_function(var)
    now = contexts[-1]
    if now.has_var(var):
        raise Exception( "Variable "+var+" already defined")
    else:
        now.set_var(var,typ.lower())

def get_params(node):
    if node.type == "parameter":
        return [check(node.args[0])]
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

def check(node):
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
            contexts.append(Context())
            check(node.args)
            pop()

        elif node.type == "vars_declaration":
            var_type = node.args[0].args[0]
            var_name = node.args[1].args[0]
            set_var(var_name, var_type)

        elif node.type in ['funcion','procedure']:
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
                

            functions[name] = (rettype,args)


            contexts.append(Context(name))
            for i in args:
                set_var(i[0],i[1])
            check(node.args[1])
            pop()

        elif node.type in ["llamarfun"]:
            fname = node.args[0].args[0].lower()
            if fname not in functions:
                raise Exception( "Function "+fname+" is not defined")
            if len(node.args) > 1:
                args = get_params(node.args[1])
            else:
                args = []
            rettype,vargs = functions[fname]

            if len(args) != len(vargs):
                raise Exception( "Function "+fname+" is expecting "+len(vargs)+" parameters and got "+len(args))
            else:
                for i in range(len(vargs)):
                    if vargs[i][1] != args[i]:
                        raise Exception( "Parameter "+(i+1)+" passed to function "+fname+" should be of type "+vargs[i][1]+" and not "+args[i])
            return rettype

        elif node.type == "asignacion":
            varn = check(node.args[0]).lower()
            if is_function_name(varn):
                vartype = functions[varn][0]
            else:
                if not has_var(varn):
                    raise Exception( "Variable "+varn+" not declared" )
                vartype = get_var(varn)
            assgntype = check(node.args[1])
            

            if vartype != assgntype:
                raise Exception( "Variable "+varn+" if of type "+vartype+" and does not support "+assgntype)

        elif node.type == "and_or":
            op = node.args[0].args[0]
            for i in range(1,2):
                a = check(node.args[i])
                if a != "boolean":
                    raise Exception( op+" requires a boolean. Got "+a+" instead.")

        elif node.type == "op":
            op = node.args[0].args[0]
            vt1 = check(node.args[1])
            vt2 = check(node.args[2])

            if vt1 != vt2:
                raise Exception( "Arguments of operation '"+op+"' must be of the same type. Got "+vt1+" and "+vt2+".")

            if op == '/':
                if vt1 != 'real':
                    raise Exception( "Operation "+op+" requires reals.")

            if op in ['==','<=','>=','>','<','!=']:
                return 'boolean'
            else:
                return vt1

        elif node.type in ['if','while']:
            c = 0
            t = check(node.args[c])
            if t != 'boolean':
                raise Exception( node.type+" condition requires a boolean. Got "+t+" instead.")

            # check body
            check(node.args[1])
            
            #check else/elseif
            if len(node.args) > 2:
                check(node.args[2])
            #check else when elseif
            if len(node.args) == 4:
                check(node.args[3])

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
                return get_var(node.args[0].args[0])
            elif node.args[0].type == 'llamarfun':
                return check(node.args[0])
            else:
                if node.args[0].type in types:
                    return node.args[0].type
                else:
                    return check(node.args[0])
        
        elif node.type == "escritura":
            check(node.args[0])
            
        
        elif node.type == "escritura_vars":
            if len(node.args) > 1:
                check(node.args[1])
            check(node.args[0])
        
        elif node.type == "lectura":
            check(node.args[0])
            return get_var(node.args[0].args[0])

        else:
            print ("semantic missing:", node.type)
