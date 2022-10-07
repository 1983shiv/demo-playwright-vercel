# import asyncio
from playwright.async_api import async_playwright
# from flask import Flask
import json
import time
from bs4 import BeautifulSoup as bs
from fastapi import FastAPI
import uvicorn


async def scrap():
    items = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.ergodotisi.com/en/SearchResults.aspx")

        i = 0
        # while i < 15:
        #     page.mouse.wheel(0, 4000)
        #     page.locator("text=More Job Posts...").click()
        #     i = i + 1

        time.sleep(3)
        html = await page.content()

        soup = bs(html, 'html.parser')
        # print(soup.prettify())
        allListing = soup.find_all(
            'article', attrs={'class': 'search-result-card'})
        # print(len(allListing))
        for listing in allListing:
            if ("yesterday" in listing.find_all("p")[3].text):
                # print(listing.find_all("p")[3].text)
                item = {
                    "title": listing.find_all("a")[0].text,
                    "url": listing.find_all("a")[1].text,
                    "city": listing.find_all("p")[0].text,
                    "cmpy": listing.find_all("p")[1].text,
                    "view": listing.find_all("p")[2].text,
                    "date": listing.find_all("p")[3].text,
                    "expire": listing.find_all("p")[4].text,
                    "typeofjob": listing.find_all("p")[5].text
                }
                items.append(item)
        # print(len(items))
        await browser.close()
    return items

app = FastAPI()

# asyncio.run(scrap())


@app.get('/')
async def root():

    items = await scrap()
    # data = {"data": items, "Timestamp": time.time()}
    # json_dump = await json.dumps(data)
    # print("running server...")
    return items


# app = Flask(__name__)

# @app.route('/')
# async def home():
#     # data = {"data": await scrap(), "Timestamp": time.time()}
#     # json_dump = await json.dumps(data)
#     # print("running server...")
#     return scrap()

# async def main():
#     await scrap()


# app.run(app())


if __name__ == '__main__':
    uvicorn.run("app:app", port=8000, host='0.0.0.0')
