"""
Módulo NexusScale: Motor Combinatório Cartesiano (1-to-N).
Gera variações massivas de vídeo através do produto cartesiano de ganchos, b-rolls e CTAs.
"""

from dataclasses import dataclass, field
import hashlib
import itertools
import json
import os
import random
from typing import List, Optional, Dict, Any

class ScaleMatrixError(Exception):
    """Exceção levantada para erros de validação ou processamento na ScaleMatrix."""
    pass

@dataclass(frozen=True)
class ScaleVariation:
    """Representa uma variação única e imutável de vídeo gerada pela ScaleMatrix."""
    variation_id: str
    niche: str
    hook: str
    broll_file: str
    cta: str
    body_text: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def full_script(self) -> str:
        """Monta o roteiro completo combinando hook, corpo e CTA."""
        parts = [self.hook.strip()]
        if self.body_text and self.body_text.strip():
            parts.append(self.body_text.strip())
        parts.append(self.cta.strip())
        return " ".join(parts)

    def to_dict(self) -> Dict[str, Any]:
        """Converte a variação em dicionário serializável."""
        return {
            "variation_id": self.variation_id,
            "niche": self.niche,
            "hook": self.hook,
            "broll_file": self.broll_file,
            "cta": self.cta,
            "body_text": self.body_text,
            "full_script": self.full_script,
            "metadata": self.metadata
        }

class ScaleMatrix:
    """
    Motor combinatório 1-to-N para produção de variações em massa.
    Cruza ganchos (hooks) x B-rolls x CTAs gerando planos de renderização estruturados.
    """

    def __init__(
        self,
        niche: str,
        hooks: List[str],
        broll_files: List[str],
        ctas: List[str],
        body_text: str = ""
    ):
        if not niche or not isinstance(niche, str):
            raise ScaleMatrixError("O nicho deve ser uma string não vazia.")

        if not hooks or not isinstance(hooks, list):
            raise ScaleMatrixError("A lista de ganchos (hooks) não pode ser vazia.")

        if not broll_files or not isinstance(broll_files, list):
            raise ScaleMatrixError("A lista de b-rolls não pode ser vazia.")

        if not ctas or not isinstance(ctas, list):
            raise ScaleMatrixError("A lista de chamadas para ação (CTAs) não pode ser vazia.")

        self.niche = niche.strip().lower()
        self.hooks = [h.strip() for h in hooks if h and h.strip()]
        self.broll_files = [b.strip() for b in broll_files if b and b.strip()]
        self.ctas = [c.strip() for c in ctas if c and c.strip()]
        self.body_text = body_text.strip()

        if not self.hooks:
            raise ScaleMatrixError("Nenhum gancho válido fornecido.")
        if not self.broll_files:
            raise ScaleMatrixError("Nenhum arquivo de b-roll válido fornecido.")
        if not self.ctas:
            raise ScaleMatrixError("Nenhuma chamada para ação (CTA) válida fornecida.")

    @property
    def total_combinations(self) -> int:
        """Calcula o total teórico de combinações possíveis: |H| x |B| x |C|."""
        return len(self.hooks) * len(self.broll_files) * len(self.ctas)

    def _generate_id(self, hook: str, broll: str, cta: str) -> str:
        """Gera um hash determinístico curto para identificar a variação."""
        payload = f"{self.niche}:{hook}:{broll}:{cta}".encode("utf-8")
        return hashlib.sha256(payload).hexdigest()[:12]

    def generate_variations(
        self,
        count: Optional[int] = None,
        seed: Optional[int] = None
    ) -> List[ScaleVariation]:
        """
        Computa o produto cartesiano e retorna a lista de ScaleVariations.
        Se count for especificado, extrai uma amostra (amostragem aleatória se seed for fornecida).
        """
        if count is not None and count <= 0:
            raise ScaleMatrixError(f"A contagem solicitada deve ser um inteiro positivo (> 0). Recebido: {count}")

        # Produto cartesiano H x B x C
        raw_combinations = list(itertools.product(self.hooks, self.broll_files, self.ctas))

        if count is not None and count < len(raw_combinations):
            if seed is not None:
                rng = random.Random(seed)
                selected_combinations = rng.sample(raw_combinations, count)
            else:
                selected_combinations = raw_combinations[:count]
        else:
            selected_combinations = raw_combinations

        variations: List[ScaleVariation] = []
        for hook, broll, cta in selected_combinations:
            var_id = self._generate_id(hook, broll, cta)
            variation = ScaleVariation(
                variation_id=var_id,
                niche=self.niche,
                hook=hook,
                broll_file=broll,
                cta=cta,
                body_text=self.body_text,
                metadata={
                    "total_matrix_pool": self.total_combinations,
                    "seed": seed
                }
            )
            variations.append(variation)

        return variations

    def save_manifest(self, variations: List[ScaleVariation], output_path: str) -> None:
        """Serializa a lista de variações geradas em um arquivo manifesto JSON."""
        dir_name = os.path.dirname(output_path)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)

        manifest_data = {
            "niche": self.niche,
            "total_combinations": self.total_combinations,
            "generated_count": len(variations),
            "variations": [v.to_dict() for v in variations]
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(manifest_data, f, indent=2, ensure_ascii=False)

    @classmethod
    def from_preset(
        cls,
        niche: str,
        presets_dir: str = "presets",
        topic: str = "",
        body_text: str = ""
    ) -> "ScaleMatrix":
        """
        Carrega automaticamente ganchos, b-rolls e CTAs a partir do diretório do preset do nicho.
        Suporta prompts.yaml e prompts.json com interpolação dinâmica de tópico.
        """
        niche_dir = os.path.join(presets_dir, niche)
        if not os.path.exists(niche_dir):
            raise ScaleMatrixError(f"Diretório de preset do nicho não encontrado: {niche_dir}")

        # Busca B-Rolls
        broll_dir = os.path.join(niche_dir, "b_roll")
        broll_files = []
        if os.path.exists(broll_dir):
            for file in sorted(os.listdir(broll_dir)):
                if file.lower().endswith((".mp4", ".mov", ".mkv")):
                    broll_files.append(os.path.join(broll_dir, file))

        if not broll_files:
            raise ScaleMatrixError(f"Nenhum arquivo de vídeo encontrado em: {broll_dir}")

        # Busca Prompts / Ganchos e CTAs padrão (YAML ou JSON)
        yaml_file = os.path.join(niche_dir, "prompts.yaml")
        json_file = os.path.join(niche_dir, "prompts.json")
        hooks = []
        ctas = []

        cfg = {}
        if os.path.exists(yaml_file):
            try:
                import yaml
                with open(yaml_file, "r", encoding="utf-8") as f:
                    cfg = yaml.safe_load(f) or {}
            except Exception:
                pass
        elif os.path.exists(json_file):
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    cfg = json.load(f) or {}
            except Exception:
                pass

        raw_hooks = cfg.get("hooks", [])
        ctas = cfg.get("ctas", [])

        # Formata os ganchos com o tópico se fornecido
        topic_str = topic.strip() if topic else niche
        if raw_hooks:
            for h in raw_hooks:
                if isinstance(h, str):
                    formatted_hook = h.replace("{topic}", topic_str)
                    hooks.append(formatted_hook)

        # Fallbacks caso o arquivo de configuração não tenha as chaves exatas
        if not hooks:
            hooks = [
                f"Vazamento inacreditável sobre {topic_str} no {niche.upper()}!",
                f"Você sabia desse detalhe absurdo sobre {topic_str} que quase ninguém notou?",
                f"Isso confirma a teoria de {topic_str} que todo mundo estava esperando!"
            ]

        if not ctas:
            ctas = [
                f"Segue para mais novidades diárias sobre {niche.upper()}!",
                "Comenta aqui embaixo o que você acha que vai acontecer!"
            ]

        return cls(
            niche=niche,
            hooks=hooks,
            broll_files=broll_files,
            ctas=ctas,
            body_text=body_text
        )
