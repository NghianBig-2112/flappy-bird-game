# 🐦 Flappy Bird AI - Genetic Algorithm & Neural Network from Scratch

A Python/Pygame implementation of the classic Flappy Bird game powered by an AI agent trained via **Genetic Algorithm (GA)** and a **Custom Single-Layer Perceptron** built completely from scratch (no external ML black-box frameworks).

Includes an interactive **Human vs. AI Solo Mode** to test your skills against the trained champion model!

---

## 📸 Demo Preview

<!-- Gợi ý: Thay link ảnh/gif thực tế của bạn vào đây -->
![Training Demo](assets/demo_training.gif)
*(Training mode with real-time raycasting vision & Human vs. AI duel mode)*

---

## 🌟 Key Highlights

- **Built from Scratch**: Zero reliance on high-level ML libraries (like NEAT or PyTorch). All neural activations (Sigmoid), linear algebra (dot products), and genetic operators are implemented natively with NumPy.
- **Raycasting Perception**: Real-time visual rays highlighting the inputs processed by the bird's brain.
- **Human vs. AI Mode**: Load the serialized champion weights (`best_bird.json`) and challenge the AI head-to-head.
- **Fast Convergence**: Reaches superhuman survival scores (50+ pipes) within just a few generations.

---

## 🧠 AI Brain Architecture

The bird makes flight decisions using a single artificial neuron (Perceptron):

$$\text{Output} = \sigma \left( \sum_{i=1}^{5} w_i \cdot x_i + b \right)$$

Decision rule: If $\text{Output} > 0.45$ and the bird is currently falling ($\text{velocity} > 0$), it triggers a flap (`fly_up()`).

### Input Features ($x_1 \dots x_5$ normalized):
| Feature | Description | Normalization |
| :--- | :--- | :--- |
| **$x_1$** | Bird's Y position (center) | Divided by screen height |
| **$x_2$** | Current vertical velocity | Divided by 10 |
| **$x_3$** | Horizontal distance to nearest pipe | Divided by screen width |
| **$x_4$** | Vertical distance to the top pipe gap | Divided by screen height |
| **$x_5$** | Vertical distance to the bottom pipe gap | Divided by screen height |
| **$b$** | Neuron bias | Learnable parameter |

---

## 🧬 Genetic Algorithm Pipeline

1. **Population**: 30 birds per generation, each carrying a 6-parameter chromosome ($[w_1, w_2, w_3, w_4, w_5, b]$).
2. **Fitness Function**:
   $$\text{Fitness} = \text{Score} \times 100 + \text{Survival Time}$$
   Prioritizes clearing pipes while rewarding birds that stay alive longer.
3. **Selection**: Top 50% highest-fitness birds survive to form the parent pool.
4. **Elitism**: The single best-performing individual is directly passed to the next generation without mutation.
5. **Uniform Crossover**: Genes are randomly inherited with a 50/50 probability from either parent.
6. **Gaussian Mutation**: 10% chance per gene to mutate with noise sampled from $\mathcal{N}(0, 0.3^2)$.
7. **Model Checkpointing**: Automatically serializes the chromosome to `best_bird.json` once a bird hits 50 points.

---

## 📁 Project Structure

```text
├── assets/                             # Sprites and visual assets
├── best_bird.json                      # Trained champion chromosome weights
├── flappy_bird_base.py                 # Original human-playable Flappy Bird
├── flappy_bird_genetic_algorithm.py    # Training simulation with GA visualization
├── main.py                             # Interactive Human vs. AI battle mode
├── requirements.txt                    # Project dependencies
└── README.md                           # Documentation
```

---

## 🚀 Quick Start

### 1. Clone & Install Dependencies
```bash
git clone https://github.com/your-username/flappy-bird-genetic-algorithm.git
cd flappy-bird-genetic-algorithm
pip install -r requirements.txt
```

### 2. Play Human vs. AI (Solo Mode)
Challenge the pre-trained champion AI:
```bash
python main.py
```
- Controls: Press `SPACE` to flap.

### 3. Train from Scratch
Watch the population evolve in real-time:
```bash
python flappy_bird_genetic_algorithm.py
```

---

## 🛠️ Tech Stack
- **Language**: Python 3.10+
- **Graphics & Physics**: Pygame
- **Math & Computing**: NumPy
- **Persistence**: JSON