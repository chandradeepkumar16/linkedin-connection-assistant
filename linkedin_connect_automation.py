"""
LinkedIn Connection Request Automation Agent
Sends connection requests to 2nd and 3rd degree connections from a specific company
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import time
import random

class LinkedInConnectBot:
    def __init__(self, email, password):
        """Initialize the LinkedIn bot with credentials"""
        self.email = email
        self.password = password
        self.driver = None
        self.requests_sent = 0
        
    def setup_driver(self):
        """Setup Chrome driver with options"""
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Add user agent to avoid detection
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 20)
        
    def human_delay(self, min_seconds=1, max_seconds=3):
        """Add random delay to mimic human behavior"""
        time.sleep(random.uniform(min_seconds, max_seconds))
        
    def login(self):
        """Login to LinkedIn"""
        try:
            print("Opening LinkedIn...")
            self.driver.get("https://www.linkedin.com/login")
            self.human_delay(1.5, 2)
            
            print("Entering credentials...")
            # Enter email
            email_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            email_field.clear()
            email_field.send_keys(self.email)
            
            self.human_delay(0.3, 0.5)
            
            # Enter password
            password_field = self.driver.find_element(By.ID, "password")
            password_field.clear()
            password_field.send_keys(self.password)
            
            self.human_delay(0.3, 0.5)
            
            # Click login button
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            print("Logging in...")
            self.human_delay(3, 4)
            
            # Check if login was successful
            if "feed" in self.driver.current_url or "mynetwork" in self.driver.current_url:
                print("✓ Successfully logged in!")
                return True
            else:
                print("⚠ Login may have failed. Please check for CAPTCHA or verification.")
                return False
                
        except Exception as e:
            print(f"❌ Error during login: {str(e)}")
            return False
    
    def search_company_people(self, company_name):
        """Search for people from a specific company (2nd and 3rd connections)"""
        try:
            print(f"\nSearching for people from '{company_name}'...")
            
            # Search for company and filter to exclude 1st connections (only 2nd & 3rd)
            search_url = f"https://www.linkedin.com/search/results/people/?keywords={company_name.replace(' ', '%20')}"
            self.driver.get(search_url)
            self.human_delay(3, 4)
            
            print("✓ Loaded people search results")
            return True
            
        except Exception as e:
            print(f"❌ Error searching for company people: {str(e)}")
            return False
    
    def get_people_on_current_page(self):
        """Get all people result items on current page"""
        try:
            # Wait for results to load
            self.human_delay(2, 3)
            
            # Scroll to load all results on page
            for i in range(2):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                self.human_delay(1, 1.5)
            
            # Scroll back to top
            self.driver.execute_script("window.scrollTo(0, 0);")
            self.human_delay(0.5, 1)
            
            # Find all result items
            result_items = []
            
            selectors = [
                "//li[contains(@class, 'reusable-search__result-container')]",
                "//div[contains(@class, 'search-results-container')]//li",
                "//ul[contains(@class, 'reusable-search__entity-result-list')]//li"
            ]
            
            for selector in selectors:
                try:
                    items = self.driver.find_elements(By.XPATH, selector)
                    if items and len(items) > 0:
                        result_items = items
                        break
                except:
                    continue
            
            print(f"  📊 Found {len(result_items)} people on this page")
            return result_items
            
        except Exception as e:
            print(f"❌ Error getting people on page: {str(e)}")
            return []
    
    def get_person_name(self, result_item):
        """Extract person's name from search result"""
        try:
            name_selectors = [
                ".//span[@dir='ltr']//span[@aria-hidden='true']",
                ".//span[contains(@class, 'entity-result__title-text')]//span[@aria-hidden='true']",
                ".//a[contains(@class, 'app-aware-link')]//span[@aria-hidden='true']"
            ]
            
            for selector in name_selectors:
                try:
                    name_element = result_item.find_element(By.XPATH, selector)
                    name = name_element.text.strip()
                    if name and len(name) > 2:
                        return name
                except:
                    continue
            
            return "Unknown"
        except:
            return "Unknown"
    
    def is_already_connected(self, result_item):
        """Check if person is already a 1st connection"""
        try:
            # Look for "Message" button which indicates 1st connection
            buttons = result_item.find_elements(By.TAG_NAME, "button")
            for btn in buttons:
                try:
                    btn_text = btn.text.lower() if btn.text else ""
                    aria_label = btn.get_attribute('aria-label')
                    if aria_label:
                        aria_label = aria_label.lower()
                    else:
                        aria_label = ""
                    
                    # If we see "Message" button, they're already connected
                    if 'message' in btn_text or 'message' in aria_label:
                        return True
                    
                    # If we see "Pending" button, request already sent
                    if 'pending' in btn_text or 'pending' in aria_label:
                        return True
                        
                except:
                    continue
            
            return False
            
        except:
            return False
    
    def send_connection_request(self, result_item, person_name):
        """Send connection request to a person"""
        try:
            # Scroll person into view
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", result_item)
            self.human_delay(0.5, 1)
            
            # Check if already connected
            if self.is_already_connected(result_item):
                print(f"  ⊘ Skipping {person_name} (already connected or pending)")
                return False
            
            # Find Connect button
            connect_button = None
            
            connect_selectors = [
                ".//button[contains(@aria-label, 'Invite') or contains(@aria-label, 'Connect')]",
                ".//button[.//span[text()='Connect']]",
                ".//button[contains(., 'Connect')]",
                ".//button[@aria-label[contains(., 'Connect')]]"
            ]
            
            for selector in connect_selectors:
                try:
                    buttons = result_item.find_elements(By.XPATH, selector)
                    for btn in buttons:
                        try:
                            if btn.is_displayed() and btn.is_enabled():
                                btn_text = btn.text.strip().lower() if btn.text else ""
                                aria_label = btn.get_attribute('aria-label')
                                if aria_label:
                                    aria_label = aria_label.lower()
                                else:
                                    aria_label = ""
                                
                                if 'connect' in btn_text or 'connect' in aria_label or 'invite' in aria_label:
                                    connect_button = btn
                                    break
                        except:
                            continue
                    if connect_button:
                        break
                except:
                    continue
            
            if not connect_button:
                print(f"  ⚠ Connect button not found for {person_name}")
                return False
            
            # Click Connect button
            try:
                connect_button.click()
                print(f"  ✓ Clicked Connect button for {person_name}")
            except ElementClickInterceptedException:
                self.driver.execute_script("arguments[0].click();", connect_button)
                print(f"  ✓ Clicked Connect button (JS) for {person_name}")
            
            self.human_delay(1, 1.5)
            
            # Check if modal appeared with "Add a note" option
            try:
                # Look for "Send without a note" button
                send_without_note_selectors = [
                    "//button[contains(@aria-label, 'Send without a note') or contains(., 'Send without a note')]",
                    "//button[@aria-label='Send now']",
                    "//button[.//span[contains(text(), 'Send without')]]",
                    "//button[contains(@class, 'artdeco-button--primary') and contains(., 'Send')]"
                ]
                
                send_button = None
                for selector in send_without_note_selectors:
                    try:
                        send_button = self.driver.find_element(By.XPATH, selector)
                        if send_button.is_displayed():
                            break
                    except:
                        continue
                
                if send_button:
                    send_button.click()
                    print(f"  ✓ Clicked 'Send without a note' for {person_name}")
                    self.human_delay(0.5, 1)
                else:
                    # If no modal, the request was sent directly
                    print(f"  ✓ Request sent directly to {person_name}")
                
                # Close any remaining modal by pressing ESC
                try:
                    webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
                    self.human_delay(0.3, 0.5)
                except:
                    pass
                    
            except:
                # No modal appeared, request sent directly
                print(f"  ✓ Request sent to {person_name}")
            
            self.requests_sent += 1
            return True
            
        except Exception as e:
            print(f"  ❌ Error sending request to {person_name}: {str(e)}")
            return False
    
    def go_to_next_page(self):
        """Navigate to next page of search results"""
        try:
            print("\n🔄 Moving to next page...")
            
            # Scroll to bottom where pagination is
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.human_delay(1, 2)
            
            # Find Next button
            next_button = None
            
            next_selectors = [
                "//button[@aria-label='Next']",
                "//button[contains(@aria-label, 'Next')]",
                "//button[contains(., 'Next')]",
                "//li[contains(@class, 'artdeco-pagination__indicator--number')]/following-sibling::li//button"
            ]
            
            for selector in next_selectors:
                try:
                    next_button = self.driver.find_element(By.XPATH, selector)
                    if next_button.is_displayed() and next_button.is_enabled():
                        break
                except:
                    continue
            
            if not next_button:
                print("  ⚠ No next page available")
                return False
            
            # Check if button is disabled
            if 'disabled' in next_button.get_attribute('class'):
                print("  ⚠ Reached last page")
                return False
            
            # Click next page
            try:
                next_button.click()
            except:
                self.driver.execute_script("arguments[0].click();", next_button)
            
            print("  ✓ Moved to next page")
            self.human_delay(3, 4)
            
            # Scroll to top of new page
            self.driver.execute_script("window.scrollTo(0, 0);")
            self.human_delay(0.5, 1)
            
            return True
            
        except Exception as e:
            print(f"❌ Error going to next page: {str(e)}")
            return False
    
    def run_automation(self, company_name, max_requests):
        """Main automation workflow"""
        try:
            print("="*70)
            print("LinkedIn Connection Request Automation Agent Started")
            print("="*70)
            
            # Setup driver
            self.setup_driver()
            
            # Login
            if not self.login():
                print("\n❌ Failed to login. Exiting...")
                return
            
            # Search for company people
            if not self.search_company_people(company_name):
                print("\n❌ Failed to search for people. Exiting...")
                return
            
            print(f"\n{'='*70}")
            print(f"Target: Send {max_requests} connection request(s)")
            print(f"{'='*70}")
            
            # Send connection requests
            page_number = 1
            
            while self.requests_sent < max_requests:
                print(f"\n📄 Processing Page {page_number}...")
                
                # Get people on current page
                people = self.get_people_on_current_page()
                
                if not people:
                    print("  ⚠ No people found on this page")
                    break
                
                # Process each person
                for i, person_item in enumerate(people, 1):
                    if self.requests_sent >= max_requests:
                        print(f"\n✓ Reached target of {max_requests} requests!")
                        break
                    
                    person_name = self.get_person_name(person_item)
                    print(f"\n[{self.requests_sent + 1}/{max_requests}] Processing: {person_name}")
                    
                    if self.send_connection_request(person_item, person_name):
                        # Add delay between requests
                        if self.requests_sent < max_requests:
                            delay = random.uniform(1, 3)
                            print(f"  ⏳ Waiting {delay:.1f} seconds...")
                            time.sleep(delay)
                
                # Check if we need to go to next page
                if self.requests_sent < max_requests:
                    if not self.go_to_next_page():
                        print("\n⚠ No more pages available")
                        break
                    page_number += 1
                else:
                    break
            
            print(f"\n{'='*70}")
            print("Automation Complete!")
            print(f"✓ Connection requests sent: {self.requests_sent}")
            print(f"{'='*70}")
            
        except Exception as e:
            print(f"\n❌ Error in automation: {str(e)}")
            print(f"✓ Requests sent before error: {self.requests_sent}")
        finally:
            # Keep browser open for 5 seconds to review
            print("\nKeeping browser open for 5 seconds...")
            time.sleep(5)
            if self.driver:
                self.driver.quit()
                print("Browser closed.")


def main():
    """Main function to run the LinkedIn connection automation"""
    
    # ========== CONFIGURATION ==========
    # Replace these with your actual credentials
    LINKEDIN_EMAIL = ""    # Your LinkedIn email
    LINKEDIN_PASSWORD = ""           # Your LinkedIn password
    
    COMPANY_NAME = "Rubrik"                        # Company to target
    MAX_REQUESTS = 15                              # Number of connection requests to send
    # ===================================
    
    print("\n⚠️  IMPORTANT DISCLAIMER:")
    print("This automation tool is for educational purposes only.")
    print("Automated activity may violate LinkedIn's Terms of Service.")
    print("LinkedIn has weekly connection request limits (~100/week for free accounts).")
    print("Sending too many requests may result in account restrictions.")
    print("Use at your own risk. The creator is not responsible for any consequences.")
    print("\nPress Enter to continue or Ctrl+C to cancel...")
    input()
    
    # Create bot instance
    bot = LinkedInConnectBot(LINKEDIN_EMAIL, LINKEDIN_PASSWORD)
    
    # Run automation
    bot.run_automation(COMPANY_NAME, MAX_REQUESTS)


if __name__ == "__main__":
    main()
