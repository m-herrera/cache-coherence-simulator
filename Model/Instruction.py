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

    def get_data_str(self):
        return '0x' + '{:04x}'.format(self.mem_data).upper()

    def get_address_str(self):
        return '{:04b}'.format(self.mem_address)

    def __str__(self):
        representation = self.parent + ": " + self.instruction_type.name
        if self.instruction_type != InstructionTypes.CALC:
            representation += " " + self.get_address_str()
            if self.instruction_type == InstructionTypes.WRITE:
                representation += " " + self.get_data_str()
        return representation

    def set_instruction_type(self, instruction_type):
        self.instruction_type = instruction_type
