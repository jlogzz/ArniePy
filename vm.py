class Machine(object):

    #def __init__(self, cuadruplos, memGlobalEntero, memGlobalDecimal, memGlobalTexto, memLocalEntero, memLocalDecimal, memLocalTexto):
    def __init__(self, cuadruplos):
        # The program--a tuple of tuples which represent instructions.
        self.program = cuadruplos
        
        self.programSize = len(self.program)

        # Whether to branch
        self.flag = False

        # Code pointer
        self.pc = 0
        
        self.f = open('output.txt', 'w')
        
        # self.memGlobalEntero = memGlobalEntero #Contador para memoria virtual de variables globales enteras
        # self.memGlobalDecimal = memGlobalDecimal #Contador para memoria virtual de variables globales decimales
        # self.memGlobalTexto = memGlobalTexto #Contador para memoria virtual de variables globales texto
        # self.memLocalEntero = memLocalEntero #Contador para memoria virtual de variables locales y temporales enteras
        # self.memLocalDecimal = memLocalDecimal #Contador para memoria virtual de variables locales y temporales decimales
        # self.memLocalTexto = memLocalTexto #Contador para memoria virtual de variables locales y temporales texto
        
        #Declaracion de memoria
        self.param_vars  = [{}, {}, {}] #[0] integer, [1] float, [2] string
        self.int_vars    = [{}, {}, {}] #[0] global, [1] local, [2] temporal
        self.float_vars  = [{}, {}, {}] #[0] global, [1] local, [2] temporal
        self.string_vars = [{}, {}, {}] #[0] global, [1] local, [2] temporal
        
        self.param_count = []
        self.saltos = []
        self.returns = []
        
    def getOper(self, instr):
        if instr == "=":
            return "assign"
        elif instr == "==":
            return "eq"
        elif instr == "!=":
            return "neq"
        elif instr == "+":
            return "plus"
        elif instr == "-":
            return "subs"
        elif instr == "*":
            return "mult"
        elif instr == "/":
            return "div"
        elif instr == "<=":
            return "lteq"
        elif instr == ">=":
            return "gteq"
        elif instr == ">":
            return "gt"
        elif instr == "<":
            return "lt"
        

    def execute(self):
        print("Empezando ejecución del programa",file=self.f)
        print(file=self.f)
        while self.pc is not None:
            i = self.program[self.pc]
            #print (self.pc, self.flag, i)
            
            instr, rest = i[0], i[1:]
            self.pc += 1 # Don't forget to increment the counter
            if instr in ['=','==','!=','+','-','*','/','>=','<=','>','<']:
                instr = self.getOper(instr)
            getattr(self, 'i_'+instr)(*rest)
            # print(self.param_vars)
            # print(self.int_vars)
            # print(self.float_vars)
            # print(self.string_vars)
    
    def i_end(self, a, b, c):
        print(file=self.f)
        print("Ejecucion de programa finalizada",file=self.f)
        print("program ended successfully")
        self.pc = None
        
    def i_imprimir(self, a, b, c):
        if b != 'identifier':
            print(c, file=self.f)
        else:
            print(self.readFromMem(c), file=self.f)
    
    def i_gotof(self, a, b, c):
        if self.readFromMem(a) == 0:
            self.pc = c
    
    def i_gotov(self, a, b, c):
        if self.readFromMem(a) == 1:
            self.pc = c
            
    def i_goto(self, a, b, c):
        self.pc = c
    
    def i_era(self, a, b, c):
        #variables locales
        #asigna espacios de memoria donde c es la cantidad de vars
        self.pc = self.pc
        
    def i_param(self, a, b, c):
        #set_param(valor,tipo,dir)
        if type(a) is int:
            value = self.readFromMem(a)
        else:
            if b == "string":
                value = a
            elif b == "int":
                value = int(a)
            else:
                value = float(a)
        self.writeToMem(value,c)
        self.pc = self.pc
    
    def i_gosub(self, a, b, c):
        self.saltos.append(self.pc)
        self.pc = c
    
    def i_return(self, a, b, c):
        #variables locales
        if c != None:
            self.returns.append(c)
        #print(self.saltos.pop())
        self.pc = self.saltos.pop()
        
    def i_assign(self, a, b, c):
        #copia el valor de la direccion a en c
        if type(a) is int:
            value = self.readFromMem(a)
        else:
            if b == "string":
                value = a
            elif b == "int":
                value = int(a)
            else:
                value = float(a)
        self.writeToMem(value,c)
        self.pc = self.pc
    
    def i_plus(self, a, b, c):
        #suma los valores de las direcciones a + b y lo asigna en temporal c
        if type(a) is int:
            v1 = self.readFromMem(a)
        else:
            v1 = float(a)
        
        if type(b) is int:
            v2 = self.readFromMem(b)
        else:
            v2 = float(b)
            
        self.writeToMem(v1+v2,c)
        self.pc = self.pc
        
    def i_subs(self, a, b, c):
        #resta los valores de a - b y lo asigna en temporal c
        if type(a) is int:
            v1 = self.readFromMem(a)
        else:
            v1 = float(a)
        
        if type(b) is int:
            v2 = self.readFromMem(b)
        else:
            v2 = float(b)
            
        self.writeToMem(v1-v2,c)
        self.pc = self.pc
    
    def i_mult(self, a, b, c):
        #multiplica a * b y lo asigna a temporal c
        if type(a) is int:
            v1 = self.readFromMem(a)
        else:
            v1 = float(a)
        
        if type(b) is int:
            v2 = self.readFromMem(b)
        else:
            v2 = float(b)
            
        self.writeToMem(v1*v2,c)
        self.pc = self.pc
        
    def i_div(self, a, b, c):
        #divide a / b y lo asigna a temporal c
        if type(a) is int:
            v1 = self.readFromMem(a)
        else:
            v1 = float(a)
        
        if type(b) is int:
            v2 = self.readFromMem(b)
        else:
            v2 = float(b)
            
        self.writeToMem(v1/v2,c)
        self.pc = self.pc
        
    def i_eq(self, a, b, c):
        #resultado bool de a == b y lo asigna a temporal c
        if type(a) is int:
            v1 = self.readFromMem(a)
        else:
            v1 = float(a)
        
        if type(b) is int:
            v2 = self.readFromMem(b)
        else:
            v2 = float(b)
        if v1 == v2:
            self.writeToMem(True,c)
        else:
            self.writeToMem(False,c)
        self.pc = self.pc
        
    def i_neq(self, a, b, c):
        #resultado bool de a != b y lo asigna a temporal c
        if type(a) is int:
            v1 = self.readFromMem(a)
        else:
            v1 = float(a)
        
        if type(b) is int:
            v2 = self.readFromMem(b)
        else:
            v2 = float(b)
        if v1 != v2:
            self.writeToMem(True,c)
        else:
            self.writeToMem(False,c)
        self.pc = self.pc
        
    def i_lteq(self, a, b, c):
        #resultado bool de a <= b y lo asigna a temporal c
        if type(a) is int:
            v1 = self.readFromMem(a)
        else:
            v1 = float(a)
        
        if type(b) is int:
            v2 = self.readFromMem(b)
        else:
            v2 = float(b)
        if v1 <= v2:
            self.writeToMem(True,c)
        else:
            self.writeToMem(False,c)
        self.pc = self.pc
    
    def i_gteq(self, a, b, c):
        #resultado bool de a >= b y lo asigna a temporal c
        if type(a) is int:
            v1 = self.readFromMem(a)
        else:
            v1 = float(a)
        
        if type(b) is int:
            v2 = self.readFromMem(b)
        else:
            v2 = float(b)
        if v1 >= v2:
            self.writeToMem(True,c)
        else:
            self.writeToMem(False,c)
        self.pc = self.pc
        
    def i_gt(self, a, b, c):
        #resultado bool de a > b y lo asigna a temporal c
        if type(a) is int:
            v1 = self.readFromMem(a)
        else:
            v1 = float(a)
        
        if type(b) is int:
            v2 = self.readFromMem(b)
        else:
            v2 = float(b)
        if v1 > v2:
            self.writeToMem(True,c)
        else:
            self.writeToMem(False,c)
        self.pc = self.pc
    
    def i_lt(self, a, b, c):
        #resultado bool de a < b y lo asigna a temporal c
        if type(a) is int:
            v1 = self.readFromMem(a)
        else:
            v1 = float(a)
        
        if type(b) is int:
            v2 = self.readFromMem(b)
        else:
            v2 = float(b)
        if v1 < v2:
            self.writeToMem(True,c)
        else:
            self.writeToMem(False,c)
        self.pc = self.pc
            
        
    def resetMemoria(self):
        #limpia memoria
        self.param_vars  = [[], [], []] #[0] integer, [1] float, [2] string
        self.int_vars    = [[], [], []] #[0] global, [1] local, [2] temporal
        self.float_vars  = [[], [], []] #[0] global, [1] local, [2] temporal
        self.string_vars = [[], [], []] #[0] global, [1] local, [2] temporal
        
    def transDir(self, dir):
        scope = self.getScope(dir)
        type = self.getType(dir)
        if scope == 0:
            if type == "int":
                return dir
            elif type == "float":
                return dir - 5000
            elif type == "string":
                return dir - 10000
        elif scope == 1:
            if type == "int":
                return dir - 15000
            elif type == "float":
                return dir - 25000
            elif type == "string":
                return dir - 35000
                
    def getScope(self, dir):
        if dir < 15000:
            return 0
        else:
            return 1
            
    def getType(self, dir):
        if dir < 5000:
            return "int"
        elif dir < 10000:
            return "float"
        elif dir < 15000:
            return "string"
        elif dir < 25000:
            return "int"
        elif dir < 25000:
            return "float"
        else:
            return "string"
            
        
    def writeToMem(self, value, dir):
        scope = self.getScope(dir)
        type = self.getType(dir)
        if type == "int":
            self.int_vars[scope][self.transDir(dir)] = value
        elif type == "float":
            self.float_vars[scope][self.transDir(dir)] = value
        elif type == "string":
            self.string_vars[scope][self.transDir(dir)] = value
        elif type == "param":
            self.param_vars[scope][self.transDir(dir)] = value
        elif type == "return":
            self.returns.append(value)
            
    def readFromMem(self, dir):
        scope = self.getScope(dir)
        type = self.getType(dir)
        if type == "int":
            return int(self.int_vars[scope][self.transDir(dir)])
        elif type == "float":
            return float(self.float_vars[scope][self.transDir(dir)])
        elif type == "string":
            return self.string_vars[scope][self.transDir(dir)]  
        elif type == "param":
            return self.param_vars[scope][self.transDir(dir)]  
        elif type == "return":
            return self.returns.pop()
            
    def countLocals(self):
        return len(self.int_vars[1])+len(self.float_vars[1])+len(self.string_vars[1])