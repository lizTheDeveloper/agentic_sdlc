"""
Database models and schema DDL for users, roles, and cohorts.
"""

CURRICULUM_TABLE_DDL = """
CREATE TABLE IF NOT EXISTS curriculum (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    cohort_id INTEGER REFERENCES cohorts(id),
    published BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS lessons (
    id SERIAL PRIMARY KEY,
    curriculum_id INTEGER REFERENCES curriculum(id),
    title TEXT NOT NULL,
    content_markdown TEXT,
    order_index INTEGER,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS assignments (
    id SERIAL PRIMARY KEY,
    lesson_id INTEGER REFERENCES lessons(id),
    title TEXT NOT NULL,
    description TEXT,
    due_date TIMESTAMP,
    max_score INTEGER,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
"""

SCHEDULING_TABLE_DDL = """
CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    cohort_id INTEGER REFERENCES cohorts(id),
    title TEXT NOT NULL,
    description TEXT,
    event_type TEXT, -- e.g., 'class', 'deadline', 'meeting'
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    location TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS enrollments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    cohort_id INTEGER REFERENCES cohorts(id),
    enrolled_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, cohort_id)
);
"""

ASSIGNMENT_SUBMISSION_DDL = """
CREATE TABLE IF NOT EXISTS submissions (
    id SERIAL PRIMARY KEY,
    assignment_id INTEGER REFERENCES assignments(id),
    user_id INTEGER REFERENCES users(id),
    file_url TEXT,
    submitted_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(assignment_id, user_id)
);

CREATE TABLE IF NOT EXISTS grades (
    id SERIAL PRIMARY KEY,
    submission_id INTEGER REFERENCES submissions(id),
    grader_id INTEGER REFERENCES users(id),
    score INTEGER,
    feedback TEXT,
    graded_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(submission_id, grader_id)
);
"""

USER_TABLE_DDL = """
CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS cohorts (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT NOT NULL,
    role_id INTEGER REFERENCES roles(id),
    cohort_id INTEGER REFERENCES cohorts(id),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS auth_codes (
    id SERIAL PRIMARY KEY,
    email TEXT NOT NULL,
    code TEXT NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);
""" + CURRICULUM_TABLE_DDL + SCHEDULING_TABLE_DDL + ASSIGNMENT_SUBMISSION_DDL 