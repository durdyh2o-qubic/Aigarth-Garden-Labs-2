# Aigarth-Garden-Labs

**Public Observatory for Qubic Aigarth Hyperidentity Evolution**  
*May 2026*

A living garden laboratory studying the growth of the **Intelligent Tissue** through Useful Proof-of-Work (uPoW), local ternary hyperidentity simulations, mining logs, and agentic analysis.

## Current Status (May 10, 2026)
- Best Fitness: **0.303941**
- Stable Plateau: ~0.3035 – 0.3039
- Latest 120-gen run: **0.303701**

## Quick Start

```bash
git clone https://github.com/durdyh2o-qubic/Aigarth-Garden-Labs-2.git
cd Aigarth-Garden-Labs-2

python3 -m venv garden_venv
source garden_venv/bin/activate
pip install numpy pandas matplotlib click

cd simulations
python run_experiment.py --mut 0.20 --gens 60 --pop 128 --seed 2354D8B800D56AD4831F93FA895050EA74C4778CDC1055133AFA5CC4C7B8C984
