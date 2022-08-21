import newsapi
from bs4 import BeautifulSoup
import requests
import lxml 
from datetime import date
import time
import os


class News:

  newsSources = {'The Wall Street Journal' : 'the-wall-street-journal',
                 'BBC News' : 'bbc-news',
                 'The Washington Post' : 'the-washington-post'}

  SciTechSources = {'The Verge' : 'the-verge',
                    'TechCrunch' : 'techcrunch',
                    'Wired' : 'wired'}


  def __init__(self) -> None:
    self.newsapi = newsapi.NewsApiClient(api_key = os.environ.get('newsAPIKey'))
    self.headlinesFile = 'headlines.txt'
    self.SciTechFile = 'SciTech.txt'
    self.covidFile = 'covid.txt'
    self.tennisNewsFile = 'tennis.txt'
    self.tennisScoresFile = 'tennisScores.txt'
    self.headlinesTitle = 'Top Headlines-----------------------------------'
    self.SciTechTitle =   'Tech and Media News--------------------------'
    self.covidTitle =     'COVID-19 Update-------------------------------'
    self.tennisNewsTitle =    'Tennis Update----------------------------------'
    self.tennisScoresTitle = 'Scores and Matches'
    self.covidWebsite = 'https://www.hsph.harvard.edu/news/hsph-in-the-news/the-latest-on-the-coronavirus/'
    self.tennisNewsWebsite = 'https://www.tennis.com/'
    self.tennisScoresWebsite = 'http://m.espn.com/general/tennis/dailyresults?w=1nbk5&i=MENU&wjb'


  """ writes down the title, description,
      and url of the top headlines from a dictionary of
      given news sources into headlines.txt using newsapi"""
  def getNews(self, fileName:str, sources:dict, title:str):

    with open(fileName, 'w', encoding="utf-8") as file:

      file.write(title + '\n' + '\n')
      try:
        for name, source in sources.items():
          data = self.newsapi.get_top_headlines(sources=source, page = 1, page_size=100)
          article = data["articles"]

          file.write(name + '\n')
          count = 0
          for ar in article:
            if count == 1: break
            file.write(ar['title'] + '\n')
            file.write(ar['description'] + "\n")
            file.write(ar['url']  + '\n' + '\n'+ '\n')
            count += 1
      except:
        print("NewsAPI Error")
        file.write("NewsAPI Error" + '\n' + '\n'+ '\n')



  """returns the current date format: (August 16)"""
  def getDate(self):
    today = date.today()
    day = today.strftime("%B %d")
    return day


  """checks if a connection to a website can be made
      returns the html of the website if it can and  bool
      value representing if a connection can be made"""
  def connectToWebsite(self, successMsg:str, url:str):
    connection = False

    # tries connecting to the website 10 times before quitting
    for x in range(0, 10):
      try:
        website = requests.get(url).text
        connection = True
        print(successMsg)
        return website, connection
      except requests.exceptions.ConnectionError:
        print("Trying to connect to: " + url)
        time.sleep(5)
      else:
        break
    return "none", connection


  """writes into the given file and the console that the connection
    to the website cannot be made"""
  def connectionFailure(self, fileName:str, website:str, title:str):
    with open(fileName, 'w', encoding="utf-8") as file:
      print("Failed to Connect to Website:" + website + self.getDate())
      file.write(title + '\n')
      file.write("Failed to Connect to Website:" + website)


  """webscrapes from the harvard website to see the current covid update
      writes down the results into covid.txt"""
  def getCovidNews(self):
    successMsg = "Covid website connection successful"
    website, connect = self.connectToWebsite(successMsg, self.covidWebsite) #check if connection can be made

    if connect == False:
      self.connectionFailure(self.covidFile, self.covidWebsite, self.covidTitle)
      return

    soup = BeautifulSoup(website, 'lxml')

    day = self.getDate()

    with open(self.covidFile, 'w', encoding="utf-8") as file:
      update = False
      dateFound = False
      file.write(self.covidTitle + '\n')
      file.write(self.covidWebsite + '\n' + '\n')

      #finds p tags with the wanted date
      for data in soup.find_all("p"):
        text = data.text
        #if date is found write p tag content into file and mark bool value so that you can write the next p tag in the next iteration
        if text.find(day) != -1 and text.find("See stories from") == -1: 
          file.write(text + '\n')
          link = data.a
          file.write(link.get('href') + '\n')
          dateFound = True
          update = True
        elif dateFound == True: #if the previous iteration had date write the current p tag
          file.write(text + '\n' + '\n')
          dateFound = False
      if update == False: # if date was not found at all
        file.write("No update today \n \n")


  # webscrapes tennis.com to get information on the top article and writes it into tennis.txt
  def getTennisNews(self):
    successMsg = "Tennis website connection successful"
    successMsg2 = "Tennis article successful"

    # first goes to the main page
    website, connect = self.connectToWebsite(successMsg, self.tennisNewsWebsite)
    if connect == False:
      self.connectionFailure(self.tennisNewsFile, self.tennisNewsWebsite, self.tennisNewsTitle)
      return

    # then get the link to the top article and connect to that website
    soup = BeautifulSoup(website, 'lxml')
    data = soup.find("a", class_='fa-button -outline -blur -primary -cta1')
    articleLink = self.tennisNewsWebsite+data.get('href')

    website, connect = self.connectToWebsite(successMsg2, articleLink)
    if connect == False:
      self.connectionFailure(self.tennisNewsFile, self.tennisNewsWebsite, self.tennisNewsTitle)
      return

    # scrapes for the name and summary of the article
    soup = BeautifulSoup(website, 'lxml')
    articleTitle = soup.find("h1", class_='oc-c-article__title').text
    articleSum = soup.find("p", class_='oc-c-article__summary').text
    with open(self.tennisNewsFile, 'w', encoding="utf-8") as file:
      file.write(self.tennisNewsTitle + '\n' + '\n')
      file.write(articleTitle + '\n')
      file.write(articleSum + '\n')
      file.write(articleLink + '\n' + '\n')


  # webscrapes daily espn men's tennis scores and writes it into tennisScores.txt
  def getTennisScores(self):
    successMsg = "Tennis scores website connection successful"
    website, connect = self.connectToWebsite(successMsg, self.tennisScoresWebsite)
    if connect == False:
      self.connectionFailure(self.tennisScoresFile, self.tennisScoresWebsite, self.tennisScoresTitle)
      return

    soup = BeautifulSoup(website, 'html.parser')
    tournament = soup.find('div', class_='sec row').text

    with open(self.tennisScoresFile, 'w', encoding="utf-8") as file:
      file.write(self.tennisScoresTitle+'\n'+'\n')
      file.write(tournament + '\n'+'\n')
      tags = soup.find_all('div', {"class":"ind"})

      # only iterates between 1 and the length-13 to only get match info
      for tag in tags[1:(len(tags)-13)]:
        if (tag.find('b')):
          result = tag.find('b')
          if result != None:
            file.write(result.get_text()+'\n')
            matchInfo = tag.find_all('br')
            for info in matchInfo:
              if info != None:
                info = str(info.next_sibling)
                file.write(info+'\n')
            file.write('\n')
        else:
          file.write(tag.text + '\n' + '\n')
