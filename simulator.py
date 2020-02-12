from selenium import webdriver
from secrets import u, p
from time import sleep
import json
import random


class ExamFx:
    def __init__(self, username, pw):
        driver_path = r"C:\Users\rhill\Downloads\chromedriver_win32\chromedriver.exe"
        self.driver = webdriver.Chrome(driver_path)
        self.driver.get('https://login.examfx.com')
        sleep(5)
        # ENTER EMAIL AND PASSWORD IN FIELDS AND LOGIN CLICK
        email_field = self.driver.find_element_by_xpath(
            "//*[@id='Content_txtEMail']")
        email_field.send_keys(username)
        pw_field = self.driver.find_element_by_xpath(
            "//*[@id='Content_txtPassword']")
        pw_field.send_keys(pw)
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
        # SELECT BEGINNING CHAPTER
        ch_dropdown = self.driver.find_element_by_xpath(
            '//*[@id="selectedChapter"]')
        ch_dropdown.click()
        ch = self.driver.find_element_by_xpath(
            '//*[@id="ctl00_PageHeader_TopicsLV_itemPlaceholderContainer"]/nav/ul/li[2]/a')
        ch.click()
        sleep(3)

        # SELECT QUIZ
        menu = self.driver.find_element_by_xpath(
            '//*[@id="aspnetForm"]/div[3]/header[2]/div/span[2]')
        menu.click()
        quiz = self.driver.find_element_by_xpath(
            '//*[@id="ctl00_PageHeader_QuizButton"]')
        quiz.click()
        sleep(3)

        progress = self.driver.find_element_by_xpath(
            '//*[@id="question-progress"]').text.split(' ')[1]

        while int(progress) <= 15:
            self.answer_question()
            sleep(3)
            progress = self.driver.find_element_by_xpath(
                '//*[@id="question-progress"]').text.split(' ')[1]


        print('Done')

    def close_popup(self):
        popup = self.driver.find_element_by_xpath(
            '//*[@id="wm-shoutout-64358"]/div[3]/div[1]/a[3]/span/div')
        popup.click()

    def answer_question(self):

        A = self.driver.find_element_by_id('divAnswer1')
        B = self.driver.find_element_by_id('divAnswer2')
        C = self.driver.find_element_by_id('divAnswer3')
        D = self.driver.find_element_by_id('divAnswer4')
        choices = [A, B, C, D]
        choice = random.choice(choices)

        # quizResult = self.driver.find_element_by_xpath('//*[@id="score-overview"]/table/tbody/tr/td[4]').text

        # menu2btn = self.driver.find_element_by_xpath('//*[@id="aspnetForm"]/header[2]/div/span')
        # reviewQuizBtn = self.driver.find_element_by_xpath('//*[@id="ctl00_PageHeader_ReviewLink"]')
        # closeQuizBtn = self.driver.find_element_by_xpath('//*[@id="ctl00_PageHeader_CloseReviewLink"]')

        with open('qna.json') as f:
            data = json.load(f)

        question = self.driver.find_element_by_xpath('//*[@id="divQuestion"]').text
        if data.get(question) == None:

            # SELECT RANDOM ANSWER
            choice.click()
            sleep(3)
            # GET CORRECT ANSWER AND SET TO VARIABLE
            correct_answer = self.driver.find_element_by_class_name('correct-choice').text.split('\n')[1]
            # SET Q & A IN DATA DICT
            data[question] = correct_answer
            # DUMP DICT BACK INTO JSON FILE
            with open('qna.json', 'w') as f:
                json.dump(data, f, indent=2)
            # CLICK NEXT
            correct_answer = ''
            next_q = self.driver.find_element_by_xpath('//*[@id="ctl00_content_NextQuestionLink"]')
            next_q.click()
        else:
            print('Checking for answer....')
            # GET CORRECT ANSWER FROM DATA
            correct_answer = data[question]
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
                        sleep(1)
            # SELECT THE CORRECT ANSWER BY A CLICK ACTION
            # CLICK NEXT
            correct_answer = ''
            print('Done.')
            next_q = self.driver.find_element_by_xpath('//*[@id="ctl00_content_NextQuestionLink"]')
            next_q.click()
            

                


ExamFx(u,p)
