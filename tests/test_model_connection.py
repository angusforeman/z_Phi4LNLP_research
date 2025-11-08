"""Test model connectivity."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from translator import Translator


def test_model_available():
    """Verify Phi4 model is available in Ollama."""
    translator = Translator(model_name="phi4")
    assert translator.check_model_available(), "Phi4 model not found in Ollama"


def test_model_responds():
    """Verify model can respond to a simple prompt."""
    translator = Translator(model_name="phi4")
    
    response = translator.translate("Say hello")
    
    assert response is not None
    assert response.response_time > 0
