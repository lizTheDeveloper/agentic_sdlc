export interface User {
  id: number
  email: string
  role: "student" | "instructor" | "admin"
}

export interface Cohort {
  id: number
  name: string
  start_date: Date
  end_date: Date
}

export interface Curriculum {
  id: number
  title: string
  description: string
  cohort_id: number
  published: boolean
  lessons?: Lesson[]
}

export interface Lesson {
  id: number
  curriculum_id: number
  title: string
  content_markdown: string
  order_index: number
  is_video?: boolean
}

export interface Assignment {
  id: number
  lesson_id: number
  title: string
  description: string
  due_date: Date
  max_score: number
}

export interface Grade {
  id: number
  submission_id: number
  grader_id: number
  score: number
  feedback: string
}

export interface AssignmentSubmission {
  id: number
  assignment_id: number
  user_id: number
  file_url: string
  submitted_at: Date
  status: "pending" | "submitted" | "graded"
  assignment: Assignment
  grade?: Grade | null
}

export interface Event {
  id: number
  cohort_id: number
  title: string
  description: string
  event_type: "class" | "deadline" | "meeting"
  start_time: Date
  end_time: Date
  location: string
}
