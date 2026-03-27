"""Data access layer for talent database operations."""
import json
from datetime import datetime
from db import get_connection, dict_from_row


# ─── Talent CRUD ──────────────────────────────────────────────

def add_talent(name, category, stage_name=None, bio=None, gender=None,
               location_city=None, location_country=None, email=None,
               website=None, agency=None, tags=None, notes=None,
               discovered_via=None, status="active"):
    """Add a new talent to the database. Returns the new talent ID."""
    conn = get_connection()
    cursor = conn.execute("""
        INSERT INTO talent (name, stage_name, bio, category, gender,
            location_city, location_country, email, website, agency,
            tags, notes, discovered_via, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, stage_name, bio, category, gender, location_city,
          location_country, email, website, agency, tags, notes,
          discovered_via, status))
    conn.commit()
    talent_id = cursor.lastrowid
    conn.close()
    return talent_id


def get_talent(talent_id):
    """Get a single talent by ID."""
    conn = get_connection()
    row = conn.execute("SELECT * FROM talent WHERE id = ?", (talent_id,)).fetchone()
    conn.close()
    return dict_from_row(row)


def update_talent(talent_id, **kwargs):
    """Update talent fields. Pass only the fields you want to change."""
    if not kwargs:
        return
    kwargs["updated_at"] = datetime.now().isoformat()
    sets = ", ".join(f"{k} = ?" for k in kwargs)
    values = list(kwargs.values()) + [talent_id]
    conn = get_connection()
    conn.execute(f"UPDATE talent SET {sets} WHERE id = ?", values)
    conn.commit()
    conn.close()


def delete_talent(talent_id):
    """Delete a talent and all associated data (cascades)."""
    conn = get_connection()
    conn.execute("DELETE FROM talent WHERE id = ?", (talent_id,))
    conn.commit()
    conn.close()


def search_talent(query=None, category=None, location_country=None,
                  tags=None, status=None, min_followers=None,
                  platform=None, order_by="name", limit=50, offset=0):
    """
    Flexible talent search with filters.
    Returns list of talent dicts with their top platform stats.
    """
    conditions = []
    params = []

    if query:
        conditions.append("(t.name LIKE ? OR t.stage_name LIKE ? OR t.tags LIKE ? OR t.bio LIKE ?)")
        q = f"%{query}%"
        params.extend([q, q, q, q])
    if category:
        conditions.append("t.category = ?")
        params.append(category)
    if location_country:
        conditions.append("t.location_country = ?")
        params.append(location_country)
    if tags:
        for tag in tags.split(","):
            conditions.append("t.tags LIKE ?")
            params.append(f"%{tag.strip()}%")
    if status:
        conditions.append("t.status = ?")
        params.append(status)

    where = "WHERE " + " AND ".join(conditions) if conditions else ""

    # Join with platform_accounts to get max followers
    having = ""
    if min_followers:
        having = f"HAVING max_followers >= {int(min_followers)}"

    if platform:
        platform_filter = "AND pa.platform = ?"
        params.append(platform)
    else:
        platform_filter = ""

    sql = f"""
        SELECT t.*,
               MAX(pa.followers) as max_followers,
               GROUP_CONCAT(DISTINCT pa.platform) as platforms
        FROM talent t
        LEFT JOIN platform_accounts pa ON t.id = pa.talent_id {platform_filter}
        {where}
        GROUP BY t.id
        {having}
        ORDER BY {order_by}
        LIMIT ? OFFSET ?
    """
    params.extend([limit, offset])

    conn = get_connection()
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return [dict_from_row(r) for r in rows]


def list_categories():
    """Get all distinct categories and their counts."""
    conn = get_connection()
    rows = conn.execute("""
        SELECT category, COUNT(*) as count
        FROM talent GROUP BY category ORDER BY count DESC
    """).fetchall()
    conn.close()
    return [dict_from_row(r) for r in rows]


# ─── Platform Accounts ───────────────────────────────────────

def add_platform_account(talent_id, platform, username, profile_url=None,
                         followers=None, following=None, posts_count=None,
                         engagement_rate=None, verified=False, raw_data=None):
    """Add a platform account for a talent."""
    conn = get_connection()
    cursor = conn.execute("""
        INSERT OR REPLACE INTO platform_accounts
            (talent_id, platform, username, profile_url, followers, following,
             posts_count, engagement_rate, verified, raw_data)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (talent_id, platform.lower(), username, profile_url, followers,
          following, posts_count, engagement_rate, int(verified),
          json.dumps(raw_data) if raw_data else None))
    conn.commit()
    account_id = cursor.lastrowid
    conn.close()
    return account_id


def get_talent_accounts(talent_id):
    """Get all platform accounts for a talent."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM platform_accounts WHERE talent_id = ? ORDER BY platform",
        (talent_id,)
    ).fetchall()
    conn.close()
    return [dict_from_row(r) for r in rows]


def update_account_metrics(account_id, followers=None, following=None,
                           posts_count=None, engagement_rate=None):
    """Update an account's metrics and log to history."""
    conn = get_connection()
    updates = {}
    if followers is not None: updates["followers"] = followers
    if following is not None: updates["following"] = following
    if posts_count is not None: updates["posts_count"] = posts_count
    if engagement_rate is not None: updates["engagement_rate"] = engagement_rate

    if updates:
        updates["last_scraped"] = datetime.now().isoformat()
        updates["updated_at"] = datetime.now().isoformat()
        sets = ", ".join(f"{k} = ?" for k in updates)
        values = list(updates.values()) + [account_id]
        conn.execute(f"UPDATE platform_accounts SET {sets} WHERE id = ?", values)

        # Log to history
        conn.execute("""
            INSERT INTO metrics_history (account_id, followers, following,
                posts_count, engagement_rate)
            VALUES (?, ?, ?, ?, ?)
        """, (account_id, followers, following, posts_count, engagement_rate))

    conn.commit()
    conn.close()


# ─── Collaborations ──────────────────────────────────────────

def add_collaboration(talent_id_1, talent_id_2, collab_type=None,
                      description=None, platform=None, url=None, collab_date=None):
    """Record a collaboration between two talent."""
    conn = get_connection()
    cursor = conn.execute("""
        INSERT INTO collaborations (talent_id_1, talent_id_2, collab_type,
            description, platform, url, collab_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (talent_id_1, talent_id_2, collab_type, description, platform,
          url, collab_date))
    conn.commit()
    collab_id = cursor.lastrowid
    conn.close()
    return collab_id


def get_talent_collabs(talent_id):
    """Get all collaborations involving a talent."""
    conn = get_connection()
    rows = conn.execute("""
        SELECT c.*, t1.name as talent_1_name, t2.name as talent_2_name
        FROM collaborations c
        JOIN talent t1 ON c.talent_id_1 = t1.id
        JOIN talent t2 ON c.talent_id_2 = t2.id
        WHERE c.talent_id_1 = ? OR c.talent_id_2 = ?
        ORDER BY c.collab_date DESC
    """, (talent_id, talent_id)).fetchall()
    conn.close()
    return [dict_from_row(r) for r in rows]


# ─── Lists / Collections ─────────────────────────────────────

def create_list(name, description=None):
    """Create a custom list/collection."""
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO lists (name, description) VALUES (?, ?)",
        (name, description))
    conn.commit()
    list_id = cursor.lastrowid
    conn.close()
    return list_id


def add_to_list(list_id, talent_id):
    """Add a talent to a list."""
    conn = get_connection()
    conn.execute(
        "INSERT OR IGNORE INTO list_members (list_id, talent_id) VALUES (?, ?)",
        (list_id, talent_id))
    conn.commit()
    conn.close()


def get_list_members(list_id):
    """Get all talent in a list."""
    conn = get_connection()
    rows = conn.execute("""
        SELECT t.* FROM talent t
        JOIN list_members lm ON t.id = lm.talent_id
        WHERE lm.list_id = ?
        ORDER BY t.name
    """, (list_id,)).fetchall()
    conn.close()
    return [dict_from_row(r) for r in rows]


# ─── Stats / Dashboard ───────────────────────────────────────

def get_stats():
    """Get overall database statistics."""
    conn = get_connection()
    stats = {}
    stats["total_talent"] = conn.execute("SELECT COUNT(*) FROM talent").fetchone()[0]
    stats["total_accounts"] = conn.execute("SELECT COUNT(*) FROM platform_accounts").fetchone()[0]
    stats["total_collabs"] = conn.execute("SELECT COUNT(*) FROM collaborations").fetchone()[0]

    rows = conn.execute("""
        SELECT category, COUNT(*) as count FROM talent
        GROUP BY category ORDER BY count DESC
    """).fetchall()
    stats["by_category"] = {r["category"]: r["count"] for r in rows}

    rows = conn.execute("""
        SELECT platform, COUNT(*) as count FROM platform_accounts
        GROUP BY platform ORDER BY count DESC
    """).fetchall()
    stats["by_platform"] = {r["platform"]: r["count"] for r in rows}

    rows = conn.execute("""
        SELECT platform, SUM(followers) as total_followers,
               AVG(followers) as avg_followers,
               MAX(followers) as top_followers
        FROM platform_accounts
        GROUP BY platform ORDER BY total_followers DESC
    """).fetchall()
    stats["platform_reach"] = [dict_from_row(r) for r in rows]

    conn.close()
    return stats
