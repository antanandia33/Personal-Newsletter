import src
import os

EMAIL_ADDRESS = os.environ.get('pythonEmailUser')


# sends a newsletter to the given email
def sendNewsLetter(emailAddress:str):
  newsLetter = src.news()
  newsLetter.getNews(newsLetter.headlinesFile, newsLetter.newsSources, newsLetter.headlinesTitle)
  newsLetter.getNews(newsLetter.SciTechFile, newsLetter.SciTechSources, newsLetter.SciTechTitle)
  newsLetter.getCovidNews()
  newsLetter.getTennisNews()
  newsLetter.getTennisScores()
  mail = src.email(emailAddress)
  headlines = mail.getMessage(newsLetter.headlinesFile)
  SciTechNews = mail.getMessage(newsLetter.SciTechFile)
  covidNews = mail.getMessage(newsLetter.covidFile)
  tennisNews = mail.getMessage(newsLetter.tennisNewsFile)
  tennisScores = mail.getMessage(newsLetter.tennisScoresFile)
  mail.setEmail(headlines+SciTechNews+covidNews+tennisNews+tennisScores)
  mail.sendEmail()


sendNewsLetter(EMAIL_ADDRESS)
