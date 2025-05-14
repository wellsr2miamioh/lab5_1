```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import unittest

class TestTasks(unittest.TestCase):
    BASE_URL = "http://10.48.10.107"  # Replace with your Flask app URL

    def setUp(self):
        # Setup Firefox options
        firefox_options = Options()
        firefox_options.add_argument("--headless")             # Ensures the browser window does not open
        firefox_options.add_argument("--no-sandbox")
        firefox_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Firefox(options=firefox_options)

    def test_tasks(self):
        driver = self.driver
        driver.get(self.BASE_URL)
        
        for i in range(10):
            test_task = f'Test Task {i}'
            self.assertIn(
                test_task,
                driver.page_source,
                f"Test task '{test_task}' not found in page source"
            )
        print("Test completed successfully. All 10 test tasks were verified.")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(verbosity=2)
```
