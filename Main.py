import os
import winshell
from bs4 import BeautifulSoup
import re
import requests
import pandas as pd
from PandasModel import PandasModel
import numpy as np
import lxml.html
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(QtWidgets.QWidget):
    def __init__(self, df = pd.DataFrame() ,parent=None):
        QtWidgets.QWidget.__init__(self, parent=None)
        self.df = df
        MainWindow.setObjectName("Web Crawler")
        MainWindow.resize(1600, 900)
        MainWindow.setAutoFillBackground(True)
        
        # vLayout = QtWidgets.QVBoxLayout(self)
        # hLayout = QtWidgets.QHBoxLayout()

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(0, 160, 1600, 800))
        self.tableView.setObjectName("tableView")
        # vLayout.addWidget(self.tableView)
        self.tableView.setSortingEnabled(True)

        self.CpnButton = QtWidgets.QPushButton(self.centralwidget)
        self.CpnButton.setGeometry(QtCore.QRect(20, 50, 180, 50))
        self.CpnButton.setAutoFillBackground(True)
        self.CpnButton.setObjectName("CpnButton")
        self.CpnButton.clicked.connect(self.Company)

        self.PrfButton = QtWidgets.QPushButton(self.centralwidget)
        self.PrfButton.setGeometry(QtCore.QRect(210, 50, 150, 50))
        self.PrfButton.setObjectName("PrfButton")
        self.PrfButton.clicked.connect(self.Profile)

        self.IndeedButton = QtWidgets.QPushButton(self.centralwidget)
        self.IndeedButton.setGeometry(QtCore.QRect(390, 50, 150, 50))
        self.IndeedButton.setAutoFillBackground(True)
        self.IndeedButton.setObjectName("IndeedButton")
        self.IndeedButton.clicked.connect(self.Indeed)

        self.ExportButton = QtWidgets.QPushButton(self.centralwidget)
        self.ExportButton.setGeometry(QtCore.QRect(1400, 50, 150, 50))
        self.ExportButton.setAutoFillBackground(True)
        self.ExportButton.setObjectName("ExportButton")
        self.ExportButton.clicked.connect(self.Export)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 523, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Web Crawler"))
        self.CpnButton.setText(_translate("MainWindow", "Crawl TCN Companies"))
        self.PrfButton.setText(_translate("MainWindow", "Crawl TCN Frofiles"))
        self.IndeedButton.setText(_translate("MainWindow", "Crawl Indeed.com"))
        self.ExportButton.setText(_translate("MainWindow", "Export"))


    def Profile(self):
        name = []
        desired = []
        wishes = []
        location = []
        work_place = []
        salary = []
        introduce =[]
        birthday = []
        gender =[]
        updated = []
        experience = []
        introduce = []

        pages = np.arange(1, 5, 1)
        for page in pages:
            page = requests.get("https://tuyencongnhan.vn/tim-ho-so?&page=" + str(page))

            soup = BeautifulSoup(page.content, 'html.parser')
            results = soup.find(id='result-search-job')
            #print(results.prettify())
            # jobs = results.find_all('div', class_='mng-company')
            
            for job in results.find_all('div', class_='mng-company'):
                updated_elem = job.find('p', class_='expired').text
                updated.append(updated_elem)

                hrefs = job.find_all('a', class_='btn btn-apply-s m-width-100', href=True)
                for links in hrefs:
                    href = links['href']
                    page2 = requests.get("https://tuyencongnhan.vn" + href)
                    soup2 = BeautifulSoup(page2.content, 'html.parser')
                    results2 = soup2.find(id='view-profile')
                    
                    TopCard = results2.find_all('div', class_='masthead')
                    for job_elem in TopCard:
                        name_elem = job_elem.find('h1', class_='mar-0').text.strip()
                        name.append(name_elem)
                        
                        desired_elem = job_elem.find('h2', class_='mar-0 mb-15').text.strip()
                        desired.append(desired_elem)

                        gender_elem = job_elem.find('div', class_='field').text.replace("Giới tính", "").strip()
                        gender.append(gender_elem)

                        location_elem = job_elem.find('div', class_='field').find_next_sibling("div").text.replace("Địa chỉ:", "").strip()
                        location.append(location_elem)

                        birth_elem = job_elem.find('div', class_='field').find_next_sibling("div").find_next_sibling("div").text.replace("Ngày sinh", "").strip()
                        birthday.append(birth_elem)


                    doc = lxml.html.fromstring(page2.content)
                    # section = doc.xpath('//*[@id="view-profile"]/div[2]/div')[0]

                    exp_elem = doc.xpath('//*[@id="view-profile"]/div[2]/div/div/div[1]/div[1]/div/div[2]/p[2]/text()')
                    experience.append(exp_elem)

                    place_elem = doc.xpath('//*[@id="view-profile"]/div[2]/div/div/div[1]/div[6]/div/div[2]/p[2]/a/text()')
                    work_place.append(place_elem)

                    salary_elem = doc.xpath('//*[@id="view-profile"]/div[2]/div/div/div[1]/div[5]/div/div[2]/p[2]/text()')
                    salary.append(salary_elem)
                    

                    # contents = doc.xpath('//*[@id="content"]')[0]
                    intro_elem = doc.xpath('//*[@id="content"]/div[2]/div/div/text()')
                    introduce.append(intro_elem)

                    wish_elem = doc.xpath('//*[@id="content"]/div[10]/div/div/text()')
                    wishes.append(wish_elem)
        self.df = pd.DataFrame(
            {"Name":name, "Gender":gender,"Birthday":birthday, "Location":location, "Experience":experience,
            "Place want to work":work_place, "Introduce":introduce, "Desired Salary":salary, "Desired":desired, "Wishes":wishes})
        model = PandasModel(self.df)
        self.tableView.setModel(model)       


    def Company(self):
        Cpn_name = []
        job_name = []
        expired =[]
        salary = []
        amount = []
        location = []
        fields = []
        benefit = []
        require = []
        profile_require = []


        pages = np.arange(1, 3, 1)
        for page in pages:
            page = requests.get("https://tuyencongnhan.vn/tim-nha-tuyen-dung?keyword=&city_id=&career_id=" + str(page))

            soup = BeautifulSoup(page.content, 'html.parser')
            results = soup.find(id='search-job')
            doc = lxml.html.fromstring(page.content)

            for hrefs in soup.findAll('p', class_='job-title'):
                links = hrefs.findAll('a')
                for link in links:
                    # hrefs = link.get('href')
                    href = link['href']
                    pages1 = np.arange(1, 5, 1)
                    for page1 in pages1:
                        page1 = requests.get("https://tuyencongnhan.vn" + href + "?page=" + str(page1))
                        soup = BeautifulSoup(page1.content, 'html.parser')
                        results = soup.find(id='pjax-employer-detail')
                        jobs = results.find_all('article', class_='job-available')
                        for job in jobs:
                            job_name_elem = job.find('span', class_='i-title').text
                            job_name.append(job_name_elem)

                            # href2 = job.find_all('a', class_='btn btn-apply-s m-width-100', href=True)
                            for link2 in job.find_all('a', class_='btn btn-apply-s m-width-100', href=True):
                                href2 = link2['href']
                                page2 = requests.get("https://tuyencongnhan.vn" + href2)
                                soup = BeautifulSoup(page2.content, 'html.parser')
                                results = soup.find(id='tab-job-detail')
                                doc = lxml.html.fromstring(page2.content)
                                
                                # Info = doc.xpath('//*[@id="tab-job-detail"]')[0]
                                cpn_name_elem = doc.xpath('//*[@id="tab-job-detail"]/div/div/div[2]/div[5]/address/strong/a/text()')
                                Cpn_name.append(cpn_name_elem)

                                expired_elem = doc.xpath('//*[@id="tab-job-detail"]/div/div/div[1]/div/div[1]/div[2]/p/text()')
                                expired.append(expired_elem)

                                salary_elem = doc.xpath('//*[@id="tab-job-detail"]/div/div/div[1]/div/div[2]/div[2]/p/text()')
                                salary.append(salary_elem)

                                amount_elem = doc.xpath('//*[@id="tab-job-detail"]/div/div/div[1]/div/div[3]/div[2]/p/text()')
                                amount.append(amount_elem)

                                location_elem = doc.xpath('//*[@id="tab-job-detail"]/div/div/div[1]/div/div[5]/div[2]/p/a/text()')
                                location.append(location_elem)

                                fields_elem = doc.xpath('//*[@id="tab-job-detail"]/div/div/div[1]/div/div[6]/div[2]/p/a/text()')
                                fields.append(fields_elem)

                                description = results.find_all('div', class_='col-xs-12 col-md-8 pull-right')
                                for d in description:
                                    benefit_elem = d.find('div', class_='content-job-detail quyen-loi-duoc-huong').get_text().strip()
                                    benefit.append(benefit_elem)

                                    require_elem = d.find('div', class_='content-job-detail yeu-cau-cong-viec').get_text().strip()
                                    require.append(require_elem)

                                    profile_require_elem = d.find('div', class_='content-job-detail yeu-cau-ho-so').get_text().strip()
                                    profile_require.append(profile_require_elem)

        self.df = pd.DataFrame(
            {'Company Name':Cpn_name, 'Job Name':job_name, 'Amount':amount, 'Expired':expired, 'Salary':salary, 
            'Location':location, 'Fields':fields, 'Benefit':benefit, 'Require':require, 'Profile_require':profile_require})
        # df.replace("(['\\n,\s+])", "", regex=True, inplace=True)
        self.df['Amount'] = [re.sub(r"(['\\n,\s+])", "", str(x)) for x in self.df['Amount']]
        self.df['Expired'] = [re.sub(r"(['\\n,\s+])", "", str(x)) for x in self.df['Expired']]
        self.df['Salary'] = [re.sub(r"(['\\n,\s+])", "", str(x)) for x in self.df['Salary']]
        model = PandasModel(self.df)
        self.tableView.setModel(model)
        # df.to_excel(os.path.join(winshell.desktop(), "Companies.xlsx"))


    def Indeed(self):
        job_name = []
        company_name = []
        salary = []
        date = []
        Location = []
        info = []
        expired =[]

        chrome_options = Options()
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--incognito')
        driver = webdriver.Chrome(options=chrome_options)

        pages = np.arange(0, 51, 10)
        for page in pages:
            page = driver.get("https://vn.indeed.com/jobs?q=Công+Nhân&l=Hà+Nội&start=" + str(page))
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            results = soup.find(id='resultsCol')

            elements = results.find_all('div', class_='clickcard')
            for elem in elements:
                
                company_elements = elem.find('span', class_='company')
                if company_elements is None:
                    company_name.append('None')
                else:
                    company_name.append(company_elements.text.strip())

                job_elements = elem.find('h2', class_='title').text.strip()
                job_name.append(job_elements)


                salary_elements = elem.find('span', class_='salaryText')
                if salary_elements is None:
                    salary.append('None')
                else:
                    salary.append(salary_elements.text)

                date_elements = elem.find('span', class_='date').text
                if date_elements is None:
                    date.append('None')
                else:
                    date.append(date_elements)

                location_elements = elem.find(class_='location accessible-contrast-color-location')
                if location_elements is None:
                    Location.append('None')
                else:
                    Location.append(location_elements.text)

                info_elements = elem.find('div', class_='summary').text
                if info_elements is None:
                    info.append('None')
                else:
                    info.append(info_elements)
        driver.close()
            # hrefs_elements = driver.find_elements_by_css_selector('.turnstileLink')
            # for href in hrefs_elements:
            #     links = href.get_attribute('href')
            #     page2 = requests.get(links)
            #     soup = BeautifulSoup(page2.content, 'html.parser')
            #     doc = lxml.html.fromstring(page2.content)

        self.df = pd.DataFrame(
                {'Company': company_name, 'Job': job_name, 'Salary': salary, 'location': Location, 'Date': date, 'Info': info})
        model = PandasModel(self.df)
        self.tableView.setModel(model)
        # df.to_excel(os.path.join(winshell.desktop(), "Indeed.xlsx"))

               

    def Export(self):
        self.df.to_excel(os.path.join(winshell.desktop(), "Result.xlsx"))

        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    # ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())