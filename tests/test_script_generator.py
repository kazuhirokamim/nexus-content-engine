"""Testes unitários para ScriptGenerator no Nexus Content Engine - Padrão Tear Rule #3."""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from script_generator import ScriptGenerator, VideoScript


class TestScriptGenerator(unittest.TestCase):
    """Garante integridade e estabilidade do gerador de roteiros multi-nicho."""

    def setUp(self):
        self.generator = ScriptGenerator()

    def test_happy_path_gta6_niche(self):
        """Cenário 1: Caminho feliz com pauta de GTA 6."""
        topic = "mapa expandido de Vice City"
        script = self.generator.generate(topic, niche="gta6")

        self.assertIsInstance(script, VideoScript)
        self.assertEqual(script.topic, topic)
        self.assertEqual(script.niche, "gta6")
        self.assertIn("Atenção:", script.hook)
        self.assertTrue(len(script.body_paragraphs) >= 3)
        self.assertIn("E se você achava", script.loop_cta)
        self.assertGreater(script.estimated_duration_seconds, 30)

    def test_happy_path_generic_niche(self):
        """Cenário 2: Caminho feliz com nicho alternativo (ex: tech)."""
        topic = "modelos de IA locais"
        script = self.generator.generate(topic, niche="tech")

        self.assertIsInstance(script, VideoScript)
        self.assertEqual(script.niche, "tech")
        self.assertIn("muda completamente o jogo", script.hook)
        self.assertIn("mais surpreendente", script.loop_cta)

    def test_edge_case_and_error_handling(self):
        """Cenário 3: Casos de borda e resiliência."""
        topic = "Niche @#$% 12345"
        script = self.generator.generate(topic, niche="desconhecido")
        self.assertEqual(script.topic, topic)
        self.assertIn(topic, script.full_text())


if __name__ == "__main__":
    unittest.main()
