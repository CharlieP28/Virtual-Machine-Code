class CPU():
    def __init__(self, ram, input_function):
        self.__input_function = input_function
        self.__RAM = ram
        self.__PC = 0
        self.__MAR = 0
        self.__MDR = 0
        self.__CIR={
            'opcode': None,
            'operand': None
        }
        self.__ACC=0   

        self.__z=0
        self.__s=0

        self.__instructionSet = {
            '0001': 'ADD',
            '0010': 'SUB',
            '0011': 'STO',
            '0100': 'OUT',
            '0101': 'INP',
            '0110': 'LOAD',
            '0111': 'HALT',
            '1000': 'JMP',
            '1001': 'JMZ',
            '1010': 'JMPP'
        }
        self.outputVal = ''

    def update_flags(self):
        self.__z = 1 if self.__ACC == 0 else 0
        self.__s = 1 if self.__ACC < 0 else 0
    
    def ALU(self):
        if self.__CIR['opcode'] == "ADD":
            self.__ACC += self.__MDR
        elif self.__CIR['opcode'] == 'SUB':
            self.__ACC -= self.__MDR
        self.update_flags()
    

    def fetch(self):
        self.__MAR = self.__PC
        self.__MDR = self.__RAM.get_instruction(self.__MAR)

        if self.__MDR == [None, None]:
            return False, ''

        self.__CIR = {
            "opcode": self.__MDR[0],
            "operand": self.__MDR[1]
        }

        return True, ''

    def decode(self):
        self.__CIR['opcode'] = self.__instructionSet[self.__CIR['opcode']]
    
    def execute(self):
        self.outputVal = ''
        advance_pc = True
        if self.__CIR['opcode'] == "LOAD":
            self.__MAR = self.__CIR["operand"]
            self.__MDR = self.__RAM.get_data(self.__MAR)
            self.__ACC = self.__MDR
            self.update_flags()
            
            
        elif self.__CIR['opcode'] == "ADD" or self.__CIR['opcode'] == "SUB":
            self.__MAR = self.__CIR["operand"]
            self.__MDR = self.__RAM.get_data(self.__MAR)
            self.ALU()

        elif self.__CIR['opcode'] == 'STO':
            self.__RAM.set_data(self.__CIR['operand'], self.__ACC)
        
        elif self.__CIR['opcode'] == 'INP':
            inputVal = self.__input_function()
            self.__ACC = inputVal
            self.update_flags()
            advance_pc = True

        elif self.__CIR['opcode'] == 'OUT':
            self.outputVal = str(self.__ACC)
        
        elif self.__CIR["opcode"] == "HALT":
            return False, ''

        elif self.__CIR['opcode'] == 'JMP':
            self.__PC = self.__CIR["operand"]
            advance_pc = False
        
        elif self.__CIR['opcode'] == "JMZ":
            if self.__z == 1:
                self.__PC = self.__CIR["operand"]
                advance_pc = False
        
        elif self.__CIR['opcode'] == 'JMPP':
            if self.__s == 0:
                self.__PC = self.__CIR['operand']
                advance_pc = False

        if advance_pc:
            self.__PC += 1
        else:
            pass
        
        return True, self.outputVal
    


class RAM():
    def __init__(self):
        self.__instructions = [[None, None] for _ in range(50)]
        self.__data = [0]*50

    def get_instruction(self, index):
        return self.__instructions[index]
    
    def get_data(self, index):
        return self.__data[index]
    
    def set_instruction(self, index, opcode, operand):
        self.__instructions[index] = [opcode, operand]

    def set_data(self, index, data):
        self.__data[index] = data
        


class Assembler():
    def __init__(self):
        self.opcodes = {
            "ADD": "0001",
            "SUB": "0010",
            "STO": "0011",
            "OUT": "0100",
            "INP": "0101",
            "LOAD": "0110",
            "HALT": "0111",
            "JMP": '1000',
            'JMZ': '1001',
            'JMPP': '1010'
        }

    def tokenise(self, source):
        lines = source.split("\n")

        self.tokens = []

        for line in lines:
            line = line.split(";")[0].strip()
            if line == "":
                continue

            self.tokens.append(line.split())
    
    def generate_symbol_tree(self):
        self.instructions = []
        self.data_values = []
        self.symbols = {}

        data_address_index = 0

        instruction_address = 0


        for token in self.tokens:
            if len(token) > 1 and token[1] == 'DAT':
                label = token[0]
                value = int(token[2])

                self.symbols[label] = data_address_index
                data_address_index += 1

                self.data_values.append(value)
            
            elif token[0].endswith(":"):
                label = token[0][:-1]
                self.symbols[label] = instruction_address
                continue

            else:
                self.instructions.append(token)
                instruction_address += 1

            
    
    def generate_machine_code(self):
        machine_code = []

        for instruction in self.instructions:         
            opcode = self.opcodes[instruction[0]]

            operand = 0

            if len(instruction) > 1:
                op = instruction[1]

                if op in self.symbols:
                    operand = self.symbols[op]
                elif op.isdigit():
                    operand = int(op)
                else:
                    raise ValueError(f"Unknown operand: {op}")
            
            machine_code.append([opcode, operand])

        return machine_code
            



class VM:
    def __init__(self, input_function):
        self.input_function = input_function
        self.ram = RAM()
        self.cpu = CPU(self.ram, self.input_function)
        self.assembler = Assembler()
    
    def reset(self):
        self.ram = RAM()
        self.cpu = CPU(self.ram, self.input_function)
    
    def load(self, source):
        self.assembler.tokenise(source)
        self.assembler.generate_symbol_tree()
        code = self.assembler.generate_machine_code()

        for i, instruction in enumerate(code):
            self.ram.set_instruction(i, instruction[0], instruction[1])
        
        for i, data in enumerate(self.assembler.data_values):
            self.ram.set_data(i, data)
    
    def run(self):

        output = []

        running = True

        while running:

            if self.cpu.fetch()[0] == False:
                break
            self.cpu.decode()
            result = self.cpu.execute()
            

            if result[0] == False:
                running = False
            
            elif result[0] == True and result[1] != '':
                output.append(result[1])
        return output
        


# vm = VM()
# vm.load(""" 
#         **INSERT ASSEMBLY CODE HERE**
#         """ )

# vm.run()
