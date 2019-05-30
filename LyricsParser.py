# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import urllib, traceback, os, sys
from song import Song

class LyricsParser:
    def __init__(self, keyword):
        # 아래의 옵션들은 selenium을 headless모드로 띄우기 위한 옵션들이다.
        chrome_options = Options()
        chrome_options.add_argument('headless')
        chrome_options.add_argument('window-size=1920x1080')
        chrome_options.add_argument("disable-gpu")

        # 가짜 useragent를 만들어서 우리의 selenium에 설정해주자.
        # ua.firefox, ua.chrome등 다양한 설정등이 있다.
        ua = UserAgent()
        chrome_options.add_argument('User-Agent=' + ua.chrome)
        try:
            drive_path = os.path.abspath("chromedriver.exe")
            # print(drive_path)
            self.web = webdriver.Chrome(executable_path=drive_path, options=chrome_options)
        except:
            drive_path = os.path.abspath("chromedriver")
            # print(drive_path)
            self.web = webdriver.Chrome(executable_path=drive_path, options=chrome_options)
        # 페이지가 로딩될 때까 지 암묵적으로 3초간 대기시켜준다.
        self.web.implicitly_wait(3)

        # 검색어
        self.keyword = keyword

        # 노래 정보
        self.song = Song()

    def getLink(self):
        lyrics_search_link = ""

        # 검색방식 : 구글 검색 -> 가사 검색결과
        baseURL = "https://www.google.com/search"
        siteOption = "site:http://boom4u.net/lyrics/"

        # 검색조건 설정
        values = {
             'q': self.keyword + " " + siteOption,
            'oq': self.keyword,
             'aqs': 'chrome..69i57.35694j0j7',
                'sourceid': 'chrome',
                'ie': 'UTF-8',
             }

        # URL형식으로 변환
        query_string = urllib.parse.urlencode(values)
        
        # 구글 검색 결과를 토대로 가사 검색후 링크 확보
        try:
            req = self.web.get(baseURL + '?' + query_string)
            print("구글 검색 URL \t:\n", baseURL + '?' + query_string)
            soup = BeautifulSoup(self.web.page_source, 'html.parser')
            search_result = soup.select_one(".r > a")
        except:
            print("songParser Error!! ================================")
            traceback.print_exc()

        # search_result에서 링크 부분만 추출해낸다.
        try:
            lyrics_search_link = search_result.get('href')
            return ("success", "페이지를 찾았습니다.", lyrics_search_link)
        except:
            return ("error", "페이지를 찾지 못했습니다.", "")


    def getSongData(self):
        status, message, lyrics_search_link = self.getLink()
        print("{}".format(message))
        if status == "error":
            return (status, message, lyrics_search_link)

        self.web.get(lyrics_search_link)
        soup = BeautifulSoup(self.web.page_source, 'html.parser')

        name_auth = soup.select('td > font > a')
        self.song.setName(name_auth[0].getText())
        self.song.setAuth(name_auth[1].getText())

        if (self.song.getName() not in self.keyword) and (self.keyword not in self.song.getName()):
            print(self.keyword)
            return ("error", "검색결과가 일치하지 않습니다.", "")

        print("노래 제목 \t: " + self.song.getName())
        print("가수 \t: " + self.song.getAuth())
        print("추출한 주소 \t:\n" + lyrics_search_link)



        tag_string = []
        for s in soup.select('table.tabletext > tbody > tr'):
            tag_string.append(s.getText())
        self.song.setLyrics('\n'.join(tag_string))
        return ("success", "성공적으로 저장되었습니다.", "")


if __name__ == '__main__':
    cmd = ""
    while cmd != "quit":
        
        keyword = input("검색하실 노래의 제목을 입력해주세요 : ")
        lp = LyricsParser(keyword)
        status, message, data = lp.getSongData()
        print(message)
        
        if input("결과물 확인(1) : ") == '1':
           lp.song.printData()
        
        if input("결과물 저장(1) : ") == '1':
            lp.song.saveData()
        
        if input("프로그램을 종료하시려면 quit") == "quit":
            cmd = "quit"