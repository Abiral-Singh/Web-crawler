import requests
from bs4 import BeautifulSoup
import random
from csv import DictReader
url = "http://quotes.toscrape.com/"


def read_quotes():
    with open("quote_data.csv", "r") as file:
        csv_reader = DictReader(file)
        return list(csv_reader)
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


data = read_quotes()
start_game(data)
