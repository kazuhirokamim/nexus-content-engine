"""Nexus Content Engine - Renderizador de Vídeo Vertical 9:16.

Governança: Cânone Tear & Noesis Architecture Swarm.
Regra #24: Orçamento de linhas < 700.
"""

import os
import sys
import subprocess
import shutil
from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class VideoRenderResult:
    """Metadados do vídeo renderizado."""
    output_path: str
    duration_seconds: float
    width: int
    height: int
    encoder_used: str


class VideoAssembler:
    """Compila vídeos verticais 9:16 combinando B-Roll, áudio neural e legendas."""

    def __init__(self, ffmpeg_exe: Optional[str] = None):
        if ffmpeg_exe and os.path.exists(ffmpeg_exe):
            self.ffmpeg_exe = ffmpeg_exe
        else:
            # Tenta resolver via imageio_ffmpeg ou PATH do sistema
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
            # Testa h264_videotoolbox no macOS
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

    def render(
        self,
        audio_path: str,
        output_path: str,
        b_roll_path: Optional[str] = None,
        subtitles_path: Optional[str] = None,
        resolution: Tuple[int, int] = (1080, 1920),
        fps: int = 30
    ) -> VideoRenderResult:
        """Renderiza o vídeo vertical combinando os elementos audiovisuais.
        
        Args:
            audio_path: Arquivo de áudio .mp3.
            output_path: Arquivo final .mp4.
            b_roll_path: Arquivo de vídeo de fundo (opcional).
            subtitles_path: Arquivo .srt ou .ass para legendas queimadas (opcional).
            resolution: (largura, altura) - padrão 1080x1920 (9:16).
            fps: Taxa de quadros.
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Arquivo de áudio não encontrado: {audio_path}")

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        width, height = resolution
        encoder = self._detect_encoder()

        # Montagem dos argumentos do FFmpeg
        cmd = [self.ffmpeg_exe, "-y"]

        # Entrada 1: Vídeo de fundo ou gerador procedural se não houver B-roll
        has_real_broll = b_roll_path and os.path.exists(b_roll_path)
        if has_real_broll:
            cmd.extend(["-stream_loop", "-1", "-i", b_roll_path])
        else:
            # Fallback: Fundo estilizado degradê neon (Vice City aesthetic)
            cmd.extend([
                "-f", "lavfi",
                "-i", f"color=c=0x0b0b14:s={width}x{height}:r={fps}"
            ])

        # Entrada 2: Áudio narrado
        cmd.extend(["-i", audio_path])

        # Construção do Filtergraph
        filter_chains = []
        
        if has_real_broll:
            # Ajuste de proporção para 9:16 com crop centralizado
            filter_chains.append(
                f"scale=w={width}:h={height}:force_original_aspect_ratio=increase,crop={width}:{height}"
            )
        else:
            filter_chains.append("null")

        # Inclusão de legendas caso arquivo SRT exista
        if subtitles_path and os.path.exists(subtitles_path):
            # Escape de caminho para sintaxe de filtros do FFmpeg
            escaped_srt = os.path.abspath(subtitles_path).replace("\\", "/").replace(":", "\\:")
            # Estilização: Fonte amarela neon, contorno preto forte, centralizada
            style = "FontSize=24,PrimaryColour=&H0000FFFF,OutlineColour=&H00000000,BorderStyle=3,Outline=3,Alignment=2,MarginV=250"
            filter_chains.append(f"subtitles={escaped_srt}:force_style='{style}'")

        full_filter = ",".join([fc for fc in filter_chains if fc != "null"])
        if full_filter:
            cmd.extend(["-vf", full_filter])

        # Configurações de encoding de vídeo e áudio
        cmd.extend([
            "-c:v", encoder,
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",  # Limita duração exata ao fim do áudio
            output_path
        ])

        # Execução controlada com timeout
        process = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=120
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
