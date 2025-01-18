from dataclasses import dataclass
from collections import deque
import operator


@dataclass
class Wire:
    symbol: str
    value: int=None


@dataclass
class Operator:
    symbol: str
    input_wire_a: Wire
    input_wire_b: Wire
    output_wire: Wire

    symbol_to_operator = {
        'AND': operator.and_,
        'OR': operator.or_,
        'XOR': operator.xor
    }

    def executable(self):
        return None not in {self.input_wire_a.value, self.input_wire_b.value}

    def execute(self):
        op = self.symbol_to_operator[self.symbol]

        if self.executable():
            self.output_wire.value = op(
                self.input_wire_a.value,
                self.input_wire_b.value
            )


with open('input.txt') as f:
    data = f.read()

starting_data, operations_data = data.split('\n\n')

starting_data = starting_data.splitlines()
operations_data = operations_data.splitlines()

wires = {}
operators = deque()

for line in starting_data:
    symbol, value = line.split(': ')

    wires[symbol] = Wire(symbol=symbol, value=int(value))

for line in operations_data:
    op, output_wire_symbol = line.split(' -> ')
    operand_a, operator, operand_b = op.split(' ')

    if operand_a not in wires:
        wires[operand_a] = Wire(symbol=operand_a)

    if operand_b not in wires:
        wires[operand_b] = Wire(symbol=operand_b)

    if output_wire_symbol not in wires:
        wires[output_wire_symbol] = Wire(symbol=output_wire_symbol)

    operator = Operator(
        input_wire_a=wires[operand_a],
        symbol=operator,
        input_wire_b=wires[operand_b],
        output_wire=wires[output_wire_symbol]
    )

    operators.append(operator)

while operators:
    operation = operators.popleft()

    if operation.executable():
        operation.execute()
    else:
        operators.append(operation)

result = sorted([(w.symbol, str(w.value)) for w in wires.values() if w.symbol.startswith('z')], reverse=True)
result = ''.join(item[1] for item in result)

print(int(result, base=2))
