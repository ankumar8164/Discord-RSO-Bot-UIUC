# these are imports we need
import interactions
from interactions import Client, CommandContext, Embed
from interactions.ext.paginator import Page, Paginator

# a class called RSO
class RSO:
    def __init__ (self, name, websiteKey, summary, categories):
        # just initialize all variables
        self.name = name ; self.websiteKey = websiteKey; self.summary = summary ; self.categories = categories ; self.rsoLink = "https://illinois.campuslabs.com/engage/organization/"

    def getEmbed(self):
        # create embed and add fields as needed before returning
        # the new line chars are just there to make it look a little nicer
        embed = Embed(title = self.name, description = self.summary)
        embed.add_field(name = "Link", value = self.rsoLink + self.websiteKey)
        embed.add_field(name = "Categories", value = str(self.categories))
        return embed

    def generateFullSummary(self):
        # combines all these into one string for ease in checkValidity
        return (self.name + " - Link: " + self.rsoLink
            + self.websiteKey + " " + self.summary + " Categories : " + str(self.categories)).lower()

    def confirmAllWords(self, fullSummary, wordArray):
        allWordsIn = True
        for word in wordArray:
            #make sure that all words are present (for example for table tennis, we would check both table and tennis)
            if word not in fullSummary:
                allWordsIn = False
                break
        return allWordsIn

    def checkValidity(self, userInput):
        # the idea is that if our userInput is just one word, we either want that word present at least twice or be in the website key
        # the reason for website key is that for some inputs (like if someone searches 'hkn'), it may discount actually valid RSOs
        # because the phrase 'hkn' does not appear twice in the description, but it is in the website key
        # if it is two words, we want to check word by word (e.g. HKN is also related to EE, but the description says electrical and computer engineering)
        # by checking each word separately, we will "find" EE even though it may not be explicitly written as such
        if userInput.count(' ') + 1 > 1:
            return userInput in self.websiteKey or self.confirmAllWords(self.generateFullSummary(), userInput.split())
        else:
            return self.generateFullSummary().count(userInput) > 1 or userInput in self.websiteKey
