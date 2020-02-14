from selenium import webdriver
from secrets import u, p
from time import sleep
import json
import random


class HealthFxSimulator:

    def __init__(self):

        # email = input('Email: ')
        # password = input('Password: ')

        driver_path = r"C:\Users\rhill\Downloads\chromedriver_win32\chromedriver.exe"
        self.driver = webdriver.Chrome(driver_path)
        self.driver.get('https://login.examfx.com')
        sleep(5)
        # ENTER EMAIL AND PASSWORD IN FIELDS AND LOGIN CLICK
        email_field = self.driver.find_element_by_xpath(
            "//*[@id='Content_txtEMail']")
        email_field.send_keys(u)
        pw_field = self.driver.find_element_by_xpath(
            "//*[@id='Content_txtPassword']")
        pw_field.send_keys(p)
        loginBtn = self.driver.find_element_by_xpath(
            "//*[@id='Content_lbnLogin']")
        loginBtn.click()
        sleep(5)

        # SELECT THE COURSE FROM DEFAULT PAGE
        course = self.driver.find_element_by_xpath(
            "//*[@id='Content_divCourseLinks']/a")
        course.click()
        sleep(5)

        # CLICK NEXT ON VERIFICATION PAGE
        nextbtn = self.driver.find_element_by_xpath(
            '//*[@id="content_btnNext"]')
        nextbtn.click()
        sleep(3)

        try:
            # CLOSE THE POP UP FOR TUTORIAL
            self.close_popup()
            sleep(3)
        except Exception:

            # SELECT COURSE
            health = self.driver.find_element_by_xpath(
                '//*[@id="ctl00_PageHeader_ListView2_itemPlaceholderContainer"]/nav/ul/li[2]/a')
            health.click()
            sleep(3)

        # EXIT TOOLTIP
        try:
            tooltip = self.driver.find_element_by_xpath(
                '//*[@id="walkme-balloon-1299718"]/div/div[1]/div[4]/div[2]/div/button/span')
            tooltip.click()
            sleep(3)
        except Exception:

            # SELECT THE STUDY BY TOPIC OPTION
            study_topics = self.driver.find_element_by_xpath(
                '//*[@id="ctl00_content_FeatureRptr_ctl01_feature_"]')
            study_topics.click()
            sleep(3)

        # SCROLL PAGE
        self.scroll_page()
        sleep(1)

        # SELECT CHAPTERS DROPDOWN
        # ch_dropdown = self.driver.find_element_by_xpath(
        #     '//*[@id="selectedChapter"]')
        # ch_dropdown.click()
        # sleep(1)

        #SELECT INCOMPLETE CHAPTER
        # self.select_incomplete_chapter()

        # SELECTING FIRST CHAPTER IN DROPDOWN LIST
        # ch = self.driver.find_element_by_xpath(
        #     '//*[@id="ctl00_PageHeader_TopicsLV_itemPlaceholderContainer"]/nav/ul/li[2]/a')
        # ch.click()
        # sleep(3)

        # SELECT QUIZ
        menu = self.driver.find_element_by_xpath(
            '//*[@id="aspnetForm"]/div[3]/header[2]/div/span[2]')
        menu.click()
        quiz = self.driver.find_element_by_xpath(
            '//*[@id="ctl00_PageHeader_QuizButton"]')
        quiz.click()
        sleep(3)
        x=1
        while True:
            if x < 16:
                sleep(2)
                self.take_quiz()
                print('Progress is:', x)
                x += 1
            else:
                sleep(3)
                quizResult = self.driver.find_element_by_xpath('//*[@id="score-overview"]/table/tbody/tr/td[4]').text
                if quizResult == 'Pass':
                    x = 1
                    self.continue_to_next_quiz()
                else:
                    x = 1
                    sleep(1)
                    self.retake_quiz()

        print('Done')

    def close_popup(self):
        popup = self.driver.find_element_by_xpath(
            '//*[@id="wm-shoutout-64358"]/div[3]/div[1]/a[3]/span/div')
        popup.click()

    def take_quiz(self):
        progress = 1
        A = self.driver.find_element_by_id('divAnswer1')
        B = self.driver.find_element_by_id('divAnswer2')
        C = self.driver.find_element_by_id('divAnswer3')
        D = self.driver.find_element_by_id('divAnswer4')
        choices = [A, B, C, D]
        choice = random.choice(choices)
        sleep(2)
        question = self.driver.find_element_by_xpath('//*[@id="divQuestion"]').text
        with open('qna-health.json') as f:
            data = json.load(f)

        

            if data.get(question) == None:
                print('Question not found...')
                # SELECT RANDOM ANSWER
                print('Selecting answer...')
                sleep(7)
                choice.click()
                sleep(3)
                # GET CORRECT ANSWER AND SET TO VARIABLE
                correct_answer = self.driver.find_element_by_class_name('correct-choice').text.split('\n')[1]
                # SET Q & A IN DATA DICT
                data[question] = correct_answer
                # DUMP DICT BACK INTO JSON FILE
                with open('qna-health.json', 'w') as f:
                    json.dump(data, f, indent=2)
                # CLICK NEXT
                correct_answer = ''
                sleep(3)
                print('Done. Retrieved correct answer.')
                next_q = self.driver.find_element_by_xpath('//*[@id="ctl00_content_NextQuestionLink"]')
                next_q.click()
                
            else:
                sleep(5)
                print('Checking for answer....')
                correct_answer = data[question]
                print(correct_answer)
                sleep(10)
                # GET CORRECT ANSWER FROM DATA
                # ITERATE THROUGH ANSWERS LIST FOR A MATCH
                answer_el = self.driver.find_elements_by_class_name('answer-option')
                # MUST BE SPLIT BY '\n' AND CHECK FOR EMPTIES
                answers = [answer.text for answer in answer_el]
                for answer in answers:
                    if answer != '':
                        if answer.split('\n')[1] == correct_answer:
                            c = {'A': 0, 'B': 1, 'C':2, 'D': 3}
                            ch = choices[c[answer.split('\n')[0]]]
                            ch.click()
                            sleep(3)
                # SELECT THE CORRECT ANSWER BY A CLICK ACTION
                # CLICK NEXT
                correct_answer = ''
                print('Done.')
                next_q = self.driver.find_element_by_xpath('//*[@id="ctl00_content_NextQuestionLink"]')
                next_q.click()
                
            
    def continue_to_next_quiz(self):
        # CHOOSE TO REVIEW MATERIAL OR QUIZ
        menu2btn = self.driver.find_element_by_xpath('//*[@id="aspnetForm"]/header[2]/div/span')
        menu2btn.click()
        # CHOOSE REVIEW QUIZ OPTION
        sleep(2)
        topics = self.driver.find_element_by_xpath('//*[@id="ctl00_PageHeader_StudyTopicsLink"]')
        topics.click()
        sleep(4)
        self.scroll_page()
        sleep(6)
        menu = self.driver.find_element_by_xpath('//*[@id="aspnetForm"]/div[3]/header[2]/div/span[2]')
        menu.click()
        quiz = self.driver.find_element_by_xpath('//*[@id="ctl00_PageHeader_QuizButton"]')
        quiz.click()
        # CLOSE QUIZ WILL AUTOMATICALLY ADVANCE
        # closeQuizBtn = self.driver.find_element_by_xpath('//*[@id="ctl00_PageHeader_CloseReviewLink"]')
        # closeQuizBtn.click()

    def retake_quiz(self):
        # CHOOSE TO REVIEW MATERIAL OR QUIZ
        menu2btn = self.driver.find_element_by_xpath(
            '//*[@id="aspnetForm"]/header[2]/div/span')
        menu2btn.click()
        # CHOOSE REVIEW QUIZ OPTION
        sleep(2)
        reviewQuizBtn = self.driver.find_element_by_xpath(
            '//*[@id="ctl00_PageHeader_ReviewLink"]')
        reviewQuizBtn.click()
        sleep(5)
        # CLOSE QUIZ WILL AUTOMATICALLY ADVANCE
        closeQuizBtn = self.driver.find_element_by_xpath(
            '//*[@id="ctl00_PageHeader_CloseReviewLink"]')
        closeQuizBtn.click()
        sleep(3)
        self.scroll_page()
        sleep(7)
        menu = self.driver.find_element_by_xpath('//*[@id="aspnetForm"]/div[3]/header[2]/div/span[2]')
        menu.click()
        quiz = self.driver.find_element_by_xpath('//*[@id="ctl00_PageHeader_QuizButton"]')
        quiz.click()


    def select_incomplete_chapter(self):

        incomplete_chapter = self.driver.find_elements_by_class_name('chapter-incomplete')

        print(incomplete_chapter)

        for chapter in incomplete_chapter:
            chapter[0].click() 
    
    def scroll_page(self):

        SCROLL_PAUSE_TIME = 1

        # Get scroll height
        """last_height = driver.execute_script("return document.body.scrollHeight")

        this dowsnt work due to floating web elements on youtube
        """

        last_height = self.driver.execute_script("return document.documentElement.scrollHeight")
        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0,document.documentElement.scrollHeight);")

            # Wait to load page
            sleep(2)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                print("break")
                break
            last_height = new_height

HealthFxSimulator()
