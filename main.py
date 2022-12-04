# rso contains a class made to make this cleaner
from rso import RSO
import os
# this import allows us to access the bot token without making it visible to others
from dotenv import load_dotenv
load_dotenv()
# interactions is the library used for this bot (chosen for its paginator capability)
import interactions
from interactions.ext.paginator import Page, Paginator
# requests allows us to access the data from the RSO API
import requests
# set up the bot and important bot variables (a link to the RSO page essentially)
bot = interactions.Client(os.environ["TOKEN"])
bot.rsoLink = "https://illinois.campuslabs.com/engage/organization/"

@bot.command()
@interactions.option()
async def rso(ctx: interactions.CommandContext, search: str):
  # make the search lower case just for ease later
  search = search.lower()
  apiURL = "https://illinois.campuslabs.com/engage/api/discovery/search/organizations"
  parameters = {"top": "1000", "filter": "", "query": search, "skip": "0"}
  # get the data
  relevantDataFromAPI = requests.get(apiURL, parameters).json()
  # an array of RSOs to store all those that we get initially
  initialRSOs = []
  # construct and insert all the RSOs we get
  for v in relevantDataFromAPI["value"]:
    initialRSOs.append(RSO(v["Name"], v["WebsiteKey"], v["Summary"], v["CategoryNames"]))
  # this will be used to construct our paginator later
  pages = []
  # use methods of the rso class to check validity
  for rso in initialRSOs:
    if rso.checkValidity(search) == True:
      pages.append(Page("", rso.getEmbed()))
  # conditional handling for different valid RSO counts
  if len(pages) == 0:
    await ctx.send("Sorry, I could not find an RSO matching your query on the official website.")
  elif len(pages) == 1:
    await ctx.send(embeds = pages[0])
  else:
    await Paginator(bot, ctx, pages, use_index = True, use_select = True).run()

bot.start()
