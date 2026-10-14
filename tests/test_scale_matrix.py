import unittest
import os
import tempfile
import json
from src.core.scale_matrix import ScaleMatrix, ScaleVariation, ScaleMatrixError

class TestScaleMatrix(unittest.TestCase):
    def setUp(self):
        self.hooks = [
            "Você viu o novo segredo do GTA 6?",
            "Isso muda tudo o que sabemos sobre o mapa!",
            "A física de água vazada impressionou todo mundo."
        ]
        self.broll_files = [
            "presets/gta6/b_roll/gameplay_01.mp4",
            "presets/gta6/b_roll/gta6_trailer_official.mp4"
        ]
        self.ctas = [
            "Segue para mais vazamentos diários de GTA 6!",
            "Comenta embaixo o que você achou dessa teoria!"
        ]

    # --- 1. Happy Path ---
    def test_cartesian_product_generation(self):
        """Verifica a geração correta do produto cartesiano H x B x C."""
        matrix = ScaleMatrix(
            niche="gta6",
            hooks=self.hooks,
            broll_files=self.broll_files,
            ctas=self.ctas
        )
        variations = matrix.generate_variations()
        expected_total = len(self.hooks) * len(self.broll_files) * len(self.ctas) # 3 * 2 * 2 = 12
        self.assertEqual(len(variations), expected_total)
        self.assertEqual(matrix.total_combinations, expected_total)

        # Valida a integridade da primeira variação
        first_var = variations[0]
        self.assertIsInstance(first_var, ScaleVariation)
        self.assertEqual(first_var.niche, "gta6")
        self.assertIn(first_var.hook, self.hooks)
        self.assertIn(first_var.broll_file, self.broll_files)
        self.assertIn(first_var.cta, self.ctas)
        self.assertTrue(len(first_var.variation_id) > 0)

    def test_sampling_with_count_and_seed(self):
        """Verifica amostragem de contagem máxima com semente reproduzível."""
        matrix = ScaleMatrix(
            niche="gta6",
            hooks=self.hooks,
            broll_files=self.broll_files,
            ctas=self.ctas
        )
        # Amostragem de 4 variações com seed fixa
        sample1 = matrix.generate_variations(count=4, seed=42)
        sample2 = matrix.generate_variations(count=4, seed=42)

        self.assertEqual(len(sample1), 4)
        self.assertEqual(len(sample2), 4)
        # Deve ser 100% determinístico e idêntico com a mesma seed
        ids1 = [v.variation_id for v in sample1]
        ids2 = [v.variation_id for v in sample2]
        self.assertEqual(ids1, ids2)

    def test_export_metadata_manifest(self):
        """Verifica a serialização e exportação do manifesto de variações em JSON."""
        matrix = ScaleMatrix(
            niche="tech_ai",
            hooks=["Nova IA lançada hoje!", "Essa ferramenta vai substituir programadores?"],
            broll_files=["presets/tech_ai/b_roll/server.mp4"],
            ctas=["Link nos comentários!"]
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest_path = os.path.join(tmpdir, "manifest.json")
            variations = matrix.generate_variations(count=2)
            matrix.save_manifest(variations, manifest_path)

            self.assertTrue(os.path.exists(manifest_path))
            with open(manifest_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertEqual(data["niche"], "tech_ai")
            self.assertEqual(len(data["variations"]), 2)

    def test_from_preset_gta6_real_loading(self):
        """Verifica o carregamento automático a partir do preset real de GTA 6."""
        matrix = ScaleMatrix.from_preset(
            niche="gta6",
            presets_dir="presets",
            topic="vazamento de carros"
        )
        self.assertEqual(matrix.niche, "gta6")
        self.assertTrue(len(matrix.hooks) >= 4)
        self.assertTrue(len(matrix.broll_files) >= 2)
        # Verifica se o tópico foi interpolado
        self.assertTrue(any("vazamento de carros" in h for h in matrix.hooks))
        variations = matrix.generate_variations(count=3)
        self.assertEqual(len(variations), 3)

    # --- 2. Edge Cases ---
    def test_single_element_matrix(self):
        """Verifica matriz 1x1x1 (caso unitário)."""
        matrix = ScaleMatrix(
            niche="gta6",
            hooks=["Gancho único"],
            broll_files=["broll.mp4"],
            ctas=["CTA único"]
        )
        variations = matrix.generate_variations()
        self.assertEqual(len(variations), 1)
        self.assertEqual(variations[0].hook, "Gancho único")

    def test_count_exceeding_total_combinations(self):
        """Verifica solicitação de contagem maior que o total disponível."""
        matrix = ScaleMatrix(
            niche="gta6",
            hooks=["Gancho 1", "Gancho 2"],
            broll_files=["broll.mp4"],
            ctas=["CTA 1"]
        )
        # Total é 2 x 1 x 1 = 2, mas solicitamos 10
        variations = matrix.generate_variations(count=10)
        self.assertEqual(len(variations), 2)

    # --- 3. Error Paths ---
    def test_empty_hooks_raises_error(self):
        """Verifica exceção ao fornecer lista de ganchos vazia."""
        with self.assertRaises(ScaleMatrixError):
            ScaleMatrix(
                niche="gta6",
                hooks=[],
                broll_files=self.broll_files,
                ctas=self.ctas
            )

    def test_empty_broll_raises_error(self):
        """Verifica exceção ao fornecer lista de b-rolls vazia."""
        with self.assertRaises(ScaleMatrixError):
            ScaleMatrix(
                niche="gta6",
                hooks=self.hooks,
                broll_files=[],
                ctas=self.ctas
            )

    def test_empty_ctas_raises_error(self):
        """Verifica exceção ao fornecer lista de CTAs vazia."""
        with self.assertRaises(ScaleMatrixError):
            ScaleMatrix(
                niche="gta6",
                hooks=self.hooks,
                broll_files=self.broll_files,
                ctas=[]
            )

    def test_invalid_count_raises_error(self):
        """Verifica exceção ao solicitar contagem menor ou igual a zero."""
        matrix = ScaleMatrix(
            niche="gta6",
            hooks=self.hooks,
            broll_files=self.broll_files,
            ctas=self.ctas
        )
        with self.assertRaises(ScaleMatrixError):
            matrix.generate_variations(count=0)
        with self.assertRaises(ScaleMatrixError):
            matrix.generate_variations(count=-5)

if __name__ == "__main__":
    unittest.main()
