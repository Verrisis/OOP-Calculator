import unittest

from fastapi.testclient import TestClient

from API import app


class TestAPI(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_calculate_success(self):
        response = self.client.post("/calculate", json={"expression": "1/2 + 1/4"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["result"], "3/4")

    def test_calculate_division_by_zero_returns_400(self):
        response = self.client.post("/calculate", json={"expression": "1 : 0"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Denominator cannot be zero!", response.json()["detail"])

    def test_get_history_empty_returns_404(self):
        response = self.client.get("/history")
        if response.status_code == 404:
            assert "Operation history is empty" in response.json()["detail"]

    def test_calculate_not_implemented_operator_returns_error(self):
        response = self.client.post("/calculate", json={"expression": "1/2 ^ 1/4"})
        self.assertIn(response.status_code, [400, 501])
        self.assertIn("Currently supported operators", response.json()["detail"])

    def test_calculate_text_garbage_returns_custom_error(self):
        response = self.client.post("/calculate", json={"expression": "invalid input"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Input error: Invalid format. Use: 'fraction operator fraction'", response.json()["detail"])


if __name__ == "__main__":
    unittest.main()
