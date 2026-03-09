import unittest

from src.common.circuit import Circuit, Gate, build_circuit_from_patterns, evaluate_circuit, render_circuit


class CircuitTestCase(unittest.TestCase):
    def test_build_circuit_constant_zero(self) -> None:
        circuit = build_circuit_from_patterns("F", ("A", "B"), ())
        self.assertEqual(circuit.output_source, "0")
        self.assertEqual(circuit.gates, tuple())

    def test_build_circuit_constant_one(self) -> None:
        circuit = build_circuit_from_patterns("F", ("A", "B"), ("--",))
        self.assertEqual(circuit.output_source, "1")
        self.assertEqual(circuit.gates, tuple())

    def test_build_circuit_with_or_gate(self) -> None:
        circuit = build_circuit_from_patterns("F", ("A", "B"), ("1-", "-1"))
        gate_types = [gate.gate_type for gate in circuit.gates]
        self.assertEqual(gate_types.count("OR"), 1)
        self.assertEqual(circuit.output_source, "F")

    def test_build_circuit_with_not_and_and(self) -> None:
        circuit = build_circuit_from_patterns("F", ("A", "B"), ("01",))
        gate_types = {gate.gate_type for gate in circuit.gates}
        self.assertIn("NOT", gate_types)
        self.assertIn("AND", gate_types)
        rendered = render_circuit(circuit)
        self.assertIn("F = t1", rendered)

    def test_evaluate_circuit_supports_xor(self) -> None:
        circuit = Circuit(
            output_name="F",
            output_source="xor1",
            gates=(
                Gate(name="XOR1", gate_type="XOR", inputs=("A", "B"), output="xor1"),
            ),
        )
        self.assertEqual(evaluate_circuit(circuit, {"A": 0, "B": 0}), 0)
        self.assertEqual(evaluate_circuit(circuit, {"A": 0, "B": 1}), 1)
        self.assertEqual(evaluate_circuit(circuit, {"A": 1, "B": 0}), 1)
        self.assertEqual(evaluate_circuit(circuit, {"A": 1, "B": 1}), 0)


if __name__ == "__main__":
    unittest.main()
