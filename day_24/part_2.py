from dataclasses import dataclass


@dataclass
class Operator:
    symbol: str
    input_wire_a: str
    input_wire_b: str
    output_wire: str


class Xor(Operator):
    def is_valid(self, operations):
        is_not_or_input = self.output_wire not in operations['OR']['inputs']
        is_x_y_input = self.input_wire_a[0] in {'x', 'y'} and self.input_wire_b[0] in {'x', 'y'}
        is_output_z = self.output_wire.startswith('z')

        inputs = {self.input_wire_a, self.input_wire_b}

        if 'x00' in inputs and 'y00' in inputs:
            return is_not_or_input and is_output_z

        return is_not_or_input and (is_x_y_input ^ is_output_z)


class Or(Operator):
    def is_valid(self, _operations):
        return self.output_wire == 'z45' or not self.output_wire.startswith('z')


class And(Operator):
    def is_valid(self, operations):
        is_or_input = self.output_wire in operations['OR']['inputs']
        is_not_output_z = not self.output_wire.startswith('z')

        if 'x00' in {self.input_wire_a, self.input_wire_b}:
            return is_not_output_z and not is_or_input

        return is_not_output_z and is_or_input


with open('input.txt') as f:
    data = f.read()

_, operations_data = data.split('\n\n')

operations_data = operations_data.splitlines()

wires = {}
operators = []

operations = {
    'AND': {'inputs': set(), 'outputs': set()},
    'OR': {'inputs': set(), 'outputs': set()},
    'XOR': {'inputs': set(), 'outputs': set()}
}

op_to_cls = {
    'XOR': Xor,
    'OR': Or,
    'AND': And
}

for line in operations_data:
    op, output_wire = line.split(' -> ')
    operand_a, operator, operand_b = op.split(' ')

    operations[operator]['inputs'].add(operand_a)
    operations[operator]['inputs'].add(operand_b)
    operations[operator]['outputs'].add(output_wire)

    operator = op_to_cls[operator](
        input_wire_a=operand_a,
        symbol=operator,
        input_wire_b=operand_b,
        output_wire=output_wire
    )

    operators.append(operator)

wrong_gates = set()

for operator in operators:
    if not operator.is_valid(operations):
        wrong_gates.add(operator.output_wire)

gates = sorted(wrong_gates)
print(','.join(gates))
