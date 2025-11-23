# -*- coding: utf-8 -*-
"""
Pytest configuration and shared fixtures for Modelo X Framework tests.
"""

import sys
import os
import pytest
import numpy as np

# Ensure src is in path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from model_x import (
    EntropySyntropyCalculator,
    EnergyModulationEngine,
    SimulationEngine,
    ModelXVisualizer,
    ValidationUtils,
    EnergyModulatedModel
)
from model_x.patterned_datasets import create_patterned_datasets


# ==================== Fixtures: Calculators ====================

@pytest.fixture
def calculator():
    """Provides an EntropySyntropyCalculator instance."""
    return EntropySyntropyCalculator()


@pytest.fixture
def modulator():
    """Provides an EnergyModulationEngine instance."""
    return EnergyModulationEngine()


# ==================== Fixtures: Simulation ====================

@pytest.fixture
def simulation_engine():
    """Provides a SimulationEngine with default settings."""
    return SimulationEngine(dt=0.01, max_steps=1000)


@pytest.fixture
def small_simulation_engine():
    """Provides a SimulationEngine for quick tests."""
    return SimulationEngine(dt=0.01, max_steps=50)


# ==================== Fixtures: Visualization ====================

@pytest.fixture
def visualizer():
    """Provides a ModelXVisualizer instance."""
    return ModelXVisualizer()


# ==================== Fixtures: Utils ====================

@pytest.fixture
def validation_utils():
    """Provides a ValidationUtils instance."""
    return ValidationUtils()


# ==================== Fixtures: Models ====================

@pytest.fixture
def balanced_model():
    """Provides an EnergyModulatedModel with balanced parameters."""
    return EnergyModulatedModel(entropy=0.5, syntropy=0.5, energy=1.0)


@pytest.fixture
def syntropy_dominant_model():
    """Provides an EnergyModulatedModel with syntropy dominant."""
    return EnergyModulatedModel(entropy=0.2, syntropy=0.8, energy=1.0)


@pytest.fixture
def entropy_dominant_model():
    """Provides an EnergyModulatedModel with entropy dominant."""
    return EnergyModulatedModel(entropy=0.8, syntropy=0.2, energy=1.0)


# ==================== Fixtures: States ====================

@pytest.fixture
def balanced_state():
    """Provides a balanced initial state dictionary."""
    return {'entropy': 0.5, 'syntropy': 0.5, 'energy': 1.0}


@pytest.fixture
def syntropy_dominant_state():
    """Provides a syntropy-dominant initial state dictionary."""
    return {'entropy': 0.3, 'syntropy': 0.7, 'energy': 1.5}


@pytest.fixture
def entropy_dominant_state():
    """Provides an entropy-dominant initial state dictionary."""
    return {'entropy': 0.7, 'syntropy': 0.3, 'energy': 1.5}


# ==================== Fixtures: Data ====================

@pytest.fixture
def sample_data_uniform():
    """Provides uniformly distributed sample data."""
    return list(np.random.uniform(0, 1, 100))


@pytest.fixture
def sample_data_normal():
    """Provides normally distributed sample data."""
    return list(np.random.normal(0.5, 0.1, 100))


@pytest.fixture
def sample_data_sinusoidal():
    """Provides sinusoidal sample data (low entropy)."""
    t = np.linspace(0, 4 * np.pi, 100)
    return list(np.sin(t) + 1)  # Shift to positive values


@pytest.fixture
def sample_data_constant():
    """Provides constant sample data (minimal entropy)."""
    return [0.5] * 100


@pytest.fixture
def patterned_datasets():
    """Provides the patterned datasets."""
    return create_patterned_datasets()


@pytest.fixture
def default_datasets(validation_utils):
    """Provides the default validation datasets."""
    return validation_utils.create_default_datasets()


# ==================== Fixtures: Simulation History ====================

@pytest.fixture
def sample_simulation_history():
    """Provides a sample simulation history for testing."""
    return [
        {'step': 0, 'time': 0.0, 'state': {'entropy': 0.5, 'syntropy': 0.5, 'energy': 1.0}, 'dilation': 1.0},
        {'step': 1, 'time': 0.01, 'state': {'entropy': 0.51, 'syntropy': 0.49, 'energy': 0.999}, 'dilation': 0.98},
        {'step': 2, 'time': 0.02, 'state': {'entropy': 0.52, 'syntropy': 0.48, 'energy': 0.998}, 'dilation': 0.96},
        {'step': 3, 'time': 0.03, 'state': {'entropy': 0.53, 'syntropy': 0.47, 'energy': 0.997}, 'dilation': 0.94},
        {'step': 4, 'time': 0.04, 'state': {'entropy': 0.54, 'syntropy': 0.46, 'energy': 0.996}, 'dilation': 0.92},
    ]


# ==================== Fixtures: File Cleanup ====================

@pytest.fixture
def temp_json_file(tmp_path):
    """Provides a temporary JSON file path that is cleaned up after test."""
    return str(tmp_path / "test_output.json")


# ==================== Helper Functions ====================

def assert_valid_entropy(value):
    """Assert that a value is a valid entropy (0 <= value <= 1)."""
    assert isinstance(value, (int, float)), f"Expected numeric type, got {type(value)}"
    assert 0.0 <= value <= 1.0, f"Expected value in [0, 1], got {value}"


def assert_valid_syntropy(value):
    """Assert that a value is a valid syntropy (0 <= value <= 1)."""
    assert isinstance(value, (int, float)), f"Expected numeric type, got {type(value)}"
    assert 0.0 <= value <= 1.0, f"Expected value in [0, 1], got {value}"


def assert_valid_energy(value, min_energy=0.1):
    """Assert that a value is a valid energy (>= min_energy)."""
    assert isinstance(value, (int, float)), f"Expected numeric type, got {type(value)}"
    assert value >= min_energy, f"Expected energy >= {min_energy}, got {value}"


def assert_valid_state(state):
    """Assert that a state dictionary has valid structure and values."""
    assert isinstance(state, dict), f"Expected dict, got {type(state)}"
    assert 'entropy' in state, "State missing 'entropy' key"
    assert 'syntropy' in state, "State missing 'syntropy' key"
    assert 'energy' in state, "State missing 'energy' key"
    assert_valid_entropy(state['entropy'])
    assert_valid_syntropy(state['syntropy'])
    assert_valid_energy(state['energy'])


# Make helpers available as fixtures too
@pytest.fixture
def state_validator():
    """Provides the assert_valid_state function."""
    return assert_valid_state
