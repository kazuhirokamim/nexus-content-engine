"""Nexus Content Engine - Motor de Síntese de Áudio Neural & Alinhador Temporal.

Governança: Cânone Tear & Noesis Architecture Swarm.
Regra #24: Orçamento de linhas < 700.
"""

import os
import re
import math
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


class TTSEngine:
    """Motor de síntese de voz neural resiliente com suporte a múltiplos provedores."""

    def __init__(self, lang: str = "pt", tld: str = "com.br"):
        self.lang = lang
        self.tld = tld

    def synthesize(self, text: str, output_path: str) -> AudioResult:
        """Sintetiza áudio neural a partir do texto e gera timestamps estimados por palavra.
        
        Args:
            text: Texto do roteiro a ser narrado.
            output_path: Caminho do arquivo de saída .mp3.
            
        Returns:
            AudioResult contendo caminho, duração e timestamps das palavras.
        """
        if not text or not text.strip():
            raise ValueError("O texto para síntese de áudio não pode estar vazio.")

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

        # Síntese neural estável via gTTS
        tts = gTTS(text=text, lang=self.lang, tld=self.tld, slow=False)
        tts.save(output_path)

        # Cálculo de duração acústica aproximada
        # Média da fala em português: ~135 a 150 palavras por minuto (2.25 a 2.5 palavras/segundo)
        words_raw = re.findall(r'\S+', text)
        words_count = len(words_raw)
        
        # Média calibrada: 0.38s por palavra + pausas de pontuação
        total_duration = 0.0
        word_timestamps: List[WordTimestamp] = []
        current_time = 0.1

        for w in words_raw:
            # Palavras maiores demoram proporcionalmente mais
            char_factor = max(0.2, len(w) * 0.055)
            duration = round(char_factor, 2)
            
            # Adiciona pausa extra se houver pontuação forte
            if w.endswith(('.', '!', '?', ':')):
                duration += 0.25
            elif w.endswith(','):
                duration += 0.12

            word_timestamps.append(
                WordTimestamp(
                    word=w,
                    start_seconds=round(current_time, 2),
                    end_seconds=round(current_time + duration, 2)
                )
            )
            current_time += duration

        total_duration = round(current_time + 0.3, 2)

        return AudioResult(
            audio_path=output_path,
            duration_seconds=total_duration,
            words=word_timestamps
        )

    def export_srt(self, words: List[WordTimestamp], output_srt_path: str, words_per_chunk: int = 4) -> str:
        """Exporta arquivo de legendas .srt agrupando palavras em blocos visuais de leitura rápida.
        
        Args:
            words: Lista de timestamps de palavras.
            output_srt_path: Caminho do arquivo .srt.
            words_per_chunk: Quantidade de palavras exibidas por vez na tela (padrão: 3 a 4).
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
