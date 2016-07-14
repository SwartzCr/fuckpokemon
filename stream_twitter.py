from twython import Twython
from twython import TwythonStreamer
import json
retweets = {}

class TweetStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            do_twitter(data)
    def on_error(self, status_code, data):
        print status_code
        #self.disconnect()

def load_retweets():
    with open("retweets.json", 'r') as f:
        out = json.load(f)
    return out

def write_retweets():
    with open("retweets.json", 'w') as f:
        json.dump(retweets, f)

def do_twitter(data):
    twitter = auth()
    if "fuck pokemon" in data['text'].lower() and data['id'] not in retweets:
        retweets[data['id']] = True
        write_retweets()
        twitter.retweet(id=data['id'])


def auth():
    with open("access.json", 'r') as f:
        db = json.load(f)
    return Twython(db["API_Key"], db["API_Secret"], db["Access_Token"], db["Access_Token_Secret"])


def auth_streamer():
    with open("access.json", 'r') as f:
        db = json.load(f)
    return TweetStreamer(db["API_Key"], db["API_Secret"], db["Access_Token"], db["Access_Token_Secret"])

def main():
    retweets = load_retweets()
    twitter = auth_streamer()
    twitter.statuses.filter(track='pokemon')

if __name__ == "__main__":
    main()
