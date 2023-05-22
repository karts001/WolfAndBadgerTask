import unittest
from unittest import mock

from flask_app import create_app
from flask_app.extensions import db
from flask_app.src.forms.personal_info import PersonalInfoForm
from flask_app.src.models.personal_info import PersonalInfo


class TestTheUpdateInfoRoute(unittest.TestCase):
    app = create_app("test")

    def setUp(self):
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.client = self.app.test_client()
        self.app.config["WTF_CSRF_ENABLED"] = False
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_redirected_to_github_authentication_page_if_not_authorized(self):
        response = self.client.get("/")
        response_code = response.status_code

        self.assertEqual(302, response_code)

    def test_the_update_info_route_has_flask_form_with_two_buttons(self):
        with mock.patch(
            "flask_app.src.routes.views.get_user_info", return_value="karts001"
        ):
            response = self.client.get("/authorized/update_info")
            html = response.data.decode()
            expected_text1 = "First Name"
            expected_text2 = "Submit"
            expected_text3 = "Delete Record"

            self.assertEqual(response.status_code, 200)
            self.assertIn(expected_text1, html)
            self.assertIn(expected_text2, html)
            self.assertIn(expected_text3, html)

    def test_the_form_is_blank_if_the_user_has_not_submitted_any_data(self):
        with mock.patch(
            "flask_app.src.routes.views.get_user_info", return_value="karts001"
        ):
            response = self.client.get("/authorized/update_info")
            personal_info_form = PersonalInfoForm()
            html = response.data.decode()
            first_name_current_value = personal_info_form.first_name.data
            print(f"This is the current first name: {first_name_current_value}")

    def test_the_form_redirects_to_success_route_when_validated_data_is_sent(self):
        mock_github_user = "test"
        with mock.patch(
            "flask_app.src.routes.views.get_user_info", return_value=mock_github_user
        ):
            response = self.client.post(
                "/authorized/update_info",
                data=dict(
                    github_user_name=mock_github_user,
                    first_name="Test",
                    last_name="Name",
                    age=27,
                    email="test@email.com",
                    phone_number="+47787546823",
                    address="28 Random Street",
                    post_code="PX21 4RT",
                    submit="",
                ),
                follow_redirects=True,
            )

            exists = (
                db.session.query(PersonalInfo)
                .filter_by(github_user_name=mock_github_user)
                .first()
                is not None
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(True, exists)
            self.assertEqual(1, len(response.history))
            self.assertEqual("/authorized/info_updated", response.request.path)

    def test_the_form_does_not_validate_if_the_first_name_field_is_blank(self):
        mock_github_user = "test"
        with mock.patch(
            "flask_app.src.routes.views.get_user_info", return_value=mock_github_user
        ):
            response = self.client.post(
                "/authorized/update_info",
                data=dict(
                    github_user_name=mock_github_user,
                    first_name="",
                    last_name="Name",
                    age=27,
                    email="test@email.com",
                    phone_number="+47787546823",
                    address="28 Random Street",
                    post_code="PX21 4RT",
                    submit="",
                ),
                follow_redirects=True,
            )

            html = response.data.decode()

            exists = (
                db.session.query(PersonalInfo)
                .filter_by(github_user_name=mock_github_user)
                .first()
                is not None
            )
            self.assertEqual(False, exists)
            self.assertEqual("/authorized/update_info", response.request.path)
            self.assertIn("This field is required", html)

    def test_the_form_does_not_validate_if_the_last_name_field_is_blank(self):
        mock_github_user = "test"
        with mock.patch(
            "flask_app.src.routes.views.get_user_info", return_value=mock_github_user
        ):
            response = self.client.post(
                "/authorized/update_info",
                data=dict(
                    github_user_name=mock_github_user,
                    first_name="Test",
                    last_name="",
                    age=27,
                    email="test@email.com",
                    phone_number="+47787546823",
                    address="28 Random Street",
                    post_code="PX21 4RT",
                    submit="",
                ),
                follow_redirects=True,
            )

            html = response.data.decode()

            exists = (
                db.session.query(PersonalInfo)
                .filter_by(github_user_name=mock_github_user)
                .first()
                is not None
            )
            self.assertEqual(False, exists)
            self.assertEqual("/authorized/update_info", response.request.path)
            self.assertIn("This field is required", html)

    def test_the_form_does_not_validate_if_the_age_field_is_blank(self):
        mock_github_user = "test"
        with mock.patch(
            "flask_app.src.routes.views.get_user_info", return_value=mock_github_user
        ):
            response = self.client.post(
                "/authorized/update_info",
                data=dict(
                    github_user_name=mock_github_user,
                    first_name="Test",
                    last_name="Name",
                    age="",
                    email="test@email.com",
                    phone_number="+47787546823",
                    address="28 Random Street",
                    post_code="PX21 4RT",
                    submit="",
                ),
                follow_redirects=True,
            )

            html = response.data.decode()

            exists = (
                db.session.query(PersonalInfo)
                .filter_by(github_user_name=mock_github_user)
                .first()
                is not None
            )
            self.assertEqual(False, exists)
            self.assertEqual("/authorized/update_info", response.request.path)
            self.assertIn("This field is required", html)

    def test_the_form_does_not_validate_if_the_age_field_contains_a_value_not_in_the_range_0_100(
        self,
    ):
        mock_github_user = "test"
        with mock.patch(
            "flask_app.src.routes.views.get_user_info", return_value=mock_github_user
        ):
            response = self.client.post(
                "/authorized/update_info",
                data=dict(
                    github_user_name=mock_github_user,
                    first_name="Test",
                    last_name="Name",
                    age=101,
                    email="test@email.com",
                    phone_number="+47787546823",
                    address="28 Random Street",
                    post_code="PX21 4RT",
                    submit="",
                ),
                follow_redirects=True,
            )

            html = response.data.decode()

            exists = (
                db.session.query(PersonalInfo)
                .filter_by(github_user_name=mock_github_user)
                .first()
                is not None
            )
            self.assertEqual(False, exists)
            self.assertEqual("/authorized/update_info", response.request.path)
            self.assertIn("Number must be between 0 and 100.", html)

    def test_the_form_does_not_validate_if_the_email_field_contains_an_invalid_email_address(
        self,
    ):
        mock_github_user = "test"
        with mock.patch(
            "flask_app.src.routes.views.get_user_info", return_value=mock_github_user
        ):
            response = self.client.post(
                "/authorized/update_info",
                data=dict(
                    github_user_name=mock_github_user,
                    first_name="Test",
                    last_name="Name",
                    age=100,
                    email="test@email.com@",
                    phone_number="+47787546823",
                    address="28 Random Street",
                    post_code="PX21 4RT",
                    submit="",
                ),
                follow_redirects=True,
            )

            html = response.data.decode()

            exists = (
                db.session.query(PersonalInfo)
                .filter_by(github_user_name=mock_github_user)
                .first()
                is not None
            )
            self.assertEqual(False, exists)
            self.assertEqual("/authorized/update_info", response.request.path)
            self.assertIn("Please enter a valid email!", html)

    def test_the_form_does_not_validate_if_the_email_field_is_blank(self):
        mock_github_user = "test"
        with mock.patch(
            "flask_app.src.routes.views.get_user_info", return_value=mock_github_user
        ):
            response = self.client.post(
                "/authorized/update_info",
                data=dict(
                    github_user_name=mock_github_user,
                    first_name="Test",
                    last_name="Name",
                    age=100,
                    email="",
                    phone_number="+47787546823",
                    address="28 Random Street",
                    post_code="PX21 4RT",
                    submit="",
                ),
                follow_redirects=True,
            )

            html = response.data.decode()

            exists = (
                db.session.query(PersonalInfo)
                .filter_by(github_user_name=mock_github_user)
                .first()
                is not None
            )
            self.assertEqual(False, exists)
            self.assertEqual("/authorized/update_info", response.request.path)
            self.assertIn("Please enter a valid email!", html)

    def test_the_form_does_not_validate_if_the_phone_number_field_is_blank(self):
        mock_github_user = "test"
        with mock.patch(
            "flask_app.src.routes.views.get_user_info", return_value=mock_github_user
        ):
            response = self.client.post(
                "/authorized/update_info",
                data=dict(
                    github_user_name=mock_github_user,
                    first_name="Test",
                    last_name="Name",
                    age=100,
                    email="test@email.com",
                    phone_number="",
                    address="28 Random Street",
                    post_code="PX21 4RT",
                    submit="",
                ),
                follow_redirects=True,
            )

            html = response.data.decode()

            exists = (
                db.session.query(PersonalInfo)
                .filter_by(github_user_name=mock_github_user)
                .first()
                is not None
            )
            self.assertEqual(False, exists)
            self.assertEqual("/authorized/update_info", response.request.path)
            self.assertIn("This field is required", html)

    def test_the_form_does_not_validate_if_the_phone_number_field_does_not_contian_between_12_and_16_characters(
        self,
    ):
        mock_github_user = "test"
        with mock.patch(
            "flask_app.src.routes.views.get_user_info", return_value=mock_github_user
        ):
            response = self.client.post(
                "/authorized/update_info",
                data=dict(
                    github_user_name=mock_github_user,
                    first_name="Test",
                    last_name="Name",
                    age=100,
                    email="test@email.com",
                    phone_number="123",
                    address="28 Random Street",
                    post_code="PX21 4RT",
                    submit="",
                ),
                follow_redirects=True,
            )

            html = response.data.decode()

            exists = (
                db.session.query(PersonalInfo)
                .filter_by(github_user_name=mock_github_user)
                .first()
                is not None
            )
            self.assertEqual(False, exists)
            self.assertEqual("/authorized/update_info", response.request.path)
            self.assertIn("Field must be between 12 and 16 characters long.", html)

    def test_the_form_does_not_validate_if_the_address_field_is_blank(self):
        mock_github_user = "test"
        with mock.patch(
            "flask_app.src.routes.views.get_user_info", return_value=mock_github_user
        ):
            response = self.client.post(
                "/authorized/update_info",
                data=dict(
                    github_user_name=mock_github_user,
                    first_name="Test",
                    last_name="Name",
                    age=100,
                    email="test@email.com",
                    phone_number="+47787546823",
                    address="",
                    post_code="PX21 4RT",
                    submit="",
                ),
                follow_redirects=True,
            )

            html = response.data.decode()

            exists = (
                db.session.query(PersonalInfo)
                .filter_by(github_user_name=mock_github_user)
                .first()
                is not None
            )
            self.assertEqual(False, exists)
            self.assertEqual("/authorized/update_info", response.request.path)
            self.assertIn("This field is required", html)

    def test_the_form_does_not_validate_if_the_post_code_field_is_blank(self):
        mock_github_user = "test"
        with mock.patch(
            "flask_app.src.routes.views.get_user_info", return_value=mock_github_user
        ):
            response = self.client.post(
                "/authorized/update_info",
                data=dict(
                    github_user_name=mock_github_user,
                    first_name="Test",
                    last_name="Name",
                    age=100,
                    email="test@email.com",
                    phone_number="+47787546823",
                    address="28 Random Street",
                    post_code="",
                    submit="",
                ),
                follow_redirects=True,
            )

            html = response.data.decode()

            exists = (
                db.session.query(PersonalInfo)
                .filter_by(github_user_name=mock_github_user)
                .first()
                is not None
            )
            self.assertEqual(False, exists)
            self.assertEqual("/authorized/update_info", response.request.path)
            self.assertIn("This field is required", html)

    def test_the_form_is_populated_with_the_data_from_the_database_if_a_user_exists(
        self,
    ):
        mock_github_user = "test"
        # personal_info_form = PersonalInfoForm()
        with mock.patch(
            "flask_app.src.routes.views.get_user_info", return_value=mock_github_user
        ):
            response = self.client.post(
                "/authorized/update_info",
                data=dict(
                    github_user_name=mock_github_user,
                    first_name="Test",
                    last_name="Name",
                    age=100,
                    email="test@email.com",
                    phone_number="+47787546823",
                    address="28 Random Street",
                    post_code="PX8 2RT",
                    submit="",
                ),
                follow_redirects=True,
            )

            response = self.client.get("/authorized/update_info")
            html = response.data.decode()

            self.assertIn("Test", html)
            self.assertIn("Name", html)
            self.assertIn("100", html)
            self.assertIn("test@email.com", html)
            self.assertIn("47787546823", html)
            self.assertIn("28 Random Street", html)
            self.assertIn("PX8 2RT", html)

    def test_the_delete_record_button_removes_the_users_data_from_the_database(self):
        mock_github_user = "test"
        # personal_info_form = PersonalInfoForm()
        with mock.patch(
            "flask_app.src.routes.views.get_user_info", return_value=mock_github_user
        ):
            response = self.client.post(
                "/authorized/update_info",
                data=dict(
                    github_user_name=mock_github_user,
                    first_name="Test",
                    last_name="Name",
                    age=100,
                    email="test@email.com",
                    phone_number="+47787546823",
                    address="28 Random Street",
                    post_code="PX8 2RT",
                    submit="",
                ),
                follow_redirects=True,
            )

            exists = (
                db.session.query(PersonalInfo)
                .filter_by(github_user_name=mock_github_user)
                .first()
            )
            self.assertNotEqual(exists, None)

            # return to form route
            response = self.client.get("/authorized/update_info")
            # "click" the delete record button
            response = self.client.post(
                "/authorized/update_info",
                data=dict(delete_button=""),
                follow_redirects=True,
            )

            exists = (
                db.session.query(PersonalInfo)
                .filter_by(github_user_name=mock_github_user)
                .first()
            )
            self.assertEqual(None, exists)
            self.assertEqual(1, len(response.history))
            self.assertEqual(
                f"/authorized/delete_record/{mock_github_user}", response.request.path
            )


if __name__ == "__main__":
    unittest.main()
