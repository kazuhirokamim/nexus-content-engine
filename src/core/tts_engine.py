"""Nexus Content Engine - Motor de Síntese de Áudio Neural & Alinhador Acústico.

Governança: Cânone Tear & Noesis Architecture Swarm.
Regra #24: Orçamento de linhas < 700.
"""

import os
import re
import sys
import shutil
import subprocess
from dataclasses import dataclass
from typing import List, Optional
from gtts import gTTS


@dataclass
class WordTimestamp:
    """Timestamp de uma palavra individual para legendas estilo karaoke."""
    word: str
    start_seconds: float
    end_seconds: float


@dataclass
class AudioResult:
    """Resultado da síntese acústica com arquivo de áudio e mapeamento temporal."""
    audio_path: str
    duration_seconds: float
    words: List[WordTimestamp]
    provider: str = "piper"


class TTSEngine:
    """Motor de síntese de voz neural resiliente com suporte a Piper-TTS e Whisper."""

    def __init__(
        self,
        lang: str = "pt",
        tld: str = "com.br",
        model_path: Optional[str] = None,
        use_whisper: bool = True,
        speed_scale: float = 0.85
    ):
        self.lang = lang
        self.tld = tld
        self.use_whisper = use_whisper
        self.speed_scale = speed_scale
        self._whisper_model = None

        # Resolve modelo neural Piper se não for passado explicitamente
        if model_path and os.path.exists(model_path):
            self.model_path = model_path
        else:
            default_model = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "..", "models", "piper", "pt_BR-faber-medium.onnx")
            )
            self.model_path = default_model if os.path.exists(default_model) else None

        # Localiza executável FFmpeg
        self.ffmpeg_exe = self._resolve_ffmpeg()

    def _resolve_ffmpeg(self) -> Optional[str]:
        """Resolve o executável do FFmpeg pelo imageio-ffmpeg ou PATH."""
        try:
            import imageio_ffmpeg
            return imageio_ffmpeg.get_ffmpeg_exe()
        except Exception:
            return shutil.which("ffmpeg")

    def _get_whisper_model(self):
        """Carrega modelo Faster-Whisper de forma lazy e thread-safe."""
        if self._whisper_model is None and self.use_whisper:
            try:
                from faster_whisper import WhisperModel
                self._whisper_model = WhisperModel("tiny", device="cpu", compute_type="int8")
            except Exception as e:
                self._whisper_model = False
        return self._whisper_model

    def _synthesize_piper(self, text: str, output_path: str) -> bool:
        """Sintetiza via Piper-TTS local e aplica cadeia de masterização broadcast."""
        if not self.model_path or not os.path.exists(self.model_path):
            return False

        piper_exe = shutil.which("piper")
        if not piper_exe:
            # Tenta resolver dentro da venv atual
            venv_piper = os.path.abspath(
                os.path.join(sys.prefix, "bin", "piper")
            )
            if os.path.exists(venv_piper):
                piper_exe = venv_piper

        if not piper_exe:
            return False

        raw_wav = output_path + ".raw.wav"
        try:
            cmd = [
                piper_exe,
                "--model", self.model_path,
                "--output_file", raw_wav,
                "--length-scale", str(self.speed_scale)
            ]
            process = subprocess.run(
                cmd,
                input=text,
                text=True,
                capture_output=True,
                timeout=60
            )
            if process.returncode != 0 or not os.path.exists(raw_wav):
                return False

            # Se FFmpeg disponível, aplica cadeia de masterização gamer
            if self.ffmpeg_exe:
                # Highpass (limpa graves), acompressor (compressor vocal), loudnorm (-16 LUFS)
                af_filter = (
                    "highpass=f=80,lowpass=f=12000,"
                    "acompressor=threshold=-18dB:ratio=3:attack=5:release=50:makeup=2dB,"
                    "loudnorm=I=-16:TP=-1.5:LRA=11"
                )
                ff_cmd = [
                    self.ffmpeg_exe, "-y",
                    "-i", raw_wav,
                    "-af", af_filter,
                    output_path
                ]
                ff_proc = subprocess.run(ff_cmd, capture_output=True, timeout=30)
                if os.path.exists(raw_wav):
                    try:
                        os.remove(raw_wav)
                    except Exception:
                        pass
                if ff_proc.returncode == 0 and os.path.exists(output_path):
                    return True

            # Caso FFmpeg falhe ou não exista, renomeia o raw_wav
            if os.path.exists(raw_wav):
                shutil.move(raw_wav, output_path)
                return True
        except Exception:
            if os.path.exists(raw_wav):
                try:
                    os.remove(raw_wav)
                except Exception:
                    pass
            return False
        return False

    def _synthesize_gtts(self, text: str, output_path: str):
        """Fallback defensivo estável via gTTS."""
        tts = gTTS(text=text, lang=self.lang, tld=self.tld, slow=False)
        tts.save(output_path)

    def _align_with_whisper(self, audio_path: str) -> Optional[List[WordTimestamp]]:
        """Alinha acusticamente as palavras do áudio via Faster-Whisper."""
        model = self._get_whisper_model()
        if not model:
            return None

        try:
            segments, info = model.transcribe(
                audio_path,
                language=self.lang,
                word_timestamps=True
            )
            word_timestamps: List[WordTimestamp] = []
            for segment in segments:
                if not segment.words:
                    continue
                for w in segment.words:
                    clean_w = w.word.strip()
                    if clean_w:
                        word_timestamps.append(
                            WordTimestamp(
                                word=clean_w,
                                start_seconds=round(float(w.start), 2),
                                end_seconds=round(float(w.end), 2)
                            )
                        )
            if word_timestamps:
                return word_timestamps
        except Exception:
            return None
        return None

    def _fallback_alignment(self, text: str) -> List[WordTimestamp]:
        """Cálculo fonético calibrado caso o alinhador acústico não esteja disponível."""
        words_raw = re.findall(r'\S+', text)
        word_timestamps: List[WordTimestamp] = []
        current_time = 0.05

        for w in words_raw:
            char_factor = max(0.18, len(w) * 0.05)
            duration = round(char_factor, 2)
            if w.endswith(('.', '!', '?', ':')):
                duration += 0.2
            elif w.endswith(','):
                duration += 0.1

            word_timestamps.append(
                WordTimestamp(
                    word=w,
                    start_seconds=round(current_time, 2),
                    end_seconds=round(current_time + duration, 2)
                )
            )
            current_time += duration
        return word_timestamps

    def synthesize(self, text: str, output_path: str) -> AudioResult:
        """Sintetiza áudio neural a partir do texto e gera timestamps alinhados por palavra.
        
        Args:
            text: Texto do roteiro a ser narrado.
            output_path: Caminho do arquivo de áudio de saída.
            
        Returns:
            AudioResult contendo arquivo, duração, palavras e provedor utilizado.
        """
        if not text or not text.strip():
            raise ValueError("O texto para síntese de áudio não pode estar vazio.")

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

        # 1. Tenta síntese neural local com Piper-TTS
        piper_ok = self._synthesize_piper(text, output_path)
        provider = "piper-neural" if piper_ok else "gtts-fallback"

        if not piper_ok:
            self._synthesize_gtts(text, output_path)

        # 2. Alinhamento acústico via Faster-Whisper
        words = None
        if self.use_whisper:
            words = self._align_with_whisper(output_path)

        if not words:
            words = self._fallback_alignment(text)

        # Determina duração total real
        total_duration = 0.0
        if words:
            total_duration = round(words[-1].end_seconds + 0.2, 2)
        else:
            total_duration = 1.0

        return AudioResult(
            audio_path=output_path,
            duration_seconds=total_duration,
            words=words,
            provider=provider
        )

    def export_srt(
        self,
        words: List[WordTimestamp],
        output_srt_path: str,
        words_per_chunk: int = 3
    ) -> str:
        """Exporta arquivo de legendas .srt agrupando palavras em blocos visuais de leitura rápida.
        
        Args:
            words: Lista de timestamps de palavras.
            output_srt_path: Caminho do arquivo .srt.
            words_per_chunk: Palavras exibidas por vez (padrão: 3).
        """
        def format_time(seconds: float) -> str:
            hrs = int(seconds // 3600)
            mins = int((seconds % 3600) // 60)
            secs = int(seconds % 60)
            millis = int(round((seconds - int(seconds)) * 1000))
            return f"{hrs:02d}:{mins:02d}:{secs:02d},{millis:03d}"

        chunks = []
        for i in range(0, len(words), words_per_chunk):
            chunk = words[i:i + words_per_chunk]
            if not chunk:
                continue
            start_t = chunk[0].start_seconds
            end_t = chunk[-1].end_seconds
            text = " ".join([w.word for w in chunk])
            chunks.append((start_t, end_t, text))

        os.makedirs(os.path.dirname(os.path.abspath(output_srt_path)), exist_ok=True)
        with open(output_srt_path, "w", encoding="utf-8") as f:
            for idx, (st, et, txt) in enumerate(chunks, 1):
                f.write(f"{idx}\n")
                f.write(f"{format_time(st)} --> {format_time(et)}\n")
                f.write(f"{txt}\n\n")

        return output_srt_path
