"""Testes unitários para VideoAssembler - Padrão Tear Rule #3."""

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
        self.tts = TTSEngine()
        self.temp_dir = tempfile.mkdtemp()

        # Cria um pequeno arquivo de áudio real de 2 segundos para teste
        self.audio_path = os.path.join(self.temp_dir, "test_audio.mp3")
        self.srt_path = os.path.join(self.temp_dir, "test_sub.srt")
        res = self.tts.synthesize("Teste rápido de vídeo para o Nexus Engine.", self.audio_path)
        self.tts.export_srt(res.words, self.srt_path)

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

    def test_happy_path_render_with_fallback_background(self):
        """Cenário 1: Caminho feliz gerando vídeo 9:16 vertical com fundo gerado."""
        out_mp4 = os.path.join(self.temp_dir, "output_happy.mp4")
        result = self.assembler.render(
            audio_path=self.audio_path,
            output_path=out_mp4,
            subtitles_path=self.srt_path,
            resolution=(540, 960),  # Resolução leve 9:16 para agilidade de teste
            fps=24
        )

        self.assertIsInstance(result, VideoRenderResult)
        self.assertTrue(os.path.exists(out_mp4))
        self.assertGreater(os.path.getsize(out_mp4), 5000)
        self.assertEqual(result.width, 540)
        self.assertEqual(result.height, 960)

    def test_edge_case_render_without_subtitles(self):
        """Cenário 2: Caso de borda sem arquivo de legenda."""
        out_mp4 = os.path.join(self.temp_dir, "output_no_subs.mp4")
        result = self.assembler.render(
            audio_path=self.audio_path,
            output_path=out_mp4,
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
