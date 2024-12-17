import re

with open('input') as infile:
    content = infile.read()
    registers, program = content.split('\n\n')
    registers = [int(re.findall(r'(\d+)', line)[0]) for line in registers.strip().split('\n')]
    program = [int(p) for p in program.strip().removeprefix('Program: ').split(',')]

def combo(val, registers):
    if val <= 3:
        return val
    elif val <= 6:
        return registers[val - 4]
    else:
        print(f"invalid combo {val}")
        1/0

A = 0
B = 1
C = 2

def run(program, registers):
    output = []
    ip = 0
    while True:
        if ip not in range(len(program)):
            break
        instruction = program[ip]
        arg = program[ip + 1]
        if instruction == 0:
            registers[A] = registers[A] // 2**combo(arg, registers)
        elif instruction == 1:
            registers[B] = registers[B] ^ arg
        elif instruction == 2:
            registers[B] = combo(arg, registers) % 8
        elif instruction == 3:
            if registers[A] != 0:
                ip = arg
                continue
        elif instruction == 4:
            registers[B] = registers[B] ^ registers[C]
        elif instruction == 5:
            output.append(combo(arg, registers) % 8)
        elif instruction == 6:
            registers[B] = registers[A] // 2**combo(arg, registers)
        elif instruction == 7:
            registers[C] = registers[A] // 2**combo(arg, registers)
        ip += 2
    return output

print(','.join(str(c) for c in run(program, registers)))

ipt = []

def find_all_with_input_so_far(input_so_far, program):
    for i in range(8):
        ipt = [i] + input_so_far
        joined = sum(v << 3*idx for idx, v in enumerate(ipt) )
        output = run(program, [joined, 0, 0])
        if output == program[-len(output):]:
            yield i

def recurse(ipt, program):
    joined = sum(v << 3*idx for idx, v in enumerate(ipt) )
    output = run(program, [joined, 0, 0])
    if output == program:
        return joined
    for possible_prepend in find_all_with_input_so_far(ipt, program):
        result = recurse([possible_prepend] + ipt, program)
        if result is not None:
            return result

print(recurse([], program))
