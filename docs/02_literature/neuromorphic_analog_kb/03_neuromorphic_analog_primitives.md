# Neuromorphic Analog Primitives: Basic Research Needs

## 1. The Call for "Bio-Functional" Primitives

**Context**: The 2024 DOE Workshop asks: *"What are the key neuromorphic circuit primitives that are needed to capture critical biological computing mechanisms?"*

To support a "Brain Foundation Model", we cannot rely on simple "Integrate-and-Fire" neurons. We need primitives that capture the **complexity** and **robustness** of biology.

## 2. Key Primitives & Analog Implementation

Based on 2025 Reviews on Neuromorphic Circuits:

### 2.1 The "Memristive" Synapse (Plasticity Primitive)

* **biological Mechanism**: Synaptic Efficacy ($w$) changes based on spike timing (STDP), calcium concentration, and neuromodulation.
* **Analog Primitive**: **Memristors (RRAM / PCM)**.
  * **Function**: A two-terminal device where resistance $R$ changes based on the history of charge $q$ ($M(q) = d\phi/dq$).
  * **Advantage**: Non-volatile storage of weights *at the site of computation* (In-Memory).
  * **Challenge**: "Device-to-Device Variability" and "Conductance Drift".
  * **Research Need**: Developing "Drift-Resilient" encoding schemes (e.g., population coding) that allow a BFM to function despite hardware imperfections.

### 2.2 The "Active" Dendrite (Computation Primitive)

* **Biological Mechanism**: Dendrites are not passive cables; they perform non-linear filtering (NMDA spikes) and coincidence detection.
* **Analog Primitive**: **Sub-threshold CMOS Circuits**.
  * **Function**: Using transistors in the "weak inversion" region where current effectively exponential with voltage ($I_{ds} \propto e^{V_{gs}}$), mimicking the Boltzmann physics of ion channels.
  * **Research Need**: Circuits that implement "Dendritic Integration" allowing a single neuron to solve XOR problems, increasing the computational density per neuron.

### 2.3 The "Stochastic" Neuron (Robustness Primitive)

* **Biological Mechanism**: Noise is not a bug; it's a feature used for probabilistic inference and exploration.
* **Analog Primitive**: **Thermal Noise exploitation**.
  * **Function**: Instead of spending energy to shield circuits from noise, we use the intrinsic thermal noise of analog components to drive stochastic sampling (like Boltzmann Machines).
  * **Advantage**: Massive energy saving and better generalization (Bayesian Brain hypothesis).

## 3. Technologies for Prototyping

**Reference**: *Roadmap to neuromorphic computing (2024).*

1. **CMOS + Memristor Hybrid**: The most mature path. Standard CMOS for control logic + RRAM back-end-of-line (BEOL) integration for high-density synapses.
2. **Organic Electrochemical Transistors (OECTs)**: Emerging tech. OECTs operate with ion movements (like biology) rather than just electrons, offering intrinsic compatibility with bio-sensing for "Wetware" interfaces.

## 4. Trade-off Analysis: Analog vs. Digital

| Feature | Analog Neuromorphic | Digital Neuromorphic | Traditional GPU |
| :--- | :--- | :--- | :--- |
| **Physics** | Continuous (Time/Voltage) | Discrete | Discrete |
| **Energy** | **Femtojoules (fJ)** / op | Picojoules (pJ) / op | Nanojoules (nJ) / op |
| **Precision** | Low (4-8 bit, noisy) | High (32-64 bit, exact) | High (FP16/FP32) |
| **Scaling** | Difficult (Signal degradation) | Easy (Perfect copy) | Limited by Power |
| **Role in BFM** | **Inference (Edge/Implant)** | Training/Routing | Pre-training |

**Conclusion for Proposal**: We focusing on the **Analog** domain because the "Brain Foundation Model" allows us to learn *robust representations* that are resilient to the low precision of analog hardware, unlocking the energy efficiency needed for implantable AI.

## References

* [Mehonic et al. (2024) - Neuromorphic Roadmap](./pdfs/mehonic_2024_neuromorphic_roadmap.pdf)
