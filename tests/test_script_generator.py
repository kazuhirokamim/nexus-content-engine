"""Testes unitários para ScriptGenerator - Padrão Tear Rule #3."""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from script_generator import ScriptGenerator, VideoScript


class TestScriptGenerator(unittest.TestCase):
    """Garante integridade e estabilidade do gerador de roteiros."""

    def setUp(self):
        self.generator = ScriptGenerator()

    def test_happy_path_generation(self):
        """Cenário 1: Caminho feliz com pauta válida."""
        topic = "mapa expandido de Vice City"
        script = self.generator.generate(topic)

        self.assertIsInstance(script, VideoScript)
        self.assertEqual(script.topic, topic)
        self.assertIn("Atenção:", script.hook)
        self.assertTrue(len(script.body_paragraphs) >= 3)
        self.assertIn("E se você achava", script.loop_cta)
        self.assertGreater(script.estimated_duration_seconds, 30)
        self.assertLess(script.estimated_duration_seconds, 60)

    def test_edge_case_empty_or_minimal_topic(self):
        """Cenário 2: Caso de borda com tópico curto ou caracteres especiais."""
        topic = "GTA VI 4K HDR! @#$% &"
        script = self.generator.generate(topic)

        self.assertIsInstance(script, VideoScript)
        self.assertIn(topic, script.hook)
        full_text = script.full_text()
        self.assertIn(topic, full_text)

    def test_error_path_non_string_topic(self):
        """Cenário 3: Tratamento de tipos inesperados."""
        # Se passado None ou número, converte ou trata sem quebrar
        script = self.generator.generate(str(12345))
        self.assertIn("12345", script.hook)


if __name__ == "__main__":
    unittest.main()
