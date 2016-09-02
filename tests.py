import json
import unittest
from unittest import TestCase
import server
from server import app


class FlaskRouteTests(TestCase):
    """Flask tests."""

################# Testing Necessities #################

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

##################### Test Routes ######################

    def test_home_route(self):
        """Test route to homepage."""

        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertIn('Connect!', result.data)

    def test_mapJSON_route(self):
        """Test route to map paths."""

        result = self.client.get("/statejson")
        self.assertEqual(result.status_code, 200)

    def test_statewordsJSON_route(self):
        """Test route to state words json."""

        result = self.client.get("/getstatewords.json")
        self.assertEqual(result.status_code, 200)

    def test_legwordsJSON_route(self):
        """Test route to leg words json."""

        result = self.client.get("/getlegwords.json")
        self.assertEqual(result.status_code, 200)

################### Test API Return ####################

    def test_gather_sunlight_congress(self):
        """Test rep detail queries"""

        client = server.app.test_client()
        result = self.client.post("/repdetails", 
            data={'city':'atlanta', 'state':'GA'},
            follow_redirects=True)
        self.assertIn("Democrat", result.data)


if __name__ == "__main__":
    unittest.main()
