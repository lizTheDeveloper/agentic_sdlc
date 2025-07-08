import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card"
import { getStudentAssignments } from "@/lib/api"
import type { AssignmentSubmission } from "@/types/api"
import AssignmentsTabs from "@/components/assignments-tabs"

const placeholderAssignments: AssignmentSubmission[] = [
  {
    id: 1,
    assignment_id: 1,
    user_id: 1,
    file_url: "",
    submitted_at: new Date(),
    status: "pending",
    grade: null,
    assignment: {
      id: 1,
      lesson_id: 1,
      title: "Intro to FastAPI",
      description: "Web Development",
      due_date: new Date("2025-07-09"),
      max_score: 100,
    },
  },
  {
    id: 2,
    assignment_id: 2,
    user_id: 1,
    file_url: "",
    submitted_at: new Date(),
    status: "graded",
    grade: { id: 1, submission_id: 2, grader_id: 1, score: 92, feedback: "Good work" },
    assignment: {
      id: 2,
      lesson_id: 2,
      title: "Robotics Ethics Essay",
      description: "AI & Robotics",
      due_date: new Date("2025-07-05"),
      max_score: 100,
    },
  },
  {
    id: 3,
    assignment_id: 3,
    user_id: 1,
    file_url: "",
    submitted_at: new Date(),
    status: "submitted",
    grade: null,
    assignment: {
      id: 3,
      lesson_id: 3,
      title: "Data Structures Quiz",
      description: "Core Concepts",
      due_date: new Date("2025-07-02"),
      max_score: 100,
    },
  },
  {
    id: 4,
    assignment_id: 4,
    user_id: 1,
    file_url: "",
    submitted_at: new Date(),
    status: "graded",
    grade: { id: 2, submission_id: 4, grader_id: 1, score: 88, feedback: "Solid effort" },
    assignment: {
      id: 4,
      lesson_id: 4,
      title: "React State Management",
      description: "Web Development",
      due_date: new Date("2025-06-28"),
      max_score: 100,
    },
  },
  {
    id: 5,
    assignment_id: 5,
    user_id: 1,
    file_url: "",
    submitted_at: new Date(),
    status: "pending",
    grade: null,
    assignment: {
      id: 5,
      lesson_id: 5,
      title: "Neural Network Basics",
      description: "AI & Robotics",
      due_date: new Date("2025-07-15"),
      max_score: 100,
    },
  },
]

export default async function AssignmentsPage() {
  // In a real app, user_id would come from the session
  const userId = 1
  let assignments = await getStudentAssignments(userId)

  if (!assignments || assignments.length === 0) {
    assignments = placeholderAssignments
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>My Assignments</CardTitle>
        <CardDescription>Track and manage all your coursework from one place.</CardDescription>
      </CardHeader>
      <CardContent>
        <AssignmentsTabs assignments={assignments} />
      </CardContent>
    </Card>
  )
}
