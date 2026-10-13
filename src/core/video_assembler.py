"""Nexus Content Engine - Renderizador de Vídeo Vertical 9:16.

Governança: Cânone Tear & Noesis Architecture Swarm.
Regra #24: Orçamento de linhas < 700.
"""

import os
import sys
import glob
import random
import subprocess
import shutil
from dataclasses import dataclass
from typing import Optional, Tuple, List


@dataclass
class VideoRenderResult:
    """Metadados do vídeo renderizado."""
    output_path: str
    duration_seconds: float
    width: int
    height: int
    encoder_used: str


class VideoAssembler:
    """Compila vídeos verticais 9:16 combinando B-Roll dinâmico, áudio neural, música e legendas."""

    def __init__(self, ffmpeg_exe: Optional[str] = None):
        if ffmpeg_exe and os.path.exists(ffmpeg_exe):
            self.ffmpeg_exe = ffmpeg_exe
        else:
            try:
                import imageio_ffmpeg
                self.ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
            except Exception:
                sys_ffmpeg = shutil.which("ffmpeg")
                if not sys_ffmpeg:
                    raise RuntimeError("Executável FFmpeg não encontrado no sistema.")
                self.ffmpeg_exe = sys_ffmpeg

    def _detect_encoder(self) -> str:
        """Detecta encoder acelerado por hardware ou seleciona libx264."""
        if sys.platform == "darwin":
            try:
                res = subprocess.run(
                    [self.ffmpeg_exe, "-encoders"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if "h264_videotoolbox" in res.stdout:
                    return "h264_videotoolbox"
            except Exception:
                pass
        return "libx264"

    def _resolve_broll_file(self, b_roll_target: Optional[str]) -> Optional[str]:
        """Resolve o arquivo de B-Roll se for um arquivo único ou escolhe de um diretório."""
        if not b_roll_target:
            return None
        if os.path.isfile(b_roll_target) and os.path.exists(b_roll_target):
            return b_roll_target
        if os.path.isdir(b_roll_target):
            candidates = glob.glob(os.path.join(b_roll_target, "*.mp4")) + \
                         glob.glob(os.path.join(b_roll_target, "*.mov"))
            if candidates:
                # Ordena para determinismo ou seleciona o de maior relevância
                candidates.sort()
                return candidates[0]
        return None

    def render(
        self,
        audio_path: str,
        output_path: str,
        b_roll_path: Optional[str] = None,
        background_music_path: Optional[str] = None,
        subtitles_path: Optional[str] = None,
        resolution: Tuple[int, int] = (1080, 1920),
        fps: int = 30
    ) -> VideoRenderResult:
        """Renderiza o vídeo vertical combinando todos os elementos audiovisuais.
        
        Args:
            audio_path: Arquivo de áudio .wav ou .mp3 (voz).
            output_path: Arquivo final .mp4.
            b_roll_path: Arquivo ou diretório com vídeos de gameplay de fundo.
            background_music_path: Trilha sonora sutil com ducking (opcional).
            subtitles_path: Arquivo .srt com legendas karaokê sincronizadas.
            resolution: (largura, altura) - padrão 1080x1920 (9:16).
            fps: Taxa de quadros por segundo.
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Arquivo de áudio não encontrado: {audio_path}")

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        width, height = resolution
        encoder = self._detect_encoder()

        resolved_broll = self._resolve_broll_file(b_roll_path)
        has_real_broll = resolved_broll is not None and os.path.exists(resolved_broll)
        has_bg_music = background_music_path is not None and os.path.exists(background_music_path)

        cmd = [self.ffmpeg_exe, "-y"]

        # Entrada 0: Vídeo de fundo (Loop infinito)
        if has_real_broll:
            cmd.extend(["-stream_loop", "-1", "-i", resolved_broll])
        else:
            cmd.extend([
                "-f", "lavfi",
                "-i", f"color=c=0x0b0b14:s={width}x{height}:r={fps}"
            ])

        # Entrada 1: Voz narrada
        cmd.extend(["-i", audio_path])

        # Entrada 2: Música de fundo (se houver)
        if has_bg_music:
            cmd.extend(["-stream_loop", "-1", "-i", background_music_path])

        # Filtros de Vídeo e Legenda
        v_filters = []
        if has_real_broll:
            v_filters.append(
                f"scale=w={width}:h={height}:force_original_aspect_ratio=increase,crop={width}:{height}"
            )
        else:
            v_filters.append("null")

        if subtitles_path and os.path.exists(subtitles_path):
            escaped_srt = os.path.abspath(subtitles_path).replace("\\", "/").replace(":", "\\:")
            # Estilo Karaokê ViceScale: Amarelo neon (&H0000FFFF), contorno preto forte (Outline=4), safe-zone 9:16
            style = "FontSize=24,PrimaryColour=&H0000FFFF,OutlineColour=&H00000000,BorderStyle=3,Outline=4,Alignment=2,MarginV=280"
            v_filters.append(f"subtitles={escaped_srt}:force_style='{style}'")

        v_filter_str = ",".join([f for f in v_filters if f != "null"])

        # Filtros de Áudio (Mixagem e Ducking)
        if has_bg_music:
            # Entrada 1 é voz (volume=1.0), Entrada 2 é música (volume=0.08 / ducked a -22dB)
            filter_complex = f"[0:v]{v_filter_str}[vout];[1:a]volume=1.0[voice];[2:a]volume=0.08[music];[voice][music]amix=inputs=2:duration=first:dropout_transition=2[aout]"
            cmd.extend([
                "-filter_complex", filter_complex,
                "-map", "[vout]",
                "-map", "[aout]"
            ])
        else:
            if v_filter_str:
                cmd.extend(["-vf", v_filter_str])
            cmd.extend(["-map", "0:v", "-map", "1:a"])

        # Parâmetros de codificação
        cmd.extend([
            "-c:v", encoder,
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",  # Limita duração ao fim da narração
            output_path
        ])

        process = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=180
        )

        if process.returncode != 0:
            raise RuntimeError(f"Erro durante a renderização do FFmpeg:\n{process.stderr[-800:]}")

        return VideoRenderResult(
            output_path=output_path,
            duration_seconds=0.0,
            width=width,
            height=height,
            encoder_used=encoder
        )
