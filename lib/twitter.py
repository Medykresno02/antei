from .tweetyy import Twitter
from utilities import jsonify

def tweetS(req):
    if (url := req.GET.get("url")):
        tw = Tweet(url).get_tweet
        if isinstance(tw, str):
            return jsonify({"status": 409, "msg": "Terjadi kesalahan, mungkin url tidak valid"}, 409)
        tww = tw.__dict__
        tww.update({"status": 200})
        return jsonify(tww, 200)
    else:
        return jsonify({"status": 400, "msg": "Parameter url jangan kosong"}, 400)

def tweetP(req):
    if (username := req.GET.get("username")):
        pr = Profile(username).stalk
        if isinstance(pr, str):
            return jsonify({"status": 409, "msg": "Terjadi kesalahan, username tidak ditemukan"}, 409)
        prr = pr.__dict__
        prr.update({"status": 200})
        return jsonify(prr, 200)
    else:
        return jsonify({"status": 400, "msg": "Parameter username jangan kosong"}, 400)

def tweetT():
    tr = Trends().get_trends
    return jsonify({"status": 409, "msg": "Terjadi kesalahan saat mengambil Trending Tweet"}, 409) if isinstance(tr, str) else jsonify({"status": 200, "result": tr}, 200)

def tweetTr(req):
    if (city := req.GET.get("city")):
        if city.lower().title() in ['Bekasi', 'Depok', 'Pekanbaru', 'Surabaya', 'Makassar', 'Bandung', 'Jakarta', 'Medan', 'Palembang', 'Semarang', 'Tangerang']:
            city = city.lower()
            trc = TrendsCity()
            return jsonify({"status": 200, "result": trc.get_city(city)}, 200)
        else:
            return jsonify({"status": 409, "msg": "City/Kota tidak ada pada Trending Tweet Indonesia"}, 409)
    else:
        return jsonify({"status": 400, "msg": "Parameter city jangan kosong"}, 400)

class Auth:
    CONSUMER_KEY = "6wQC0AUhnDPP6zfKjxZ2PfERZ"
    CONSUMER_SECRET = "ylnGRhk31SEkZeupL0d7ules8bbi9S2RWgYv9innWqpL0x2y7e"
    ACCESS_KEY = "1418043098106531843-a6gt6MfUKZIippoveDluZDTm21kK4q"
    ACCESS_SECRET = "AQ6KkngNnWUpkywqx2ShXPx95CbLU3wuDTNbKcRrO54PM"

class MediaTweet:
    def __init__(self):
        self.author = None
        self.username = None
        self.tweet_id = None
        self.caption = None
        self.created_at = None
        self.likes = None
        self.retweets = None
        self.media = None
        self.type = None
        self.is_retweet = None

class ProfileTweet:
    def __init__(self):
        self.name = None
        self.username = None
        self.description = None
        self.profile_pic = None
        self.profile_banner = None
        self.follower_count = None
        self.following_count = None
        self.tweet_count = None
        self.location = None
        self.created_at = None
        self.verified = False
        self.protected = False

class Tweet:

    def __init__(self, url: str) -> None:
        self.tweet = Twitter()
        self.media = MediaTweet()
        self.url = url

    @property
    def get_id(self):
        ids = self.url.split("/")[-1]
        return ids if "?" not in ids else ids.split("?")[0]

    @property
    def get_username(self):
        return self.url.split("/")[3]

    @property
    def get_tweet(self) -> MediaTweet:
        try:
            id = self.get_id
            profile = Profile(self.get_username).stalk
            tweet = self.tweet.tweet_detail(id)["tweet"]
            self.media.author = profile.name
            self.media.username = profile.username
            self.media.tweet_id = tweet.get("id_str")
            self.media.caption = tweet.get("full_text")
            self.media.created_at = tweet.get("created_at").split("+")[0].strip()
            self.media.likes = tweet.get("favorite_count")
            self.media.retweets = tweet.get("retweet_count")
            self.media.is_retweet = tweet.get("retweeted")
            if len(tweet.get("extended_entities").get("media")) < 2:
                self.media.media = tweet.get("extended_entities").get("media")[0].get("video_info").get("variants")[-1].get("url") if tweet.get("extended_entities").get("media")[0].get("type") == "video" else tweet.get("extended_entities").get("media")[0].get("media_url_https")
            else:
                self.media.media = [i.get("video_info").get("variants")[-1].get("url") if i.get("type") == "video" else i.get("media_url_https") for i in tweet.get("extended_entities").get("media")]
            self.media.type = tweet.get("extended_entities").get("media")[0].get("type")
            return self.media
        except Exception as e:
            print(e)
            return "Err"

class Profile:

    def __init__(self, username: str) -> None:
        self.tweet = Twitter(username)
        self.profile = ProfileTweet()
        self.username = username

    @property
    def stalk(self) -> ProfileTweet:
        try:
            tweet = self.tweet.get_user_info()["data"]["user"]["result"]["legacy"]
            self.profile.name = tweet.get("name")
            self.profile.username = tweet.get("screen_name")
            self.profile.description = tweet.get("description")
            self.profile.profile_pic = tweet.get("profile_image_url_https") if "_normal" not in tweet.get("profile_image_url_https") else tweet.get("profile_image_url_https").replace("_normal","")
            self.profile.profile_banner = tweet.get("profile_banner_url")
            self.profile.follower_count = tweet.get("followers_count")
            self.profile.following_count = tweet.get("friends_count")
            self.profile.tweet_count = tweet.get("statuses_count")
            self.profile.location = tweet.get("location")
            self.profile.created_at = tweet.get("created_at").split("+")[0].strip()
            self.profile.verified = tweet.get("verified")
            self.profile.protected = tweet.get("protected")
            return self.profile
        except Exception as e:
            print(e)
            return "Err"

class Trends(Auth):

    def __init__(self):
        self.tweet = Twitter()

    @property
    def get_trends(self):
        return self.tweet.trends_available()

class TrendsCity(Auth):

    def __init__(self):
        auth = OAuthHandler(self.CONSUMER_KEY, self.CONSUMER_SECRET)
        auth.set_access_token(self.ACCESS_KEY, self.ACCESS_SECRET)
        self.tweet = API(auth)
        self.trends = [i for i in self.tweet.trends_available() if i.get("country") == "Indonesia"]

    def get_city(self, city):
        for i in self.trends:
            if i.get("name") == city.title():
                return self.tweet.trends_place(id=i.get("woeid"))[0].get("trends")
