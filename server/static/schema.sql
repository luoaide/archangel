DROP TABLE IF EXISTS live_feeds;

CREATE TABLE live_feeds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uplink_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN,
    zt_node_id TEXT NOT NULL,
    gcs_mgrs TEXT,
    ip TEXT,
    port TEXT,
    stream_path TEXT
);