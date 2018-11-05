from bs4 import BeautifulSoup as BS4
import requests
from pytube import YouTube
from pytube.exceptions import VideoUnavailable


class YoutubeScraper():
    def __init__(self):
        while True:
            try:
                choice = int(input("\nChose 0 for exit the program \n""Chose 1 for insert URL or 2 for Search a video: "))
                if choice in [1, 2, 0]:
                    break
            except ValueError:
                print("Insert a integer number\n ")

        if choice == 1:
             URL = input("Insert Url ")
             while True:
                 try:
                     choice = int(input("\nChose 0 for exit the program \n""Chose 1 for download the video or 2 for download the sound of the video: "))
                     if choice in [1, 2, 0]:
                         break
                 except ValueError:
                     print("Insert a integer number\n ")

             if choice == 1: YoutubeScraper.DownloadVideoURL(URL)
             elif choice == 2: YoutubeScraper.DownloadAudioURL(URL)
             elif choice == 0: exit()

        elif choice == 2: YoutubeScraper.SearchVideos()
        elif choice == 0: exit()


    def SearchVideos():
        search = input("Name of the video: ")
        base = "https://www.youtube.com/results?search_query="
        result = base+search
        print(result)
        Page_Html = requests.get(result).text
        Page = BS4(Page_Html, "lxml")

        videolist = []


        for res in Page.findAll("h3"):
            for vids in res.findAll("a"):
                final = "https://www.youtube.com" + vids["href"]
                videolist.append(final)

        f_dic = YoutubeScraper.InsertVideos(videolist)
        YoutubeScraper.PrintVideoList(f_dic)
        Selection = YoutubeScraper.ChoseVideo(f_dic,videolist)

        while True:
            try:
                choice = int(input("\nChose 0 for exit the program \n""Chose 1 for download the video or 2 for download the sound of the video: "))
                if choice in [1, 2, 0]:
                    break
            except ValueError:
                print("Insert a integer number\n ")

        if choice == 1:YoutubeScraper.DownloadVideo(Selection)
        elif choice == 2: YoutubeScraper.DownloadAudio(Selection)
        elif choice == 0: exit()

    def InsertVideos(videolist):
        x = 0
        dic = {}
        for video in videolist:
            try:
                yt = YouTube(video)

                print("Video Number: ",x)
                dic[x] = {"Video Number": x,"URL": videolist[x], "Title": yt.title, "Description": yt.description, "Length": yt.length, "Rating": yt.rating, "Thumbnail_url": yt.thumbnail_url}

                x += 1
            except VideoUnavailable:
                print("Video Not found,Continue Searching")
            except LiveStreamError:
                print("Video is in Live Streaming, Continue Searching")
        return dic

    def PrintVideoList(dic):
        for Video_ID, Video_Info in dic.items():
            print("-------------")
            for key in Video_Info:
                print(key + ':', Video_Info[key])


    def ChoseVideo(dic,videolist):
        while True:
            try:
                choice = int(input("\nChose witch video you want: "))
                if choice >= 0 and choice < len(videolist):
                     break
            except ValueError:
                print("Insert a integer number\n ")

        print(dic[choice])
        final = dic[choice]
        return final

    def DownloadVideo(Selection):

        yt = YouTube(Selection["URL"])
        print(Selection["Title"])

        #videos = yt.streams.filter(progressive=True).all()
        #for video in videos:
        #    print(video)
        #Choose a video by the itag, so with given quality and format
        #choice = int(input("\nChose the Itag "))
        #yt.streams.get_by_itag(choice).download("./")

        print("Downloading..................... ")
        yt.streams.filter(progressive=True).first().download()
        print("Download Complete! ")

    def DownloadAudio(Selection):
        yt = YouTube(Selection["URL"])
        print(Selection["Title"])
        #print(yt.streams.filter(only_audio=True).all())
        print("Downloading..................... ")
        yt.streams.filter(only_audio=True).first().download()
        print("Download Complete! ")

    def DownloadVideoURL(URL):
        yt = YouTube(URL)
        print(yt.title)
        print("Downloading..................... ")
        yt.streams.filter(progressive=True).first().download()
        print("Download Complete! ")

    def DownloadAudioURL(URL):
        yt = YouTube(URL)
        print(yt.title)
        print("Downloading..................... ")
        yt.streams.filter(only_audio=True).first().download()
        print("Download Complete! ")

YoutubeScraper()
