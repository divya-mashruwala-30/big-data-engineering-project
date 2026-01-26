-- Faculty master table
CREATE TABLE IF NOT EXISTS faculty (
    faculty_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    faculty_type TEXT,
    education TEXT,
    bio TEXT,
    specialization_list TEXT,
    research_tags TEXT,
    email TEXT,
    phone TEXT,
    address TEXT,
    address_line TEXT,
    city TEXT,
    state_pincode TEXT,
    country TEXT,
    combined_text TEXT
);

-- Helpful indexes for chatbot/search
CREATE INDEX IF NOT EXISTS idx_faculty_city ON faculty(city);
CREATE INDEX IF NOT EXISTS idx_faculty_type ON faculty(faculty_type);
