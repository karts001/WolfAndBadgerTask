import unittest

from flask_app import create_app
from flask_app.extensions import db


class TestTheGithubOAuthPage(unittest.TestCase):
    app = create_app("test")

    def setUp(self):
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_root_page_redirects_to_the_github_authentication_page_if_the_user_is_not_signed_in(
        self,
    ):
        response = self.client.get("/")
        response_code = response.status_code

        html = response.data.decode()
        expected_text = "Redirecting"
        another_expected_text = "github"

        self.assertEqual(302, response_code)
        self.assertIn(expected_text, html)
        self.assertIn(another_expected_text, html)


if __name__ == "__main__":
    unittest.main()
