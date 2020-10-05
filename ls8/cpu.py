"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0]*256
        self.reg = [0]*12
        self.pc = 0

    def load(self):

        # Address location in RAM
        address = 0

        # If length of args is less than 2 then return print statement
        if len(sys.argv) < 2:
            print(f"Please enter an additional argument\nCurrent Args: {sys.argv[0]}")
        
        # Open file and filter out lack and commented lines
        else:
            with open(sys.argv[1], "r") as f:
                for x in f:
                    # Skip the line if it starts with "#" or length of stripped line == 0
                    if x[0] == "#" or len(x.rstrip()) == 0:
                        continue

                    # Add line to RAM at current address
                    else:
                        val = bin(int(x.split()[0], 2))
                        # Save to ram and increment address
                        self.ram[address] = val
                        address+=1
            f.close()

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

        elif op == "MUL": 
            self.reg[reg_a] *= self.reg[reg_b]
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
            if int(self.ram_read(self.pc), 2) == LDI:

                # register address location
                opperand_a = int(self.ram[self.pc+1], 2)

                # value to be saved
                opperand_b = int(self.ram[self.pc+2], 2)

                # Assign value to address in register
                self.reg[opperand_a] = opperand_b

                # store result in instruction register
                inst_reg.append(opperand_b)

                # Increment pc by 3
                self.pc+=3
            
            # print the value
            elif int(self.ram_read(self.pc),2) == PRN:
                # Store idx location
                reg_idx = int(self.ram[self.pc+1], 2)

                #print the value
                print(self.reg[reg_idx])

                # append the result to instruction register
                inst_reg.append(self.reg[reg_idx])

                # Increment pc by 2
                self.pc+=2
            
            # Multiply 
            elif int(self.ram_read(self.pc), 2) == MUL:

                # Find index location of numbers to be multiplied
                reg1 = int(self.ram[self.pc+1],2)
                reg2 = int(self.ram[self.pc+2],2)

                # Passinto alu for processing
                self.alu("MUL", reg1, reg2)

                # Increment pc by 3
                self.pc+=3

            # Exit the program if HLT byte code appears
            elif int(self.ram_read(self.pc),2) == HLT:
                break