import argparse
from api import hearthstonejson

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-uDB", "--updateDB",
        help="Update database with API Data",
        action="store_true")
    parser.add_argument(
        "-uBG", "--updateBG",
        help="Update battlegrounds database with API Data",
        action="store_true")
    args = parser.parse_args()

    if args.updateDB:
        hearthstonejson.call_api()
    if args.updateBG:
        hearthstonejson.save_battlegrounds_cards()
    #app.run()

