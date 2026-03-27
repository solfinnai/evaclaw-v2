-- Talent Database Schema
-- A relational database for tracking talent across platforms

-- Core talent profile
CREATE TABLE IF NOT EXISTS talent (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    stage_name TEXT,
    bio TEXT,
    category TEXT NOT NULL,  -- 'model', 'musician', 'cosplayer', 'content_creator', 'multi'
    gender TEXT,
    location_city TEXT,
    location_country TEXT,
    email TEXT,
    website TEXT,
    agency TEXT,
    tags TEXT,               -- comma-separated tags like "streetwear,fitness,gaming"
    notes TEXT,
    discovered_via TEXT,     -- how you found them
    status TEXT DEFAULT 'active',  -- 'active', 'inactive', 'watchlist'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Platform accounts (one talent can have many)
CREATE TABLE IF NOT EXISTS platform_accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    talent_id INTEGER NOT NULL,
    platform TEXT NOT NULL,      -- 'instagram', 'tiktok', 'youtube', 'twitter', 'twitch', 'onlyfans', 'patreon', etc.
    username TEXT NOT NULL,
    profile_url TEXT,
    followers INTEGER,
    following INTEGER,
    posts_count INTEGER,
    engagement_rate REAL,        -- percentage
    verified INTEGER DEFAULT 0,  -- boolean
    last_scraped TIMESTAMP,
    raw_data TEXT,               -- JSON blob for platform-specific data
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (talent_id) REFERENCES talent(id) ON DELETE CASCADE,
    UNIQUE(talent_id, platform, username)
);

-- Follower/engagement snapshots over time
CREATE TABLE IF NOT EXISTS metrics_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    followers INTEGER,
    following INTEGER,
    posts_count INTEGER,
    engagement_rate REAL,
    avg_likes INTEGER,
    avg_comments INTEGER,
    avg_views INTEGER,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES platform_accounts(id) ON DELETE CASCADE
);

-- Collaborations between talent
CREATE TABLE IF NOT EXISTS collaborations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    talent_id_1 INTEGER NOT NULL,
    talent_id_2 INTEGER NOT NULL,
    collab_type TEXT,           -- 'feature', 'photoshoot', 'video', 'event', 'brand_deal'
    description TEXT,
    platform TEXT,
    url TEXT,
    collab_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (talent_id_1) REFERENCES talent(id) ON DELETE CASCADE,
    FOREIGN KEY (talent_id_2) REFERENCES talent(id) ON DELETE CASCADE
);

-- Content pieces worth tracking
CREATE TABLE IF NOT EXISTS content (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    talent_id INTEGER NOT NULL,
    platform TEXT NOT NULL,
    content_type TEXT,          -- 'post', 'reel', 'video', 'story', 'tiktok', 'tweet'
    url TEXT,
    title TEXT,
    description TEXT,
    likes INTEGER,
    comments INTEGER,
    views INTEGER,
    shares INTEGER,
    posted_at TIMESTAMP,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (talent_id) REFERENCES talent(id) ON DELETE CASCADE
);

-- Custom lists / collections
CREATE TABLE IF NOT EXISTS lists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS list_members (
    list_id INTEGER NOT NULL,
    talent_id INTEGER NOT NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (list_id, talent_id),
    FOREIGN KEY (list_id) REFERENCES lists(id) ON DELETE CASCADE,
    FOREIGN KEY (talent_id) REFERENCES talent(id) ON DELETE CASCADE
);

-- Indexes for fast queries
CREATE INDEX IF NOT EXISTS idx_talent_category ON talent(category);
CREATE INDEX IF NOT EXISTS idx_talent_status ON talent(status);
CREATE INDEX IF NOT EXISTS idx_talent_location ON talent(location_country, location_city);
CREATE INDEX IF NOT EXISTS idx_platform_accounts_platform ON platform_accounts(platform);
CREATE INDEX IF NOT EXISTS idx_platform_accounts_talent ON platform_accounts(talent_id);
CREATE INDEX IF NOT EXISTS idx_platform_accounts_followers ON platform_accounts(followers);
CREATE INDEX IF NOT EXISTS idx_metrics_history_account ON metrics_history(account_id, recorded_at);
CREATE INDEX IF NOT EXISTS idx_content_talent ON content(talent_id);
CREATE INDEX IF NOT EXISTS idx_content_platform ON content(platform);
