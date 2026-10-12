"""GTA 6 Content Engine - CLI Entrypoint."""

import sys
import argparse
from script_generator import ScriptGenerator


def main():
    parser = argparse.ArgumentParser(description="GTA 6 Content Engine - Geração Automática")
    parser.add_argument("--topic", type=str, required=True, help="Tópico ou tema do vídeo")
    args = parser.parse_args()

    print("=" * 60)
    print("🌴 GTA 6 Content Engine - Geração Automática de Vídeo")
    print(f"🎯 Pauta: {args.topic}")
    print("=" * 60)

    generator = ScriptGenerator()
    script = generator.generate(args.topic)

    print("\n📝 Roteiro Gerado:")
    print(f"👉 Gancho (0-3s): {script.hook}")
    print("\n📖 Conteúdo:")
    for p in script.body_paragraphs:
        print(f"   • {p}")
    print(f"\n🔄 Loop / CTA: {script.loop_cta}")
    print(f"\n⏱️ Duração Estimada: {script.estimated_duration_seconds} segundos")
    print("\n[OK] Roteiro estruturado pronto para síntese neural e montagem FFmpeg.")


if __name__ == "__main__":
    main()
