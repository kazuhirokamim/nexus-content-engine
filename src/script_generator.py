"""GTA 6 Content Engine - Gerador de Roteiros Neurais de Alta Retenção."""

from dataclasses import dataclass
from typing import List


@dataclass
class VideoScript:
    """Estrutura formal de um roteiro de vídeo curto."""
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
    """Gera roteiros estruturados baseados em psicologia de retenção gamer."""

    def __init__(self, model_name: str = "gemini-2.5-flash"):
        self.model_name = model_name

    def generate(self, topic: str) -> VideoScript:
        """Gera um roteiro a partir de um tópico ou pauta quente.
        
        Em produção real, conecta ao Gemini via google-genai.
        """
        # Template padrão de retenção de 45 segundos
        hook = f"Atenção: um novo vazamento acaba de mudar tudo o que sabíamos sobre {topic} no GTA 6!"
        body = [
            "Arquivos internos da Take-Two revelam que a Rockstar reconstruiu todo o motor de física.",
            "Diferente do GTA 5, cada impacto em veículos e superfícies agora deforma o modelo em tempo real sem scripts pré-definidos.",
            "Além disso, o comportamento dos NPCs em Vice City promete reagir a qualquer movimento suspeito do jogador."
        ]
        loop_cta = "E se você achava que isso era exagero, repare só no detalhe em que..."
        
        return VideoScript(
            topic=topic,
            hook=hook,
            body_paragraphs=body,
            loop_cta=loop_cta,
            estimated_duration_seconds=42
        )
