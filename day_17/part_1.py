import re


def sliding_window(iterable, n=2):
    from itertools import islice

    args = [islice(iter(iterable), i, None) for i in range(n)]
    return zip(*args)


def combo(memory, operand):
    if operand in range(4):
        return operand
    
    if operand == 4:
        return memory['A']

    if operand == 5:
        return memory['B']

    if operand == 6:
        return memory['C']
    
    raise 'Unexpected combo operand'


def adv(memory, operand):
    memory['A'] >>= combo(memory, operand)


def bxl(memory, operand):
    memory['B'] ^= operand


def bst(memory, operand):
    memory['B'] = combo(memory, operand) % 8


def jnz(memory, operand):
    if memory['A'] == 0:
        return

    return operand
   

def bxc(memory, _operand):
    memory['B'] ^= memory['C']


def out(memory, operand):
    memory['out'].append(combo(memory, operand) % 8)


def bdv(memory, operand):
    memory['B'] = memory['A'] >> combo(memory, operand)


def cdv(memory, operand):
    memory['C'] = memory['A'] >> combo(memory, operand)


def run(memory, program):
    opcode_function = {
        0: adv,
        1: bxl,
        2: bst,
        3: jnz,
        4: bxc,
        5: out,
        6: bdv,
        7: cdv,
    }

    exec_pointer = 0

    while exec_pointer in range(len(program) - 1):
        opcode, operand = program[exec_pointer], program[exec_pointer + 1]

        try:    
            exec_pointer_jump = opcode_function[opcode](memory, operand)
        except:
            print(f'{exec_pointer}=exec_pointer')
            print(f'{len(program)}=len(program)')
            print(f'{opcode}=opcode')
            print(f'{operand}=operand')

            raise
        
        if exec_pointer_jump is not None:
            exec_pointer = exec_pointer_jump
        else:
            exec_pointer += 2


with open('input.txt') as f:
    data = f.read()

    memory_data, program_data = data.split('\n\n')

    memory_data = memory_data.splitlines()
    program_data = program_data.strip('Program: ')

memory = {}

regex = re.compile(r'(\w): (\d+)')

for line in memory_data:
    [(register, data)] = regex.findall(line)
    memory[register] = int(data)

memory['out'] = []
program = [int(c) for c in program_data.split(',')]

run(memory, program)

print(','.join(str(i) for i in memory['out']))