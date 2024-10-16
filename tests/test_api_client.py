import unittest, requests
import unittest.mock
from src.api_client import get_location
from unittest.mock import patch


class ApiClientTests(unittest.TestCase):

    @patch("src.api_client.requests.get")
    def test_get_location_returns_expected_data(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "countryName": "USA",
            "cityName": "Florida",
            "regionName": "Miami",
            "countryCode": "US",
        }
        result = get_location("8.8.8.8")
        self.assertEqual(result.get("countryName"), "USA")
        self.assertEqual(result.get("cityName"), "Florida")
        self.assertEqual(result.get("regionName"), "Miami")
        self.assertEqual(result.get("countryCode"), "US")

        mock_get.assert_called_once_with("http://freeipapi.com/api/json/8.8.8.8")

    @patch("src.api_client.requests.get")
    def test_get_location_returns_side_effect(self, mock_get):
        mock_get.side_effect = [
            requests.exceptions.RequestException("Service Unavailable"),
            unittest.mock.Mock(
                status_code=200,
                json=lambda: {
                    "countryName": "USA",
                    "cityName": "Florida",
                    "regionName": "Miami",
                    "countryCode": "US",
                    }
            )
        ]

        with self.assertRaises(requests.exceptions.RequestException):
            get_location("8.8.8.8")

        result = get_location("8.8.8.8")
        self.assertEqual(result.get("countryName"), "USA")
        self.assertEqual(result.get("cityName"), "Florida")
        self.assertEqual(result.get("regionName"), "Miami")
        self.assertEqual(result.get("countryCode"), "US")

    def test_get_location_with_invalid_ip(self):
        invalid_ip = "8.8.8.9988"
        with self.assertRaises(ValueError):
            get_location(invalid_ip)
