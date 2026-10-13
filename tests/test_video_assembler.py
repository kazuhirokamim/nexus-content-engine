"""Testes unitários para VideoAssembler - Padrão Tear Rule #3 (TDD).

Governança: Cânone Tear & Noesis QA Swarm.
Regra #24: Orçamento de linhas < 700.
"""

import os
import sys
import unittest
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from core.video_assembler import VideoAssembler, VideoRenderResult
from core.tts_engine import TTSEngine


class TestVideoAssembler(unittest.TestCase):
    """Garante estabilidade, renderização e tratamento de exceções no FFmpeg."""

    def setUp(self):
        self.assembler = VideoAssembler()
        self.tts = TTSEngine(use_whisper=False)
        self.temp_dir = tempfile.mkdtemp()

        # Cria um pequeno arquivo de áudio para teste
        self.audio_path = os.path.join(self.temp_dir, "test_audio.mp3")
        self.srt_path = os.path.join(self.temp_dir, "test_sub.srt")
        res = self.tts.synthesize("Teste rápido de vídeo para o Nexus Engine.", self.audio_path)
        self.tts.export_srt(res.words, self.srt_path)

        # Caminho do b_roll real baixado se disponível
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        broll_cand = os.path.join(base_dir, "presets", "gta6", "b_roll", "gameplay_01.mp4")
        self.real_broll = broll_cand if os.path.exists(broll_cand) else None

        # Caminho da trilha de fundo se disponível
        bg_cand = os.path.join(base_dir, "presets", "gta6", "audio", "background_synthwave.mp3")
        self.bg_music = bg_cand if os.path.exists(bg_cand) else None

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

    def test_happy_path_render_with_real_broll_and_music(self):
        """Cenário 1: Caminho feliz com B-roll de gameplay real e trilha de fundo."""
        out_mp4 = os.path.join(self.temp_dir, "output_happy_real.mp4")
        result = self.assembler.render(
            audio_path=self.audio_path,
            output_path=out_mp4,
            b_roll_path=self.real_broll,
            background_music_path=self.bg_music,
            subtitles_path=self.srt_path,
            resolution=(540, 960),  # Resolução leve 9:16 para agilidade de teste
            fps=24
        )

        self.assertIsInstance(result, VideoRenderResult)
        self.assertTrue(os.path.exists(out_mp4))
        self.assertGreater(os.path.getsize(out_mp4), 10000)
        self.assertEqual(result.width, 540)
        self.assertEqual(result.height, 960)

    def test_edge_case_render_without_subtitles_or_music(self):
        """Cenário 2: Caso de borda sem arquivo de legenda nem trilha de fundo."""
        out_mp4 = os.path.join(self.temp_dir, "output_no_subs.mp4")
        result = self.assembler.render(
            audio_path=self.audio_path,
            output_path=out_mp4,
            b_roll_path=self.real_broll,
            background_music_path=None,
            subtitles_path=None,
            resolution=(540, 960),
            fps=24
        )
        self.assertTrue(os.path.exists(out_mp4))

    def test_error_path_nonexistent_audio(self):
        """Cenário 3: Caminho de erro com áudio inexistente."""
        out_mp4 = os.path.join(self.temp_dir, "output_err.mp4")
        with self.assertRaises(FileNotFoundError):
            self.assembler.render(
                audio_path="/caminho/falso/inexistente.mp3",
                output_path=out_mp4
            )


if __name__ == "__main__":
    unittest.main()
