"""Testes unitários para TTSEngine - Padrão Tear Rule #3."""

import os
import unittest
import sys
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from core.tts_engine import TTSEngine, AudioResult, WordTimestamp


class TestTTSEngine(unittest.TestCase):
    """Garante estabilidade, tratamento de erros e integridade do gerador de áudio."""

    def setUp(self):
        self.engine = TTSEngine(lang="pt", tld="com.br")
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Limpeza segura de arquivos temporários de teste
        for f in os.listdir(self.temp_dir):
            try:
                os.remove(os.path.join(self.temp_dir, f))
            except Exception:
                pass
        try:
            os.rmdir(self.temp_dir)
        except Exception:
            pass

    def test_happy_path_synthesis_and_srt(self):
        """Cenário 1: Caminho feliz com texto válido e exportação de legendas."""
        text = "O GTA 6 terá gráficos revolucionários em Vice City."
        out_audio = os.path.join(self.temp_dir, "teste_audio.mp3")
        out_srt = os.path.join(self.temp_dir, "teste_legendas.srt")

        result = self.engine.synthesize(text, out_audio)

        self.assertIsInstance(result, AudioResult)
        self.assertTrue(os.path.exists(out_audio))
        self.assertGreater(os.path.getsize(out_audio), 1000)
        self.assertGreater(result.duration_seconds, 1.0)
        self.assertEqual(len(result.words), 9)

        # Teste de exportação SRT
        srt_path = self.engine.export_srt(result.words, out_srt, words_per_chunk=3)
        self.assertTrue(os.path.exists(srt_path))
        with open(srt_path, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("00:00:", content)
            self.assertIn("GTA 6", content)

    def test_edge_case_special_characters_and_punctuation(self):
        """Cenário 2: Caso de borda com pontuação densa e números."""
        text = "Vazou: R$ 350,00?! Sim... @RockstarGames #GTA6 100%!"
        out_audio = os.path.join(self.temp_dir, "teste_edge.mp3")

        result = self.engine.synthesize(text, out_audio)
        self.assertTrue(os.path.exists(out_audio))
        self.assertGreater(len(result.words), 0)

    def test_error_path_empty_text(self):
        """Cenário 3: Caminho de erro com texto vazio ou apenas espaços."""
        out_audio = os.path.join(self.temp_dir, "teste_vazio.mp3")
        with self.assertRaises(ValueError):
            self.engine.synthesize("", out_audio)

        with self.assertRaises(ValueError):
            self.engine.synthesize("   \n\t  ", out_audio)


if __name__ == "__main__":
    unittest.main()
