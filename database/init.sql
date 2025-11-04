CREATE TABLE IF NOT EXISTS chats (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(100) NOT NULL,
    user_message TEXT NOT NULL,
    bot_response TEXT NOT NULL,
    document_context TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add column if table already exists
ALTER TABLE chats ADD COLUMN IF NOT EXISTS document_context TEXT;

CREATE INDEX IF NOT EXISTS idx_session_id ON chats(session_id);
CREATE INDEX IF NOT EXISTS idx_timestamp ON chats(timestamp);