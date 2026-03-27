#!/usr/bin/env python3
"""
Talent Database CLI — manage your talent database from the command line.

Usage:
    python cli.py init                          Initialize the database
    python cli.py add                           Add talent interactively
    python cli.py search [query]                Search talent
    python cli.py show <id>                     Show talent details
    python cli.py import-csv <file>             Import from CSV
    python cli.py export-csv [file]             Export to CSV
    python cli.py stats                         Show database stats
    python cli.py list-create <name>            Create a list
    python cli.py list-add <list_id> <talent_id> Add talent to list
    python cli.py top [--platform X] [--limit N] Top talent by followers
"""
import sys
import os
import csv
import json

# Ensure we can import from the same directory
sys.path.insert(0, os.path.dirname(__file__))

from db import init_db, get_connection
from models import (
    add_talent, get_talent, update_talent, delete_talent, search_talent,
    add_platform_account, get_talent_accounts, get_talent_collabs,
    create_list, add_to_list, get_list_members, get_stats, list_categories
)


def cmd_init():
    """Initialize the database."""
    path = init_db()
    print(f"Database initialized at: {path}")


def cmd_add():
    """Add a talent interactively."""
    print("=== Add New Talent ===")
    name = input("Name: ").strip()
    if not name:
        print("Name is required.")
        return

    stage_name = input("Stage name (optional): ").strip() or None
    print("Categories: model, musician, cosplayer, content_creator, multi")
    category = input("Category: ").strip()
    if category not in ("model", "musician", "cosplayer", "content_creator", "multi"):
        print(f"Warning: '{category}' is not a standard category, using anyway.")

    gender = input("Gender (optional): ").strip() or None
    city = input("City (optional): ").strip() or None
    country = input("Country (optional): ").strip() or None
    tags = input("Tags (comma-separated, optional): ").strip() or None
    discovered = input("Discovered via (optional): ").strip() or None

    talent_id = add_talent(
        name=name, category=category, stage_name=stage_name,
        gender=gender, location_city=city, location_country=country,
        tags=tags, discovered_via=discovered
    )
    print(f"\nAdded: {name} (ID: {talent_id})")

    # Offer to add platform accounts
    while True:
        add_acct = input("\nAdd a platform account? (y/n): ").strip().lower()
        if add_acct != "y":
            break
        platform = input("  Platform (instagram/tiktok/youtube/twitter/twitch): ").strip()
        username = input("  Username: ").strip()
        followers = input("  Followers (optional): ").strip()
        followers = int(followers) if followers else None

        url = None
        if platform == "instagram":
            url = f"https://instagram.com/{username}"
        elif platform == "tiktok":
            url = f"https://tiktok.com/@{username}"
        elif platform == "youtube":
            url = f"https://youtube.com/@{username}"
        elif platform == "twitter":
            url = f"https://twitter.com/{username}"

        add_platform_account(
            talent_id=talent_id, platform=platform, username=username,
            profile_url=url, followers=followers
        )
        print(f"  Added {platform} account: @{username}")


def cmd_search(args):
    """Search for talent."""
    query = " ".join(args) if args else None
    category = None
    platform = None
    min_followers = None

    # Parse flags
    i = 0
    positional = []
    while i < len(args):
        if args[i] == "--category" and i + 1 < len(args):
            category = args[i + 1]
            i += 2
        elif args[i] == "--platform" and i + 1 < len(args):
            platform = args[i + 1]
            i += 2
        elif args[i] == "--min-followers" and i + 1 < len(args):
            min_followers = int(args[i + 1])
            i += 2
        else:
            positional.append(args[i])
            i += 1

    query = " ".join(positional) if positional else None
    results = search_talent(query=query, category=category, platform=platform,
                            min_followers=min_followers)

    if not results:
        print("No results found.")
        return

    print(f"\n{'ID':<6} {'Name':<25} {'Category':<18} {'Platforms':<30} {'Top Followers':<15}")
    print("-" * 94)
    for t in results:
        platforms = t.get("platforms") or "-"
        followers = t.get("max_followers") or "-"
        if isinstance(followers, int):
            followers = f"{followers:,}"
        print(f"{t['id']:<6} {t['name'][:24]:<25} {t['category']:<18} {str(platforms)[:29]:<30} {followers:<15}")

    print(f"\n{len(results)} result(s)")


def cmd_show(talent_id):
    """Show detailed talent profile."""
    t = get_talent(int(talent_id))
    if not t:
        print(f"Talent ID {talent_id} not found.")
        return

    print(f"\n{'='*50}")
    print(f"  {t['name']}", end="")
    if t["stage_name"]:
        print(f" ({t['stage_name']})", end="")
    print(f"  [ID: {t['id']}]")
    print(f"{'='*50}")
    print(f"  Category:  {t['category']}")
    if t["gender"]:
        print(f"  Gender:    {t['gender']}")
    if t["location_city"] or t["location_country"]:
        loc = ", ".join(filter(None, [t["location_city"], t["location_country"]]))
        print(f"  Location:  {loc}")
    if t["agency"]:
        print(f"  Agency:    {t['agency']}")
    if t["tags"]:
        print(f"  Tags:      {t['tags']}")
    if t["website"]:
        print(f"  Website:   {t['website']}")
    if t["discovered_via"]:
        print(f"  Found via: {t['discovered_via']}")
    print(f"  Status:    {t['status']}")

    # Platform accounts
    accounts = get_talent_accounts(int(talent_id))
    if accounts:
        print(f"\n  Platform Accounts:")
        for a in accounts:
            followers = f"{a['followers']:,}" if a['followers'] else "?"
            verified = " ✓" if a['verified'] else ""
            print(f"    {a['platform']:<12} @{a['username']}{verified}  ({followers} followers)")
            if a['profile_url']:
                print(f"    {'':12} {a['profile_url']}")

    # Collaborations
    collabs = get_talent_collabs(int(talent_id))
    if collabs:
        print(f"\n  Collaborations:")
        for c in collabs:
            other = c["talent_2_name"] if c["talent_id_1"] == int(talent_id) else c["talent_1_name"]
            print(f"    with {other} ({c['collab_type'] or 'unspecified'})")

    if t["bio"]:
        print(f"\n  Bio: {t['bio']}")
    if t["notes"]:
        print(f"\n  Notes: {t['notes']}")
    print()


def cmd_import_csv(filepath):
    """
    Import talent from a CSV file.

    Expected columns (all optional except name and category):
        name, stage_name, category, gender, location_city, location_country,
        tags, email, website, agency, discovered_via, notes, status,
        instagram, tiktok, youtube, twitter, twitch
        ig_followers, tiktok_followers, yt_followers
    """
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    imported = 0
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get("name", "").strip()
            category = row.get("category", "content_creator").strip()
            if not name:
                continue

            talent_id = add_talent(
                name=name,
                stage_name=row.get("stage_name", "").strip() or None,
                category=category,
                gender=row.get("gender", "").strip() or None,
                location_city=row.get("location_city", "").strip() or None,
                location_country=row.get("location_country", "").strip() or None,
                tags=row.get("tags", "").strip() or None,
                email=row.get("email", "").strip() or None,
                website=row.get("website", "").strip() or None,
                agency=row.get("agency", "").strip() or None,
                discovered_via=row.get("discovered_via", "").strip() or None,
                notes=row.get("notes", "").strip() or None,
                status=row.get("status", "active").strip(),
            )

            # Add platform accounts from CSV columns
            platforms = {
                "instagram": ("instagram", row.get("instagram"), row.get("ig_followers")),
                "tiktok": ("tiktok", row.get("tiktok"), row.get("tiktok_followers")),
                "youtube": ("youtube", row.get("youtube"), row.get("yt_followers")),
                "twitter": ("twitter", row.get("twitter"), row.get("twitter_followers")),
                "twitch": ("twitch", row.get("twitch"), row.get("twitch_followers")),
            }
            for platform, (pname, username, followers) in platforms.items():
                username = (username or "").strip()
                if username:
                    fcount = None
                    if followers:
                        try:
                            fcount = int(str(followers).replace(",", "").strip())
                        except ValueError:
                            pass
                    url_map = {
                        "instagram": f"https://instagram.com/{username}",
                        "tiktok": f"https://tiktok.com/@{username}",
                        "youtube": f"https://youtube.com/@{username}",
                        "twitter": f"https://twitter.com/{username}",
                        "twitch": f"https://twitch.tv/{username}",
                    }
                    add_platform_account(
                        talent_id=talent_id, platform=pname, username=username,
                        profile_url=url_map.get(pname), followers=fcount
                    )

            imported += 1

    print(f"Imported {imported} talent from {filepath}")


def cmd_export_csv(filepath=None):
    """Export all talent to CSV."""
    filepath = filepath or "talent_export.csv"
    conn = get_connection()
    rows = conn.execute("""
        SELECT t.*,
            GROUP_CONCAT(DISTINCT pa.platform || ':' || pa.username) as accounts,
            MAX(pa.followers) as max_followers
        FROM talent t
        LEFT JOIN platform_accounts pa ON t.id = pa.talent_id
        GROUP BY t.id
        ORDER BY t.name
    """).fetchall()
    conn.close()

    if not rows:
        print("No data to export.")
        return

    fieldnames = list(dict(rows[0]).keys())
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(dict(row))

    print(f"Exported {len(rows)} talent to {filepath}")


def cmd_stats():
    """Show database statistics."""
    stats = get_stats()
    print(f"\n{'='*40}")
    print(f"  TALENT DATABASE STATS")
    print(f"{'='*40}")
    print(f"  Total talent:        {stats['total_talent']}")
    print(f"  Platform accounts:   {stats['total_accounts']}")
    print(f"  Collaborations:      {stats['total_collabs']}")

    if stats["by_category"]:
        print(f"\n  By Category:")
        for cat, count in stats["by_category"].items():
            print(f"    {cat:<20} {count}")

    if stats["by_platform"]:
        print(f"\n  By Platform:")
        for plat, count in stats["by_platform"].items():
            print(f"    {plat:<20} {count}")

    if stats["platform_reach"]:
        print(f"\n  Platform Reach:")
        for p in stats["platform_reach"]:
            total = f"{int(p['total_followers']):,}" if p["total_followers"] else "0"
            avg = f"{int(p['avg_followers']):,}" if p["avg_followers"] else "0"
            top = f"{int(p['top_followers']):,}" if p["top_followers"] else "0"
            print(f"    {p['platform']:<12}  total: {total:<15} avg: {avg:<12} top: {top}")
    print()


def cmd_top(args):
    """Show top talent by followers."""
    platform = None
    limit = 20
    i = 0
    while i < len(args):
        if args[i] == "--platform" and i + 1 < len(args):
            platform = args[i + 1]
            i += 2
        elif args[i] == "--limit" and i + 1 < len(args):
            limit = int(args[i + 1])
            i += 2
        else:
            i += 1

    results = search_talent(platform=platform, order_by="max_followers DESC", limit=limit)
    if not results:
        print("No results.")
        return

    title = f"Top {limit} Talent"
    if platform:
        title += f" on {platform}"
    print(f"\n  {title}")
    print(f"  {'='*70}")
    print(f"  {'#':<4} {'Name':<25} {'Category':<18} {'Followers':<15}")
    print(f"  {'-'*70}")
    for i, t in enumerate(results, 1):
        followers = t.get("max_followers") or 0
        print(f"  {i:<4} {t['name'][:24]:<25} {t['category']:<18} {followers:>12,}")
    print()


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return

    command = args[0]

    if command == "init":
        cmd_init()
    elif command == "add":
        cmd_add()
    elif command == "search":
        cmd_search(args[1:])
    elif command == "show" and len(args) > 1:
        cmd_show(args[1])
    elif command == "import-csv" and len(args) > 1:
        cmd_import_csv(args[1])
    elif command == "export-csv":
        cmd_export_csv(args[1] if len(args) > 1 else None)
    elif command == "stats":
        cmd_stats()
    elif command == "top":
        cmd_top(args[1:])
    elif command == "list-create" and len(args) > 1:
        name = " ".join(args[1:])
        lid = create_list(name)
        print(f"Created list '{name}' (ID: {lid})")
    elif command == "list-add" and len(args) > 2:
        add_to_list(int(args[1]), int(args[2]))
        print("Added to list.")
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
