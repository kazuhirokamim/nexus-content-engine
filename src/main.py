"""Nexus Content Engine - CLI Entrypoint."""

import argparse
from script_generator import ScriptGenerator


def main():
    parser = argparse.ArgumentParser(description="Nexus Content Engine - Geração Automática")
    parser.add_argument("--topic", type=str, required=True, help="Tópico ou tema do vídeo")
    parser.add_argument("--niche", type=str, default="gta6", help="Nicho de atuação (default: gta6)")
    args = parser.parse_args()

    print("=" * 60)
    print("⚡ Nexus Content Engine - Geração Automática de Vídeo")
    print(f"🎯 Nicho: {args.niche.upper()} | Pauta: {args.topic}")
    print("=" * 60)

    generator = ScriptGenerator()
    script = generator.generate(topic=args.topic, niche=args.niche)

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
