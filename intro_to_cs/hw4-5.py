program_counter = [0]   # to accomplish pass by reference

# This function adds given line to given memory address
# Example: (25 03, 0)
def add_memory(line, addr):
    first_byte = line[:2]               # 25
    second_byte = line[3:]              # 03

    memory[addr] = first_byte           # memory[0] = 25
    memory[addr + 1] = second_byte      # memory[0+1] = 03


def fetch():
    # value should be like 25
    value = memory[program_counter[0]]  # equal with value=memory[program_counter]

    # we need to parse all parts
    op_code = value[:1]                 # op-code is the first char
    operand = value[1:]                 # read from given memory cell (e.q. 5)
    operand += memory[program_counter[0] + 1]  # read from next memory cell (e.q. 5+03)

    if op_code == '1':
        one_rxy(operand)
    if op_code == '2':
        two_rxy(operand)
    if op_code == '3':
        three_rxy(operand)
    if op_code == '4':
        four_0rs(operand)
    if op_code == '5':
        five_rst(operand)
    if op_code == '7' or op_code == '8' or op_code == '9':
        bitwise_rst(operand, op_code)
    if op_code == 'A':
        a_r0x(operand)
    if op_code == 'B':
        b_rxy(operand)
    if op_code == 'C':
        return False


# LOAD the register R with the bit pattern found in the memory cell whose address is XY
# e.q operand = 4A3
def one_rxy(operand):
    r = operand[:1]                     # register 4
    xy = operand[1:]                    # address A3
    content = memory[int(xy, 16)]       # content = memory[A3]
    registers[r] = content              # register[4] = content


# LOAD the register R with the bit pattern XY
# e.q. operand = 0A3
def two_rxy(operand):
    r = operand[:1]                     # register 0
    xy = operand[1:]                    # xy = A3
    registers[r] = xy                   # register[0] = A3


# STORE the bit pattern found in register R in the memory cell whose address is XY
# e.q. operand = 5B1
def three_rxy(operand):
    r = operand[:1]                     # register 5
    xy = operand[1:]                    # xy = B1
    content = registers[r]              # content = register[5]
    memory[int(xy, 16)] = content       # memory[B1] = content


# MOVE the bit pattern found in register R to register S
# e.q. operand = 0A4
def four_0rs(operand):
    r = operand[-2:-1]                  # register A
    s = operand[-1]                     # register 4
    content = registers[r]              # content = register[A]
    registers[s] = content              # register[4] = content


# ADD the bit patterns in registers S and T as though they were two’s complement representations
# and leave the result in register R
# e.q. operand = 726
def five_rst(operand):
    r = operand[:1]                     # register 7
    s = operand[1:2]                    # register 2
    t = operand[-1]                     # register 6
    content_s = registers[s]            # content_s = register[2]
    content_t = registers[t]            # content_t = register[6]

    # [2:] for getting rid of '0x' prefix and overflow
    # need to use upper() because i have register 'A', not 'a'
    # need to use zfill(2) because we have to store like 03, not just 3
    registers[r] = hex(int(content_s, 16)+int(content_t, 16))[2:].upper().zfill(2)


# I merged these 3 operations because they're very similar.
def bitwise_rst(operand, operator):
    r = operand[:1]
    s = operand[1:2]
    t = operand[-1]

    content_s = int(bin(int(registers[s], 16)), 2)
    content_t = int(bin(int(registers[t], 16)), 2)
    if operator == '7':
        value = bin(content_t | content_s)      # OR operation
    if operator == '8':
        value = bin(content_t & content_s)      # AND operation
    if operator == '9':
        value = bin(content_t ^ content_s)      # XOR operation

    # [2:] for getting rid of '0x' prefix
    # need to use upper() because we have to store like 0A, not 0a
    # need to use zfill(2) because we have to store like 03, not just 3
    content = hex(int(value, 2))[2:].upper().zfill(2)
    registers[r] = content


# ROTATE the bit pattern in register R one bit to the right X times
def a_r0x(operand):
    r = operand[:1]                 # register r
    x = int(operand[-1])            # rotate n times

    # for example, registers[r] has 02 value
    # first, we need to convert 02 to binary (10)
    # then, convert it to 8 bit (00000010)
    content = bin(int(registers[r], 16))[2:].zfill(8)

    # enter the loop x times
    for i in range(0, x):
        # take the right most bit and concat with rest
        content = content[-1] + content[:-1]

    # convert it to hexadecimal, and use [2:] for getting rid of 0x prefix
    content = hex(int(content, 2))[2:].upper()
    registers[r] = content


# JUMP to the instruction located in the memory cell at address XY...
def b_rxy(operand):
    r = operand[:1]
    xy = operand[1:]

    cond1 = registers[r]                # take the value in given register
    cond2 = registers['0']              # take the value in register 0
    if cond1 == cond2:                  # compare them. If they're equal, than jump
        #program_counter[0] = int(bin(int(xy, 16)), 2)

        # assign xy to program counter
        # decrease 2 from counter because after this function
        # end, program counter will increase 2 in 'fetch'
        # so, if i don't decrease, then counter will point to xy+2 address
        program_counter[0] = int(bin(int(xy, 16)), 2)-2

############################################
############################################

memory = {}
memory_size = 0
registers = {'0': '00', '1': '00', '2': '00', '3': '00',
             '4': '00', '5': '00', '6': '00', '7': '00',
             '8': '00', '9': '00', 'A': '00', 'B': '00',
             'C': '00', 'D': '00', 'E': '00', 'F': '00'}


# Read file line by line
with open('input.txt') as file:
    for line in file:
        # Add each line to memory
        add_memory(line[:5], memory_size)   # [:-1] to get rid of newline character
        memory_size += 2                    # each line is 2 memory cell length
    file.close()


# Until op-code is C, keep fetch & execute process
# and increase program counter
while fetch() != False:
    program_counter[0] += 2


# For printing registers 0 to 15
for i in range(0, 16):
    if i != 0 and i % 4 == 0:
        print()
    print(end='R'+str(i).ljust(2)+': '+str(registers[hex(i)[2:].upper()])+'   ')


# print([[k, v] for k, v in registers.items() if v != '00'])

