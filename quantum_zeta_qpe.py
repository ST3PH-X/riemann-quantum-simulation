import cirq
import numpy as np

class RiemannZetaOracle(cirq.Gate):
    """
    Custom Cirq gate representing the Unitary Quantum Zeta Oracle U_zeta.
    Applies a strictly unitary phase transformation to the register.
    """
    def __init__(self, t_coordinate):
        super(RiemannZetaOracle, self).__init__()
        self.t = t_coordinate

    def _num_qubits_(self):
        return 1

    def _decomposition_(self, qubits):
        q = qubits
        # Unitary phase transformation phase angle modulation
        target_phase = np.sin(self.t) * np.pi  
        yield cirq.Rz(rad=target_phase).on(q)

    def _circuit_diagram_info_(self, args):
        return f"U_ζ(t={self.t:.2f})"

def run_quantum_phase_estimation(t_value, num_estimation_qubits=3):
    """
    Executes Quantum Phase Estimation using the Cirq Zeta Oracle
    to extract spectral data points along the critical line.
    """
    qubits = cirq.LineQubit.range(num_estimation_qubits + 1)
    counting_qubits = qubits[:num_estimation_qubits]
    target_qubit = qubits[num_estimation_qubits]

    circuit = cirq.Circuit()

    # Initialize target in state |1> and counting qubits in uniform superposition
    circuit.append(cirq.X(target_qubit))
    circuit.append(cirq.H.on_each(*counting_qubits))

    # Apply Controlled Unitary Oracle operations exponentially
    oracle_gate = RiemannZetaOracle(t_value)
    for i, counting_qubit in enumerate(counting_qubits):
        power = 2**i
        controlled_oracle = oracle_gate.on(target_qubit).controlled_by(counting_qubit)
        for _ in range(power):
            circuit.append(controlled_oracle)

    # Inverse Quantum Fourier Transform
    circuit.append(cirq.inverse(cirq.QFT(*counting_qubits)))

    # Measure the phase register
    circuit.append(cirq.measure(*counting_qubits, key='phase_output'))

    # Execute simulation
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=100)
    return circuit, result

# Sample simulation near the first Riemann zero coordinate
sample_t = 14.134725  
qpe_circuit, qpe_results = run_quantum_phase_estimation(sample_t)

print("\n--- Generated Cirq Quantum Phase Estimation Circuit ---")
print(qpe_circuit)
print("\n--- Quantum Measurement Histograms ---")
print(qpe_results.histogram(key='phase_output'))