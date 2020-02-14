from selenium import webdriver
from secrets import u, p
from time import sleep
import random
import json




class LifeExamSimulator:
    def __init__(self):

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
        nextbtn = self.driver.find_element_by_xpath('//*[@id="content_btnNext"]')
        nextbtn.click()
        sleep(5)

        popup = self.driver.find_element_by_xpath('//*[@id="wm-shoutout-64358"]/div[3]/div[1]/a[3]/span/div')
        popup.click()
        sleep(3)


        # SELECT COURSE
        course_menu = self.driver.find_element_by_xpath('//*[@id="selectedCourse"]')
        course_menu.click()
        sleep(1)
        health = self.driver.find_element_by_xpath('//*[@id="ctl00_PageHeader_ListView2_itemPlaceholderContainer"]/nav/ul/li[2]/a')
        health.click()
        sleep(3)
        # CLOSE TOOLTIP
        tooltip = self.driver.find_element_by_xpath('//*[@id="walkme-balloon-1299718"]/div/div[1]/div[4]/div[2]/div/button/span')
        tooltip.click()

        simulate_exam = self.driver.find_element_by_xpath('//*[@id="ctl00_content_FeatureRptr_ctl07_feature_"]')
        simulate_exam.click()
        sleep(2)
        next_to_exam = self.driver.find_element_by_xpath('//*[@id="ctl00_content_btnNext"]')
        next_to_exam.click()

        x=1
        while True:
            if x < 88:
                sleep(1)
                self.take_exam()
                print('Progress:', x)
                x += 1
            else:
                print('Ive Completed your exam sir.')
                sleep(500)

        
        
        
    def take_exam(self):

    
        answer1_text = self.driver.find_element_by_xpath('//*[@id="divContent"]/table/tbody/tr[3]/td[2]').text
        answer2_text = self.driver.find_element_by_xpath('//*[@id="divContent"]/table/tbody/tr[4]/td[2]').text
        answer3_text = self.driver.find_element_by_xpath('//*[@id="divContent"]/table/tbody/tr[5]/td[2]').text
        answer4_text = self.driver.find_element_by_xpath('//*[@id="divContent"]/table/tbody/tr[6]/td[2]').text

        answer1_input = self.driver.find_element_by_xpath('//*[@id="Answer1"]')
        answer2_input = self.driver.find_element_by_xpath('//*[@id="Answer2"]')
        answer3_input = self.driver.find_element_by_xpath('//*[@id="Answer3"]')
        answer4_input = self.driver.find_element_by_xpath('//*[@id="Answer4"]')

        answers = [answer1_input, answer2_input, answer3_input, answer4_input]
        random_answer = random.choice(answers)
        sleep(2)
        exam_question = self.driver.find_element_by_xpath('//*[@id="divContent"]/table/tbody/tr[1]/td[2]').text

        with open('qna-health.json') as f:
            data = json.load(f)
            sleep(5)
            
        if data.get(exam_question) == None:
            print('Question not found...')

            # SELECT A RANDOM ANSWER
            print('Seleceting random answer...')
            sleep(1)
            random_answer.click()
            sleep(3)
            print('Done selecting random.')
            next_question_btn = self.driver.find_element_by_xpath('//*[@id="ctl00_content_btnNext"]')
            next_question_btn.click()

        else:
            sleep(5)
            print('Checking for answer....')
            correct_answer = data[exam_question]
            sleep(1)
            if correct_answer.endswith('.'):
                correct_answer = correct_answer[0:-1]
            print(correct_answer)
            sleep(10)
            answers_t = [answer1_text, answer2_text, answer3_text, answer4_text]

            for answer in answers_t:
                if answer[3:].endswith('.'):
                    if answer[3:-1] == correct_answer:
                        a = {'1': 0, '2': 1, '3': 2, '4': 3}
                        print('Answer to match :', answer[3:-1])
                        sleep(3)
                        ans = answers[a[answer[0]]]

                        print('Selecting right answer...')
                        sleep(5)
                        ans.click()
                        sleep(10)
                else:
                    if answer[3:] == correct_answer:
                        a = {'1': 0, '2': 1, '3': 2, '4': 3}
                        print('Answer to match :', answer[3:])
                        sleep(3)
                        ans = answers[a[answer[0]]]

                        print('Selecting right answer...')
                        sleep(5)
                        ans.click()
                        sleep(10)
            
            
            print('Done.')
            correct_answer = ''
            next_question_btn = self.driver.find_element_by_xpath('//*[@id="ctl00_content_btnNext"]')
            next_question_btn.click()


LifeExamSimulator()