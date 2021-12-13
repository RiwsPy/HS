import argparse
from api.hearthstonejson import call_api, save_battlegrounds_cards

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
        call_api()
    if args.updateBG:
        save_battlegrounds_cards()
