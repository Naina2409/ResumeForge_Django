"""Run with: python -m unittest tests.test_model_smoke"""
import unittest
from ml_engine.scoring import load_artifact, score_pair

class ModelSmokeTest(unittest.TestCase):
    def test_original_model_returns_expected_shape(self):
        artifact = load_artifact()
        result = score_pair(
            "Python developer with Django REST APIs SQL and Git experience",
            "Seeking Python developer with Django, REST API, SQL and Git skills",
            artifact,
        )
        self.assertIn(result["label"], {"Good Fit", "Potential Fit", "No Fit"})
        self.assertGreaterEqual(result["score"], 0)
        self.assertLessEqual(result["score"], 1)
        self.assertEqual(set(result["features"]), set(artifact["feature_columns"]))

if __name__ == "__main__":
    unittest.main()
