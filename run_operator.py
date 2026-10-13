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
    """Executa a esteira completa: Roteiro -> Áudio -> Legendas -> Vídeo MP4."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    work_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "output", "temp", timestamp))
    os.makedirs(work_dir, exist_ok=True)

    final_output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "output"))
    os.makedirs(final_output_dir, exist_ok=True)
    final_video_path = os.path.join(final_output_dir, f"{niche}_{timestamp}.mp4")

    print("\n" + "=" * 60)
    print("⚡ NEXUS CONTENT ENGINE — ESTEIRA PROGRAMÁTICA DE VÍDEO")
    print(f"🎯 Nicho: {niche.upper()} | Pauta: {topic}")
    print("=" * 60)

    # 1. Roteirização Neural
    print("\n[1/4] 📝 Gerando Roteiro Psicológico de Alta Retenção...")
    generator = ScriptGenerator()
    script = generator.generate(topic=topic, niche=niche)
    print(f"      👉 Gancho: {script.hook[:60]}...")
    print(f"      ⏱️ Duração estimada: {script.estimated_duration_seconds}s")

    # 2. Síntese Acústica Neural
    print("\n[2/4] 🎙️ Sintetizando Voz Neural e Calculando Timestamps...")
    audio_path = os.path.join(work_dir, "audio.mp3")
    tts = TTSEngine(lang="pt", tld="com.br")
    audio_res = tts.synthesize(script.full_text(), audio_path)
    print(f"      ✅ Áudio gerado: {audio_res.duration_seconds}s | {len(audio_res.words)} palavras alinhadas.")

    # 3. Exportação de Legendas
    print("\n[3/4] ⏱️ Exportando Legendas Sincronizadas...")
    srt_path = os.path.join(work_dir, "subtitles.srt")
    tts.export_srt(audio_res.words, srt_path, words_per_chunk=3)
    print(f"      ✅ Legendas salvas em: {os.path.basename(srt_path)}")

    # 4. Compilação e Renderização em Vídeo 9:16
    print("\n[4/4] 🎬 Compilando Vídeo Vertical 9:16 com FFmpeg...")
    assembler = VideoAssembler()
    
    # Verifica se há B-Roll na pasta do preset
    b_roll_candidate = os.path.join(os.path.dirname(__file__), "presets", niche, "b_roll", "gameplay.mp4")
    b_roll_path = b_roll_candidate if os.path.exists(b_roll_candidate) else None

    start_render = time.time()
    render_res = assembler.render(
        audio_path=audio_res.audio_path,
        output_path=final_video_path,
        b_roll_path=b_roll_path,
        subtitles_path=srt_path,
        resolution=(1080, 1920),
        fps=30
    )
    render_time = round(time.time() - start_render, 2)
    print(f"      ⚡ Renderizado em {render_time}s via {render_res.encoder_used}!")

    print("\n" + "=" * 60)
    print("🎉 VÍDEO CONCLUÍDO COM SUCESSO!")
    print(f"📁 Arquivo Final: {final_video_path}")
    print(f"📏 Resolução: {render_res.width}x{render_res.height} (9:16)")
    print("=" * 60)

    # Dicas de postagem para o operador
    print("\n📋 SUGESTÃO DE COMENTÁRIO FIXADO (Copie e cole):")
    print("   'Qual plataforma você vai jogar GTA 6? Separei os menores preços:")
    print("   👉 PS5 Slim: https://amzn.to/exemplo-ps5")
    print("   👉 SSD 2TB: https://amzn.to/exemplo-ssd'")
    print("\n🏷️ HASHTAGS:")
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
