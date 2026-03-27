"""
Platform scraper scaffolding.

These are starter templates for pulling talent data from social platforms.
Each scraper follows the same pattern:
    1. Fetch profile data from the platform
    2. Normalize it into our schema
    3. Upsert into the database

IMPORTANT: Most platforms require API keys or have rate limits.
Some (like Instagram) don't have a public API and require workarounds.

Options for data collection:
- Official APIs: YouTube Data API, TikTok Research API
- Third-party APIs: Social Blade, HypeAuditor, Modash, CreatorIQ
- Browser automation: Playwright/Selenium (fragile, use as last resort)
- Manual + CSV: Often the most practical starting point
"""
import json
import time
from datetime import datetime
from models import add_talent, add_platform_account, update_account_metrics, search_talent


class BaseScraper:
    """Base class for platform scrapers."""

    platform = "unknown"
    rate_limit_delay = 1.0  # seconds between requests

    def __init__(self, api_key=None):
        self.api_key = api_key

    def fetch_profile(self, username):
        """Fetch raw profile data from the platform. Override this."""
        raise NotImplementedError

    def normalize(self, raw_data):
        """
        Convert raw API data into our standard format.
        Should return a dict with keys:
            name, username, bio, followers, following, posts_count,
            engagement_rate, verified, profile_url, avatar_url
        """
        raise NotImplementedError

    def scrape_and_save(self, username, talent_id=None, category="content_creator"):
        """Fetch a profile and save/update it in the database."""
        raw = self.fetch_profile(username)
        if not raw:
            print(f"  Could not fetch {self.platform}/@{username}")
            return None

        data = self.normalize(raw)

        # Create talent if needed
        if talent_id is None:
            talent_id = add_talent(
                name=data.get("name", username),
                category=category,
                bio=data.get("bio"),
                discovered_via=f"{self.platform} scraper",
            )

        account_id = add_platform_account(
            talent_id=talent_id,
            platform=self.platform,
            username=data["username"],
            profile_url=data.get("profile_url"),
            followers=data.get("followers"),
            following=data.get("following"),
            posts_count=data.get("posts_count"),
            engagement_rate=data.get("engagement_rate"),
            verified=data.get("verified", False),
            raw_data=raw,
        )

        time.sleep(self.rate_limit_delay)
        return talent_id


# ─── YouTube ─────────────────────────────────────────────────

class YouTubeScraper(BaseScraper):
    """
    YouTube Data API v3 scraper.

    Get an API key at: https://console.cloud.google.com/apis/credentials
    Enable: YouTube Data API v3

    Usage:
        scraper = YouTubeScraper(api_key="YOUR_KEY")
        scraper.scrape_and_save("MrBeast")
    """
    platform = "youtube"

    def fetch_profile(self, username):
        try:
            import requests
        except ImportError:
            print("  pip install requests")
            return None

        # Search for channel by username/handle
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "q": username,
            "type": "channel",
            "maxResults": 1,
            "key": self.api_key,
        }
        resp = requests.get(url, params=params)
        if resp.status_code != 200:
            return None

        items = resp.json().get("items", [])
        if not items:
            return None

        channel_id = items[0]["snippet"]["channelId"]

        # Get full channel stats
        url = "https://www.googleapis.com/youtube/v3/channels"
        params = {
            "part": "snippet,statistics",
            "id": channel_id,
            "key": self.api_key,
        }
        resp = requests.get(url, params=params)
        if resp.status_code != 200:
            return None

        channels = resp.json().get("items", [])
        return channels[0] if channels else None

    def normalize(self, raw_data):
        snippet = raw_data.get("snippet", {})
        stats = raw_data.get("statistics", {})
        return {
            "name": snippet.get("title", ""),
            "username": snippet.get("customUrl", "").lstrip("@"),
            "bio": snippet.get("description", "")[:500],
            "followers": int(stats.get("subscriberCount", 0)),
            "posts_count": int(stats.get("videoCount", 0)),
            "profile_url": f"https://youtube.com/{snippet.get('customUrl', '')}",
            "verified": False,  # Not available via API
        }


# ─── TikTok ──────────────────────────────────────────────────

class TikTokScraper(BaseScraper):
    """
    TikTok scraper placeholder.

    TikTok's official Research API requires an application:
    https://developers.tiktok.com/products/research-api/

    Alternatives:
    - Unofficial APIs (ensembledata, tiktok-scraper npm package)
    - Third-party services (Modash, CreatorIQ, Phyllo)
    - Manual CSV export from TikTok analytics

    Usage (once you have an API):
        scraper = TikTokScraper(api_key="YOUR_KEY")
        scraper.scrape_and_save("charlidamelio")
    """
    platform = "tiktok"

    def fetch_profile(self, username):
        # TODO: Implement with your chosen TikTok data source
        print(f"  TikTok scraper not configured. Add @{username} manually or via CSV.")
        print(f"  See: https://developers.tiktok.com/products/research-api/")
        return None

    def normalize(self, raw_data):
        # Template for when you connect an API
        return {
            "name": raw_data.get("nickname", ""),
            "username": raw_data.get("uniqueId", ""),
            "bio": raw_data.get("signature", ""),
            "followers": raw_data.get("followerCount", 0),
            "following": raw_data.get("followingCount", 0),
            "posts_count": raw_data.get("videoCount", 0),
            "verified": raw_data.get("verified", False),
            "profile_url": f"https://tiktok.com/@{raw_data.get('uniqueId', '')}",
        }


# ─── Instagram ───────────────────────────────────────────────

class InstagramScraper(BaseScraper):
    """
    Instagram scraper placeholder.

    Instagram has NO public API for profile data (Meta shut it down).

    Options:
    - Meta Business API (only for accounts you manage)
    - Third-party services: Modash, HypeAuditor, Phyllo, RapidAPI scrapers
    - Browser automation with Playwright (fragile, may get blocked)
    - Manual entry / CSV import (most reliable)

    Usage (with a third-party API):
        scraper = InstagramScraper(api_key="YOUR_RAPIDAPI_KEY")
        scraper.scrape_and_save("kendalljenner")
    """
    platform = "instagram"

    def fetch_profile(self, username):
        # TODO: Implement with your chosen Instagram data source
        print(f"  Instagram scraper not configured. Add @{username} manually or via CSV.")
        print(f"  Recommended: Modash API or Phyllo for IG data.")
        return None

    def normalize(self, raw_data):
        return {
            "name": raw_data.get("full_name", ""),
            "username": raw_data.get("username", ""),
            "bio": raw_data.get("biography", ""),
            "followers": raw_data.get("follower_count", 0),
            "following": raw_data.get("following_count", 0),
            "posts_count": raw_data.get("media_count", 0),
            "verified": raw_data.get("is_verified", False),
            "profile_url": f"https://instagram.com/{raw_data.get('username', '')}",
        }


# ─── Batch Operations ────────────────────────────────────────

def batch_scrape(usernames, scraper, category="content_creator"):
    """
    Scrape multiple profiles with a given scraper.

    Usage:
        yt = YouTubeScraper(api_key="...")
        batch_scrape(["MrBeast", "PewDiePie", "Markiplier"], yt, "content_creator")
    """
    results = []
    for i, username in enumerate(usernames):
        print(f"  [{i+1}/{len(usernames)}] Scraping {scraper.platform}/@{username}...")
        talent_id = scraper.scrape_and_save(username, category=category)
        results.append({"username": username, "talent_id": talent_id})
    return results


# ─── Quick Reference ─────────────────────────────────────────

THIRD_PARTY_APIS = """
Recommended third-party APIs for talent data:

1. Modash (modash.io)
   - Instagram, TikTok, YouTube
   - Influencer discovery, audience analytics
   - Has a search/discovery API

2. HypeAuditor (hypeauditor.com)
   - Instagram, TikTok, YouTube, Twitch
   - Fraud detection, audience quality scores

3. Phyllo (getphyllo.com)
   - Unified API across 100+ platforms
   - Creator identity, engagement, earnings data

4. CreatorIQ (creatoriq.com)
   - Enterprise-level creator data
   - Discovery, vetting, campaign management

5. Social Blade (socialblade.com)
   - YouTube, Twitch, Instagram, Twitter
   - Historical growth data, rankings
   - Free tier available

6. RapidAPI marketplace
   - Various scraper APIs for individual platforms
   - Quality varies, good for prototyping
"""
