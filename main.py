import os
from dotenv import load_dotenv
from dotenv import dotenv_values
load_dotenv()
#import discord
#from discord.ext import commands
import interactions
from interactions import Client, CommandContext, Embed
from interactions.ext.paginator import Page, Paginator
import requests
from googlesearch import search
from nltk.corpus import wordnet
# bot = commands.Bot(command_prefix='!', intents = discord.Intents.all())
# bot = interactions.Client(dotenv_values(".env")["TOKEN"])
bot = interactions.Client(os.envrion["TOKEN"])
bot.rsoLink = "https://illinois.campuslabs.com/engage/organization/"
# client = interactions.Client(os.getenv("TOKEN"))
bot.linkDict = {}
bot.useCount = 0

@bot.command()
@interactions.option()
async def rso(ctx: interactions.CommandContext, text: str):
  # x = ' '.join(args)
  # argCount = len(args)
  bot.useCount += 1
  x = text
  words = []
  argCount = text.count(' ') + 1
  idealOccurence = 0
  if argCount > 1:
    words = text.split(' ')
  if argCount == 1:
    idealOccurence = 1
  def itContains(thing, rso):
    output = True
    for i in thing:
      if i.lower() not in rso:
        output = False
    return output
  url = "https://illinois.campuslabs.com/engage/api/discovery/search/organizations"
  parameters = {"top": "1000", "filter": "", "query": x, "skip": "0"}
  page = requests.get(url, parameters).json()
  links = []
  pageTitles = []
  pageLinks = []
  pageDescs = []
  pageCats = []
  realPageTitles = []
  realPageLinks = []
  realPageDescs = []
  realPageCats = []
  for v in page["value"]:
    links.append(
            v["Name"] + " - Link: " + bot.rsoLink
            + v["WebsiteKey"] + " " + v["Summary"] + " Categories : " + str(v["CategoryNames"]),
        )
    pageTitles.append(v["Name"])
    pageLinks.append(bot.rsoLink + v["WebsiteKey"])
    pageDescs.append(v["Summary"])
    pageCats.append(str(v["CategoryNames"]))
    bot.linkDict[v["Name"] + " - Link: " + bot.rsoLink
            + v["WebsiteKey"] + " " + v["Summary"] + " Categories : " + str(v["CategoryNames"])] = v["WebsiteKey"]
  output = ""
  count = 0
  for a in range(len(links)):
    if (links[a].lower().count(x.lower()) > idealOccurence or x.lower() in bot.linkDict[links[a]].lower()) and itContains(words, links[a].lower()):
        realPageTitles.append(pageTitles[a])
        realPageCats.append(pageCats[a])
        realPageDescs.append(pageDescs[a])
        realPageLinks.append(pageLinks[a])
        count += 1
  pages = []
  for i in range(len(realPageTitles)):
    embedAdd = Embed(title = realPageTitles[i], description = realPageDescs[i])
    embedAdd.add_field(name = "Link", value = realPageLinks[i])
    embedAdd.add_field(name = "Categories", value = realPageCats[i])
    pages.append(Page(realPageTitles[i], embedAdd))
  if count == 0:
    #for j in search("uiuc rso " + x, tld = "com", num = 1, stop = 1):
      #output += j
    await ctx.send("Sorry, I could not find an RSO matching your query on the official website.")
  elif count == 1:
    await ctx.send(embeds = Embed(title = realPageTitles[0], description = realPageDescs[0]))
  else:
    await Paginator(bot, ctx, pages, use_index = True, use_select = True).run()

bot.start()
