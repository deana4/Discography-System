import regex as re

class Album:
    def __init__(self, name = "Default", songsList = [], year = 0):
        self.albumName = name
        self.listOfSongs = songsList
        self.debutYear = year

    def setAlbumName(self, name):
        self.albumName = name
        return self

    def setSongsList(self, list):
        self.listOfSongs = list
        return self

    def setDebutYear(self, year):
        self.debutYear = year
        return self

    def addSongToAlbum(self, song):
        if type(song) != Song:
            print("Cant add none type Song to the list")
            return -1
        else:
            self.listOfSongs.append(song)
            return 1

#ignoring the guest singer
class Song:
    def __init__(self, name = "Default", durationTime = 0, lyrics = "", albumName = ""):
        self.songName = name
        self.durationTime = durationTime
        self.lyrics = lyrics
        self.inWhichAlbum = albumName
        self.guestSingers = []

    def setSongName(self, name):
        self.songName = name
        return self
    def setDurationTime(self, durationTime):
        self.durationTime = durationTime
        return self
    def setLyrics(self, lyrics):
        self.lyrics = lyrics
        return self
    def setAlbumBelonging(self, albumName):
        self.inWhichAlbum = albumName
        return self
    def addGuestSinger(self, singerName):
        self.guestSingers.append(singerName)
        return self

class DataOrganizator:
    def __init__(self, dataPath):
        self.listOfAlbums = []
        self.listOfSongs = []

        theData = open(dataPath, encoding='utf8').read()
        splittedByAlbums = re.split("^[#]", theData, flags=re.MULTILINE)

        #cleaning empty albums
        for i, album in enumerate(splittedByAlbums):
            if len(album) == 0:
                splittedByAlbums.pop(i)

        print(splittedByAlbums[1])

        #creating archive of albums
        for textAlbum in splittedByAlbums:
            album = Album()
            # print(textAlbum)

            strippedAlbum = textAlbum.strip()

            albumDetails = re.split("::", strippedAlbum.split('\n')[0]) #Make a convention which cell 0 contains the name and cell 1 contains the debut year.

            listOfSongsOnCurrentAlbum = re.split("^[*]", strippedAlbum, flags=re.MULTILINE)

            listOfSongsOnCurrentAlbum.pop(0) #removing the first element which is the album details

            # print(len(listOfSongsOnCurrentAlbum))
            songsList = []
            for songText in listOfSongsOnCurrentAlbum:
                song = Song()
                # print(songText)
                songDetails = re.split("::", songText) #Make a convention which cell 0 contains the name, 1 - the guest singers, 2 - duration, 3 - lyrics
                song.setSongName(songDetails[0].strip()).setDurationTime(songDetails[2]).setLyrics(songDetails[3]).setAlbumBelonging(albumDetails[0])

                album.setAlbumName(albumDetails[0]).setDebutYear(albumDetails[1])
                songsList.append(song)

                self.listOfSongs.append(song)

            album.setSongsList(songsList)

            self.listOfAlbums.append(album)

class SystemManager:
    def __init__(self, path):
        self.systemData = DataOrganizator(path)
        self.flag = 1

    def runSystem(self):
        while self.flag != 0:
            userInput = input("Please choose an action:\n"
                              "1. Get Album List\n"
                              "2. Get the list of songs in an Album\n"
                              "3. Get the duration time of a song\n"
                              "4. Get the lyrics of a song\n"
                              "5. Check in which Album the song is\n"
                              "6. Get songs by name\n"
                              "7. Get songs by lyrics\n"
                              "8. Exit\n")

            retVal = self.switchCase(userInput)


    def switchCase(self, number):
        try:
            number = int(number)
        except:
            print("An exception occurred, couldn't cast to Int.")

        match(number):
            case 1:
                albumList = self.getAlbumList()
                print(albumList)
                return albumList
            case 2:
                albumName = input("Please enter album name: \n").strip()
                songsInAlbum = self.getSongsInAlbumName(albumName)
                if len(songsInAlbum) == 0:
                    print("No songs on this album")
                else:
                    print(songsInAlbum)
                return songsInAlbum
            case 3:
                songName = input("Please enter song name: \n").strip()
                val = self.getDruationTimeOfSong(songName)
                if val == -1:
                    print("Didnt find song with the name given")
                    return 0
                else:
                    print(val)
                    return val
            case 4:
                songName = input("Please enter song name: \n").strip()
                val = self.getLyricsOfSong(songName)
                if val == -1:
                    print("Didnt find song with the name given")
                    return 0
                else:
                    print(val)
                    return val
            case 5:
                songName = input("Please enter song name: \n").strip()
                val = self.getTheAlbumOfaSong(songName)
                if val == -1:
                    print("Didnt find song with the name given")
                    return 0
                else:
                    print(val)
                    return val
            case 6:
                songName = input("Please enter song name: \n").strip()
                listOfSongsContaining = self.findSongByName(songName)
                if len(listOfSongsContaining) == 0:
                    print("Didnt find songs with the name given")
                    return 0
                else:
                    print(listOfSongsContaining)
                    return listOfSongsContaining
            case 7:
                sentence = input("Please enter a sentence that could be in some song lyrics: \n").strip()
                listOfSongsContaining = self.findSongsByLyrics(sentence)
                if len(listOfSongsContaining) == 0:
                    print("Didnt find songs with the name given")
                    return 0
                else:
                    print(listOfSongsContaining)
                    return listOfSongsContaining
            case 8:
                print("You choose to exit the system.\n")
                self.flag = 0
                return
            case _:
                print("Please enter only numbers between 1 to 8 include.\n")
                return

    def getAlbumList(self):
        listOfAlbums = []
        albums = self.systemData.listOfAlbums

        for album in albums:
            listOfAlbums.append(album.albumName)

        return listOfAlbums

    def getSongsInAlbumName(self, _albumName):
        listOfSongsInAlbum = []
        albums = self.systemData.listOfAlbums
        for album in albums:
            if album.albumName == _albumName:
                for song in album.listOfSongs:
                    listOfSongsInAlbum.append(song.songName)
                break

        return listOfSongsInAlbum

    def getDruationTimeOfSong(self, songName):
        songs = self.systemData.listOfSongs
        for song in songs:
            if song.songName == songName:
                return song.durationTime
        return -1

    def getLyricsOfSong(self, songName):
        songs = self.systemData.listOfSongs
        for song in songs:
            if song.songName == songName:
                if song.lyrics.strip() == "Instrumental":
                    return "This song has no lyrics, only instrumentals.\n"
                else:
                    return song.lyrics
        return -1

    def getTheAlbumOfaSong(self, songName):
        songs = self.systemData.listOfSongs
        for song in songs:
            if song.songName == songName:
                return song.inWhichAlbum
        return -1

    def findSongByName(self, songName):
        listOfSongsContains = []
        if type(songName) != str:
            pass
        else:
            songName = songName.lower()
            for song in self.systemData.listOfSongs:
                if song.songName.lower().__contains__(songName):
                    listOfSongsContains.append(song.songName)

        return listOfSongsContains

    def findSongsByLyrics(self, word):
        listOfSongsContains = []
        if type(word) != str:
            pass
        else:
            word = word.lower()
            for song in self.systemData.listOfSongs:
                if song.lyrics.lower().__contains__(word):
                    listOfSongsContains.append(song.songName)

        return listOfSongsContains

if __name__ == '__main__':
    systemOperator = SystemManager("Pink_Floyd_DB.TXT")
    systemOperator.runSystem()
    