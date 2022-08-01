import requests
from bs4 import BeautifulSoup
def getQuotesAuthors(keys, values):
    quotes = {}
    keysLength = len(keys)
    for each in range(keysLength):
        quotes[keys[each]] = values[each]
    return quotes
def getScrapingData(url):
    site_data = requests.get(url)
    soup = BeautifulSoup(site_data.content, "html.parser")
    results = soup.find(class_="container")
    return results
def removeDuplicatesAuthors(authorList):
    updatedAuthors = []
    Auth = []
    for eachAuthor in authorList:
        if eachAuthor["name"] not in Auth:
            Auth.append(eachAuthor["name"])
            updatedAuthors.append(eachAuthor)
    return updatedAuthors
Quotes = []
Authors = []
scrapingUrl = "http://quotes.toscrape.com/"
quotesData = getScrapingData(scrapingUrl)
job_elements = quotesData.find_all("div", class_="quote")
for job in job_elements:
    textElement = job.find("span", itemprop="text");
    authorElement = job.find("small", itemprop="author")
    tagsElement = job.find("div", class_="tags")
    tagName = tagsElement.find_all("a", class_="tag")
    tagNameList = []
    for name in tagName:
        tagNameList.append(name.text)
    quoteKeys = ["quote", "author", "tags"]
    quoteValues = [textElement.text, authorElement.text, tagNameList]
    getQuotes = getQuotesAuthors(quoteKeys, quoteValues)
    Quotes.append(getQuotes)
    anchorName = job.find("a")
    linkUrl = anchorName["href"]
    #Getting Authors Data
    aboutLink = f"http://quotes.toscrape.com/{linkUrl}"
    authorResults = getScrapingData(aboutLink)
    authorDetails = authorResults.find("div", class_="author-details")
    authorBOD = authorDetails.find("span", class_="author-born-date")
    authorLocation = authorDetails.find("span", class_="author-born-location")
    authorKeys = ["name", "born", "reference"]
    authorValues = [authorElement.text, authorBOD.text+" "+authorLocation.text, aboutLink]
    author = getQuotesAuthors(authorKeys, authorValues)
    Authors.append(author)
removeDuplicates = removeDuplicatesAuthors(Authors)
scrapedDataObtained = {"quotes": Quotes, "authors": Authors}
print(scrapedDataObtained)

