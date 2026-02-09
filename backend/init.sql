-- Initialize AutoCV Database
-- This script runs automatically when the PostgreSQL container starts for the first time

-- Drop existing table to recreate with new schema
DROP TABLE IF EXISTS url_submissions CASCADE;

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS vector;

-- Create table for job description submissions
CREATE TABLE IF NOT EXISTS url_submissions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    job_description TEXT NOT NULL,  -- Actual job description text
    role VARCHAR(50),  -- Job role selection
    embedding vector(768),  -- Vector embeddings for semantic search (768 dimensions)
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    processed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Note: TEXT type in PostgreSQL can store up to 1GB of text data

-- Create index on submitted_at for faster queries
CREATE INDEX IF NOT EXISTS idx_url_submissions_submitted_at ON url_submissions(submitted_at DESC);

-- Create vector similarity index for semantic search
CREATE INDEX IF NOT EXISTS idx_url_submissions_embedding ON url_submissions 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Create a trigger to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_url_submissions_updated_at 
    BEFORE UPDATE ON url_submissions 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Insert a test record (optional - you can remove this)
-- INSERT INTO url_submissions (url) VALUES ('https://example.com/test');
