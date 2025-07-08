import os
import pytest
import asyncpg
import asyncio

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "postgresql://localhost/lms_test_db")
os.environ["DATABASE_URL"] = TEST_DATABASE_URL

@pytest.fixture(scope="function")
def client():
    async def reset_and_seed_db():
        # Reset schema
        pool = await asyncpg.create_pool(TEST_DATABASE_URL)
        async with pool.acquire() as conn:
            await conn.execute("""
            DO $$ DECLARE
                r RECORD;
            BEGIN
                FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = current_schema()) LOOP
                    EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
                END LOOP;
            END $$;
            """)
            from app.models import USER_TABLE_DDL
            await conn.execute(USER_TABLE_DDL)
            # Insert test data
            await conn.execute("INSERT INTO roles (id, name) VALUES (1, 'student'), (2, 'instructor'), (3, 'admin') ON CONFLICT DO NOTHING;")
            await conn.execute("INSERT INTO users (id, email, full_name, role_id) VALUES (1, 'student@example.com', 'Student User', 1), (2, 'instructor@example.com', 'Instructor User', 2) ON CONFLICT DO NOTHING;")
            await conn.execute("INSERT INTO curriculum (id, title) VALUES (1, 'Test Curriculum') ON CONFLICT DO NOTHING;")
            await conn.execute("INSERT INTO lessons (id, curriculum_id, title) VALUES (1, 1, 'Test Lesson') ON CONFLICT DO NOTHING;")
            await conn.execute("INSERT INTO assignments (id, lesson_id, title, description, due_date, max_score) VALUES (1, 1, 'Test Assignment', 'Desc', NOW(), 100) ON CONFLICT DO NOTHING;")
            # Debug: check assignments table
            row = await conn.fetchrow("SELECT * FROM assignments WHERE id=1;")
            if not row:
                rows = await conn.fetch("SELECT * FROM assignments;")
                print("Assignments table after insert:", rows)
                raise Exception("Test assignment with id=1 not found after insert!")
        await pool.close()
    asyncio.run(reset_and_seed_db())
    # Import and instantiate the app only after DB is ready
    from app.main import app
    from app.db import db
    asyncio.run(db.disconnect())
    asyncio.run(db.connect())
    from fastapi.testclient import TestClient
    with TestClient(app) as c:
        yield c

def create_test_data():
    # No-op: test data is now set up in the fixture
    pass

def test_healthcheck(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_assignment_submission_and_update(client):
    create_test_data()
    assignment_id = 1
    user_id = 1
    file_url_1 = "https://example.com/file1.pdf"
    file_url_2 = "https://example.com/file2.pdf"

    # Submit assignment
    response = client.post("/submissions", json={
        "assignment_id": assignment_id,
        "user_id": user_id,
        "file_url": file_url_1
    })
    assert response.status_code == 200
    data = response.json()
    assert data["assignment_id"] == assignment_id
    assert data["user_id"] == user_id
    assert data["file_url"] == file_url_1
    assert "submitted_at" in data

    # Submit again (should update file_url)
    response = client.post("/submissions", json={
        "assignment_id": assignment_id,
        "user_id": user_id,
        "file_url": file_url_2
    })
    assert response.status_code == 200
    data = response.json()
    assert data["file_url"] == file_url_2

    # List submissions for assignment
    response = client.get(f"/submissions/{assignment_id}")
    assert response.status_code == 200
    submissions = response.json()
    assert any(s["user_id"] == user_id for s in submissions)

    # List submissions for user
    response = client.get(f"/submissions/user/{user_id}")
    assert response.status_code == 200
    user_submissions = response.json()
    assert any(s["assignment_id"] == assignment_id for s in user_submissions)

def test_grading_and_dashboards(client):
    create_test_data()
    # Create a submission to grade
    submission_payload = {
        "assignment_id": 1,
        "user_id": 1,
        "file_url": "https://example.com/file1.pdf"
    }
    client.post("/submissions", json=submission_payload)
    submission_id = 1
    grader_id = 2
    score = 95
    feedback = "Excellent work!"

    # Grade submission
    response = client.post("/grades", json={
        "submission_id": submission_id,
        "grader_id": grader_id,
        "score": score,
        "feedback": feedback
    }, headers={"X-User-Email": "instructor@example.com"})
    assert response.status_code == 200
    grade = response.json()
    assert grade["submission_id"] == submission_id
    assert grade["grader_id"] == grader_id
    assert grade["score"] == score
    assert grade["feedback"] == feedback
    assert "graded_at" in grade

    # List grades for submission
    response = client.get(f"/grades/{submission_id}")
    assert response.status_code == 200
    grades = response.json()
    assert any(g["grader_id"] == grader_id for g in grades)

    # Instructor dashboard
    instructor_id = grader_id
    response = client.get(f"/instructor/assignments/{instructor_id}", headers={"X-User-Email": "instructor@example.com"})
    assert response.status_code == 200
    assignments = response.json()
    assert isinstance(assignments, list)

    # Student dashboard
    user_id = 1
    response = client.get(f"/student/assignments/{user_id}")
    assert response.status_code == 200
    student_assignments = response.json()
    assert isinstance(student_assignments, list) 