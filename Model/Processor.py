import numpy as np
from Model.Instruction import *
import matplotlib.pyplot as plt


class Processor:

    def __init__(self, identifier, clock_frequency, memory_blocks=16):
        self.identifier = identifier
        self.clock_frequency = clock_frequency
        self.instructions = []
        self.memory_blocks = memory_blocks

    def __str__(self):
        return self.identifier

    def load_instructions(self, amount):
        sigma = 1
        distribution = np.random.normal(0, sigma, amount)
        plt.hist(distribution, 30, density=True)
        plt.show()
        rw_instructions = 0
        for point in distribution:
            instruction = Instruction(self.identifier)  # default instruction type is CALC
            if point < -sigma:
                rw_instructions += 1
                instruction.set_instruction_type(InstructionTypes.READ)
            elif sigma < point:
                rw_instructions += 1
                instruction.set_instruction_type(InstructionTypes.WRITE)
                instruction.mem_data = np.random.randint(0, 65536)  # 0xFFFF + 1
            self.instructions.append(instruction)

        _lambda = 16
        distribution = np.random.poisson(_lambda, rw_instructions)
        plt.hist(distribution, self.memory_blocks, density=True)
        plt.show()
        minx = min(distribution)
        maxx = max(distribution)
        step = (maxx - minx) / self.memory_blocks
        i = 0
        for instruction in self.instructions:
            if instruction.instruction_type != InstructionTypes.CALC:
                point = distribution[i]
                threshold = step + minx
                address = 0
                while point > threshold:
                    threshold += step
                    address += 1
                instruction.mem_address = address
                i += 1
