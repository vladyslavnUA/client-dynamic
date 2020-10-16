from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random
import sys
import time
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

class TargetBot:
    username = 'aladdinmattressandrug@gmail.com'
    password = 'Albertlevy@2020'

    def __init__(self):
        self.browser = webdriver.Firefox(executable_path='/Users/Anas/Downloads/geckodriver')
        # self.login()
        self.run()
        
        
    def login(self):
        self.browser.get('https://accounts.craigslist.org/login?rp=%2Flogin%2Fhome&rt=L')
        time.sleep(2)

        username_field = self.browser.find_element_by_xpath("//*[@id='inputEmailHandle']")
        username_field.clear()
        username_field.send_keys(self.username)
        time.sleep(1)

        password_field = self.browser.find_element_by_xpath("//*[@id='inputPassword']")
        password_field.clear()
        password_field.send_keys(self.password)
        time.sleep(1)

        login_button = self.browser.find_element_by_xpath("//*[@id='login']")
        login_button.click()
        time.sleep(2)

    def run(self):
        self.createPost()
        # self.getTopPosts()
        # self.execute()
        # self.finalize()

    def createPost(self):
        self.browser.get('https://www.target.com/s?searchTerm=2020+mosaic+football&category=0%7CAll%7Cmatchallpartial%7Call+categories&tref=typeahead%7Cterm%7C0%7C2020+mosaic+football%7C%7C%7C%7Cservice%7C10%7C1%7C0%7Cspellcorrect&searchRawTerm=mosaic+footbal&sortBy=bestselling&Nao=0')
        # click on new post button
        self.clickButton("//*[@id='mainContainer']/div[4]/div[2]/div/div[2]/div[3]/div[2]/ul/li[1]/div/div[2]/div/div/div/div[5]/div[1]/div/div/button")
        
        
        
        
    def uploadImages(self, image):
        pass
    
    def fillInput(self, value, input):
        time.sleep(1)
        element = self.browser.find_element_by_xpath(input)
        element.clear()
        element.send_keys(value)
    
    def clickButton(self, button):
        time.sleep(1)
        try:
            continueButton = self.browser.find_element_by_xpath(button)
            continueButton.click()
        except:
            print("Could not click on button"+button)
        
    def checkbox(self, input):
        time.sleep(1)
        element = self.browser.find_element_by_xpath(input)
        if not element.is_selected():
            element.click()
        
    def getTopPosts(self):
        for hashtag in self.hashtags:
            self.browser.get('https://www.instagram.com/explore/tags/' + hashtag +'/')
            time.sleep(2)

            links = self.browser.find_elements_by_tag_name('a')
            condition = lambda link: '.com/p/' in link.get_attribute('href')
            valid_links = list(filter(condition, links))

            for i in range(0, 9):
                link = valid_links[i].get_attribute('href')
                if link not in self.links:
                    self.links.append(link)

    def execute(self):
        for link in self.links:
            self.browser.get(link)
            time.sleep(1)

            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            
            self.comment()
            time.sleep(2)
            
            self.like()

            self.price += 0.02
            sleeptime = random.randint(18, 28)
            time.sleep(sleeptime)

    def comment(self):
        comment_input = lambda: self.browser.find_element_by_tag_name('textarea')
        comment_input().click()
        comment_input().clear()

        comment = random.choice(self.comments)
        for letter in comment:
            comment_input().send_keys(letter)
            delay = random.randint(1, 7) / 30
            time.sleep(delay)

        comment_input().send_keys(Keys.RETURN)

    def like(self):
        like_button = lambda: self.browser.find_element_by_class_name('wpO6b ')
        like_button().click()

    def finalize(self):
        print('You gave $' + string(self.price) + ' back to the community.')
        self.browser.close()
        sys.exit()

bot = TargetBot()


