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
        self.assertIn("Mianownik nie może być zerem!", response.json()["detail"])

    def test_get_history_empty_returns_404(self):
        response = self.client.get("/history")
        if response.status_code == 404:
            assert "Historia operacji jest pusta" in response.json()["detail"]

    def test_calculate_invalid_format_returns_400(self):
        response = self.client.post("/calculate", json={"expression": "ala ma kota"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Niepoprawny format", response.json()["detail"])

    def test_calculate_not_implemented_operator_returns_error(self):
        response = self.client.post("/calculate", json={"expression": "1/2 ^ 1/4"})
        self.assertIn(response.status_code, [400, 501])
        self.assertIn("Obecnie obsługujemy tylko operatory", response.json()["detail"])


if __name__ == "__main__":
    unittest.main()