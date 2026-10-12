"""Nexus Content Engine - Gerador de Roteiros Neurais de Alta Retenção."""

from dataclasses import dataclass
from typing import List


@dataclass
class VideoScript:
    """Estrutura formal de um roteiro de vídeo curto."""
    niche: str
    topic: str
    hook: str
    body_paragraphs: List[str]
    loop_cta: str
    estimated_duration_seconds: int

    def full_text(self) -> str:
        """Gera o texto completo contínuo para o sintetizador de voz."""
        body = " ".join(self.body_paragraphs)
        return f"{self.hook} {body} {self.loop_cta}"


class ScriptGenerator:
    """Gera roteiros estruturados baseados em psicologia de retenção e ganchos neurais."""

    def __init__(self, model_name: str = "gemini-2.5-flash"):
        self.model_name = model_name

    def generate(self, topic: str, niche: str = "gta6") -> VideoScript:
        """Gera um roteiro a partir de um tópico e nicho especificado."""
        # Se for o nicho flagship (GTA 6)
        if niche.lower() in ["gta6", "gta-6", "gtavi"]:
            hook = f"Atenção: um novo vazamento acaba de mudar tudo o que sabíamos sobre {topic} no GTA 6!"
            body = [
                "Arquivos internos da Take-Two revelam que a Rockstar reconstruiu todo o motor de física.",
                "Diferente do GTA 5, cada impacto em veículos e superfícies agora deforma o modelo em tempo real sem scripts pré-definidos.",
                "Além disso, o comportamento dos NPCs em Vice City promete reagir a qualquer movimento suspeito do jogador."
            ]
            loop_cta = "E se você achava que isso era exagero, repare só no detalhe em que..."
        else:
            # Roteiro genérico para qualquer nicho (tech, finanças, games, curiosidades)
            hook = f"Você provavelmente não sabia disso, mas este detalhe sobre {topic} muda completamente o jogo!"
            body = [
                f"Pesquisas recentes e análises aprofundadas sobre {topic} revelam um padrão surpreendente.",
                "Poucas pessoas no mercado perceberam o impacto real dessa mudança no comportamento do público.",
                "Quem dominar esse conceito primeiro vai ter uma vantagem desproporcional nos próximos meses."
            ]
            loop_cta = "E o mais surpreendente sobre tudo isso é que..."

        return VideoScript(
            niche=niche,
            topic=topic,
            hook=hook,
            body_paragraphs=body,
            loop_cta=loop_cta,
            estimated_duration_seconds=42
        )
