#!/usr/bin/env python3
\"\"\"Basic usage example of Modelo X Framework\"\"\"
import sys
sys.path.insert(0, '../src')
from model_x import EntropySyntropyCalculator, SimulationEngine

def main():
    \"\"\"Basic example\"\"\"
    print(\"🔬 Modelo X Framework - Basic Example\")
    print(\"=\"*50)
    
    # Initialize components
    calc = EntropySyntropyCalculator()
    sim = SimulationEngine()
    
    # Run validation
    results = sim.run_validation()
    
    print(f\"✅ Framework executed successfully!\")
    print(f\"📊 Validation Score: {results['overall_score']:.1f}/100\")
    print(f\"📁 Files generated: validation_*_final.json\")

if __name__ == '__main__':
    main()
