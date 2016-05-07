class Computer:
    def __init__(self):
        self.ram = RAM(1000)
        self.registers = []
        for i in xrange(10):
            register = Register(0)
            self.registers.append(register)

    def load(self, instructions):  # Into RAM
        # Skip header
        index = 0
        while index < len(instructions):
            inst = instructions[index]
            inst = inst.strip()
            if len(inst) == 1 or len(inst) == 0:
                case = instructions.pop(index)
                index -= 1
            index += 1

        for index, inst in enumerate(instructions):
            if len(inst) != 3:
                raise Exception('Encountered invalid instruction, must be 3 digits %s.' % (inst))
            self.ram.set(index, inst)

    def showRegisters(self):
        for i in xrange(len(self.registers)):
            print 'Register %d has value %d'%(i, self.registers[i].value)

    def execute(self):
        numberInstructionsExecuted = 0
        done = False
        index = 0
        while not done:
            instruction = self.ram.array[index]
            inst,mem,val = instruction  # 3 digits

            # Set of 10 possible instructions
            inst = inst.strip().lower()
            mem = int(mem)
            val= int(val)

            if inst == '1':  # Halt
                done = True
            elif inst == '2':  # Set register
                self.registers[mem].value = val %1000
            elif inst == '3':  # Add to register
                self.registers[mem].value = (self.registers[mem].value + val)%1000
            elif inst == '4':  # Multiply register
                self.registers[mem].value = (self.registers[mem].value * val)%1000

            elif inst == '5':  # Set register to register
                val = self.registers[val].value
                self.registers[mem].value = val %1000
            elif inst == '6':  # Add register to register
                val = self.registers[val].value
                self.registers[mem].value = (self.registers[mem].value + val) % 1000
            elif inst == '7':  # Multiply register to register
                val = self.registers[val].value
                self.registers[mem].value = (self.registers[mem].value * val) % 1000

            elif inst == '8':  # Set register to value in RAM
                ramAddress = self.registers[val].value
                val = int(self.ram.array[ramAddress])
                self.registers[mem].value = val %1000
            elif inst == '9':  # Set RAM to register value
                ramAddress = self.registers[val].value
                val = self.registers[mem].value %1000
                self.ram.array[ramAddress] = str(val)
            elif inst == '0':
                val = self.registers[val].value
                if val != 0:
                    val = self.registers[mem].value
                    index = val-1
            else:
                raise Exception('Invalid instruction %s'%(inst))
            index += 1
            numberInstructionsExecuted += 1
        # End-while
        print numberInstructionsExecuted

class Register:
    def __init__(self, value=0):
        self.value = value

class RAM:
    def __init__(self, size):
        self.array = []
        for i in xrange(size):
            # NB: String is not mutable, so will be inefficiently replaced
            self.array.append('000')  # 3 char

    def set(self, index, inst):
        self.array[index] = inst

    def show(self):
        for i,inst in enumerate(self.array):
            #if i >= self.size:
            #    break
            print inst


if __name__ == '__main__':

    instructions = [
        '1',
        '',
        '299',
        '492',
        '495',
        '399',
        '492',
        '495',
        '399',
        '283',
        '279',
        '689',
        '078',
        '100',
        '000',
        '000',
        '000'
    ]

    computer = Computer()
    computer.load(instructions)
    computer.execute()
