from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import unittest
import time

class TestTasks(unittest.TestCase):
    def setUp(self):
        # Setup Firefox options
        firefox_options = Options()
        firefox_options.add_argument("--headless")  # Run in headless mode
        self.driver = webdriver.Firefox(options=firefox_options)

    def test_add_and_verify_tasks(self):
        driver = self.driver
        driver.get("http://10.48.10.107")  # Replace with your Flask server URL

        # Add 5 test tasks
        for i in range(5):
            task_name = f'Test Task {i}'
            task_description = f'Description for task {i}'

            # Fill out the form
            driver.find_element(By.ID, "taskName").clear()
            driver.find_element(By.ID, "taskName").send_keys(task_name)
            driver.find_element(By.ID, "taskDescription").clear()
            driver.find_element(By.ID, "taskDescription").send_keys(task_description)
            driver.find_element(By.XPATH, "//input[@type='submit']").click()

            # Wait for page to reload and task to appear
            time.sleep(1)

            # Verify task appears in page source
            self.assertIn(task_name, driver.page_source)
            self.assertIn(task_description, driver.page_source)

        print("All test tasks successfully added and verified.")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
