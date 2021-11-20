from requests import get as fetch_page
from bs4 import BeautifulSoup
from collections import namedtuple

from .article import parse_article
from .navigation import parse_navigation

# Page information
Page = namedtuple('Page', ['records', 'navigation'])

def parse_page(url):
    page = fetch_page(url)

    if page.status_code != 200:
        # in cases when we can't fetch page
        raise Error("Got code {response}".format(response = page.status_code))

    soup = BeautifulSoup(page.text, 'html.parser')

    parsed_page = Page(records = [], navigation=parse_navigation(soup))

    # parse posts
    for post in soup.select('article.post.teaser-post'):
        parsed_page.records.append(parse_article(post))

    return parsed_page

def print_page(page):
    print("Page number {page}".format(page = page.navigation.current))
    print("Items")
    for record in page.records:
        print("  Name: {name}".format(name = record.name))
        print("  Summary: {summary}".format(summary = record.summary))
        print("  Images: {images}".format(images = str(record.images)))
        print("  Meta")
        print("    Points: ")
        print("       blue = {blue}".format(blue = record.meta.point.blue))
        print("       green = {green}".format(green = record.meta.point.green))
        print("       purple = {purple}".format(purple = record.meta.point.purple))
        print("    Keys: ")
        for key in record.meta.keys:
            print("       name = {name}".format(name = key.name))
            print("       link = {url}".format(url = key.url))
            print("       image = {image}".format(image = key.image))

        print("    Nutrition: ")
        print("       calories = {calories}".format(calories = record.meta.nutrition.calories))
        print("       carbs = {carbs}".format(carbs = record.meta.nutrition.carbs))
        print("       proteins = {proteins}".format(proteins = record.meta.nutrition.proteins))
        print("       fat = {fat}".format(fat = record.meta.nutrition.fat))
        print("  ") 

def to_csv(page):
    rows = [
        ['Name', 'Summary', 'Images', 'Blue point', 'Green Point', 'Purple Point', 'Keys', 'Calories', 'Carbs', 'Proteins', 'Fats']
    ]
    for record in page.records:

        rows.append([
            record.name,
            record.summary,
            ",".join(record.images),
            record.meta.point.blue,
            record.meta.point.green,
            record.meta.point.purple,
            ",".join([key.name for key in record.meta.keys]),
            record.meta.nutrition.calories,
            record.meta.nutrition.carbs,
            record.meta.nutrition.proteins,
            record.meta.nutrition.fat
        ])
    return rows
