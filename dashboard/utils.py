import re
from models import Classes
import mechanize
from bs4 import BeautifulSoup
from selenium import webdriver
import time
def make_class_list(netid, password):
    br = mechanize.Browser()
    br.open("https://cas.byu.edu/cas/login?service=https%3A%2F%2Flearningsuite.byu.edu")
    br.addheaders = [ ( 'User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1' ) ]

    class WhatTheHellJustHappened:
        pass
    class UglyRaceCaseCondition:
        pass

    # follow second link with element text matching regular expression
    br.select_form(nr = 0)
    br.form['username'] = username
    br.form['password'] = password
    br.submit()
    soup = BeautifulSoup(br.response().read())
    script = soup.find_all('script')[-1]
    location_href = script.text.strip().splitlines()[-1]
    #print location_href
    code = location_href.split('.')
    code = code[-1][:-2]
    #print code
    into_learning_suite = br.open("https://learningsuite.byu.edu/."+code+"/student/top").read()
    learning_suite_soup = BeautifulSoup(into_learning_suite)
    #print learning_suite_soup
    class_codes = learning_suite_soup.find_all(attrs={ "class" : "courseCode" })
    class_nums = learning_suite_soup.find_all(attrs={ "class" : "courseNum" })
    class_titles = learning_suite_soup.find_all(attrs={ "class" : "courseTitle" })
    tab_soup = BeautifulSoup(into_learning_suite).find(id="myTabContent")
    class_cids = tab_soup.find_all(attrs={ "class" : "course-title" })
    #print class_codes
    #print class_nums
    #print class_titles
    #print class_cids
    if len(class_codes) != len(class_nums) or len(class_nums) != len(class_titles):
        raise WhatTheHellJustHappened
    classes = {}
    for _class in range(len(class_codes)):
        class_code = class_codes[_class].text+class_nums[_class].text
        course_title = class_titles[_class].text
        cid = class_cids[_class]['href'].split('/')[1]
        table_soup = BeautifulSoup(br.open("https://learningsuite.byu.edu/."+code+"/"+cid+"/student/gradebook/scale").read()).find(id="gradingScale")
        entries = table_soup.find_all('td')
        grade_scale = {}
        num_intervals = len(entries)/2
        for x in range(num_intervals):
            grade_scale[entries[(x*2)].text] = entries[(x*2)+1].text
        if len(grade_scale) == 0:
            grade_scale = {'A':'93%', 'A-':'90%', 'B+':'87%', 'B':'83%', 'B-':'80%', 'C+':'77%', 'C':'73%', 'C-':'70%', 'D+':'67%', 'D':'63%', 'D-':'60%', 'E':'0%'}
        classes[_class] = {'class_code':class_code.replace(" ", ""), 'course_title':course_title, 'cid':cid, 'grade_scale':grade_scale}

    browser = webdriver.PhantomJS(executable_path="./phantomjs")
    for index in classes:
        """The following is really slow.... So instead I believe the solution is to store time of sync and warn them of last sync"""
        cid = classes[index]['cid']
        browser.get("https://learningsuite.byu.edu/."+code+"/"+cid+"/student/gradebook")
        if 'login' in browser.current_url:
            username_input = browser.find_element_by_name('username')
            username_input.send_keys(username)

            password_input = browser.find_element_by_name('password')
            password_input.send_keys(password)

            form = browser.find_element_by_id('credentials')
            form.submit()

        browser.execute_script
        time.sleep(.05)
        grade_soup = BeautifulSoup(browser.page_source)
        grade = grade_soup.find(id="currentScore").find_all('b')[1].text
        if grade is None:
            raise UglyRaceCaseCondition
        classes[index]['grade'] = grade
    for x in classes:
        Classes.objects.create(course_code=classes[x]['class_code'], course_grade=classes[x]['grade'], course_title=classes[x]['course_title'], cid=classes[x]['cid'], grade_scale=str(classes[x]['grade_scale']))
