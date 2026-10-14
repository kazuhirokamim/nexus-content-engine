import argparse
import os
import sys
from datetime import datetime

# Garante importação dos módulos locais
sys.path.insert(0, os.path.dirname(__file__))

from script_generator import ScriptGenerator
from core.scale_matrix import ScaleMatrix, ScaleMatrixError


def main():
    parser = argparse.ArgumentParser(description="Nexus Content Engine - Geração Automática & Escala")
    parser.add_argument("--topic", type=str, default="", help="Tópico ou tema do vídeo")
    parser.add_argument("--niche", type=str, default="gta6", help="Nicho de atuação (default: gta6)")
    parser.add_argument("--scale", action="store_true", help="Ativa o motor NexusScale combinatório 1-to-N")
    parser.add_argument("--count", type=int, default=5, help="Quantidade de variações a gerar no modo --scale (default: 5)")
    parser.add_argument("--seed", type=int, default=None, help="Semente determinística para amostragem no modo --scale")
    args = parser.parse_args()

    topic = args.topic.strip() if args.topic else f"novidades de {args.niche}"

    print("=" * 65)
    print("⚡ Nexus Content Engine — Plataforma Soberana de Mídia")
    print(f"🎯 Nicho: {args.niche.upper()} | Pauta: {topic}")
    print("=" * 65)

    if args.scale:
        print("\n🚀 [NexusScale] Executando Motor Combinatório 1-to-N...")
        try:
            presets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "presets")
            matrix = ScaleMatrix.from_preset(
                niche=args.niche,
                presets_dir=presets_dir,
                topic=topic
            )
            print(f"   📊 Universo de Combinações: {matrix.total_combinations} possíveis (|H|={len(matrix.hooks)} x |B|={len(matrix.broll_files)} x |C|={len(matrix.ctas)})")
            print(f"   🎯 Amostrando: {args.count} variações...")

            variations = matrix.generate_variations(count=args.count, seed=args.seed)

            # Salva o manifesto de saída
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
            manifest_file = os.path.join(output_dir, f"scale_manifest_{args.niche}_{timestamp}.json")
            matrix.save_manifest(variations, manifest_file)

            print(f"\n📋 Manifesto Gravado: {manifest_file}")
            print("\n✨ Variações Geradas:")
            for i, v in enumerate(variations, 1):
                broll_name = os.path.basename(v.broll_file)
                print(f"   [{i}/{len(variations)}] ID: {v.variation_id}")
                print(f"        👉 Gancho: \"{v.hook}\"")
                print(f"        🎮 B-Roll: {broll_name}")
                print(f"        🔄 CTA: \"{v.cta}\"\n")

            print("[OK] Matriz combinatória gerada com sucesso e pronta para renderização em lote.")
        except ScaleMatrixError as e:
            print(f"\n❌ Erro no NexusScale: {e}", file=sys.stderr)
            sys.exit(1)
        return

    # Modo padrão: Roteiro único
    generator = ScriptGenerator()
    script = generator.generate(topic=topic, niche=args.niche)

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
