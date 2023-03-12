from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
import time
import datetime
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPlainTextEdit
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
import hashlib
import requests
from Headers import headerLogin, headerOrgId, headerOriginId, headerGoal
import json
import uuid

weeklyClockInDict = dict()

def userInformationRead():
    f = open('userInformation.txt', 'r')
    phoneNumber = f.readline()
    phoneNumber = phoneNumber.rstrip()
    password = f.readline()
    f.close()
    md5 = hashlib.md5(password.encode(encoding='utf-8'))
    return phoneNumber, md5.hexdigest()

def test():
    browser = webdriver.Chrome()
    browser.get(URL)

    head = browser.find_element(By.XPATH, '//*[@id="getMonthData"]/em')
    # button = head.find_element(By.CLASS_NAME, "em class")
    head.click()
    time.sleep(1)

    path="WebSource.html"
    file=open(path, 'w', encoding='UTF-8')
    file.write(browser.page_source)

    soup = BeautifulSoup(open("WebSource.html", encoding='UTF-8'), "html.parser")
    # print(soup)
    clearfix = soup.select('ul[class="date-list clearfix"]')
    # print(clearfix)
    monthlyRecord = list()
    for i in clearfix:
        for ii in i.find_all('li'):
            data_check = ii.get('data-check')
            if data_check != None:
                monthlyRecord.append(data_check)

    pattern = re.compile('([0-1]?[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])')
    for i in range(0, len(monthlyRecord)):
        print("Day: ", i+1, "     ", end='')
        timeStamp = re.findall(pattern, monthlyRecord[i])
        for ii in timeStamp:
            print(ii)


def calculate(clockInTimeThisMonth, clockInTimeLastMonth):
    # 根据当前时间确定日期与周次
    time_tuple = time.localtime(time.time())
    theWeekToday = datetime.date(time_tuple[0], time_tuple[1], time_tuple[2]).isoweekday()
    # print("今天是{}年{}月{}日， 星期{}".format(time_tuple[0], time_tuple[1], time_tuple[2], theWeekToday))

    # 根据周次是否隔月确定两种计算方法
    startDayThisWeek = time_tuple[2]-(theWeekToday-1)

    clockInTimeSum=0
    if startDayThisWeek >= 1:
        clockInTimeSum = clockInTimeSum + sumTime(startDayThisWeek, time_tuple[2], clockInTimeThisMonth)
    else:
        clockInTimeSum = clockInTimeSum + sumTime(len(clockInTimeLastMonth)-1, len(clockInTimeLastMonth)-(1-startDayThisWeek)+2, clockInTimeLastMonth) + sumTime(1, time_tuple[2], clockInTimeThisMonth)

    return clockInTimeSum


def sumTime(startDay, endDay, clockInTimeMonthly):
    # i+1为当天日期，clockInTimeMonthly[i]为当天所有打卡时间
    clockInTimeSum = 0
    # print("Start Day: ", startDay)
    # print("End Day: ", endDay)
    for i in range(startDay-1, endDay):
        # print("Date {}: ".format(i+1))
        j = 0
        clockInTimeDaily = 0
        while j < len(clockInTimeMonthly[i])-1:
            # print("j:", j)
            if isCorrectTimeSlot(clockInTimeMonthly[i][j], clockInTimeMonthly[i][j+1]) == 0:
                clockInTimeDaily = clockInTimeDaily + int(clockInTimeMonthly[i][j+1][0]) - 13 + (int(clockInTimeMonthly[i][j+1][1]) - 30)*1.0/60
                j = j + 2
            elif isCorrectTimeSlot(clockInTimeMonthly[i][j], clockInTimeMonthly[i][j+1]) > 0:
                clockInTimeDaily = clockInTimeDaily + int(clockInTimeMonthly[i][j + 1][0]) - int(clockInTimeMonthly[i][j][0]) + (int(clockInTimeMonthly[i][j + 1][1]) - int(clockInTimeMonthly[i][j][1])) * 1.0 / 60
                j = j + 2
            else:
                j = j + 1
        # print("    ClockInTimeToday: {:.2f}".format(clockInTimeDaily), "hours")
        weeklyClockInDict[i+1] = clockInTimeDaily
        clockInTimeSum = clockInTimeSum + clockInTimeDaily
    return clockInTimeSum

def isCorrectTimeSlot(startTime, endTime):
    if int(startTime[0])*60+int(startTime[1]) >= 450 and int(endTime[0])*60+int(endTime[1]) <= 750:
        return 1
    elif int(startTime[0])*60+int(startTime[1]) >= 755 and int(startTime[0])*60+int(startTime[1]) <= 810 and int(endTime[0])*60+int(endTime[1]) <= 1110:
        return 0
    elif int(startTime[0])*60+int(startTime[1]) >= 810 and int(endTime[0])*60+int(endTime[1]) <= 1110:
        return 2
    elif int(startTime[0])*60+int(startTime[1]) >= 1115 and int(endTime[0])*60+int(endTime[1]) <= 1439:
        return 3
    else:
        return -1

'''
    spider函数用于根据URL爬取当月考勤数据，生成当月已有打卡时间数据
    补充：需要上个月的考勤数据
'''
def spider(URL):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('log-level=3')

    browser = webdriver.Chrome(options=options)
    browser.get(URL)

    clockInTimeThisMonth = calendarRead(browser)

    head = browser.find_element(By.XPATH, '//*[@id="getMonthData"]/em')
    head.click()
    time.sleep(1)

    clockInTimeLastMonth = calendarRead(browser)

    return clockInTimeThisMonth, clockInTimeLastMonth


def calendarRead(browser):
    sourceCode = BeautifulSoup(browser.page_source, "html.parser")
    dateList = sourceCode.select('ul[class="date-list clearfix"]')

    monthlyRecord = list()
    for date in dateList:
        for clockIn in date.find_all('li'):
            dataCheck = clockIn.get('data-check')
            if dataCheck != None:
                monthlyRecord.append(dataCheck)

    # 提取时间
    clockInTimeMonthly = list(list())
    pattern = re.compile('([0-1]?[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])')
    for i in range(0, len(monthlyRecord)):
        # print("Day: ", i + 1, "     ", end='')
        timeStamp = re.findall(pattern, monthlyRecord[i])
        clockInTimeMonthly.append(timeStamp)

    return clockInTimeMonthly


def showUI(weeklyClockInDict, totalTime):
    app = QApplication(sys.argv)
    w = QWidget()
    w.resize(600, 300)

    screen = QtWidgets.QDesktopWidget().screenGeometry()
    size = w.geometry()
    w.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    w.setWindowTitle("打卡时长统计助手 v1.0")
    w.setWindowIcon(QIcon("icon.ico"))

    text = QPlainTextEdit(w)
    weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    index = 0
    for key in weeklyClockInDict:
        if key < 10:
            content = "0" + str(key) + " " + weekday[index] + "  " +str(round(weeklyClockInDict[key], 2)) + " 小时"
        else:
            content =str(key) + " " + weekday[index] + "  " + str(round(weeklyClockInDict[key], 2)) + " 小时"
        text.appendPlainText(content)
        index = index + 1

    content = "本周累计打卡时间: " + str(round(totalTime, 2)) + " 小时"
    text.appendPlainText(content)
    if totalTime > 54:
        content = "恭喜您，本周打卡任务已完成，记得写周报喵！"
        text.appendPlainText(content)
    else:
        content = "还需打卡 " + str(round(54-totalTime,2)) + " 小时，请继续努力喵！"
        text.appendPlainText(content)

    text.setReadOnly(True)
    text.setStyleSheet('font-size: 20px; font-weight: bold; font-family: FangSong')
    text.resize(w.width(), w.height())

    w.show()
    sys.exit(app.exec_())

'''
    
'''
def login(phoneNumber, password):
    # Get Login Token and User_id
    # print(phoneNumber)
    # print(password)
    rLogin = requests.post("https://v2-app.delicloud.com/api/v2.0/auth/loginMobile",
                       headers=headerLogin,
                       json={'password': password, 'mobile': phoneNumber})
    loginInformation = rLogin.content.decode(rLogin.apparent_encoding)
    loginInformation = json.loads(loginInformation)
    token = loginInformation["data"]["token"]
    user_id = loginInformation["data"]["user_id"]
    # print("token: ", token)
    # print("user_id: ", user_id)

    # Get Organization_id
    GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
    GMT_TIME = datetime.datetime.utcnow().strftime(GMT_FORMAT)

    headerOrgId["user_id"] = user_id
    headerOrgId["Authorization"] = token
    headerOrgId["If-Modified-Since"] = GMT_TIME

    urlFindOrgId = "https://v2-app.delicloud.com/api/v2.3/org/findOrgDetailByUserId?user_id=" + user_id + "&is_only_usable=true"
    rOrgid = requests.get(urlFindOrgId, headers=headerOrgId)
    orgInfo = rOrgid.content.decode(rOrgid.apparent_encoding)
    orgInfo = json.loads(orgInfo)
    org_id = orgInfo["data"][0]["id"]
    # print("Org Id: ", org_id)

    # Get Orgin_member_id
    headerOriginId["org_id"] = org_id
    headerOriginId["user_id"] = user_id
    headerOriginId["Authorization"] = token
    headerOriginId["If-Modified-Since"] = GMT_TIME

    urlFindOriginId = "https://v2-app.delicloud.com/api/v2.0/orgUser/findOrgUserDetailByOrgIdAndUserId?org_id=" + org_id + "&user_id=" + user_id
    # print(urlFindOriginId)
    rOriginId = requests.get(urlFindOriginId, headers=headerOriginId)
    originInfo = rOriginId.content.decode(rOriginId.apparent_encoding)
    # print(originInfo)
    originInfo = json.loads(originInfo)
    origin_member_id = originInfo["data"]["origin_member_id"]
    # print("Origin_member_id: ", origin_member_id)

    # Get MainWindow Info
    headerGoal["org_id"] = org_id
    headerGoal["token"] = token
    headerGoal["user_id"] = user_id
    headerGoal["v1_member_id"] = origin_member_id
    headerGoal["uuid"] = str(uuid.uuid4())

    urlMW = "https://kq.delicloud.com/attend/index/home"
    rGoal = requests.get(urlMW, headers=headerGoal)
    goalInfo = rGoal.content.decode(rGoal.apparent_encoding)
    # print(goalInfo)
    goalInfo = json.loads(goalInfo)
    result = goalInfo["data"]["list"][0]["url"]
    # print(result)
    return result

if __name__ == "__main__":
    phoneNumber, password = userInformationRead()
    URL = login(phoneNumber, password)
    thisMonth, lastMonth = spider(URL)
    totalTime = calculate(thisMonth, lastMonth)
    showUI(weeklyClockInDict, totalTime)