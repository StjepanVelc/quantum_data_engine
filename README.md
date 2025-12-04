⚛ Quantum Data Engine

A modular simulation engine for quantum-inspired data structures, graph networks, storage engines and animated visualization.

<p align="center"> <img src="preview.png" width="640"> </p>
✨ Overview

Quantum Data Engine is a Python framework that combines ideas from:

Quantum computing

Graph networks

Database internals

Simulation and visualization

It is not a physics-accurate simulator — rather a conceptual engine showing how quantum-like behavior can be implemented in software.

🧩 Core Features
⚛ Quantum Nodes

amplitude (0–1)

energy state

links to other nodes

entanglement pairs

decoherence & stabilization

🌐 Quantum Graph

dynamic linking/unlinking

global amplitude decay

cleaning unstable nodes

visual layout generation

🔍 Search Engine

filter by amplitude

filter by energy

filter by value

combined multi-query filters

ranking by stability score

💾 Storage Engine

Inspired by real databases (SQLite, PostgreSQL):

Write-Ahead Log (WAL)

Shadow copy

Snapshots

Automatic recovery

🎨 Visualization

static graph rendering

animated amplitude drift

color-mapped amplitudes

energy-scaled node sizes

🚀 Run Project
python -m venv venv
.\venv\Scripts\activate

pip install -r requirements.txt
python main.py

📂 Project Structure
engine/      # Quantum logic
storage/     # WAL + snapshots + search
utils/       # hashing, logger, errors
visuals/     # plotting and animation
main.py      # entry point

🛠 Technologies

Python 3.10+

NetworkX

matplotlib

numpy