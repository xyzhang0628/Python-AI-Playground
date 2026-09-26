import unittest

from app import app


class PortfolioTests(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True, SECRET_KEY="test-secret")
        self.client = app.test_client()

    def test_pages_render_six_work_projects_and_navigation(self):
        response = self.client.get("/designer/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.count(b'class="project-card '), 6)
        self.assertIn(b'aria-current="page"', response.data)
        self.assertIn(b"Group%20634399.png", response.data)
        self.assertNotIn(b"<script", response.data)

    def test_extra_and_about_pages(self):
        extra = self.client.get("/designer/extra")
        self.assertEqual(extra.status_code, 200)
        self.assertIn(b"Extra things", extra.data)
        self.assertEqual(extra.data.count(b'class="extra-card '), 6)

        about = self.client.get("/designer/about")
        self.assertEqual(about.status_code, 200)
        self.assertIn(b"Download r\xc3\xa9sum\xc3\xa9", about.data)
        self.assertIn(b"mailto:hello@minapark.design", about.data)

    def test_local_images_and_downloadable_resume(self):
        image = self.client.get("/designer/assets/Group%20634399.png")
        self.assertEqual(image.status_code, 200)
        self.assertEqual(image.mimetype, "image/png")
        image.close()

        resume = self.client.get("/designer/resume")
        self.assertEqual(resume.status_code, 200)
        self.assertIn("attachment;", resume.headers["Content-Disposition"])


if __name__ == "__main__":
    unittest.main()