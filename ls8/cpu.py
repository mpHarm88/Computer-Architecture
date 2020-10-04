"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0]*256
        self.reg = [0]*8
        self.pc = 0

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1
    
    def ram_read(self, address):
        # Return the value stored at the address
        return self.ram[address]

    def ram_write(self, address, value):
        # Write the value to the inputted address
        for x in range(len(self.ram)):
            if self.ram[x] == address:
                self.ram[x] = value
                print(f"Value: {value}\nSaved at {address} in ram")

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        # Instruction Register
        inst_reg = list()

        while self.ram[self.pc] != 0:

            # If ram_read returns the LDI command then save the results to the appropriate register
            if self.ram_read(self.pc) == LDI:
                # register address location
                opperand_a = int(f"{(self.ram[self.pc+1])}")

                # value to be saved
                opperand_b = int(f"{(self.ram[self.pc+2])}")

                # Assign value to address in register
                self.reg[opperand_a] = opperand_b

                # store result in instruction register
                inst_reg.append(opperand_b)

                # Increment pc by 3
                self.pc+=3
            
            # print the value
            elif self.ram_read(self.pc) == PRN:
                # Store idx location
                reg_idx = int(f"{(self.ram[self.pc+1])}")

                #print the value
                print(self.reg[reg_idx])

                # append the result to instruction register
                inst_reg.append(self.reg[reg_idx])

                # Increment pc by 2
                self.pc+=2

            # Exit the program if HLT byte code appears
            elif self.ram_read(self.pc) == HLT:
                break