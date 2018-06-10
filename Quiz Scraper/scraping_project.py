import requests
from bs4 import BeautifulSoup
import random

url = "http://quotes.toscrape.com/"

def scrape_quotes():
	response = requests.get(url)

	if not response.status_code == 200:
	    raise Exception("Something is wrong")
	soup = BeautifulSoup(response.text, "html.parser")
	all_quotes = []
	href = url
	while True:
	    quotes = soup.find_all(class_="quote")

	    for quote in quotes:
	        title = quote.find_next().get_text()
	        name = quote.find_next(class_="author").get_text()
	        bio_link = quote.find_next(class_="author").find_next()["href"]
	        all_quotes.append({
	            "title": title,
	            "name": name,
	            "bio-link": bio_link
	        })
	    next = soup.find(class_="next")
	    print(f"Now Scrapping ....{href}")
	    if not next:
	        break
	    href = url+next.find_next()["href"]  # next page link
	    response = requests.get(href)
	    soup = BeautifulSoup(response.text, "html.parser")
	    # time.sleep(2)
	return all_quotes

# GamePlay
def start_game(all_quotes):
    print("*"*30)
    remaining_guess = 4
    question = random.choice(all_quotes)
    print("Here is your question : ")
    print(question["title"])
    guess = ''
    answer = question["name"]
    while True:
        print(f"Remaining guess : {remaining_guess} ")
        if remaining_guess == 4:
            guess = input("Enter name of the person : ")
            remaining_guess -= 1
        elif remaining_guess == 3:
            print("Hint : ")
            response = requests.get(url+question["bio-link"])
            soup = BeautifulSoup(response.text, "html.parser")
            born = soup.find(class_="author-born-date").get_text()
            loc = soup.find(class_="author-born-location").get_text()
            print("Born on : ", born, " ", loc)
            guess = input("Enter name of the person : ")
            remaining_guess -= 1
        elif remaining_guess == 2:
            print("Hint : ")
            print(f"First letter of name is : {answer[0:1]}")
            guess = input("Enter name of the person : ")
            remaining_guess -= 1
        elif remaining_guess == 1:
            print("Hint : ")
            print(f"Last letter of name is : {answer[:-2:-1]}")
            guess = input("Enter name of the person : ")
            remaining_guess -= 1
        if guess.lower() == answer.lower():
            print("Congrats you won !")
            break
        if remaining_guess == 0:
            print("you lost !")
            print(f"answer : {answer}")
            break

    again = ''
    while again.lower() not in ("yes", "y", "no", "n"):
        again = input("Do you want to play again (y/n)")
    if again in ("yes", "y"):
        return start_game(all_quotes)
    print("Good By !")

data = scrape_quotes()
start_game(data)
