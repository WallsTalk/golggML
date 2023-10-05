

import requests
from bs4 import BeautifulSoup
import json
import time


def main():
    with open("game_collection", "r") as game_history:
        game_history = [json.loads(game) for game in game_history.read().split("\n")[:-1]]

    x= [item["game_id"] for item in game_history if item["turney"]=="LFL Promotion 2024/"]
    print(x, len(x))



if __name__ == "__main__":
    main()