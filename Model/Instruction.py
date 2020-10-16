from enum import Enum


class InstructionTypes(Enum):
    CALC = 1
    READ = 2
    WRITE = 3


class Instruction:
    def __init__(self, parent, instruction_type=InstructionTypes.CALC, mem_address=0b0000, mem_data=0x0000):
        self.instruction_type = instruction_type
        self.parent = parent
        self.mem_address = mem_address
        self.mem_data = mem_data

    def __str__(self):
        representation = self.parent + " " + self.instruction_type.name
        if self.instruction_type != InstructionTypes.CALC:
            representation += " " + str(self.mem_address)
        return representation

    def set_instruction_type(self, instruction_type):
        self.instruction_type = instruction_type
