# 노래의 정보를 담는 클래스
class Song:
    def __init__(self):
        self.name = ""
        self.lyrics = ""
        self.auth = ""

    def setName(self, name):
        self.name = name.replace("?", "")

    def setLyrics(self, lyrics):
        self.lyrics = lyrics

    def setAuth(self, auth):
        self.auth = auth.replace("?", "")

    def getAuth(self):
        return self.auth

    def getName(self):
        return self.name

    def getLyrics(self):
        return self.lyrics

    def printData(self):
        print("노래제목 : ", self.name)
        print("가수 : \n", self.auth)
        print("가사 : \n", self.lyrics.split("-----------------")[0])
        print()

    def saveData(self):
        print("파일을 저장합니다.")
        file = open(self.name+"+"+self.auth+".txt", 'w', encoding="utf8")
        file.write(self.lyrics)
        file.close()