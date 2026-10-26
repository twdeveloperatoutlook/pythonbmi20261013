import unittest

from bmi import bmi_guidance, calculate_bmi, gauge_angle


class BmiUnitTests(unittest.TestCase):
    def test_calculate_bmi(self):
        bmi, error_field = calculate_bmi(170, 65)
        self.assertAlmostEqual(bmi, 65 / 1.7**2)
        self.assertIsNone(error_field)

    def test_calculate_bmi_rejects_unrepresentable_values(self):
        for height, weight, expected_error in [
            (1e-300, 65, "height"),
            (1e308, 65, "height"),
            (1, 1e308, "weight"),
        ]:
            with self.subTest(height=height, weight=weight):
                bmi, error_field = calculate_bmi(height, weight)
                self.assertIsNone(bmi)
                self.assertEqual(error_field, expected_error)

    def test_taiwan_adult_thresholds(self):
        for bmi, category in [
            (18.4, "體重過輕"),
            (18.5, "健康體位"),
            (23.9, "健康體位"),
            (24.0, "體重過重"),
            (26.9, "體重過重"),
            (27.0, "肥胖"),
        ]:
            with self.subTest(bmi=bmi):
                self.assertEqual(bmi_guidance(bmi)["label"], category)

    def test_gauge_angle_mapping(self):
        for bmi, angle in [(5, -90.0), (10, -90.0), (18.5, -39.0), (24, -6.0), (25, 0.0), (27, 12.0), (40, 90.0), (55, 90.0)]:
            with self.subTest(bmi=bmi):
                self.assertEqual(gauge_angle(bmi), angle)


if __name__ == "__main__":
    unittest.main()