import os
from discord.ext import commands
import requests
from googlesearch import search
bot = commands.Bot(command_prefix='!')
bot.rsoLink = "https://illinois.campuslabs.com/engage/organization/"

@bot.command()

async def rso(ctx, x):
  url = "https://illinois.campuslabs.com/engage/api/discovery/search/organizations"
  parameters = {"top": "1000", "filter": "", "query": x, "skip": "0"}
  page = requests.get(url, parameters).json()
  links = []
  for v in page["value"]:
    links.append(
            v["Name"] + " - Link: " + bot.rsoLink
            + v["WebsiteKey"] + ". " + v["Summary"] + ". Categories : " + str(v["CategoryNames"]),
        )
  output = ""
  count = 0
  for a in links:
    if x.lower() in a.lower():
        output += a + "\n" + "\n"
        count += 1
    if count == 5:
      break
  if count == 1:
    await ctx.send("Only one result was found:" + "\n" + output)
  if count > 1:
    if len(output) > 2000:
      await ctx.send("Here are the top " + str(count) + " results:" + "\n" + "\n" + output[0: 1970])
    else:
      await ctx.send("Here are the top " + str(count) + " results:" + "\n" + "\n" + output)
  if len(output) == 0:
    for j in search("uiuc rso " + x, tld = "com", num = 1, stop = 1):
      output += j
    await ctx.send("Sorry, I could not find an RSO matching your query on the official website. Perhaps the following result from a Google search might help: " + output + "\n" + "Only first result has been displayed.")

async def addDiscordServer(ctx, x, y):
  await ctx.send(x + y)

bot.run('OTgyNjkxODEwMTA5NDMxODM4.GvbZAy.Iu1ZVWfrAcXU00u5O6D4moPYwWlCpfMbPVJtDU')