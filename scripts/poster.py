import logging
import os
import random
import time

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from inst_poster.models import Results, DataCredentials
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import NoSuchElementException, TimeoutException


class Poster():

    def __init__(self):
        self.current_file = os.path.abspath(__file__)
        self.current_directory = os.path.dirname(self.current_file)
        self.chrome_options = webdriver.ChromeOptions()
        self.driver = None
        self.action = None
        self.logger = logging.getLogger('my_logger')
        self.logger.setLevel(logging.DEBUG)
        self.log_file_path = os.path.join(os.path.dirname(__file__), 'log.txt')
        self.file_handler = logging.FileHandler(self.log_file_path)
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)

    def main(self, username, password, photo_and_caption_list):
        """
        MAIN
        """
        self.selenium_settings()
        self.change_ip()
        self.start(username, password, photo_and_caption_list)
        self.driver.quit()

    def start(self, username, password, photo_and_caption_list):
        """
        START AUTOPOSTER
        """
        self.driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(random.randint(5, 7))
        self.driver.refresh()
        time.sleep(random.randint(5, 7))
        self.click_allow_cookies_button()
        time.sleep(random.randint(15, 20))

        self.login_inst(username, password)
        # Check verif via email
        self.check_verification(username)
        self.click_allow_all_cookies_button(username)
        self.click_not_now_button()
        # Trying to post
        self.create_post(username, password, photo_and_caption_list)
        return

    def selenium_settings(self):
        """
        Settings : adding extension proxy.zip .
        """
        self.chrome_options.add_extension(os.path.join(self.current_directory + '/proxy.zip'))
        self.chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.action = ActionChains(self.driver)

    def change_ip(self, timeout=30):
        """
        Change current IP using rotation
        """
        try:
            self.driver.set_page_load_timeout(timeout)
            self.driver.get('https://proxy-seller.io/api/proxy/reboot?token=2f2c60e4-fcd2-4d57-adab-a410a2a5e127')
        except TimeoutException:
            self.logger.error("Timeout occurred while loading the page.")
            return


    def click_not_now_button(self):
        """
        Click the 'Not now' button (save login info?)
        """
        for i in range(3):
            try:
                not_now_button = self.driver.find_element(By.XPATH, "//div[@role='button' and contains(text(), 'Not now')]")
                WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and contains(text(), 'Not now')]")))
                if not_now_button:
                    self.action.move_to_element(not_now_button).click().perform()
                    break
                if i == 3:
                    break
                continue
            except:
                continue

    def click_allow_cookies_button(self):
        """
        Click the 'Allow all cookies' button
        """
        for i in range(5):
            try:
                button_xpath = "//button[@class='_a9-- _ap36 _a9_0' and @tabindex='0']"

                button = self.driver.find_element(By.XPATH, button_xpath)
                if button:
                    self.action.move_to_element(button).click().perform()
                    break
                if i == 5:
                    break
                continue
            except:
                pass

    def check_verification(self, username):
        """
        Checking whether verification is required via email
        """

        #  First check if needed to verify acc using mail
        for i in range(3):
            try:
                button_xpath = "//button[@class='_abn9 _abng _abnh _abnn']"
                wait = WebDriverWait(self.driver, 10)
                button = wait.until(EC.visibility_of_element_located((By.XPATH, button_xpath)))
                if button:
                    self.action.move_to_element(button).click().perform()
                    self.logger.warning(f"Account - {username}: Need to verify email!")
                    time.sleep(random.randint(180, 200))
                    break
                if i == 3:
                    break
                else:
                    self.logger.error(f"Account - {username}: Something went wrong. Can't find verify button")
                    continue
            except:
                break

        # Second check if needed to verify acc using mail
        for i in range(3):
            try:
                wait = WebDriverWait(self.driver, 10)
                confirmation_code_button = wait.until(
                    EC.presence_of_element_located((By.XPATH, "//span[text()='Send confirmation code']")))
                action_chains = ActionChains(self.driver)
                action_chains.move_to_element(confirmation_code_button).perform()
                if confirmation_code_button:
                    self.action.move_to_element(confirmation_code_button).click().perform()
                    self.logger.warning(f"Account - {username}: Need to verify email!")
                    time.sleep(random.randint(180, 200))
                    break
                if i == 3:
                    break
                else:
                    self.logger.error(f"Account - {username}: Something went wrong. Can't find verify button #2")
                    continue
            except:
                break

    def click_login_button(self, username, password, photo_and_caption_list):
        """
        Click the 'Log In' button
        """
        try:
            login_button = self.driver.find_element(By.XPATH, "//input[@name='login' and @value='Log In']")
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@name='login' and @value='Log In']")))
            self.action.move_to_element(login_button).click().perform()
            self.logger.error(f"Account - {username}: Need to login once again")
            self.login_inst(username, password)
            self.create_post(username, password, photo_and_caption_list)
            return True
        except:
            return False

    def choose_original_size(self, username):
        """
        Choose og size
        """
        for i in range(5):
            try:
                time.sleep(random.randint(3, 5))
                first_button = self.driver.find_element(By.XPATH, "//div[@class='_abfz _abg1']")
                WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='_abfz _abg1']")))
                self.action.move_to_element(first_button).click().perform()
                second_button = self.driver.find_element(By.XPATH,
                                                         "//div[contains(@class, 'x1i10hfl') and contains(@class, 'x1qjc9v5')]")
                WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(@class, 'x1i10hfl') and contains(@class, 'x1qjc9v5')]")))
                self.action.move_to_element(second_button)
                second_button.click()
                break
            except:
                continue
        return

    def login_inst(self, username, password):
        """
        Login
        """

        for i in range(5):
            try:
                username_input = self.driver.find_element("name", "username")
                if username_input:
                    self.action.move_to_element(username_input).click().send_keys(username).perform()
                    break
                continue
            except:
                self.logger.error('Cant find username input')
                return

        for i in range(5):
            try:
                password_input = self.driver.find_element("name", "password")
                if password_input:
                    self.action.move_to_element(password_input).click().send_keys(password).perform()
                    # Click enter
                    password_input.send_keys(Keys.RETURN)
                    time.sleep(random.randint(15, 20))
                    break
                continue
            except:
                self.logger.error('Cant find password input')

    def click_allow_all_cookies_button(self, username):
        """
        Click the 'Allow all cookies' button
        """
        try:
            allow_all_cookies_button = self.driver.find_element(By.XPATH,
                                                                "//div[@data-bloks-name='bk.components.Flexbox' and @role='button' and @aria-label='Allow all cookies']")
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH,
                                                                             "//div[@data-bloks-name='bk.components.Flexbox' and @role='button' and @aria-label='Allow all cookies']")))
            self.action.move_to_element(allow_all_cookies_button).click().perform()
            return
        except:
            return

    def create_post(self, username, password, photo_and_caption_list):
        """
        Create post function
        """
        for i, element in enumerate(photo_and_caption_list):
            self.logger.info(f"Account - {username}: Trying to publish post {i+1}/{len(photo_and_caption_list)}")
            for photo_path, caption in element.items():
                for i in range(5):
                    span_element = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Create")]'))
                    )
                    if span_element:
                        self.driver.execute_script("arguments[0].click();", span_element)
                        break
                    if i == 5:
                        self.logger.error(f"Account - {username}: Error. Can't create post")
                        return
                    else:
                        continue

                time.sleep(random.randint(12, 15))

                for i in range(5):
                    upload_button = self.driver.find_element("xpath", "//input[@type='file']")
                    new_login = self.click_login_button(username, password, photo_and_caption_list)
                    if new_login:
                        return True
                    if upload_button:
                        upload_button.send_keys(photo_path)
                        self.choose_original_size(username)
                        break
                    if i == 5:
                        self.logger.error(f"Account - {username}: Error. Can't select photo to post")
                        return
                    else:
                        continue

                time.sleep(random.randint(10, 14))

                for i in range(5):
                    next_button = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Next")]'))
                    )
                    if next_button:
                        self.action.move_to_element(next_button).click().perform()
                        break
                    if i == 5:
                        self.logger.error(f"Account - {username}: Error. Can't select photo to post")
                        return
                    else:
                        continue

                time.sleep(random.randint(4, 7))

                for i in range(5):
                    next_button = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Next")]'))
                    )
                    if next_button:
                        self.action.move_to_element(next_button).click().perform()
                        break
                    if i == 5:
                        self.logger.error(f"Account - {username}: Error. Can't select photo to post")
                        return
                    else:
                        continue

                time.sleep(random.randint(12, 15))

                # Caption input
                for i in range(5):
                    caption_input = self.driver.find_element("xpath", '//div[contains(text(), "Write a caption...")]')
                    if caption_input:
                        self.action.move_to_element(caption_input).click().send_keys(caption).perform()
                        break
                    if i == 5:
                        self.logger.error(f"Account - {username}: Error. Can't insert caption")
                        return
                    else:
                        continue

                time.sleep(random.randint(5, 10))

                # Click on share button
                for i in range(5):
                    share_button = self.driver.find_element("xpath", '//div[contains(text(), "Share")]')
                    if share_button:
                        self.action.move_to_element(share_button).click().perform()
                        time.sleep(random.randint(7, 10))
                        self.check_is_posted(username)
                        break
                    if i == 5:
                        self.logger.error(f"Account - {username}: Error. Can't find share button")
                        return
                    else:
                        continue

    def check_is_posted(self, username):
        """
        Check is shared
        """
        for i in range(5):
            try:
                time.sleep(random.randint(7, 10))
                self.driver.find_element(By.XPATH, "//*[contains(text(), 'Your post has been shared')]")
                self.logger.info(f"Account - {username}: Post shared")
                self.driver.refresh()
                time.sleep(random.randint(5, 7))
                post_link_element = self.driver.find_element(By.XPATH, "//a[contains(@href, '/p/')]")
                if post_link_element:
                    post_link = post_link_element.get_attribute("href")
                    self.logger.info(f"Account - {username}: Post link: {post_link}")
                    try:
                        data_credentials = DataCredentials.objects.get(login_inst=username)
                        result = Results.objects.create(data_credentials=data_credentials, good_link=post_link,
                                                        timestamp=datetime.now())
                    except:
                        self.logger.error(f"Account - {username}: Can't save link to database.")
                    return True

                if i == 5:
                    return False
                else:
                    continue
            except NoSuchElementException:
                self.logger.error(f"Account - {username}: Check is posted failed. Try to check it manually.")
                return False