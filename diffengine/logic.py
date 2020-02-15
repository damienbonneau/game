"""
Communication modules for implement various encoding and decoding schemes

Compute energy consumption per bit, 
    each instruction used requires one unit of energy

cost, 
    based on performance of memory, 
    number of lines of instruction
    register size
    number of steps
    energy used


Protocols with bidirectional communication e.g 
    parity encoding with resend option 
    using redundant encoding 
    
Communication protocols using:
    Hadamard Code
    Binary Golay Code
    Turbo Code

Components:
    mini CPU, one input, one output, one register
    

Make building blocks:
    Interleaver
    convolutionnal code
    
Connect multiple machines in networks with noisy channels
have input buffers with finite size which can fill up -> requires larger buffer, 
    multiple channels, 
    or better encoders / decoders

Get monetary return based on information exchanged on channels and trust in the channels

Remote software deployment
Reverse engineering existing designs
Compression
Communication protocols
Encryption
Hacking


"""
from random import randint
import sys
NO_DATA = 1

VALID_SYNTAX = 0
INVALID_OPERATOR = 2
INVALID_OPERAND = 3
INVALID_NUM_OPERANDS = 4

def _print(*a, **kw):
    print(*a, **kw)
    sys.stdout.flush()

def bit_copy(register, source, dest):
    register[dest] = register[source]

def bit_flip(register, address):
    register[address] = 0 if register[address] else 1
    _print ('BFLP', register)

def bit_xor(register, src1, src2):  
    """
    in place bit xor
    """
    register[src2] = (register[src1] + register[src2]) % 2
    
def rshift(r):
    r[:] = [r[-1]] + r[:-1]

def lshift(r):
    r[:] = r[1:] + [r[0]]
    
def xor(registerA, registerB):
    """
    Applies xor between register A and register B.
    Stores the result in register B
    """
    registerB[:] = [(i + j) % 2 for i, j in zip(registerA, registerB)]
    
def cp_register(reg_source, reg_dest):
    reg_dest[:] = reg_source[:]
    
    
def _reg_to_int(reg):
    _reg = reg[:]
    _reg.reverse()
    return  int( "0b" + "".join(_ref) )
    
def _int_to_reg(a, size=8):
    s = bin(a)[2:]
    reg = [0] * size
    s.reverse()
    for i, c in enumerate(s):
        reg[i] = int(c)
    
    return reg
    
def add(reg_source, reg_dest):
    """
    addition between the two registers, stores the result in dest
    """
    
    n = len(reg_source)
    if n != len(reg_dest):
        raise ValueError("Register sizes should be equal")
       
    a = _reg_to_int(reg_source)
    b = _reg_to_int(_reg_dest)
    maxv = 2 ** n
    
    c = (a + b) % maxv
    reg_dest[:] = _int_to_reg(c)
    
def push_reg_to_ram(reg, ram, address):
    ram[address] = _reg_to_int(reg)

def pull_reg_from_ram(reg, ram, address):
    reg[:] = _int_to_reg(ram[address])


class Stream():
    def __init__(self):
        self.data = []
        
    def send(self, x):
        self.data.insert(0, x)
    
    def receive(self):
        return self.data.pop()
        
    def tick(self):
        pass

class RandomSource():
    def __init__(self, output_stream):
        self.output_stream = output_stream
     
    def tick(self):
        self.output_stream.send(randint(0, 1))
        
class Logger():
    def __init__(self, input_stream):
        self.input_stream = input_stream
        self.log = []
        
    def tick(self):
        if input_stream:
            self.log += input_stream
            input_stream.clear()
    
class Processor():
    """
    Composed of:
        - a register
        - a buffer having same size as register
        - An internal random access memory 
        - An instruction set
        - A memory to store the program
        
        Information is stored in binary in the registers
        Each memory slot can store a full integer between 0 and 2**register_size - 1
        
    """
    
    def __init__(self, register_size=16, memory_size=32, program_stack_size=16):
        self.register = [0] * register_size   # 0 / 1
        self.buffer = [0] * register_size   # 0 / 1
        self.ram = [0] * memory_size # 0 to 255 per slot
        self.program = [""] * program_stack_size
        self.program_stack_size = program_stack_size
        self.register_size = register_size
        self.stack_pointer = 0 # point to the instruction to execute in the program
        
        self.dict_operations = {
            "READ": self.read,
            "SEND": self.send,
            "SWAP": self.swap_reg, 
            "ADD": lambda :add(self.buffer, self.register),
            "RST": self.reset_reg,
            "SAVE": self.save_to_ram,
            "LOAD": self.load_from_ram,
            "BCPY": lambda src, dest: bit_copy(self.register, src, dest),
            "BFLP": lambda addr: bit_flip(self.register, addr),
            "BXOR": lambda src, dest: bit_copy(self.register, src, dest),
            "BRM": self.branch_msb,
            "BRL": self.branch_lsb,
            "RSH": lambda :rshift(self.register),
            "LSH": lambda :lshift(self.register),
        }
        
        self.dict_num_operands = {
            "READ": [0, 1],
            "SEND": [0, 1],
            "SWAP": [0], 
            "ADD": [0],
            "RST": [0],
            "SAVE": [1],
            "LOAD": [1],
            "BCPY": [2],
            "BFLP": [1],
            "BXOR": [2],
            "BRM": [1],
            "BRL": [1],
            "RSH": [0],
            "LSH": [0],
        }
        
    def branch_msb(self, stack_index):
        if self.register[-1]:
            self.stack_pointer = stack_index
            
    def branch_lsb(self, stack_index):
        if self.register[0]:
            self.stack_pointer = stack_index
        
    def swap_reg(self):
        b = self.buffer 
        self.buffer[:] = self.register[:]
        self.register[:] = b
        
    def connect_input(self, input_stream):
        self.input_stream = input_stream
        
    def connect_output(self, output_stream):
        self.output_stream = output_stream
        
    def load_from_ram(self, i):
        self.buffer[:] = _int_to_reg(self.ram[i])
        
    def save_to_ram(self, i):
        self.ram[i] = _reg_to_int(self.buffer)
        
    def set_prog_line(self, i, instruction):
        self.program[i] = instruction
        
    def read(self, size=1):
        """
        size from 0 up to input register size
        1 - read as many bits as size
        2 - store them in the register (with the first read being the LSB)

        [LSB, ..., MSB] <- the register stores the bits backwards to help with the inner machinery
        
        """
        if len(input_stream.data) < size:
            return NO_DATA
            
        i = 0
        while i < size:        
            self.register[i] = input_stream.receive()
            i += 1
        
        return 0
        
    def send(self, size=None):
        """
        send the full output_register
        """
        
        """
        send from LSB (least significant) to MSB 
        """
        
        if size is None:
            size = len(self.register)
        for i in range(size):
            self.output_stream.send(self.register[i])
    
    def reset_reg(self):
        self.register[:] = [0] * self.register_size
    
    def check_instruction_syntax(self, instruction_line):
        if not instruction_line:
            return VALID_SYNTAX
            
        splitted = instruction_line.replace('\n','').strip().split(' ')
        
        splitted = [_x for _x in splitted if len(_x)>0]
        
        if len(splitted) == 0:
            return VALID_SYNTAX
            
        operator = splitted[0]
        if operator not in self.dict_operations:
            return INVALID_OPERATOR
            
        arguments = splitted[1:]
        n_args = len(arguments) 
        if n_args not in self.dict_num_operands[operator]:
            return INVALID_NUM_OPERANDS
        
        for arg in arguments:
            try:
                int(arg)
            except:
                if arg != 'BUF': 
                    return INVALID_OPERAND
                
        return VALID_SYNTAX
    
    def execute_instruction(self, instruction_line):
        """
        One instruction per line
        When the last line is done, the program loops back to the first line
        
        # I/O
        READ <size in bits> - blocking read
        SEND <size in bits>
        
        # Register manipulation
        SWAP : swap content of register and buffer
        ADD: add buffer and register values, store result in register
        RESET: reset register to 0
        RSHIFT
        LSHIFT
        
        # For units having RAM
        SAVE <memory_address>: copy buffer content to memory block
        LOAD <memory_address>: load memory block to buffer
        
        # Bitwise operations
        in all bit operations, src and dest are an integer having representing the bit weight
        
        BITCOPY <src> <dest>
        BITFLIP <src>
        BITXOR <src> <dest>        
        
        # Branching
        BRCHMSB <program stack line index> - branch to program stack line if the most significant bit of the register is set to 1
        BRCHLSB <program stack line index> - branch to program stack line if the least significant bit of the register is set to 1
        BUF keyword can be used in place of any integer arguments. This takes the value in the buffer
        
        """
        
        if not instruction_line:
            return
        
        splitted = instruction_line.replace('\n','').split(' ')
        operator = splitted[0]
        
        arguments = [int(x) if x != 'BUF' else _reg_to_int(self.buffer) for x in splitted[1:]]                        
        f = self.dict_operations[operator]
        return f(*arguments)
   
    def is_valid_instruction(self, line):
        return self.check_instruction_syntax(line)==VALID_SYNTAX
   
    def tick(self):
        line = self.program[self.stack_pointer]
        _print(self.stack_pointer, line, self.is_valid_instruction(line))
        if self.is_valid_instruction(line):
            res = self.execute_instruction(line)
            if res in [None, 0]:
                self.stack_pointer += 1
        
        else:
            self.stack_pointer += 1
        
        if self.stack_pointer >= len(self.program):
            self.stack_pointer = 0

