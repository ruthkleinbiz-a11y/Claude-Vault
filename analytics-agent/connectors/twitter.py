"""X (Twitter) analytics via the v2 API."""

import os
from datetime import datetime, timedelta, timezone

import tweepy


def fetch(username: str, lookback_days: int = 14) -> dict:
    client = tweepy.Client(bearer_token=os.environ["TWITTER_BEARER_TOKEN"])

    end = datetime.now(tz=timezone.utc)
    start = end - timedelta(days=lookback_days)

    try:
        user_resp = client.get_user(
            username=username,
            user_fields=["public_metrics"],
        )
        if not user_resp.data:
            return {"error": f"User @{username} not found", "data": None}

        user = user_resp.data
        account_metrics = user.public_metrics  # followers_count, following_count, tweet_count

        tweets_resp = client.get_users_tweets(
            id=user.id,
            start_time=start,
            end_time=end,
            tweet_fields=["public_metrics", "created_at"],
            max_results=100,
        )

        tweets = tweets_resp.data or []
        totals = {
            "impressions": 0,
            "likes": 0,
            "retweets": 0,
            "replies": 0,
            "quotes": 0,
            "bookmarks": 0,
            "tweet_count": len(tweets),
            "followers": account_metrics.get("followers_count", 0),
        }
        for tweet in tweets:
            m = tweet.public_metrics or {}
            totals["impressions"] += m.get("impression_count", 0)
            totals["likes"] += m.get("like_count", 0)
            totals["retweets"] += m.get("retweet_count", 0)
            totals["replies"] += m.get("reply_count", 0)
            totals["quotes"] += m.get("quote_count", 0)
            totals["bookmarks"] += m.get("bookmark_count", 0)

        return {"data": totals, "error": None}

    except Exception as exc:
        return {"data": None, "error": str(exc)}
