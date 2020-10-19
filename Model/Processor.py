import time

import numpy as np
from Model.Instruction import *
import matplotlib.pyplot as plt

from Model.MemoryRequest import MemoryRequest, RequestTypes


class Processor:

    def __init__(self, identifier, clock_frequency, memory_blocks=16, snooper=None):
        self.identifier = identifier
        self.clock_frequency = clock_frequency
        self.instructions = []
        self.memory_blocks = memory_blocks
        self.snooper = snooper
        self.busy = False
        self.cycles = 0

    def __str__(self):
        return self.identifier

    def set_next(self, instruction):

        try:
            parts = instruction.split()
            if parts[1] == "READ":
                self.instructions[0].mem_address = int(parts[2], 2)
                self.instructions[0].instruction_type = InstructionTypes.READ
            elif parts[1] == "WRITE":
                self.instructions[0].mem_address = int(parts[2], 2)
                self.instructions[0].mem_data = int(parts[3], 16)
                self.instructions[0].instruction_type = InstructionTypes.WRITE
            else:
                self.instructions[0].instruction_type = InstructionTypes.CALC
        except IndexError:
            print("Wrong format")

    def load_instructions(self, amount):
        sigma = 1
        distribution = np.random.normal(0, sigma, amount)
        # plt.hist(distribution, 30, density=True)
        # plt.show()
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
        # distribution = np.random.poisson(_lambda, rw_instructions)
        # plt.hist(distribution, self.memory_blocks, density=True)
        plt.show()
        minx = min(distribution)
        max_x = max(distribution)
        step = (max_x - minx) / self.memory_blocks
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

    def execute(self):
        while True:
            time.sleep(1)
            if self.cycles != 0:
                self.step_execute()
                self.cycles -= 1

    def step_execute(self):
        instruction = self.instructions[0]
        request = MemoryRequest()
        if instruction.instruction_type == InstructionTypes.CALC:
            self.instructions.pop(0)
            self.busy = False
            return
        elif instruction.instruction_type == InstructionTypes.WRITE:
            request.type = RequestTypes.PROCESSOR_WRITE
        elif instruction.instruction_type == InstructionTypes.READ:
            request.type = RequestTypes.PROCESSOR_READ
        request.address = instruction.mem_address
        request.data = instruction.mem_data
        self.busy = True
        self.snooper.process(request)
        self.busy = False
        self.instructions.pop(0)
