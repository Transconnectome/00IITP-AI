# Structural Connectomes, Network Renormalization, and Non-Backprop Local Learning: Theoretical Foundations for 2028 IITP Brain-Inspired AI

- **Document Identifier**: `IITP-AI-2028-FOUNDATIONS-V1`
- **Target Project**: 2028 IITP AI Wonchun Research Project (*Brain-Inspired Neuromorphic Computing & Non-Backprop Learning*)
- **Authors**: Teamwork Research & Theoretical Foundations Group (SNU Neurox / Transconnectome Consortium)
- **Status**: Official Foundation Document
- **Date**: 2026-10-29

---

## Executive Abstract

Modern deep learning is fundamentally constrained by the structural and computational artifices of the von Neumann-backpropagation paradigm: global weight transport, gradient locking, backpropagation through time (BPTT) memory explosion, catastrophic forgetting, and unsustainable energetic dissipation. Biological brains resolve these challenges through an architectural blueprint that operates neither as random graphs nor as unconstrained scale-free networks, but as **hierarchical, self-similar fractals governed by network motifs, multi-scale hub repulsion, and local normative learning rules** (Milo et al. 2002, 2004; Song et al. 2005, 2006; Chklovskii et al. 2026).

This foundation monograph provides the comprehensive mathematical, physical, and computational formalization bridging structural connectomics to functional neuromorphic intelligence:
1. **Microscopic Topologies**: Formal degree-preserving null models, the 13 three-node triad dynamics (coherent and incoherent feedforward loops), and the size-invariant Triad Significance Profile ($\vec{SP}$) establishing synaptic connectomes in Superfamily 2.
2. **Mesoscopic & Macroscopic Renormalization**: Box-covering renormalization group ($N_B \sim l_B^{-d_B}$), the microscopic origin of fractality via hub repulsion ($R(k_{hub}, k_{hub}) \ll 1, k_{nn}(k) \sim k^{-\mu}$), and the structural crossover $\ell_{co}$.
3. **The Dynamical Bridge**: Rigorous physical proofs of epileptogenesis containment, extended Griffiths phases ($\Delta \lambda_{GP}$), multi-scale intrinsic temporal integration ($\tau \sim l_B^z$), and bounded energetic dissipation in continuous Lagrangian substrates (SOENs).
4. **Normative Non-Backprop Learning**: Complete mathematical derivation of Neural Similarity Matching (NSM) and Rectified Spectral Units (ReSU) via Legendre-Fenchel min-max duality, demonstrating how fast recurrent inference and slow Hebbian/anti-Hebbian plasticity eliminate the weight transport problem.
5. **Comparative Paradigm Benchmarking**: Cross-framework analysis across Predictive Coding, Equilibrium Propagation, Forward-Forward, and Direct Feedback Alignment.
6. **Core Scientific Hypotheses**: Three formal Scientific Questions (SQ1, SQ2, SQ3) featuring explicit mathematical formulations, empirical observables, and falsifiable *Wrong-If-X* conditions.

---

## 1. Network Motifs and Statistical Null Models (Milo et al. 2002, Science)

### 1.1 Formal Definition of a Network Motif
Let a directed biological or artificial connectome be represented by a graph $G = (V, E)$, where $V$ is the set of $|V| = N$ vertices (neurons or neuromorphic computational nodes) and $E \subseteq V \times V$ is the set of $|E| = M$ directed edges (synapses). 

A small directed subgraph $G_s = (V_s, E_s)$ consisting of $n = |V_s| \ll N$ vertices is defined as a **network motif** if and only if the empirical count of its topological isomorphism in $G$ is statistically significantly enriched relative to its expected frequency within an ensemble of randomized null-model graphs possessing identical single-node degree sequences.

### 1.2 Mathematical Formulation of the Degree-Preserving Null Model
Trivial graph properties—such as heavy-tailed in-degree distributions $P(k_{in})$ and out-degree distributions $P(k_{out})$—naturally increase the background probability of forming triangles and cliques. To ensure that detected subgraphs reflect true evolutionary or developmental self-organization rather than degree artifacts, the randomized graph ensemble $\Omega(G)$ must satisfy strict hard constraints:
$$\forall v \in V: \quad k_{in}^{rand}(v) = k_{in}^{real}(v) \quad \text{and} \quad k_{out}^{rand}(v) = k_{out}^{real}(v)$$

Milo et al. (2002) established a Markov-chain Monte Carlo (MCMC) edge-swapping algorithm that samples uniformly from $\Omega(G)$:
1. **Edge Selection**: Choose two directed edges uniformly at random from $E$:
   $$e_1 = (u, v), \quad e_2 = (w, z) \quad \text{such that } u \neq w \text{ and } v \neq z$$
2. **Topological Invariance Check**: Verify that the proposed rewired edges $e_1' = (u, z)$ and $e_2' = (w, v)$ do not already exist in $E$ ($e_1', e_2' \notin E$) and do not create self-loops ($u \neq z$ and $w \neq v$).
3. **Elementary Transition**: If valid, execute the topological swap:
   $$E \leftarrow (E \setminus \{(u, v), (w, z)\}) \cup \{(u, z), (w, v)\}$$
4. **Ergodic Mixing**: Repeat this elementary swap $Q \cdot M$ times (where $Q \in [100, 200]$ is the mixing factor). The resulting Markov chain is irreducible, aperiodic, and symmetric, guaranteeing convergence to the uniform stationary distribution over the constrained configuration space $\Omega(G)$.

### 1.3 Statistical Significance Quantification
Let $N_{real, i}$ be the count of subgraph type $i$ in the empirical network $G$. Across an ensemble of $K$ independent randomized realizations $\{G^{(k)}\}_{k=1}^K \subset \Omega(G)$, the counts $\{N_{rand, i}^{(k)}\}$ define the sample expectation and sample standard deviation:
$$\langle N_{rand, i} \rangle = \frac{1}{K}\sum_{k=1}^K N_{rand, i}^{(k)}$$
$$\sigma_{rand, i} = \sqrt{\frac{1}{K-1}\sum_{k=1}^K \left( N_{rand, i}^{(k)} - \langle N_{rand, i} \rangle \right)^2}$$

The statistical overrepresentation is parameterized by the **$Z$-score**:
$$Z_i = \frac{N_{real, i} - \langle N_{rand, i} \rangle}{\sigma_{rand, i}}$$

The empirical one-tailed $P$-value is computed directly as:
$$P_i = \frac{1}{K} \sum_{k=1}^K \Theta\left( N_{rand, i}^{(k)} - N_{real, i} \right)$$
where $\Theta(x)$ is the Heaviside step function ($\Theta(x) = 1$ if $x \ge 0$, and $0$ otherwise).

**Formal Criteria for Motif Status (Milo et al. 2002)**:
1. Statistical significance: $P_i < 0.01$ (or equivalently $Z_i > 2.0$ under asymptotic Gaussian limit).
2. Absolute count threshold: $N_{real, i} \ge U$ (where $U = 4$ prevents trivial low-count fluctuations).
3. Fractional difference bound:
   $$\Delta_{rel, i} = \frac{N_{real, i} - \langle N_{rand, i} \rangle}{\langle N_{rand, i} \rangle} > 0.1$$
   This ensures that in massive networks where $\sigma_{rand}$ is minuscule, minor statistical deviations are not misclassified as functional building blocks.

### 1.4 Classification of the 13 Non-Isomorphic 3-Node Triads
For directed graphs without self-loops, there exist exactly 13 topologically distinct non-isomorphic connected subgraphs of order $n=3$, fully characterized by their binary adjacency matrices:

```
  Triad 1 (ID: 6)        Triad 2 (ID: 14)       Triad 3 (ID: 36)
     X                      X                      X
    / \                    ^ \                    ^ ^
   v   v                  /   v                  /   \
  Y     Z                Y     Z                Y     Z

  Triad 4 (ID: 38, FFL)  Triad 5 (ID: 46)       Triad 6 (ID: 74)
     X                      X                      X
    / \                    ^ ^                    / \
   v   v                  /   \                  v   v
  Y --> Z                Y <-> Z                Y <-> Z

  Triad 7 (ID: 98, FBL)  Triad 8 (ID: 102)      Triad 9 (ID: 108)
     X                      X                      X
    / ^                    ^ ^                    ^ ^
   v   \                  /   \                  /   \
  Y --> Z                Y <-> Z                Y <-> Z
                         ^                      ^     ^
                         |                      |     |

  Triad 10 (ID: 110)     Triad 11 (ID: 238)     Triad 12 (ID: 46)
    (Reciprocal Loop)      (Clique w/ asymmetric) (Semi-clique)

  Triad 13 (ID: 998, Full Clique)
     X <---> Y
     ^ \   / ^
     |  \ /  |
     v   X   v
         Z
```

### 1.5 Dynamical Functions of Feedforward Loops: Coherent vs. Incoherent
The Feedforward Loop (FFL, Triad 38: $X \to Y$, $X \to Z$, $Y \to Z$) is the most dominant motif in biological neural circuits. Incorporating synaptic signs (excitatory $+$ or inhibitory $-$) partitions FFLs into 8 distinct configurations, divided into two fundamental dynamical classes:

#### A. Coherent Feedforward Loops (cFFL)
- **Mathematical Condition**: The sign of the direct path equals the product of the signs of the indirect path:
  $$\operatorname{sgn}(w_{XZ}) = \operatorname{sgn}(w_{XY}) \cdot \operatorname{sgn}(w_{YZ})$$
- **Prototypical Architecture (Type-1 cFFL)**: $w_{XZ} > 0, w_{XY} > 0, w_{YZ} > 0$.
- **Continuous Neurodynamics**: Let $x(t), y(t), z(t)$ denote continuous membrane potentials or firing rates. Unit $Z$ acts as an AND gate requiring both inputs to exceed activation thresholds:
  $$\tau_Y \frac{dy(t)}{dt} = -y(t) + \beta_Y \sigma(w_{XY} x(t) - \theta_X)$$
  $$\tau_Z \frac{dz(t)}{dt} = -z(t) + \beta_Z \sigma(w_{XZ} x(t) - \theta_{ZX}) \cdot \sigma(w_{YZ} y(t) - \theta_{ZY})$$
- **Functional Role: Sign-Sensitive Delay & Asymmetric Noise Rejection**:
  When input $x(t)$ exhibits a transient pulse of duration $T_{\text{pulse}}$, $y(t)$ rises toward its steady state:
  $$y(t) = \beta_Y (1 - e^{-t/\tau_Y})$$
  $Z$ activates only if $y(t)$ crosses $\theta_{ZY}$, which requires:
  $$T_{\text{pulse}} \ge T_{\text{delay}} = \tau_Y \ln\left( \frac{\beta_Y}{\beta_Y - \theta_{ZY}} \right)$$
  Spurious stochastic spikes ($T_{\text{pulse}} < T_{\text{delay}}$) produce zero response in $Z$. Conversely, when a sustained input ceases ($x \to 0$), the direct excitatory drive $w_{XZ} x(t)$ drops immediately below threshold, shutting down $Z$ instantaneously. The cFFL thus serves as an **on-delay filter**, shielding downstream circuits from noise.

#### B. Incoherent Feedforward Loops (iFFL)
- **Mathematical Condition**: The sign of the direct path opposes the indirect path:
  $$\operatorname{sgn}(w_{XZ}) = -\left( \operatorname{sgn}(w_{XY}) \cdot \operatorname{sgn}(w_{YZ}) \right)$$
- **Prototypical Architecture (Type-1 iFFL)**: Direct excitation ($w_{XZ} > 0$), indirect feedforward inhibition ($w_{XY} > 0, w_{YZ} < 0$).
- **Continuous Neurodynamics**:
  $$\tau_Z \frac{dz(t)}{dt} = -z(t) + \beta_Z \sigma(w_{XZ} x(t) - \theta_{ZX}) - \gamma_Z y(t)$$
- **Functional Roles**:
  1. **Biphasic Pulse Generation & Response Acceleration**: A positive step in $x(t)$ rapidly drives $z(t)$ via the fast direct path. With delay $\tau_Y$, $y(t)$ rises and applies feedforward inhibition, driving $z(t)$ back to an adapted steady-state.
  2. **Fold-Change Detection (FCD) & Scale Invariance**: Under shunting inhibition ($\frac{dz}{dt} = \beta_Z \frac{x(t)}{y(t)} - z(t)$), the transient trajectory of $z(t)$ depends strictly on the relative ratio $x(t)/x_0$, rendering perceptual processing invariant to absolute baseline intensity.

### 1.6 Four-Node Motifs: Bi-Fans and Coincidence Detection
The **Bi-Fan motif** consists of two upstream nodes ($X_1, X_2$) projecting divergently to two downstream target nodes ($Y_1, Y_2$):
```
  X1       X2
  | \     / |
  |  \   /  |
  |   \ /   |
  v    X    v
  Y1       Y2
```
- **Circuit Function**: Mediates combinatorial signal integration and dense overlapping regulons. When $Y_1, Y_2$ exhibit non-linear saturating responses, the bi-fan acts as a cross-talk-free coincidence gate, routing orthogonal sensory features into distinct downstream targets.

### 1.7 Connectome Discovery & Lineage (Milo, Chklovskii et al. 2002)
In the original 2002 Science paper, Milo et al. analyzed the somatic nervous system of *Caenorhabditis elegans* (280 non-pharyngeal neurons connected by chemical synapses and gap junctions). The empirical connectome displayed profound overrepresentation of:
- Triad 38 (Feedforward Loop): $Z = 12.4$ ($P < 0.001$)
- 4-Node Bi-Fan: $Z = 23.1$ ($P < 0.001$)

**Direct Theoretical Lineage**: Dmitry "Mitya" Chklovskii (co-author on Milo et al. 2002) established that these overrepresented microcircuits constitute the structural basis for local optimization. This directly culminated in Chklovskii's Rectified Spectral Units (ReSU, AAAI 2026), where local structural circuits implement exact similarity matching without global backpropagation.

---

## 2. Superfamilies of Evolved and Designed Networks (Milo et al. 2004, Science)

### 2.1 The Network Size Artifact in Raw $Z$-Scores
Milo et al. (2004) proved that raw $Z$-scores scale intrinsically with graph volume:
$$Z_i \propto \sqrt{N} \quad \text{or} \quad Z_i \propto \sqrt{|E|}$$
For an identical underlying generative wiring rule, a mammalian connectome ($N = 10^8$) exhibits raw $Z$-scores orders of magnitude larger than *C. elegans* ($N = 10^2$). Consequently, raw $Z$-scores cannot be used for scale-invariant cross-species or cross-domain comparisons.

### 2.2 The Normalized Triad Significance Profile (TSP / $\vec{SP}$)
To isolate topological organization from network size, Milo et al. introduced the **Triad Significance Profile (TSP)** vector $\vec{SP} \in \mathbb{R}^{13}$. The raw $Z$-score vector $\vec{Z} = (Z_1, Z_2, \dots, Z_{13})^T$ is projected onto the unit hypersphere:

$$\vec{SP}_i = \frac{Z_i}{\sqrt{\sum_{j=1}^{13} Z_j^2}}, \quad \text{such that} \quad \|\vec{SP}\|_2 = \sqrt{\sum_{i=1}^{13} \vec{SP}_i^2} = 1$$

Each coordinate $\vec{SP}_i \in [-1, 1]$ represents the scale-invariant relative enrichment or depletion of triad $i$.

### 2.3 Superfamily Classification Taxonomy
Clustering diverse real-world complex networks in the 13-dimensional $\vec{SP}$ space revealed four universal **Superfamilies**:

| Superfamily | Representative Empirical Systems | Dominant Triad Signature | Driving Functional Mechanism |
| :--- | :--- | :--- | :--- |
| **Superfamily 1: Transcription & Sensory Signaling** | *E. coli*, *S. cerevisiae* gene regulatory networks | Extreme positive peak at Triad 38 (FFL); severe suppression of cyclic feedback (Triads 98, 102). | Pure feedforward noise rejection, rapid environmental response without multistability. |
| **Superfamily 2: Synaptic Connectomes & Development** | *C. elegans* neuronal network, mammalian neocortical microcircuits, developmental gene cascades (*Drosophila*) | Strong positive Triad 38 (FFL) combined with prominent positive reciprocal/feedback triads (Triads 46, 108, 110, 111). | Hybrid feedforward-recurrent processing: supports persistent attractor memory and reverberation while maintaining directional signal flow. |
| **Superfamily 3: Lingual & Word Adjacency Graphs** | English, Japanese, French syntax networks | Pronounced peaks at bidirectional triads with cyclic paths (Triads 74, 98, 110). | Contextual adjacency, grammatical constraints, and recursive compositional syntax. |
| **Superfamily 4: Directed Hyperlinks & Social Webs** | World Wide Web, citation networks, social influence graphs | Dominance of dense mutual cliques and transitive triads (Triads 111, 238, 998). | Preferential attachment, unconstrained clustering, and popularity-driven growth. |

```
                     TRIAD SIGNIFICANCE PROFILES (SP)
  1.0 +
      |           Superfamily 2 (Synaptic Connectomes)
      |              [38: FFL]         [46: Recip]   [110: Loop]
  0.5 |                 /\                 /\           /\
      |                /  \               /  \         /  \
  0.0 +---------------+----+-------------+----+-------+----+------ (Neutral)
      |  \           /      \           /      \     /
 -0.5 |   \         /        \         /        \   /
      |    \_______/          \_______/          \_/
 -1.0 +-----------------------------------------------------------
        1   2   3   4   5   6   7   8   9   10  11  12  13 (Triad Index)
```

### 2.4 Deep Significance for Neuromorphic Connectome Design
Synaptic connectomes uniquely occupy **Superfamily 2**. 
- Purely feedforward networks (Superfamily 1) lack working memory and temporal credit assignment.
- Unconstrained recurrent networks (Superfamilies 3 & 4) suffer from chaotic bifurcations, limit cycles, and runaway positive feedback.
- Superfamily 2 achieves an evolutionary optimum: reciprocal micro-motifs provide local reverberating memory buffers, embedded within a global feedforward scaffold that guarantees directional information flow.

---

## 3. Fractal Self-Similarity and Box-Covering Renormalization (Song, Havlin & Makse 2005, Nature)

### 3.1 The Small-World vs. Fractal Scale-Invariance Paradox
A foundational assumption in network science was that scale-free complex networks could not be fractals. Because complex networks exhibit the **small-world property**—where the average shortest-path distance scales logarithmically with graph size:
$$\langle \ell \rangle \sim \ln N$$
it was assumed that network volume grows exponentially with metric radius ($V(r) \sim e^{r/\ell_0}$), precluding power-law scale-invariance.

Song, Havlin & Makse (2005) resolved this paradox by discovering that biological networks (cellular metabolism, protein interaction webs, and cortical connectomes) are genuine **self-similar fractals** under topological renormalization.

### 3.2 Formal Definition of the Box-Covering Algorithm
Let the shortest path metric between vertices $u, v \in V$ be $d(u, v)$, representing the minimum number of topological edges connecting $u$ and $v$.
1. A **topological box** $B_\alpha \subset V$ of size $l_B$ is defined as a subset of vertices such that all pairwise distances satisfy:
   $$\forall u, v \in B_\alpha: \quad d(u, v) < l_B$$
   (i.e., the maximum internal diameter is at most $l_B - 1$).
2. The network $G$ is covered by a disjoint partition of $N_B(l_B)$ boxes:
   $$\bigcup_{\alpha=1}^{N_B} B_\alpha = V \quad \text{and} \quad B_\alpha \cap B_\beta = \emptyset \quad (\alpha \ne \beta)$$
3. The optimal box covering minimizes the box count $N_B(l_B)$:
   $$N_B(l_B) = \min_{\mathcal{P}} |\mathcal{P}(l_B)|$$

### 3.3 The Fractal Scaling Relation
A network is structurally fractal if the minimum box count satisfies a power-law scaling with box size $l_B$:

$$N_B(l_B) \sim l_B^{-d_B}$$

where $d_B$ is the **fractal dimension** of the network.
- If $d_B < \infty$, the network possesses structural scale-invariance.
- For classical non-fractal small-world graphs (e.g., Erdős-Rényi random graphs, Barabási-Albert scale-free networks), the box count decays exponentially:
  $$N_B(l_B) \sim e^{-l_B / \ell_0} \quad \implies \quad d_B \to \infty$$

### 3.4 Algorithmic Implementations: Dual Graph Coloring & MEMB
Finding the optimal box covering is equivalent to the NP-hard vertex coloring problem on the dual graph $G'(l_B)$, where an edge exists between $u$ and $v$ if $d(u, v) \ge l_B$. Song et al. developed greedy burning algorithms:
1. **Compact-Box Burning (CBB)**: A node is selected as a box center, and adjacent nodes within distance $\lfloor (l_B-1)/2 \rfloor$ are greedily absorbed.
2. **Maximum Excluded Mass Burning (MEMB)**: At each iteration, choose the center node that maximizes the "excluded mass" (uncovered nodes within distance $< l_B$), yielding tight empirical bounds on $N_B(l_B)$.

### 3.5 Renormalization Group (RG) Coarse-Graining Transformation
The Renormalization Group transformation $\mathcal{R}_{l_B}: G \to G'$ coarse-grains the network at topological scale $l_B$:
1. **Super-nodes**: Each box $B_\alpha$ collapses into a single renormalized super-node $\alpha \in V'$.
2. **Super-edges**: An edge connects super-nodes $\alpha$ and $\beta$ if and only if there exists at least one microscopic edge connecting their constituent vertices:
   $$(\alpha, \beta) \in E' \iff \exists u \in B_\alpha, v \in B_\beta \quad \text{such that} \quad (u, v) \in E$$
   (Self-loops and multi-edges are eliminated).

```
   Microscopic Level G                  Renormalized Level G'
   [ (u1)---(u2)---(u3) ]               ( Super-Node A )
             |                                 |
             |                                 |
   [ (v1)---(v2)---(v3) ]               ( Super-Node B )
     Box B_alpha (size < l_B)               Super-edge (A, B)
```

### 3.6 Invariance of Degree Distribution and Exponent Relations
Under successive coarse-graining operations $\mathcal{R}_{l_B}$, fractal scale-free networks satisfy exact self-similarity:
1. **Degree Distribution Invariance**: If the microscopic network obeys power-law degree scaling $P(k) \sim k^{-\gamma}$, the renormalized network exhibits the identical exponent:
   $$P(k') \sim (k')^{-\gamma}$$
2. **Degree Scaling Law**: The degree $k'$ of a renormalized super-node scales with the maximum internal node degree $k$ within that box according to:
   $$k' = k \cdot l_B^{-d_k}$$
   where $d_k$ is the **degree fractal dimension**.
3. **Fundamental Scaling Identity**: Combining the box-covering relation $N_B \sim l_B^{-d_B}$ and the degree scaling law yields the exact relation connecting topological exponents:
   $$\gamma = 1 + \frac{d_B}{d_k}$$
4. **Edge Scaling Law**: The total number of edges $N_E(l_B)$ in the coarse-grained network scales as:
   $$N_E(l_B) \sim l_B^{-d_e}$$
   where $d_e$ is the edge capacity dimension, characterizing interconnectivity dissipation.

---

## 4. Origins of Fractality, Hub Repulsion, and Disassortativity (Song, Havlin & Makse 2006, Nature Physics)

### 4.1 The Fundamental Structural Question
Why are biological connectomes and metabolic networks fractal ($d_B \in [2.0, 3.5]$), whereas canonical scale-free models (such as the Barabási-Albert model) are non-fractal ($d_B \to \infty$)?

### 4.2 Microscopic Mechanism: Hub Repulsion (Disassortativity)
Song, Havlin & Makse (2006) proved that the structural determinant of network fractality is **Hub Repulsion**—a strong disassortativity where high-degree nodes systematically avoid connecting to one another:
- **Non-Fractal Networks (BA Model / Rich-Club)**: Hubs attach preferentially to other hubs, forming a dense central core ("rich club"). Any shortest path traverses this core, producing an ultra-small world with $\langle \ell \rangle \sim \ln \ln N$. Box-covering collapses exponentially, destroying fractality.
- **Fractal Networks (Biological Connectomes)**: Hubs are repelled from one another. Direct hub-to-hub connections are suppressed. Each hub is surrounded by a protective shell of low-degree perimeter nodes, and hub-to-hub communication is mediated across modular intermediate pathways.

### 4.3 Mathematical Quantification of Hub Repulsion

#### A. Joint Degree Distribution $P(k_1, k_2)$ and Edge Ratio $R(k_1, k_2)$
Let $e(k_1, k_2)$ be the probability that a randomly chosen edge connects a vertex of degree $k_1$ with a vertex of degree $k_2$. In an uncorrelated null graph:
$$e_{rand}(k_1, k_2) = \frac{k_1 P(k_1) k_2 P(k_2)}{\langle k \rangle^2} (2 - \delta_{k_1, k_2})$$

The degree-correlation ratio is defined as:
$$R(k_1, k_2) = \frac{e(k_1, k_2)}{e_{rand}(k_1, k_2)}$$

- In assortative / rich-club networks: $R(k_1, k_2) \gg 1$ for $k_1, k_2 \gg 1$.
- In fractal connectomes with hub repulsion:
  $$R(k_{hub}, k_{hub}) \ll 1$$
  High-degree hubs exhibit severe depletion of direct mutual synapses.

#### B. Nearest-Neighbor Degree Function $k_{nn}(k)$
The average degree of the nearest neighbors of a vertex with degree $k$ is given by:
$$k_{nn}(k) = \sum_{k'} k' P(k' | k) = \frac{\sum_{k'} k' e(k, k')}{\sum_{k'} e(k, k')}$$

In fractal networks, $k_{nn}(k)$ decays as a power law:
$$k_{nn}(k) \sim k^{-\mu}, \quad \text{with } \mu > 0$$
The positive exponent $\mu$ quantitatively characterizes the magnitude of hub repulsion.

### 4.4 The Inverse-Renormalization Growth Model (Mode I vs. Mode II)
Song et al. formulated a microscopic growth model that inverts the RG transformation, governed by a mixing parameter $e \in [0, 1]$:

```
             Generation t                         Generation t+1
Mode I:     (Hub A) ======= (Hub B)  --->  (Hub A) ======= (Hub B)
(Prob e)                                        \         /
                                                 (New Node)
            (Direct hub link preserved: Hub-Hub Attraction -> Non-Fractal)

Mode II:    (Hub A) ------- (Hub B)  --->  (Hub A)         (Hub B)
(Prob 1-e)                                      \           /
                                              (Perimeter Nodes)
            (Direct link disconnected: Hub Repulsion -> Fractal)
```

1. **Mode I (Probability $e$)**: Offspring nodes attach to existing hubs while preserving direct connections between parental hubs. This generates hub attraction, rich-club formation, and non-fractal topology ($d_B \to \infty$).
2. **Mode II (Probability $1 - e$)**: Direct connections between parental hubs are deleted; offspring nodes attach to the perimeter, pushing hubs apart by distance $\ell > 1$. This enforces strict hub repulsion and generates pure fractal self-similarity ($d_B = \frac{\ln(2m-1)}{\ln 3}$).

### 4.5 The Crossover Scale $\ell_{co}$ in Biological Connectomes
When $0 < e \ll 1$, the connectome exhibits **crossover behavior**:
- On length scales below the crossover length $\ell_{co} \sim (1/e)^\nu$, the network is **fractal**, exhibiting power-law box-covering $N_B \sim l_B^{-d_B}$ and hub repulsion.
- On length scales above $\ell_{co}$, the network crosses over to the **small-world regime**.

Biological connectomes operate precisely in this dual regime: local and mesoscopic cortical columns are self-similar and modular ($l_B < \ell_{co}$), while long-range white matter tract bundles provide small-world communication ($l_B > \ell_{co}$).

---

## 5. Topological Bridge to Functional Dynamics & Non-Backprop Learning

```
========================================================================================
       STRUCTURAL TOPOLOGY                          FUNCTIONAL DYNAMICS
========================================================================================
Network Motifs (Milo 2002/2004)            Dynamical Gain & Noise Gating
  * Coherent FFLs (cFFL)            --->     * Asymmetric noise rejection / delay filter
  * Incoherent FFLs (iFFL)          --->     * Rapid pulse generation & fold-change adaptation
  * Superfamily 2 (Reciprocal)      --->     * Persistent attractor memory / reverberation
----------------------------------------------------------------------------------------
Fractal Modularity (Song 2005)              Criticality & Multi-Scale Dynamics
  * Box-Covering N_B ~ l_B^(-d_B)   --->     * Multi-scale temporal integration (tau ~ l_B^z)
  * Self-Similar Renormalization    --->     * Scale-invariant representations across layers
----------------------------------------------------------------------------------------
Hub Repulsion (Song 2006)                  Dynamical Containment & Stability
  * Disassortativity R(k,k) << 1    --->     * Prevention of runaway epileptic avalanches
  * Extended Griffiths Phases       --->     * Broad critical parameter regime (no fine-tuning)
  * Bounded Edge Density N_E(l_B)   --->     * Bounded metabolic dissipation (SOENs dE/dt <= D)
----------------------------------------------------------------------------------------
Local Modular Encapsulation                Backprop-Free Learning (No BPTT)
  * Sparse Inter-Box Projections    --->     * Decoupled local credit assignment (ReSU)
  * Hierarchical Coarse-Graining    --->     * Equilibrium Propagation & Predictive Coding
========================================================================================
```

### 5.1 Dynamical Containment: Preventing Runaway Excitation (Epileptogenesis)
In unconstrained recurrent neural networks or assortative rich-club networks, excitatory activity cascades uncontrollably: if a hub fires, its direct connections to other hubs trigger immediate, system-wide synchronization—a catastrophic state analogous to epileptic seizures.

Hub repulsion ($R(k_{hub}, k_{hub}) \ll 1$) combined with iFFLs guarantees **dynamical containment** (Kaiser & Hilgetag 2010):
1. Because hubs never connect directly to each other, high-degree nodes cannot form a self-reinforcing positive feedback clique.
2. Spreading activity from a hub must diffuse through concentric shells of low-degree perimeter nodes.
3. These intermediate shells are populated with feedforward inhibitory motifs (iFFLs) that deliver feedforward and feedback inhibition, clamping the effective spectral radius $\rho(W) \le 1.0$ and terminating runaway cascades before they reach adjacent hubs.

### 5.2 Criticality and Extended Griffiths Phases (Moretti & Muñoz 2013)
The brain operates in a critical regime characterized by scale-free activity avalanches ($P(S) \sim S^{-3/2}$, $P(T) \sim T^{-2}$), maximizing information transmission and dynamic range. In homogeneous or random networks, criticality requires exact, fine-tuned balancing of synaptic gain ($\lambda = \lambda_c$).

Fractal modularity and topological heterogeneity fundamentally alter this phase transition:
- In fractal modular networks, rare topological regions (modules of size $l_B$) can become locally active while the rest of the network remains subcritical.
- Moretti & Muñoz (2013) proved that this structural heterogeneity stretches the isolated critical point $\lambda_c$ into an **extended Griffiths Phase** $\Delta \lambda_{GP} = [\lambda_{c1}, \lambda_{c2}]$.
- Within this extended parameter window, the network exhibits critical-like power-law dynamics, maximal sensitivity, and infinite susceptibility *without requiring any fine-tuning of global synaptic weights*.

### 5.3 Multi-Scale Temporal Integration Without Recurrent Gating
Artificial architectures require complex gating mechanisms (e.g., forget gates in LSTM, attention masks in Transformers) to retain information across varying time horizons. Fractal modular connectomes generate a multi-scale hierarchy of timescales natively through structural scaling:
- Let the characteristic relaxation time of a microscopic box of size $l_B$ scale as:
  $$\tau(l_B) \sim l_B^z$$
  where $z$ is the dynamic critical exponent.
- Microscopic motifs ($l_B = 1$) operate on fast timescales ($\tau_0 \sim 1 - 10$ ms), processing rapid sensory transients.
- Renormalized modular assemblies at scale $l_B$ integrate signals over macroscopic timescales ($\tau \sim 100 - 1000$ ms), maintaining persistent context.
- Temporal credit assignment is thus naturally partitioned across structural scales without the numerical instability of backpropagation through time (BPTT).

### 5.4 Bounding Dynamical Dissipation in Neuromorphic Substrates
In physical neuromorphic implementations (such as Shainline's Superconducting Optoelectronic Networks, SOENs), the physical energy stored in dendritic integration loops follows continuous Lagrangian neurodynamics:
$$E = \frac{1}{2} \sum_i \beta s_i^2$$
$$\frac{ds_i}{dt} = \gamma g(\phi_i, s_i) - \frac{s_i}{\tau_i}$$

If the network topology permitted dense hub-hub clustering, simultaneous activation would generate massive current surges, exceeding the critical superconducting current ($I > I_c$) or causing thermal failure.
Because the connectome enforces hub repulsion and edge scaling $N_E(l_B) \sim l_B^{-d_e}$, instantaneous dissipation is strictly bounded:
$$\dot{E} = \sum_i \beta s_i \left( \gamma g(\phi_i, s_i) - \frac{s_i}{\tau} \right) \le \mathcal{D}_{\max}$$
This architectural bound permits high-bandwidth, ultra-low energy neuromorphic execution ($< 10^{-15}$ J per synaptic event).

---

## 6. Dmitri Chklovskii et al. (AAAI 2026 / Flatiron CCN): ReSU & Neural Similarity Matching

### 6.1 Normative Similarity Matching Foundation
Standard deep learning relies on global objective functions whose gradients require the transpose of weight matrices across distant layers (the **weight transport problem**) and backward-in-time sequential credit assignment (the **backpropagation through time problem**). Neither is biologically realizable.

The normative framework of **Neural Similarity Matching (NSM)** (Pehlevan & Chklovskii, 2014, 2015; Sengupta et al., 2018) starts from an axiomatic, biologically grounded principle: *A sensory neural circuit maps high-dimensional input streams $\mathbf{x}_t \in \mathbb{R}^d$ into low-dimensional neural activity vectors $\mathbf{y}_t \in \mathbb{R}^k$ ($k < d$) such that pairwise geometric relationships (inner-product similarities) are optimally preserved.*

For a dataset of $T$ samples, the offline multidimensional similarity matching objective is formulated as:
$$\min_{\mathbf{Y} \in \mathbb{R}^{k \times T}} \frac{1}{4T^2} \sum_{t=1}^T \sum_{t'=1}^T \left( \mathbf{x}_t^T \mathbf{x}_{t'} - \mathbf{y}_t^T \mathbf{y}_{t'} \right)^2$$
Expanding the quadratic loss yields:
$$\min_{\mathbf{Y}} \frac{1}{4T^2} \left[ \sum_{t, t'} (\mathbf{x}_t^T \mathbf{x}_{t'})^2 - 2 \sum_{t, t'} (\mathbf{x}_t^T \mathbf{x}_{t'})(\mathbf{y}_t^T \mathbf{y}_{t'}) + \sum_{t, t'} (\mathbf{y}_t^T \mathbf{y}_{t'})^2 \right]$$
The first term is constant with respect to $\mathbf{Y}$. Dropping constants and writing in matrix trace notation (where $X \in \mathbb{R}^{d \times T}$, $Y \in \mathbb{R}^{k \times T}$):
$$\min_{Y} \left[ -\frac{1}{2T^2} \operatorname{Tr}\left( X^T X Y^T Y \right) + \frac{1}{4T^2} \operatorname{Tr}\left( Y^T Y Y^T Y \right) \right] = \min_{Y} \left[ -\frac{1}{2T^2} \| X Y^T \|_F^2 + \frac{1}{4T^2} \| Y Y^T \|_F^2 \right]$$

### 6.2 Duality, Legendre-Fenchel Transform, and Min-Max Formulation
The objective contains coupled fourth-order terms in $Y$, which cannot be solved sample-by-sample in an online streaming setting. Pehlevan, Sengupta, and Chklovskii introduced auxiliary synaptic weight variables via the **Legendre-Fenchel transform**:

1. **Decoupling the Input-Output Cross-Term ($-\|XY^T\|_F^2$)**:
   Using the identity $-\frac{1}{2}\|A\|_F^2 = \min_{W} \left[ \frac{1}{2} \|W\|_F^2 - \operatorname{Tr}(W A^T) \right]$ with $A = \frac{1}{T} Y X^T$:
   $$-\frac{1}{2T^2} \operatorname{Tr}(X Y^T Y X^T) = \min_{W \in \mathbb{R}^{k \times d}} \left[ \frac{1}{2} \operatorname{Tr}(W W^T) - \frac{1}{T} \sum_{t=1}^T \mathbf{y}_t^T W \mathbf{x}_t \right]$$
   Here, $W$ represents the **feedforward synaptic weight matrix**.

2. **Decoupling the Output-Output Auto-Term ($\|YY^T\|_F^2$)**:
   Using the conjugate maximization identity $\frac{1}{4}\|B\|_F^2 = \max_{M} \left[ \frac{1}{2} \operatorname{Tr}(M B) - \frac{1}{4} \|M\|_F^2 \right]$ with $B = \frac{1}{T} Y Y^T$:
   $$\frac{1}{4T^2} \operatorname{Tr}(Y Y^T Y Y^T) = \max_{M \in \mathbb{R}^{k \times k}, M \ge 0} \left[ \frac{1}{2T} \sum_{t=1}^T \mathbf{y}_t^T M \mathbf{y}_t - \frac{1}{4} \operatorname{Tr}(M M^T) \right]$$
   Here, $M$ represents the **lateral recurrent inhibitory synaptic weight matrix** ($M_{ij} \ge 0$ for $i \ne j$, with zero diagonal $M_{ii} = 0$).

Substituting both conjugate representations transforms the intractable global optimization problem into a biologically realizable **Saddle-Point (Min-Max) Objective**:
$$\min_{W, Y} \max_{M \ge 0} \mathcal{L}(W, M, Y) = \frac{1}{T} \sum_{t=1}^T \ell(\mathbf{y}_t, \mathbf{x}_t; W, M) + \frac{1}{2} \operatorname{Tr}(W W^T) - \frac{1}{4} \operatorname{Tr}(M M^T)$$
where the instantaneous loss per time step is:
$$\ell(\mathbf{y}_t, \mathbf{x}_t; W, M) = -\mathbf{y}_t^T W \mathbf{x}_t + \frac{1}{2} \mathbf{y}_t^T (I + M) \mathbf{y}_t$$

### 6.3 Two-Timescale Dynamical Separation
This minimax formulation maps directly onto a two-timescale neural circuit:

#### A. Fast Timescale: Neural Inference Dynamics (Relaxation to Equilibrium)
For an incoming input vector $\mathbf{x}_t$, synaptic weights $(W, M)$ remain frozen on the millisecond timescale. Output neurons execute continuous-time recurrent dynamics to minimize the instantaneous energy:
$$\tau_y \frac{d\mathbf{y}_t(\tau)}{d\tau} = -\nabla_{\mathbf{y}} \ell = W \mathbf{x}_t - (I + M) \mathbf{y}_t(\tau)$$
Rewriting as a leaky-integrator recurrent network:
$$\tau_y \frac{d\mathbf{y}_t(\tau)}{d\tau} = -\mathbf{y}_t(\tau) + W \mathbf{x}_t - M \mathbf{y}_t(\tau)$$
where:
- $-\mathbf{y}_t(\tau)$ is the intrinsic passive leak current.
- $W \mathbf{x}_t$ is the feedforward excitation driven by pre-synaptic inputs.
- $-M \mathbf{y}_t(\tau)$ is the recurrent lateral inhibition from neighboring neurons in the same layer.

**Convergence and Contraction Mapping**:
The Jacobian of this dynamical system is $J = -\frac{1}{\tau_y} (I + M)$. Since $M$ is symmetric positive semi-definite with non-negative off-diagonal entries, the eigenvalues of $I + M$ satisfy $\lambda_i(I + M) \ge 1 > 0$. Therefore, all eigenvalues of $J$ have strictly negative real parts:
$$\operatorname{Re}(\lambda_i(J)) \le -\frac{1}{\tau_y} < 0$$
The system is strictly contractive and converges exponentially with time constant $\tau_{\text{eff}} \le \tau_y$ to the unique fixed point:
$$\mathbf{y}_t^* = (I + M)^{-1} W \mathbf{x}_t$$

#### B. Slow Timescale: Synaptic Plasticity Dynamics
Once neural activities settle to the steady-state $\mathbf{y}_t^*$, synaptic weights adapt on a slower timescale ($\tau_w, \tau_m \gg \tau_y$) via stochastic gradient descent/ascent on the minimax objective:

1. **Feedforward Weights ($W$) — Minimization (Hebbian)**:
   $$\tau_w \frac{dW}{dt} = -\nabla_W \mathcal{L} = \mathbf{y}_t^* \mathbf{x}_t^T - W$$
   In discrete update notation:
   $$\Delta W_{ij} = \eta_w \left( y_{i,t}^* x_{j,t} - W_{ij} \right)$$
   *Local Interpretation*: The update to synapse $W_{ij}$ requires ONLY the post-synaptic activity $y_{i}^*$ and the pre-synaptic input $x_j$, balanced by a local homeostatic decay term $-W_{ij}$. This is classical **Hebbian learning with Oja-like normalization**.

2. **Lateral Inhibitory Weights ($M$) — Maximization (Anti-Hebbian)**:
   $$\tau_m \frac{dM}{dt} = +\nabla_M \mathcal{L} = \mathbf{y}_t^* (\mathbf{y}_t^*)^T - M, \quad \text{for } i \ne j$$
   In discrete update notation:
   $$\Delta M_{ij} = \eta_m \left( y_{i,t}^* y_{j,t}^* - M_{ij} \right), \quad M_{ii} = 0$$
   *Local Interpretation*: When two output neurons fire simultaneously ($y_i^* y_j^* > 0$), the mutual inhibitory connection between them strengthens. This is classical **anti-Hebbian plasticity (Földiák, 1990)**, which decorrelates neural outputs and forces individual neurons to span distinct orthogonal subspaces.

**Crucial Consequence**: No backpropagation, no error signals propagated from downstream layers, and zero weight transport ($W^T$ is never needed).

### 6.4 Rectified Spectral Units (ReSU) Architecture (AAAI 2026)
In Qin, Pughe-Sanford, Genkin, Özdil, Greengard, Sengupta, and Chklovskii (AAAI 2026, *A Network of Biologically Inspired Rectified Spectral Units (ReSUs) Learns Hierarchical Features Without Error Backpropagation*, arXiv:2512.23146), this framework was extended to spatiotemporal sequence processing:

#### Past-Future Canonical Correlation Analysis (CCA)
To capture temporal dynamics without recurrence unfolding or BPTT, the ReSU constructs:
- **Past lag vector**: $\mathbf{p}_t = \left[ x_1(t), \dots, x_1(t-L+1), \dots, x_d(t), \dots, x_d(t-L+1) \right]^T \in \mathbb{R}^{d \cdot L}$
- **Future lag vector**: $\mathbf{f}_t = \left[ x_1(t+1), \dots, x_1(t+K), \dots, x_d(t+1), \dots, x_d(t+K) \right]^T \in \mathbb{R}^{d \cdot K}$

The unit seeks canonical filter directions $\mathbf{v}$ (past) and $\mathbf{u}$ (future) that maximize mutual predictive correlation:
$$\max_{\mathbf{v}, \mathbf{u}} \frac{\mathbf{v}^T \Sigma_{pf} \mathbf{u}}{\sqrt{(\mathbf{v}^T \Sigma_{pp} \mathbf{v})(\mathbf{u}^T \Sigma_{ff} \mathbf{u})}}$$
This maps to the generalized eigenvalue problem:
$$\Sigma_{pp}^{-1} \Sigma_{pf} \Sigma_{ff}^{-1} \Sigma_{fp} \mathbf{v} = \sigma^2 \mathbf{v}$$
In the online streaming ReSU implementation, this spectral decomposition is solved dynamically via a multi-dimensional similarity matching network where feedforward weights $W$ learn the canonical past directions $\mathbf{v}$ and lateral weights $M$ perform past-lag decorrelation.

#### Rectification Mechanism (ON / OFF Segregation)
Biological sensory systems do not transmit signed continuous values; they split bipolar signals into unipolar, non-negative channels (e.g., ON and OFF pathways in the retina and *Drosophila* lamina). 
The ReSU applies half-wave rectification to the linear projection:
$$\mathbf{y}_t^{(ON)} = \left[ \mathbf{v}^T \mathbf{p}_t \right]_+ = \max\left(0, \mathbf{v}^T \mathbf{p}_t\right)$$
$$\mathbf{y}_t^{(OFF)} = \left[ -\mathbf{v}^T \mathbf{p}_t \right]_+ = \max\left(0, -\mathbf{v}^T \mathbf{p}_t\right)$$
Under the non-negative similarity matching (NNSM) formulation, the fast recurrent equilibrium incorporates this non-negativity:
$$\mathbf{y}_t^* = \left[ (I + M)^{-1} W \mathbf{p}_t \right]_+$$
This rectification breaks linearity, introduces sparsity, and allows higher layers to construct nonlinear, phase-invariant, and direction-selective motion detectors.

---

## 7. Comparative Benchmarking Across Local Learning Paradigms

| Dimension | ReSU / NSM (Chklovskii 2026) | Predictive Coding (Rao & Ballard 1999) | Equilibrium Prop (Scellier & Bengio 2017) | Forward-Forward (Hinton 2022) | Direct Feedback Alignment (Lillicrap 2016) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Mathematical Principle** | Legendre-Fenchel min-max duality & similarity matching | Variational free energy minimization | Energy-based continuous attractor contrastive gradient | Layer-wise contrastive goodness maximization | Random fixed backward projection matrix $B$ |
| **Weight Transport ($W^T$)** | **STRICTLY NONE** (Independent feedforward $W$ & lateral $M$) | Requires $U^T$ unless separate feedback channels exist | **STRICTLY NONE** (Symmetric energy connections) | **STRICTLY NONE** (Forward-only passes) | **STRICTLY NONE** (Fixed random matrix $B$) |
| **Phase / Clamping Protocol** | **Continuous Single-Phase** (Two-timescale fast/slow relaxation) | Continuous two-variable relaxation (state + error) | **Two-Phase Sequential** (Free phase $\to$ Nudged phase) | **Two-Phase Sequential** (Positive data $\to$ Negative data) | **Two-Phase Sequential** (Forward pass $\to$ Backward pass) |
| **BPTT Requirement for Sequences** | **NONE** (Past lag embedding $\mathbf{p}_t$ converts time to space) | Requires state history storage across layers | Requires sequential unrolling for dynamic inputs | Requires recurrent unrolling for temporal sequences | Requires temporal gradient unrolling |
| **Biological Plausibility** | **EXTREME** (Oja-like Hebbian + Földiák anti-Hebbian + Dale's law) | Moderate (Requires separate representation and error neurons) | Moderate (Requires precise phase coordination & clamping) | Low-Moderate (Requires synthetic negative data generator) | Moderate (Fixed synaptic pathways, but locks forward pass) |
| **Hardware Realizability (SOENs)** | **NATIVE** (Continuous ODE $\leftrightarrow$ Superconducting loops) | High (Requires dual-rail error circuits) | Moderate (Requires global phase clocking) | Moderate (Requires dual data streaming) | High (Simple matrix multiplication) |

---

## 8. Core Scientific Questions (SQs) and Testable Hypotheses

To guide the 2028 IITP AI Wonchun Project, we establish three mathematically grounded, empirically falsifiable Scientific Questions:

### Scientific Question 1 (SQ1: Hub Repulsion & Griffiths Phase Width)
> **SQ1**: How does the degree of hub repulsion (quantified by the disassortativity exponent $\mu$ and hub-hub edge suppression $R(k_{hub}, k_{hub})$) quantitatively determine the parameter width of the extended Griffiths phase ($\Delta \lambda_{GP}$) and the network's resilience against runaway epileptic excitation in synthetic cortical connectomes?

- **Formal Hypothesis H1**: The width of the extended Griffiths phase $\Delta \lambda_{GP} = \lambda_{c2} - \lambda_{c1}$ (defined as the parameter range where avalanche size distributions obey scale-free power laws $P(S) \sim S^{-\tau}$ with $\tau \in [1.4, 1.6]$) scales monotonically with the hub repulsion exponent:
  $$\Delta \lambda_{GP} \propto \mu^\alpha, \quad \text{with } \alpha \in [0.8, 1.2]$$
  Furthermore, the critical runaway threshold $\lambda_{\text{runaway}}$ (the synaptic gain at which steady-state activity saturates $>90\%$ of network nodes) is elevated by at least a factor of $3.0$ in hub-repelling fractal graphs ($\mu > 0, R(k_{hub}, k_{hub}) \ll 1$) compared to degree-matched rich-club networks ($R(k_{hub}, k_{hub}) > 1$).
- **Experimental Observables**:
  1. Hub repulsion parameter $\mu$ fitted from $k_{nn}(k) \sim k^{-\mu}$.
  2. Susceptibility $\chi = \frac{1}{N} \sum_{i, j} (\langle s_i s_j \rangle - \langle s_i \rangle \langle s_j \rangle)$ across synaptic gain $\lambda$.
  3. Neuronal avalanche size distribution $P(S)$ and duration distribution $P(T)$.
- **Falsification Condition (Wrong-If-X)**:
  *Wrong if*: Rewiring a synthetic connectome to introduce direct rich-club hub-hub connections while strictly preserving the single-node degree sequence $P(k)$ yields an equal or wider parameter window of scale-free avalanches ($\Delta \lambda_{GP}^{\text{rich-club}} \ge \Delta \lambda_{GP}^{\text{fractal}}$), or if the onset of runaway epileptic saturation occurs at equal or higher synaptic gains in the rich-club network.

### Scientific Question 2 (SQ2: Multi-Scale Box-Covering & Local Temporal Learning Without BPTT)
> **SQ2**: Can a multi-scale neuromorphic network whose structural connectivity is generated by box-covering renormalization ($N_B \sim l_B^{-d_B}$) maintain temporal context and solve long-range sequence prediction tasks using purely local Hebbian/predictive plasticity (ReSU), matching the performance of global Backpropagation Through Time (BPTT) without storing backward activation states?

- **Formal Hypothesis H2**: A fractal modular network with depth $L = \log_{l_B} N$ coarse-grained scales exhibits an intrinsic hierarchy of relaxation timescales $\tau(l) = \tau_0 \cdot l_B^{z \cdot l}$. When endowed with local ReSU spectral predictive updates at each node:
  $$\Delta W_i = \eta (y_i x_i^T - y_i y_i^T W_i)$$
  the network solves sequence prediction tasks with temporal dependencies spanning $T \ge 10^3 \cdot \tau_0$ steps with test mean squared error within $5\%$ of an identical-capacity network trained with full BPTT, whereas non-fractal (random or fully connected) networks trained with the same local rule experience exponential memory degradation ($MSE \propto e^{T/\tau_0}$).
- **Experimental Observables**:
  1. Sequence prediction MSE on synthetic multi-timescale Markov and copy-memory tasks.
  2. Effective memory capacity $C(T) = \sum_{\tau=1}^T I(x(t-\tau); y(t))$.
  3. Computational memory footprint (peak RAM and gradient cache size during training).
- **Falsification Condition (Wrong-If-X)**:
  *Wrong if*: Increasing the box-covering depth $L$ provides no statistically significant extension of the temporal memory horizon $C(T)$ under local plasticity, or if the memory retention curve of the fractal network under local learning decays at the same exponential rate as an unstructured random recurrent network.

### Scientific Question 3 (SQ3: Triad Significance Profile & Energy-Information Trade-off)
> **SQ3**: Does the specific overrepresentation of Coherent Feedforward Loops (Triad 38) and Bi-Fan motifs characteristic of Superfamily 2 maximize the ratio of transmitted mutual information to metabolic energy dissipation ($I(X; Y) / \dot{E}$) under physical noise and bandwidth constraints, compared to randomized or purely feedforward chain topologies?

- **Formal Hypothesis H3**: Under noisy, Poisson-distributed input spikes ($\sigma_{\text{noise}} > 0$), circuits structured with the Superfamily 2 motif profile ($\vec{SP}$ dominated by Triad 38 and Bi-fans) achieve an information-transmission energy efficiency:
  $$\eta_{\text{info}} = \frac{I(X_{\text{input}}; Y_{\text{output}})}{\int_0^T \dot{E}(t) dt}$$
  that is at least $40\%$ higher than in degree-matched randomized null networks or linear feedforward chains, because cFFL sign-sensitive delays eliminate non-informative noise transitions while bi-fans provide maximal code redundancy per Joule.
- **Experimental Observables**:
  1. Transmitted mutual information $I(X; Y)$ in bits between input stimulus and target readout.
  2. Dissipated energy calculated via continuous SOENs Lagrangian loss $\dot{E} = \sum_i s_i^2 / \tau_i$.
  3. Bit-per-Joule efficiency ratio $\eta_{\text{info}}$.
- **Falsification Condition (Wrong-If-X)**:
  *Wrong if*: Under equal input noise variance $\sigma_{\text{noise}}^2$ and average firing rates, linear feedforward chains or random recurrent triads yield an equal or higher information efficiency $\eta_{\text{info}}$ than the Superfamily 2 motif architecture.

---

## 9. References

1. Milo, R., Shen-Orr, S., Itzkovitz, S., Kashtan, N., Chklovskii, D., & Alon, U. (2002). Network motifs: simple building blocks of complex networks. *Science*, 298(5594), 824-827.
2. Milo, R., Itzkovitz, S., Kashtan, N., Levitt, R., Shen-Orr, S., Ayzenshtat, I., Sheffer, M., & Alon, U. (2004). Superfamilies of evolved and designed networks. *Science*, 303(5663), 1538-1542.
3. Song, C., Havlin, S., & Makse, H. A. (2005). Self-similarity of complex networks. *Nature*, 433(7024), 392-395.
4. Song, C., Havlin, S., & Makse, H. A. (2006). Origins of fractality in the growth of complex networks. *Nature Physics*, 2(4), 275-281.
5. Qin, S., Pughe-Sanford, R., Genkin, M., Özdil, P. G., Greengard, L., Sengupta, A. M., & Chklovskii, D. B. (2026). A Network of Biologically Inspired Rectified Spectral Units (ReSUs) Learns Hierarchical Features Without Error Backpropagation. *AAAI Conference on Artificial Intelligence (AAAI 2026)*, arXiv:2512.23146.
6. Pehlevan, C., & Chklovskii, D. B. (2014). A normative theory of adaptive dimensionality reduction in neural networks. *Advances in Neural Information Processing Systems (NeurIPS 2014)*, 27.
7. Pehlevan, C., Sengupta, A. M., & Chklovskii, D. B. (2018). Why do similarity matching objectives lead to Hebbian/anti-Hebbian networks? *Neural Computation*, 30(1), 84-124.
8. Moretti, P., & Muñoz, M. A. (2013). Griffiths phases and the stretching of criticality in brain networks. *Nature Communications*, 4(1), 2521.
9. Kaiser, M., & Hilgetag, C. C. (2010). Optimal hierarchical modular topologies for producing limited sustained activation of neural networks. *Frontiers in Neuroinformatics*, 4, 8.
10. Shainline, J. M., Buckley, S. M., Mirin, R. P., & Nam, S. W. (2017). Superconducting optoelectronic circuits for neuromorphic computing. *Physical Review Applied*, 7(3), 034013.
11. Buzsáki, G. (2019). *The Brain from Inside Out*. Oxford University Press.
12. Behrouz, A., Peebles, N., et al. (2024/2025). Titans: Learning to Memorize at Test Time. *arXiv:2501.00663*.
13. Keramati, M., & Gutkin, B. (2014). Homeostatic reinforcement learning for integrating reward collection and physiological stability. *eLife*, 3, e04811.
