from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
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
import logging

logging.basicConfig(level=logging.INFO)
weeklyClockInDict = dict()

class Date:
    def __init__(self,year,month,day):
        self.year=year
        self.month=month
        self.day=day

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

def calculate2(clockInTimeThisMonth, clockInTimeLastMonth):
    # 根据当前时间确定日期与周次
    # theDateToday = datetime.datetime.today()
    # theWeekToday = theDateToday.isoweekday()
    # firstDayThisWeek = theDateToday - datetime.timedelta(days=theDateToday.weekday())
    # firstDayLastWeek = firstDayThisWeek - datetime.timedelta(days=7)
    # lastDayLastWeek = firstDayThisWeek - datetime.timedelta(days=1)
    theDateToday = Date(2023, 12, 10)
    firstDayThisWeek = Date(2023, 12, 4)
    firstDayLastWeek = Date(2023, 11, 27)
    lastDayLastWeek = Date(2023, 12, 3)
    # time_tuple = time.localtime(time.time())
    # theWeekToday = datetime.date(time_tuple[0], time_tuple[1], time_tuple[2]).isoweekday()
    # logging.info("今天是{}年{}月{}日， 星期{}".format(2023, 12, 10, 7))

    # startDayThisWeek = time_tuple[2] - theWeekToday + 1

    clockInTimeSum = 0
    lastWeekTotalTime = 0

    if firstDayThisWeek.month == theDateToday.month:
        clockInTimeSum = clockInTimeSum + sumTime(firstDayThisWeek.day, theDateToday.day, clockInTimeThisMonth, 1)
    else:
        lastDayOfLastMonth = datetime.date(firstDayThisWeek.year + int(firstDayThisWeek.month / 12),
                                           (firstDayThisWeek.month % 12) + 1, 1) - datetime.timedelta(days=1)
        clockInTimeSum = clockInTimeSum + sumTime(firstDayThisWeek.day, lastDayOfLastMonth.day, clockInTimeLastMonth,
                                                  1) + sumTime(1, theDateToday.day, clockInTimeThisMonth, 1)

    if firstDayLastWeek.month == lastDayLastWeek.month & firstDayLastWeek.month == theDateToday.month:
        lastWeekTotalTime = lastWeekTotalTime + sumTime(firstDayLastWeek.day, lastDayLastWeek.day, clockInTimeThisMonth,0)
    elif firstDayLastWeek.month == lastDayLastWeek.month & firstDayLastWeek.month != theDateToday.month:
        lastWeekTotalTime = lastWeekTotalTime + sumTime(firstDayLastWeek.day, lastDayLastWeek.day, clockInTimeLastMonth,0)
    else:
        lastDayOfLastMonth = datetime.date(firstDayLastWeek.year + int(firstDayLastWeek.month / 12), (firstDayLastWeek.month % 12) + 1, 1) - datetime.timedelta(days=1)
        lastWeekTotalTime = lastWeekTotalTime + sumTime(firstDayLastWeek.day, lastDayOfLastMonth.day, clockInTimeLastMonth,0) + sumTime(1, lastDayLastWeek.day, clockInTimeThisMonth,0)
    # print("LastWeekTime: ", lastWeekTotalTime)
    return clockInTimeSum, lastWeekTotalTime

'''
    calculate函数的输入为上个月及本月每天的考勤数据
    根据这两个数组计算每天的考勤时间
'''
def calculate(clockInTimeThisMonth, clockInTimeLastMonth):
    # 根据当前时间确定日期与周次
    theDateToday = datetime.datetime.today()
    theWeekToday = theDateToday.isoweekday()
    firstDayThisWeek = theDateToday - datetime.timedelta(days=theDateToday.weekday())
    firstDayLastWeek = firstDayThisWeek - datetime.timedelta(days=7)
    lastDayLastWeek = firstDayThisWeek - datetime.timedelta(days=1)

    # time_tuple = time.localtime(time.time())
    # theWeekToday = datetime.date(time_tuple[0], time_tuple[1], time_tuple[2]).isoweekday()
    logging.info("今天是{}年{}月{}日， 星期{}".format(theDateToday.year, theDateToday.month, theDateToday.day, theWeekToday))

    # startDayThisWeek = time_tuple[2] - theWeekToday + 1

    clockInTimeSum = 0
    lastWeekTotalTime = 0

    if firstDayThisWeek.month == theDateToday.month:
        clockInTimeSum = clockInTimeSum + sumTime(firstDayThisWeek.day, theDateToday.day, clockInTimeThisMonth,1)
    else:
        lastDayOfLastMonth = datetime.date(firstDayThisWeek.year + int(firstDayThisWeek.month / 12), (firstDayThisWeek.month % 12) + 1, 1) - datetime.timedelta(days=1)
        clockInTimeSum = clockInTimeSum + sumTime(firstDayThisWeek.day, lastDayOfLastMonth.day, clockInTimeLastMonth,1) + sumTime(1, theDateToday.day, clockInTimeThisMonth,1)
    # startDayThisWeek变量用于判断当前周是否是跨月周，如果跨月需要额外的计算
    # if startDayThisWeek >= 1:
    #     clockInTimeSum = clockInTimeSum + sumTime(startDayThisWeek, time_tuple[2], clockInTimeThisMonth)
    # else:
    #     clockInTimeSum = clockInTimeSum \
    #                      + sumTime(len(clockInTimeLastMonth) + startDayThisWeek, len(clockInTimeLastMonth), clockInTimeLastMonth) \
    #                      + sumTime(1, time_tuple[2], clockInTimeThisMonth)

    if firstDayLastWeek.month == lastDayLastWeek.month & firstDayLastWeek.month == theDateToday.month:
        lastWeekTotalTime = lastWeekTotalTime + sumTime(firstDayLastWeek.day, lastDayLastWeek.day, clockInTimeThisMonth,0)
    elif firstDayLastWeek.month == lastDayLastWeek.month & firstDayLastWeek.month != theDateToday.month:
        lastWeekTotalTime = lastWeekTotalTime + sumTime(firstDayLastWeek.day, lastDayLastWeek.day, clockInTimeLastMonth,0)
    else:
        lastDayOfLastMonth = datetime.date(firstDayLastWeek.year + int(firstDayLastWeek.month / 12), (firstDayLastWeek.month % 12) + 1, 1) - datetime.timedelta(days=1)
        lastWeekTotalTime = lastWeekTotalTime + sumTime(firstDayLastWeek.day, lastDayOfLastMonth.day, clockInTimeLastMonth,0) + sumTime(1, lastDayLastWeek.day, clockInTimeThisMonth,0)

    return clockInTimeSum,lastWeekTotalTime

'''
    sumTime函数用于计算一周内每天的考勤时间，核心功能实现函数
    flag判断上周函数本周
'''
def sumTime(startDay, endDay, clockInTimeMonthly, flag):
    # i+1为当天日期，clockInTimeMonthly[i]为当天所有打卡时间

    startTime = time.time()

    clockInTimeSum = 0
    logging.info("起始日期: %d", startDay)
    logging.info("结束日期: %d", endDay)
    for i in range(startDay-1, endDay):
        # print("Date {}: ".format(i+1))
        j = 0
        clockInTimeDaily = 0

        unused, m, a, e = timePartition(clockInTimeMonthly[i])
        # print(i, unused, m, a, e)
        # 如果上午有不少于两次的打卡
        if m >= 2:
            tmp = int(clockInTimeMonthly[i][unused + m - 1][0]) - int(clockInTimeMonthly[i][unused][0]) + (
                        int(clockInTimeMonthly[i][unused + m - 1][1]) - int(
                    clockInTimeMonthly[i][unused][1])) * 1.0 / 60
            clockInTimeDaily = clockInTimeDaily + tmp
        # 如果下午有不少于两次的打卡
        # print("上午时间：", clockInTimeDaily)
        # 这里要扣除早于13:30的时间
        if a >= 2:
            if int(clockInTimeMonthly[i][unused + m][0]) * 60 + int(clockInTimeMonthly[i][unused + m][1]) > 810:
                tmp = int(clockInTimeMonthly[i][unused + m + a - 1][0]) - int(clockInTimeMonthly[i][unused + m][0]) + (
                            int(clockInTimeMonthly[i][unused + m + a - 1][1]) - int(
                        clockInTimeMonthly[i][unused + m][1])) * 1.0 / 60
            else:
                tmp = int(clockInTimeMonthly[i][unused + m + a - 1][0]) - 13 + (
                            int(clockInTimeMonthly[i][unused + m + a - 1][1]) - 30) * 1.0 / 60
            clockInTimeDaily = clockInTimeDaily + tmp
        # print("下午时间：", clockInTimeDaily)
        # 晚上同理
        if e >= 2:
            tmp = int(clockInTimeMonthly[i][unused + m + a + e - 1][0]) - int(
                clockInTimeMonthly[i][unused + m + a][0]) + (
                              int(clockInTimeMonthly[i][unused + m + a + e - 1][1]) - int(
                          clockInTimeMonthly[i][unused + m + a][1])) * 1.0 / 60
            clockInTimeDaily = clockInTimeDaily + tmp
        # print("晚上时间：", clockInTimeDaily)
        # 分别计算三个时段的时间

        # while j < len(clockInTimeMonthly[i])-1:
        #     # print("j:", j)
        #     if isCorrectTimeSlot(clockInTimeMonthly[i][j], clockInTimeMonthly[i][j+1]) == 0:
        #         clockInTimeDaily = clockInTimeDaily + int(clockInTimeMonthly[i][j+1][0]) - 13 + (int(clockInTimeMonthly[i][j+1][1]) - 30)*1.0/60
        #         j = j + 2
        #     elif isCorrectTimeSlot(clockInTimeMonthly[i][j], clockInTimeMonthly[i][j+1]) > 0:
        #         clockInTimeDaily = clockInTimeDaily + int(clockInTimeMonthly[i][j + 1][0]) - int(clockInTimeMonthly[i][j][0]) + (int(clockInTimeMonthly[i][j + 1][1]) - int(clockInTimeMonthly[i][j][1])) * 1.0 / 60
        #         j = j + 2
        #     else:
        #         j = j + 1
        # print("    ClockInTimeToday: {:.2f}".format(clockInTimeDaily), "hours")
        if flag == 1:
            weeklyClockInDict[i+1] = clockInTimeDaily
        clockInTimeSum = clockInTimeSum + clockInTimeDaily
    logging.info("sumTime Cost: %f s", time.time()-startTime)
    return clockInTimeSum


def timePartition(dailyClockInTime):
    morning = afternoon = evening = 0
    unused = 0
    i = 0
    while i<len(dailyClockInTime):
        if int(dailyClockInTime[i][0])*60+int(dailyClockInTime[i][1]) < 450:
            unused = unused + 1
        elif int(dailyClockInTime[i][0])*60+int(dailyClockInTime[i][1]) >= 450 and int(dailyClockInTime[i][0])*60+int(dailyClockInTime[i][1]) <= 750:
            morning = morning + 1
        elif int(dailyClockInTime[i][0])*60+int(dailyClockInTime[i][1]) >= 755 and int(dailyClockInTime[i][0])*60+int(dailyClockInTime[i][1]) <= 1110:
            afternoon = afternoon + 1
        elif int(dailyClockInTime[i][0])*60+int(dailyClockInTime[i][1]) >= 1115 and int(dailyClockInTime[i][0])*60+int(dailyClockInTime[i][1]) <= 1439:
            evening = evening + 1
        i = i + 1
    return unused, morning, afternoon, evening

'''
    isCorrectTimeSlot函数用于判断打卡的时间是否在规定时间内
    返回值0代表中午12:30-1:30
    返回值1代表上午正常打卡时间
    返回值2代表下午正常打卡时间
    返回值3代表晚上正常打卡时间（12:00之前）
    返回值-1代表其他时间
'''
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

    # browser = webdriver.Chrome(options=options)
    # 启动前检测浏览器版本并下载对应的驱动
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
    browser.get(URL)
    time.sleep(1)
    clockInTimeThisMonth = calendarRead(browser)
    head = browser.find_element(By.XPATH, '//*[@id="getMonthData"]/em')
    head.click()
    time.sleep(0.5)

    clockInTimeLastMonth = calendarRead(browser)
    logging.info("本月天数: %d", len(clockInTimeThisMonth))
    logging.info("上月天数: %d", len(clockInTimeLastMonth))

    browser.quit()

    return clockInTimeThisMonth, clockInTimeLastMonth


def calendarRead(browser):
    startTime = time.time()

    sourceCode = BeautifulSoup(browser.page_source, "html.parser")
    # with open('test.txt', 'w') as f:
    #     f.write(browser.page_source)
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

    logging.info("calendarRead Cost: %f s", time.time()-startTime)
    return clockInTimeMonthly


def showUI(weeklyClockInDict, totalTime, lastWeekTotalTime):
    app = QApplication(sys.argv)
    w = QWidget()
    w.resize(600, 300)

    screen = QtWidgets.QDesktopWidget().screenGeometry()
    size = w.geometry()
    w.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    w.setWindowTitle("打卡时长统计助手 v1.2")
    w.setWindowIcon(QIcon("icon.ico"))

    text = QPlainTextEdit(w)
    # 增加上周打卡时间记录
    content = "上周累计打卡时间：" + str(round(lastWeekTotalTime, 2)) + " 小时"
    text.appendPlainText(content)
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

def login(phoneNumber, password):
    # Get Login Token and User_id
    startTime = time.time()

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
    goalInfo = json.loads(goalInfo)
    result = goalInfo["data"]["list"][0]["url"]
    logging.info("URL of Calendar: %s", result)

    logging.info("LoginIn Cost: %f s", time.time()-startTime)
    return result

if __name__ == "__main__":
    phoneNumber, password = userInformationRead()
    URL = login(phoneNumber, password)
    print(URL)
    thisMonth, lastMonth = spider(URL)
    totalTime, lastWeekTotalTime = calculate(thisMonth, lastMonth)
    showUI(weeklyClockInDict, totalTime, lastWeekTotalTime)