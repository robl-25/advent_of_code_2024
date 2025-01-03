import re
from copy import deepcopy
from itertools import product


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


def run(memory, program, num_out=None):
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
        exec_pointer_jump = opcode_function[opcode](memory, operand)

        if exec_pointer_jump is not None:
            exec_pointer = exec_pointer_jump
        else:
            exec_pointer += 2

        if num_out and num_out == len(memory['out']):
            return


def bits_to_int(bits):
    return int(''.join(str(bit) for bit in bits).ljust(64, '0'), base=2)


def int_to_bits(num):
    return tuple(int(i) for i in bin(num)[2:])


def guess_value(bits, program, step):
    if step < 0:
        return bits

    for new_bits in product([0, 1], [0, 1], [0, 1], [0, 1]):
        a =  bits_to_int(bits + new_bits)
        memory = {'A': a, 'B': 0, 'C': 0, 'out': []}
        
        run(memory, program)

        if program[step] == memory['out'][-1 * (len(program) - step)]:
            attempt = guess_value(bits + new_bits, program, step - 1)

            if attempt:
                return attempt


with open('input.txt') as f:
    data = f.read()

program_data = data.split('\n\n')[1].strip('Program: ')
program = [int(c) for c in program_data.split(',')]

bits = ''.join(str(i) for i in guess_value((), program, 15)).rstrip('0')
print(int(bits, base=2))
