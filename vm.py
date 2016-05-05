class Machine(object):

    def __init__(self, cuadruplos):
        # The program--a tuple of tuples which represent instructions.
        self.program = cuadruplos
        
        self.programSize = len(self.program)

        # Registers
        self.a = self.b = self.t = None

        # Whether to branch
        self.flag = False

        # Code pointer
        self.pc = 0
        
        #Declaracion de memoria
        self.param_vars  = [[], [], []] #[0] integer, [1] float, [2] string
        self.int_vars    = [[], [], []] #[0] global, [1] local, [2] temporal
        self.float_vars  = [[], [], []] #[0] global, [1] local, [2] temporal
        self.string_vars = [[], [], []] #[0] global, [1] local, [2] temporal
        
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
        while self.pc is not None:
            i = self.program[self.pc]
            print (self.pc, self.flag, i)
            instr, rest = i[0], i[1:]
            self.pc += 1 # Don't forget to increment the counter
            if instr in ['=','==','!=','+','-','*','/','>=','<=','>','<']:
                instr = self.getOper(instr)
            getattr(self, 'i_'+instr)(*rest)
    
    def i_end(self, a, b, c):
        self.pc = None
        
    def i_imprimir(self, a, b, c):
        print(c)
    
    def i_gotof(self, a, b, c):
        if readFromMem(a,2,'int') == 0:
            self.pc = c
    
    def i_gotov(self, a, b, c):
        if readFromMem(a,2,'int') == 1:
            self.pc = c
            
    def i_goto(self, a, b, c):
        self.pc = c
    
    def i_era(self, a, b, c):
        #variables locales
        #asigna espacios de memoria donde c es la cantidad de vars
        self.pc = self.pc
        
    def i_param(self, a, b, c):
        #set_param(valor,tipo,dir)
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
        self.pc = self.pc
    
    def i_plus(self, a, b, c):
        #suma los valores de las direcciones a + b y lo asigna en temporal c
        self.pc = self.pc
        
    def i_subs(self, a, b, c):
        #resta los valores de a - c y lo asigna en temporal c
        self.pc = self.pc
    
    def i_mult(self, a, b, c):
        #multiplica a * b y lo asigna a temporal c
        self.pc = self.pc
        
    def i_div(self, a, b, c):
        #divide a / b y lo asigna a temporal c
        self.pc = self.pc
        
    def i_eq(self, a, b, c):
        #resultado bool de a == b y lo asigna a temporal c
        self.pc = self.pc
        
    def i_neq(self, a, b, c):
        #resultado bool de a != b y lo asigna a temporal c
        self.pc = self.pc
        
    def i_lteq(self, a, b, c):
        #resultado bool de a <= b y lo asigna a temporal c
        self.pc = self.pc
    
    def i_gteq(self, a, b, c):
        #resultado bool de a >= b y lo asigna a temporal c
        self.pc = self.pc
        
    def i_gt(self, a, b, c):
        #resultado bool de a > b y lo asigna a temporal c
        self.pc = self.pc
    
    def i_lt(self, a, b, c):
        #resultado bool de a < b y lo asigna a temporal c
        self.pc = self.pc
            
        
    def resetMemoria(self):
        #limpia memoria
        self.param_vars  = [[], [], []] #[0] integer, [1] float, [2] string
        self.int_vars    = [[], [], []] #[0] global, [1] local, [2] temporal
        self.float_vars  = [[], [], []] #[0] global, [1] local, [2] temporal
        self.string_vars = [[], [], []] #[0] global, [1] local, [2] temporal
        
    def writeToMem(self, value, dir, scope, type):
        if type == "int":
            self.int_vars[scope][dir] = value
        elif type == "float":
            self.float_vars[scope][dir] = value
        elif type == "string":
            self.string_vars[scope][dir] = value
        elif type == "param":
            self.param_vars[scope][dir] = value
        elif type == "return":
            self.returns.append(value)
            
    def readFromMem(self, dir, scope, type):
        if type == "int":
            return self.int_vars[scope][dir]
        elif type == "float":
            return self.float_vars[scope][dir]
        elif type == "string":
            return self.string_vars[scope][dir]  
        elif type == "param":
            return self.param_vars[scope][dir]  
        elif type == "return":
            return self.returns.pop()
            
    def countLocals(self):
        return len(self.int_vars[1])+len(self.float_vars[1])+len(self.string_vars[1])
    
    def i_copy(self, a, b):
        """Duplicates register b in register a"""
        setattr(self, a, getattr(self, b))

    def i_set(self, a, b):
        """Sets register a to the value b"""
        setattr(self, a, b)

    def i_exec(self, reg, op, *args):
        """Calls op and stores the result in reg."""
        setattr(self, reg, getattr(self, 'o_'+op)(*args))

    def i_test(self, op, *rest):
        if getattr(self, 'o_'+op)(*rest):
            self.flag = True
        else:
            self.flag = False

    def i_branch(self, line):
        """Jump to line if flag is set"""
        if self.flag: self.pc = line

    def i_jump(self, line):
        """Jump to line"""
        self.pc = line

    def o_zero(self, reg):
        """Is reg zero?"""
        return getattr(self, reg) == 0

    def o_lt(self, a, b):
        return getattr(self, a) < getattr(self, b)

    def o_sub(self, a, b):
        """reg a - reg b"""
        return getattr(self, a) - getattr(self, b)