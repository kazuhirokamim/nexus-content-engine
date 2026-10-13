#!/usr/bin/env python3
"""Nexus Content Engine - CLI Turnkey do Operador (Jayp).

Governança: Cânone Tear & Noesis Backend Swarm.
Regra #24: Orçamento de linhas < 700.
"""

import os
import sys
import time
import argparse
from datetime import datetime

# Adiciona pasta src ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from script_generator import ScriptGenerator
from core.tts_engine import TTSEngine
from core.video_assembler import VideoAssembler


def run_pipeline(topic: str, niche: str = "gta6") -> str:
    """Executa a esteira completa: Roteiro -> Voz Neural -> Whisper -> B-Roll -> Vídeo 9:16."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    work_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "output", "temp", timestamp))
    os.makedirs(work_dir, exist_ok=True)

    final_output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "output"))
    os.makedirs(final_output_dir, exist_ok=True)
    final_video_path = os.path.join(final_output_dir, f"{niche}_{timestamp}.mp4")

    print("\n" + "=" * 65)
    print("⚡ NEXUS CONTENT ENGINE — ESTEIRA PROGRAMÁTICA DE VÍDEO")
    print(f"🎯 Nicho: {niche.upper()} | Pauta: {topic}")
    print("=" * 65)

    # 1. Roteirização Psicológica de Retenção
    print("\n[1/4] 📝 Gerando Roteiro Psicológico de Alta Retenção...")
    generator = ScriptGenerator()
    script = generator.generate(topic=topic, niche=niche)
    print(f"      👉 Gancho: \"{script.hook[:60]}...\"")
    print(f"      ⏱️ Duração estimada: {script.estimated_duration_seconds}s")

    # 2. Síntese Acústica Neural & Alinhamento Faster-Whisper
    print("\n[2/4] 🎙️ Sintetizando Voz Neural Local (Piper) & Alinhando com Whisper...")
    audio_path = os.path.join(work_dir, "audio.wav")
    tts = TTSEngine(lang="pt", use_whisper=True, speed_scale=0.85)
    
    t0_audio = time.time()
    audio_res = tts.synthesize(script.full_text(), audio_path)
    audio_time = round(time.time() - t0_audio, 2)
    
    print(f"      ⚡ Síntese concluída em {audio_time}s via [{audio_res.provider}]")
    print(f"      ✅ Áudio: {audio_res.duration_seconds}s | {len(audio_res.words)} palavras alinhadas acusticamente.")

    # 3. Exportação de Legendas Estilo Karaokê
    print("\n[3/4] ⏱️ Gerando Legendas Karaokê Sincronizadas...")
    srt_path = os.path.join(work_dir, "subtitles.srt")
    tts.export_srt(audio_res.words, srt_path, words_per_chunk=3)
    print(f"      ✅ Legendas geradas em blocos de 3 palavras ({os.path.basename(srt_path)})")

    # 4. Compilação e Renderização em Vídeo 9:16 com B-Roll Real e Música
    print("\n[4/4] 🎬 Compilando Vídeo Vertical 9:16 com Gameplay Real e Trilha...")
    assembler = VideoAssembler()

    # Resolução de B-Roll e Trilha Sonora
    b_roll_dir = os.path.join(os.path.dirname(__file__), "presets", niche, "b_roll")
    bg_music_file = os.path.join(os.path.dirname(__file__), "presets", niche, "audio", "background_synthwave.mp3")

    b_roll_path = b_roll_dir if os.path.exists(b_roll_dir) else None
    bg_music_path = bg_music_file if os.path.exists(bg_music_file) else None

    if b_roll_path:
        print(f"      🎮 B-Roll vinculado: Gameplay real detectado em {os.path.basename(b_roll_dir)}/")
    if bg_music_path:
        print(f"      🎵 Trilha de fundo: Synthwave atenuada (-22dB ducking)")

    start_render = time.time()
    render_res = assembler.render(
        audio_path=audio_res.audio_path,
        output_path=final_video_path,
        b_roll_path=b_roll_path,
        background_music_path=bg_music_path,
        subtitles_path=srt_path,
        resolution=(1080, 1920),
        fps=30
    )
    render_time = round(time.time() - start_render, 2)
    print(f"      ⚡ Renderizado em {render_time}s via {render_res.encoder_used} (GPU acelerada)!")

    file_size_mb = round(os.path.getsize(final_video_path) / 1024 / 1024, 2)
    print("\n" + "=" * 65)
    print("🎉 VÍDEO CONCLUÍDO COM QUALIDADE COMERCIAL!")
    print(f"📁 Arquivo Final: {final_video_path} ({file_size_mb} MB)")
    print(f"📏 Resolução: {render_res.width}x{render_res.height} (9:16 Vertical)")
    print("=" * 65)

    # Dicas de postagem e monetização para o operador
    print("\n📋 SUGESTÃO DE COMENTÁRIO FIXADO (Copie e cole):")
    print("   'Qual plataforma você vai jogar GTA 6? Separei os menores preços:")
    print("   👉 PS5 Slim: https://amzn.to/exemplo-ps5")
    print("   👉 SSD 2TB: https://amzn.to/exemplo-ssd'")
    print("\n🏷️ HASHTAGS DE ALTA RETENÇÃO:")
    print("   #gta6 #gtavi #rockstargames #playstation5 #vicecity #games\n")

    return final_video_path


def main():
    parser = argparse.ArgumentParser(description="Nexus Content Engine - Turnkey Operator CLI")
    parser.add_argument("--topic", type=str, help="Tema ou pauta quente do vídeo")
    parser.add_argument("--niche", type=str, default="gta6", help="Nicho de atuação (default: gta6)")
    args = parser.parse_args()

    topic = args.topic
    if not topic:
        print("⚡ Nexus Content Engine - Modo Interativo")
        topic = input("👉 Digite a pauta ou notícia quente para o vídeo: ").strip()
        if not topic:
            print("Erro: A pauta não pode ser vazia.")
            sys.exit(1)

    run_pipeline(topic=topic, niche=args.niche)


if __name__ == "__main__":
    main()
