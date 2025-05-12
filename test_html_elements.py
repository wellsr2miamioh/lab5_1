from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import unittest

class TestTaskData(unittest.TestCase):
    def setUp(self):
        # Setup Firefox options
        firefox_options = Options()
        firefox_options.add_argument("--headless")  # Ensures the browser window does not open
        firefox_options.add_argument("--no-sandbox")
        firefox_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Firefox(options=firefox_options)

    def test_task_data(self):
        driver = self.driver
        driver.get("http://10.48.10.179")  # Replace with your target website
        
        # Check for the presence of the 4 test tasks
        for i in range(4):
            test_task = f'Test Task {i}'
            assert test_task in driver.page_source, f"Test task {test_task} not found in page source"
        print("Test completed successfully. All 4 test tasks were verified.")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()

