import requests
from bs4 import BeautifulSoup, SoupStrainer
import pandas as pd
from tqdm import tqdm

books = []

for i in tqdm (range(1,51), desc="Scraping..."):
	url = f"https://books.toscrape.com/catalogue/page-{i}.html"
	r = requests.get(url).text
	soup = BeautifulSoup(r, "lxml", parse_only=SoupStrainer(class_="col-sm-8 col-md-9"))
	articles = soup.find_all("article")
	
	for article in articles:
		book_url = "https://books.toscrape.com/catalogue/"

		title = article.find("img").attrs["alt"]
		link = book_url + article.find("a").attrs["href"]
		starts = article.find("p").attrs["class"][1]
		price = article.find(class_="price_color").text.strip("Â")
		in_stock = article.find(class_="instock availability").text.strip()

		books.append([title, price, starts, in_stock, link])

df = pd.DataFrame(books, columns=["Title", "Price", "Starts Rating", "In Stock", "link"])

df.to_csv("books.csv")

print("Done!\nData to: books.csv")
