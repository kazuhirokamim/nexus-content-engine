"""Testes unitários para TTSEngine - Padrão Tear Rule #3 (TDD).

Governança: Cânone Tear & Noesis QA Swarm.
Regra #24: Orçamento de linhas < 700.
"""

import os
import sys
import unittest
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from core.tts_engine import TTSEngine, AudioResult, WordTimestamp


class TestTTSEngine(unittest.TestCase):
    """Garante estabilidade, tratamento de erros e integridade do gerador de áudio neural."""

    def setUp(self):
        # Localiza o modelo piper se disponível
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        model_path = os.path.join(base_dir, "models", "piper", "pt_BR-faber-medium.onnx")
        self.model_path = model_path if os.path.exists(model_path) else None
        self.engine = TTSEngine(lang="pt", model_path=self.model_path, use_whisper=True)
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        for f in os.listdir(self.temp_dir):
            try:
                os.remove(os.path.join(self.temp_dir, f))
            except Exception:
                pass
        try:
            os.rmdir(self.temp_dir)
        except Exception:
            pass

    def test_happy_path_neural_synthesis_and_whisper_alignment(self):
        """Cenário 1: Caminho feliz com síntese neural e alinhamento acústico Whisper."""
        text = "O GTA 6 terá gráficos incríveis em Vice City."
        out_audio = os.path.join(self.temp_dir, "teste_happy.wav")
        out_srt = os.path.join(self.temp_dir, "teste_happy.srt")

        result = self.engine.synthesize(text, out_audio)

        self.assertIsInstance(result, AudioResult)
        self.assertTrue(os.path.exists(out_audio))
        self.assertGreater(os.path.getsize(out_audio), 1000)
        self.assertGreater(result.duration_seconds, 0.5)
        self.assertGreater(len(result.words), 0)

        # Valida precisão dos timestamps acústicos do Whisper
        first_word = result.words[0]
        self.assertIsInstance(first_word, WordTimestamp)
        self.assertGreaterEqual(first_word.start_seconds, 0.0)
        self.assertGreater(first_word.end_seconds, first_word.start_seconds)

        # Teste de exportação SRT com formatação karaokê
        srt_path = self.engine.export_srt(result.words, out_srt, words_per_chunk=3)
        self.assertTrue(os.path.exists(srt_path))
        with open(srt_path, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("00:00:", content)
            self.assertIn("-->", content)

    def test_edge_case_special_characters_and_punctuation(self):
        """Cenário 2: Caso de borda com pontuação densa e números."""
        text = "Vazou: R$ 350,00?! Sim... @RockstarGames #GTA6 100%!"
        out_audio = os.path.join(self.temp_dir, "teste_edge.wav")

        result = self.engine.synthesize(text, out_audio)
        self.assertTrue(os.path.exists(out_audio))
        self.assertGreater(len(result.words), 0)

    def test_error_path_empty_text(self):
        """Cenário 3: Caminho de erro com texto vazio ou apenas espaços."""
        out_audio = os.path.join(self.temp_dir, "teste_vazio.wav")
        with self.assertRaises(ValueError):
            self.engine.synthesize("", out_audio)

        with self.assertRaises(ValueError):
            self.engine.synthesize("   \n\t  ", out_audio)

    def test_fallback_resilience_without_piper_model(self):
        """Cenário 4: Resiliência e fallback gracioso caso modelo Piper não exista."""
        fallback_engine = TTSEngine(lang="pt", model_path="/caminho/inexistente/modelo.onnx", use_whisper=False)
        out_audio = os.path.join(self.temp_dir, "teste_fallback.mp3")

        result = fallback_engine.synthesize("Teste defensivo de fallback acústico.", out_audio)
        self.assertTrue(os.path.exists(out_audio))
        self.assertGreater(result.duration_seconds, 0.5)
        self.assertGreater(len(result.words), 0)


if __name__ == "__main__":
    unittest.main()
