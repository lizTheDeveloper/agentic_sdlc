# LMS Backend API Documentation

This document describes the API structure for the backend. It is intended for frontend developers and integrators.

---

## Authentication

### Request Magic Link Code
- **POST** `/auth/request_code`
- **Body:**
  ```json
  { "email": "user@example.com" }
  ```
- **Response:** `{ "message": "Auth code sent", "code": "123456" }`
- **Notes:** In production, the code is emailed. For testing, it is returned in the response.

### Verify Magic Link Code
- **POST** `/auth/verify_code`
- **Body:**
  ```json
  { "email": "user@example.com", "code": "123456" }
  ```
- **Response:** `{ "message": "Login successful", "email": "user@example.com" }`

---

## Health Check
- **GET** `/health`
- **Response:** `{ "status": "ok" }`

---

## Curriculum

### Create Curriculum
- **POST** `/curriculum`
- **Role:** Admin
- **Body:**
  ```json
  { "title": "Course Title", "description": "...", "cohort_id": 1, "published": false }
  ```
- **Response:** Curriculum object

### List Curricula
- **GET** `/curriculum`
- **Response:** List of curriculum objects

### Get Curriculum
- **GET** `/curriculum/{curriculum_id}`
- **Response:** Curriculum object

### Update Curriculum
- **PUT** `/curriculum/{curriculum_id}`
- **Role:** Admin
- **Body:** Same as create
- **Response:** Curriculum object

### Delete Curriculum
- **DELETE** `/curriculum/{curriculum_id}`
- **Role:** Admin
- **Response:** `{ "message": "Curriculum deleted" }`

---

## Lessons

### Create Lesson
- **POST** `/lessons`
- **Role:** Admin
- **Body:**
  ```json
  { "curriculum_id": 1, "title": "Lesson Title", "content_markdown": "...", "order_index": 1 }
  ```
- **Response:** Lesson object

### List Lessons
- **GET** `/lessons`
- **Response:** List of lesson objects

### Get Lesson
- **GET** `/lessons/{lesson_id}`
- **Response:** Lesson object

### Update Lesson
- **PUT** `/lessons/{lesson_id}`
- **Role:** Admin
- **Body:** Same as create
- **Response:** Lesson object

### Delete Lesson
- **DELETE** `/lessons/{lesson_id}`
- **Role:** Admin
- **Response:** `{ "message": "Lesson deleted" }`

---

## Assignments

### Create Assignment
- **POST** `/assignments`
- **Role:** Admin
- **Body:**
  ```json
  { "lesson_id": 1, "title": "Assignment Title", "description": "...", "due_date": "2024-07-01T00:00:00Z", "max_score": 100 }
  ```
- **Response:** Assignment object

### List Assignments
- **GET** `/assignments`
- **Response:** List of assignment objects

### Get Assignment
- **GET** `/assignments/{assignment_id}`
- **Response:** Assignment object

### Update Assignment
- **PUT** `/assignments/{assignment_id}`
- **Role:** Admin
- **Body:** Same as create
- **Response:** Assignment object

### Delete Assignment
- **DELETE** `/assignments/{assignment_id}`
- **Role:** Admin
- **Response:** `{ "message": "Assignment deleted" }`

---

## Cohorts

### Create Cohort
- **POST** `/cohorts`
- **Role:** Admin
- **Body:**
  ```json
  { "name": "Cohort Name", "start_date": "2024-07-01", "end_date": "2024-12-31" }
  ```
- **Response:** Cohort object

### List Cohorts
- **GET** `/cohorts`
- **Response:** List of cohort objects

### Get Cohort
- **GET** `/cohorts/{cohort_id}`
- **Response:** Cohort object

### Update Cohort
- **PUT** `/cohorts/{cohort_id}`
- **Role:** Admin
- **Body:** Same as create
- **Response:** Cohort object

### Delete Cohort
- **DELETE** `/cohorts/{cohort_id}`
- **Role:** Admin
- **Response:** `{ "message": "Cohort deleted" }`

---

## Enrollments

### Enroll User
- **POST** `/enrollments`
- **Body:**
  ```json
  { "user_id": 1, "cohort_id": 1 }
  ```
- **Response:** Enrollment object

### List Enrollments for Cohort
- **GET** `/enrollments/{cohort_id}`
- **Response:** List of enrollment objects

### Delete Enrollment
- **DELETE** `/enrollments/{enrollment_id}`
- **Role:** Admin
- **Response:** `{ "message": "Enrollment deleted" }`

---

## Events (Scheduling)

### Create Event
- **POST** `/events`
- **Role:** Admin
- **Body:**
  ```json
  { "cohort_id": 1, "title": "Event Title", "description": "...", "event_type": "class", "start_time": "2024-07-01T10:00:00Z", "end_time": "2024-07-01T12:00:00Z", "location": "Room 101" }
  ```
- **Response:** Event object

### List Events for Cohort
- **GET** `/events/{cohort_id}`
- **Response:** List of event objects

### Update Event
- **PUT** `/events/{event_id}`
- **Role:** Admin
- **Body:** Same as create
- **Response:** Event object

### Delete Event
- **DELETE** `/events/{event_id}`
- **Role:** Admin
- **Response:** `{ "message": "Event deleted" }`

---

## Assignment Submissions

### Submit Assignment
- **POST** `/submissions`
- **Body:**
  ```json
  { "assignment_id": 1, "user_id": 1, "file_url": "https://..." }
  ```
- **Response:** Submission object

### List Submissions for Assignment
- **GET** `/submissions/{assignment_id}`
- **Response:** List of submission objects

### List Submissions for User
- **GET** `/submissions/user/{user_id}`
- **Response:** List of submission objects

---

## Grading

### Grade Submission
- **POST** `/grades`
- **Role:** Instructor
- **Body:**
  ```json
  { "submission_id": 1, "grader_id": 2, "score": 95, "feedback": "Great job!" }
  ```
- **Response:** Grade object

### List Grades for Submission
- **GET** `/grades/{submission_id}`
- **Response:** List of grade objects

---

## Dashboards

### Instructor Assignments to Grade
- **GET** `/instructor/assignments/{instructor_id}`
- **Role:** Instructor
- **Response:** List of submission objects

### Student Assignment Tracking
- **GET** `/student/assignments/{user_id}`
- **Response:** List of submission objects

---

## Role-Based Access
- Endpoints requiring admin or instructor roles expect the `X-User-Email` header to be set for role verification.
- Most read/list endpoints are open to authenticated users.

---

## Data Models
- All objects returned follow the Pydantic models defined in the backend (see code for full details).
- Timestamps are in ISO 8601 format.

---

For further details, see the backend code or contact the backend team. 