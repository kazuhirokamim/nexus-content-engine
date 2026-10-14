import unittest
import os
import tempfile
from unittest.mock import patch
import run_operator

class TestRunOperator(unittest.TestCase):
    def test_run_scale_pipeline_execution(self):
        """Verifica a execução do run_scale_pipeline salvando manifesto."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Executa a geração em lote de 2 variações no nicho gta6 passando tmpdir
            run_operator.run_scale_pipeline(
                topic="teste de suspensao de carros",
                niche="gta6",
                count=2,
                output_dir=tmpdir
            )
            files = os.listdir(tmpdir)
            manifests = [f for f in files if f.startswith("scale_manifest_gta6_")]
            self.assertTrue(len(manifests) > 0, "Deveria ter gerado pelo menos um manifesto de escala.")

    def test_main_cli_scale_flag(self):
        """Verifica se a flag --scale na CLI despacha para run_scale_pipeline."""
        with patch("sys.argv", ["run_operator.py", "--topic", "vazamento mapa", "--niche", "gta6", "--scale", "--count", "2"]):
            with patch("run_operator.run_scale_pipeline") as mock_scale:
                run_operator.main()
                mock_scale.assert_called_once_with(topic="vazamento mapa", niche="gta6", count=2)

    def test_main_cli_empty_interactive_exit(self):
        """Verifica se o modo interativo encerra quando pauta vazia é fornecida."""
        with patch("sys.argv", ["run_operator.py"]):
            with patch("builtins.input", side_effect=["1", ""]):
                with self.assertRaises(SystemExit) as cm:
                    run_operator.main()
                self.assertEqual(cm.exception.code, 1)

if __name__ == "__main__":
    unittest.main()
