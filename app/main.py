from fastapi import FastAPI, Request, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr
import random, string, datetime
from app.app_logging import app_logger as logger
from app.db import db
from app.models import USER_TABLE_DDL
from typing import List, Optional

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await db.connect()

@app.on_event("shutdown")
async def shutdown_event():
    await db.disconnect()

@app.get("/health")
async def health_check():
    return {"status": "ok"}

class LoginRequest(BaseModel):
    email: EmailStr

class VerifyCodeRequest(BaseModel):
    email: EmailStr
    code: str

def generate_auth_code(length=6):
    return ''.join(random.choices(string.digits, k=length))

@app.post("/auth/request_code")
async def request_login_code(payload: LoginRequest):
    code = generate_auth_code()
    expires_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    async with db.pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO auth_codes (email, code, expires_at)
            VALUES ($1, $2, $3)
            """, payload.email, code, expires_at
        )
        logger.info(f"Auth code generated for {payload.email}")
    # In production, send code via email. For now, return it for testing.
    return {"message": "Auth code sent", "code": code}

@app.post("/auth/verify_code")
async def verify_login_code(payload: VerifyCodeRequest):
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            SELECT * FROM auth_codes WHERE email=$1 AND code=$2 AND used=FALSE AND expires_at > NOW()
            """, payload.email, payload.code
        )
        if not row:
            logger.warning(f"Failed login attempt for {payload.email}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired code.")
        await conn.execute(
            "UPDATE auth_codes SET used=TRUE WHERE id=$1", row["id"]
        )
        logger.info(f"Successful login for {payload.email}")
        # Issue a dummy session token (to be replaced with JWT or session logic)
        return {"message": "Login successful", "email": payload.email}

async def get_user_role(email: str):
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            SELECT r.name FROM users u JOIN roles r ON u.role_id = r.id WHERE u.email = $1
            """, email
        )
        if row:
            return row["name"]
        return None

def role_required(required_role: str):
    async def dependency(request: Request):
        email = request.headers.get("X-User-Email")
        if not email:
            logger.warning("Missing X-User-Email header for role check")
            raise HTTPException(status_code=401, detail="Missing user email header.")
        user_role = await get_user_role(email)
        if user_role != required_role:
            logger.warning(f"Unauthorized access attempt by {email} (role: {user_role}), required: {required_role}")
            raise HTTPException(status_code=403, detail="Insufficient role.")
        logger.info(f"Role check passed for {email} as {user_role}")
    return Depends(dependency)

@app.get("/admin/protected")
async def admin_protected_endpoint(dep=role_required("admin")):
    return {"message": "You have admin access."}

class CurriculumBase(BaseModel):
    title: str
    description: Optional[str] = None
    cohort_id: Optional[int] = None
    published: Optional[bool] = False

class CurriculumCreate(CurriculumBase):
    pass

class CurriculumUpdate(CurriculumBase):
    pass

class CurriculumOut(CurriculumBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

class LessonBase(BaseModel):
    curriculum_id: int
    title: str
    content_markdown: Optional[str] = None
    order_index: Optional[int] = None

class LessonCreate(LessonBase):
    pass

class LessonUpdate(LessonBase):
    pass

class LessonOut(LessonBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

class AssignmentBase(BaseModel):
    lesson_id: int
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime.datetime] = None
    max_score: Optional[int] = None

class AssignmentCreate(AssignmentBase):
    pass

class AssignmentUpdate(AssignmentBase):
    pass

class AssignmentOut(AssignmentBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

# Curriculum Endpoints
@app.post("/curriculum", response_model=CurriculumOut, dependencies=[role_required("admin")])
async def create_curriculum(curriculum: CurriculumCreate):
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO curriculum (title, description, cohort_id, published)
            VALUES ($1, $2, $3, $4)
            RETURNING *
            """,
            curriculum.title, curriculum.description, curriculum.cohort_id, curriculum.published
        )
        logger.info(f"Curriculum created: {row['id']}")
        return dict(row)

@app.get("/curriculum", response_model=List[CurriculumOut])
async def list_curricula():
    async with db.pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM curriculum")
        logger.info("Curriculum list retrieved")
        return [dict(row) for row in rows]

@app.get("/curriculum/{curriculum_id}", response_model=CurriculumOut)
async def get_curriculum(curriculum_id: int):
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM curriculum WHERE id=$1", curriculum_id)
        if not row:
            logger.warning(f"Curriculum not found: {curriculum_id}")
            raise HTTPException(status_code=404, detail="Curriculum not found")
        logger.info(f"Curriculum retrieved: {curriculum_id}")
        return dict(row)

@app.put("/curriculum/{curriculum_id}", response_model=CurriculumOut, dependencies=[role_required("admin")])
async def update_curriculum(curriculum_id: int, curriculum: CurriculumUpdate):
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            UPDATE curriculum SET title=$1, description=$2, cohort_id=$3, published=$4, updated_at=NOW()
            WHERE id=$5 RETURNING *
            """,
            curriculum.title, curriculum.description, curriculum.cohort_id, curriculum.published, curriculum_id
        )
        if not row:
            logger.warning(f"Curriculum not found for update: {curriculum_id}")
            raise HTTPException(status_code=404, detail="Curriculum not found")
        logger.info(f"Curriculum updated: {curriculum_id}")
        return dict(row)

@app.delete("/curriculum/{curriculum_id}", dependencies=[role_required("admin")])
async def delete_curriculum(curriculum_id: int):
    async with db.pool.acquire() as conn:
        result = await conn.execute("DELETE FROM curriculum WHERE id=$1", curriculum_id)
        logger.info(f"Curriculum deleted: {curriculum_id}")
        return {"message": "Curriculum deleted"}

# Lessons Endpoints
@app.post("/lessons", response_model=LessonOut, dependencies=[role_required("admin")])
async def create_lesson(lesson: LessonCreate):
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO lessons (curriculum_id, title, content_markdown, order_index)
            VALUES ($1, $2, $3, $4)
            RETURNING *
            """,
            lesson.curriculum_id, lesson.title, lesson.content_markdown, lesson.order_index
        )
        logger.info(f"Lesson created: {row['id']}")
        return dict(row)

@app.get("/lessons", response_model=List[LessonOut])
async def list_lessons():
    async with db.pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM lessons")
        logger.info("Lessons list retrieved")
        return [dict(row) for row in rows]

@app.get("/lessons/{lesson_id}", response_model=LessonOut)
async def get_lesson(lesson_id: int):
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM lessons WHERE id=$1", lesson_id)
        if not row:
            logger.warning(f"Lesson not found: {lesson_id}")
            raise HTTPException(status_code=404, detail="Lesson not found")
        logger.info(f"Lesson retrieved: {lesson_id}")
        return dict(row)

@app.put("/lessons/{lesson_id}", response_model=LessonOut, dependencies=[role_required("admin")])
async def update_lesson(lesson_id: int, lesson: LessonUpdate):
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            UPDATE lessons SET curriculum_id=$1, title=$2, content_markdown=$3, order_index=$4, updated_at=NOW()
            WHERE id=$5 RETURNING *
            """,
            lesson.curriculum_id, lesson.title, lesson.content_markdown, lesson.order_index, lesson_id
        )
        if not row:
            logger.warning(f"Lesson not found for update: {lesson_id}")
            raise HTTPException(status_code=404, detail="Lesson not found")
        logger.info(f"Lesson updated: {lesson_id}")
        return dict(row)

@app.delete("/lessons/{lesson_id}", dependencies=[role_required("admin")])
async def delete_lesson(lesson_id: int):
    async with db.pool.acquire() as conn:
        result = await conn.execute("DELETE FROM lessons WHERE id=$1", lesson_id)
        logger.info(f"Lesson deleted: {lesson_id}")
        return {"message": "Lesson deleted"}

# Assignments Endpoints
@app.post("/assignments", response_model=AssignmentOut, dependencies=[role_required("admin")])
async def create_assignment(assignment: AssignmentCreate):
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO assignments (lesson_id, title, description, due_date, max_score)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING *
            """,
            assignment.lesson_id, assignment.title, assignment.description, assignment.due_date, assignment.max_score
        )
        logger.info(f"Assignment created: {row['id']}")
        return dict(row)

@app.get("/assignments", response_model=List[AssignmentOut])
async def list_assignments():
    async with db.pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM assignments")
        logger.info("Assignments list retrieved")
        return [dict(row) for row in rows]

@app.get("/assignments/{assignment_id}", response_model=AssignmentOut)
async def get_assignment(assignment_id: int):
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM assignments WHERE id=$1", assignment_id)
        if not row:
            logger.warning(f"Assignment not found: {assignment_id}")
            raise HTTPException(status_code=404, detail="Assignment not found")
        logger.info(f"Assignment retrieved: {assignment_id}")
        return dict(row)

@app.put("/assignments/{assignment_id}", response_model=AssignmentOut, dependencies=[role_required("admin")])
async def update_assignment(assignment_id: int, assignment: AssignmentUpdate):
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            UPDATE assignments SET lesson_id=$1, title=$2, description=$3, due_date=$4, max_score=$5, updated_at=NOW()
            WHERE id=$6 RETURNING *
            """,
            assignment.lesson_id, assignment.title, assignment.description, assignment.due_date, assignment.max_score, assignment_id
        )
        if not row:
            logger.warning(f"Assignment not found for update: {assignment_id}")
            raise HTTPException(status_code=404, detail="Assignment not found")
        logger.info(f"Assignment updated: {assignment_id}")
        return dict(row)

@app.delete("/assignments/{assignment_id}", dependencies=[role_required("admin")])
async def delete_assignment(assignment_id: int):
    async with db.pool.acquire() as conn:
        result = await conn.execute("DELETE FROM assignments WHERE id=$1", assignment_id)
        logger.info(f"Assignment deleted: {assignment_id}")
        return {"message": "Assignment deleted"}

class CohortBase(BaseModel):
    name: str
    start_date: datetime.date
    end_date: datetime.date

class CohortCreate(CohortBase):
    pass

class CohortUpdate(CohortBase):
    pass

class CohortOut(CohortBase):
    id: int

class EnrollmentBase(BaseModel):
    user_id: int
    cohort_id: int

class EnrollmentOut(EnrollmentBase):
    id: int
    enrolled_at: datetime.datetime

class EventBase(BaseModel):
    cohort_id: int
    title: str
    description: Optional[str] = None
    event_type: Optional[str] = None
    start_time: datetime.datetime
    end_time: datetime.datetime
    location: Optional[str] = None

class EventCreate(EventBase):
    pass

class EventUpdate(EventBase):
    pass

class EventOut(EventBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

# Cohort Endpoints
@app.post("/cohorts", response_model=CohortOut, dependencies=[role_required("admin")])
async def create_cohort(cohort: CohortCreate):
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO cohorts (name, start_date, end_date)
            VALUES ($1, $2, $3)
            RETURNING *
            """,
            cohort.name, cohort.start_date, cohort.end_date
        )
        logger.info(f"Cohort created: {row['id']}")
        return dict(row)

@app.get("/cohorts", response_model=List[CohortOut])
async def list_cohorts():
    async with db.pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM cohorts")
        logger.info("Cohort list retrieved")
        return [dict(row) for row in rows]

@app.get("/cohorts/{cohort_id}", response_model=CohortOut)
async def get_cohort(cohort_id: int):
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM cohorts WHERE id=$1", cohort_id)
        if not row:
            logger.warning(f"Cohort not found: {cohort_id}")
            raise HTTPException(status_code=404, detail="Cohort not found")
        logger.info(f"Cohort retrieved: {cohort_id}")
        return dict(row)

@app.put("/cohorts/{cohort_id}", response_model=CohortOut, dependencies=[role_required("admin")])
async def update_cohort(cohort_id: int, cohort: CohortUpdate):
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            UPDATE cohorts SET name=$1, start_date=$2, end_date=$3 WHERE id=$4 RETURNING *
            """,
            cohort.name, cohort.start_date, cohort.end_date, cohort_id
        )
        if not row:
            logger.warning(f"Cohort not found for update: {cohort_id}")
            raise HTTPException(status_code=404, detail="Cohort not found")
        logger.info(f"Cohort updated: {cohort_id}")
        return dict(row)

@app.delete("/cohorts/{cohort_id}", dependencies=[role_required("admin")])
async def delete_cohort(cohort_id: int):
    async with db.pool.acquire() as conn:
        await conn.execute("DELETE FROM cohorts WHERE id=$1", cohort_id)
        logger.info(f"Cohort deleted: {cohort_id}")
        return {"message": "Cohort deleted"}

# Enrollment Endpoints
@app.post("/enrollments", response_model=EnrollmentOut)
async def enroll_user(enrollment: EnrollmentBase):
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO enrollments (user_id, cohort_id)
            VALUES ($1, $2)
            ON CONFLICT (user_id, cohort_id) DO NOTHING
            RETURNING *
            """,
            enrollment.user_id, enrollment.cohort_id
        )
        if not row:
            logger.warning(f"User {enrollment.user_id} already enrolled in cohort {enrollment.cohort_id}")
            raise HTTPException(status_code=409, detail="User already enrolled in cohort")
        logger.info(f"User {enrollment.user_id} enrolled in cohort {enrollment.cohort_id}")
        return dict(row)

@app.get("/enrollments/{cohort_id}", response_model=List[EnrollmentOut])
async def list_enrollments(cohort_id: int):
    async with db.pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM enrollments WHERE cohort_id=$1", cohort_id)
        logger.info(f"Enrollments listed for cohort {cohort_id}")
        return [dict(row) for row in rows]

@app.delete("/enrollments/{enrollment_id}", dependencies=[role_required("admin")])
async def delete_enrollment(enrollment_id: int):
    async with db.pool.acquire() as conn:
        await conn.execute("DELETE FROM enrollments WHERE id=$1", enrollment_id)
        logger.info(f"Enrollment deleted: {enrollment_id}")
        return {"message": "Enrollment deleted"}

# Event Scheduling Endpoints
@app.post("/events", response_model=EventOut, dependencies=[role_required("admin")])
async def create_event(event: EventCreate):
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO events (cohort_id, title, description, event_type, start_time, end_time, location)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            RETURNING *
            """,
            event.cohort_id, event.title, event.description, event.event_type, event.start_time, event.end_time, event.location
        )
        logger.info(f"Event created: {row['id']}")
        return dict(row)

@app.get("/events/{cohort_id}", response_model=List[EventOut])
async def list_events(cohort_id: int):
    async with db.pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM events WHERE cohort_id=$1", cohort_id)
        logger.info(f"Events listed for cohort {cohort_id}")
        return [dict(row) for row in rows]

@app.put("/events/{event_id}", response_model=EventOut, dependencies=[role_required("admin")])
async def update_event(event_id: int, event: EventUpdate):
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            UPDATE events SET cohort_id=$1, title=$2, description=$3, event_type=$4, start_time=$5, end_time=$6, location=$7, updated_at=NOW()
            WHERE id=$8 RETURNING *
            """,
            event.cohort_id, event.title, event.description, event.event_type, event.start_time, event.end_time, event.location, event_id
        )
        if not row:
            logger.warning(f"Event not found for update: {event_id}")
            raise HTTPException(status_code=404, detail="Event not found")
        logger.info(f"Event updated: {event_id}")
        return dict(row)

@app.delete("/events/{event_id}", dependencies=[role_required("admin")])
async def delete_event(event_id: int):
    async with db.pool.acquire() as conn:
        await conn.execute("DELETE FROM events WHERE id=$1", event_id)
        logger.info(f"Event deleted: {event_id}")
        return {"message": "Event deleted"}

class SubmissionBase(BaseModel):
    assignment_id: int
    user_id: int
    file_url: str

class SubmissionCreate(SubmissionBase):
    pass

class SubmissionOut(SubmissionBase):
    id: int
    submitted_at: datetime.datetime

class GradeBase(BaseModel):
    submission_id: int
    grader_id: int
    score: int
    feedback: Optional[str] = None

class GradeCreate(GradeBase):
    pass

class GradeOut(GradeBase):
    id: int
    graded_at: datetime.datetime

# Assignment Submission Endpoints
@app.post("/submissions", response_model=SubmissionOut)
async def submit_assignment(submission: SubmissionCreate):
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO submissions (assignment_id, user_id, file_url)
            VALUES ($1, $2, $3)
            ON CONFLICT (assignment_id, user_id) DO UPDATE SET file_url=EXCLUDED.file_url, submitted_at=NOW()
            RETURNING *
            """,
            submission.assignment_id, submission.user_id, submission.file_url
        )
        logger.info(f"Submission created/updated: {row['id']}")
        return dict(row)

@app.get("/submissions/{assignment_id}", response_model=List[SubmissionOut])
async def list_submissions(assignment_id: int):
    async with db.pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM submissions WHERE assignment_id=$1", assignment_id)
        logger.info(f"Submissions listed for assignment {assignment_id}")
        return [dict(row) for row in rows]

@app.get("/submissions/user/{user_id}", response_model=List[SubmissionOut])
async def list_user_submissions(user_id: int):
    async with db.pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM submissions WHERE user_id=$1", user_id)
        logger.info(f"Submissions listed for user {user_id}")
        return [dict(row) for row in rows]

# Grading Endpoints
@app.post("/grades", response_model=GradeOut, dependencies=[role_required("instructor")])
async def grade_submission(grade: GradeCreate):
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO grades (submission_id, grader_id, score, feedback)
            VALUES ($1, $2, $3, $4)
            ON CONFLICT (submission_id, grader_id) DO UPDATE SET score=EXCLUDED.score, feedback=EXCLUDED.feedback, graded_at=NOW()
            RETURNING *
            """,
            grade.submission_id, grade.grader_id, grade.score, grade.feedback
        )
        logger.info(f"Grade created/updated: {row['id']}")
        return dict(row)

@app.get("/grades/{submission_id}", response_model=List[GradeOut])
async def list_grades(submission_id: int):
    async with db.pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM grades WHERE submission_id=$1", submission_id)
        logger.info(f"Grades listed for submission {submission_id}")
        return [dict(row) for row in rows]

# Instructor Dashboard Endpoint
@app.get("/instructor/assignments/{instructor_id}", response_model=List[SubmissionOut], dependencies=[role_required("instructor")])
async def instructor_assignments(instructor_id: int):
    async with db.pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT s.* FROM submissions s
            JOIN assignments a ON s.assignment_id = a.id
            JOIN curriculum c ON a.curriculum_id = c.id
            JOIN cohorts co ON c.cohort_id = co.id
            JOIN users u ON co.id = u.cohort_id
            WHERE u.id = $1
            """,
            instructor_id
        )
        logger.info(f"Instructor {instructor_id} dashboard assignments listed")
        return [dict(row) for row in rows]

# Student Dashboard Endpoint
@app.get("/student/assignments/{user_id}", response_model=List[SubmissionOut])
async def student_assignments(user_id: int):
    async with db.pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM submissions WHERE user_id=$1", user_id)
        logger.info(f"Student {user_id} dashboard assignments listed")
        return [dict(row) for row in rows] 