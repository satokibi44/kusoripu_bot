from requests_oauthlib import OAuth1Session
import urllib.request
import json


class TweetUtil():

    def __init__(self):
        self.CK = "vPVdfstGdvW3uEc4CALVeTvjf"
        self.CS = "ZVSff6RDG3l5LcG6NWvyKZgn8MVD01rwZZ0MPTwC4hplSzpl0r"
        self.AT = "3282531025-S7EszUJNYeNnjRdnek6xTolfxCVkf1wj2MX85fJ"
        self.AS = "TpJwvMJvKnWm2horycmU3fP2jUSHwMYVzBsVwvjP0OksF"
        self.session = OAuth1Session(self.CK, self.CS, self.AT, self.AS)
        self.user_id_list = [1300452125458067457,
                             816932493962031104, 4444885817, 2799898254, 3282531025]

    def get_timeline(self):
        url = "https://api.twitter.com/1.1/statuses/home_timeline.json"
        res = self.session.get(url=url)
        tweet_id_list = []
        tweet_text_list = []
        if res.status_code == 200:
            timelines = res.json()
            for tweet in timelines:
                if (tweet['user']['id'] in self.user_id_list):
                    tweet_id = tweet['id']
                    tweet_text = tweet['text']
                    tweet_id_list.append(tweet_id)
                    tweet_text_list.append(tweet_text)
            return tweet_id_list, tweet_text_list
        else:
            print("ERROR : %d" % res.status_code)
        return

    def excute_reply(self, tweet_text, tweet_id):
        transformer_url = "http://3.139.162.86:80/predict?sentence=" + \
            urllib.parse.quote(tweet_text)
        req = urllib.request.Request(transformer_url)
        with urllib.request.urlopen(req) as res:
            res_json = res.read().decode('utf-8')
        res_json = json.loads(res_json)
        reply = res_json["decode_sentence"]

        url = "https://api.twitter.com/1.1/statuses/update.json"
        params = {"status": reply, "in_reply_to_status_id": tweet_id,
                  "auto_populate_reply_metadata": True}

        reqest = self.session.post(url, params=params)
        if reqest.status_code == 200:
            print("Succeed!")
        else:
            print("ERROR : %d" % reqest.status_code)
        return
