import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { Table, TableHeader, TableRow, TableHead, TableBody, TableCell } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import Link from "next/link"
import { Calendar, CheckCircle, Clock } from "lucide-react"
import { getStudentAssignments, getEventsForCohort } from "@/lib/api"
import type { AssignmentSubmission, Event } from "@/types/api"

const placeholderEvents: Event[] = [
  {
    id: 1,
    cohort_id: 1,
    title: "Live Class: Advanced React Patterns",
    description: "",
    event_type: "class",
    start_time: new Date("2025-07-07T14:00:00Z"),
    end_time: new Date("2025-07-07T15:00:00Z"),
    location: "",
  },
  {
    id: 2,
    cohort_id: 1,
    title: "Project 1: Portfolio Site Deadline",
    description: "",
    event_type: "deadline",
    start_time: new Date("2025-07-08T23:59:00Z"),
    end_time: new Date("2025-07-08T23:59:00Z"),
    location: "",
  },
  {
    id: 3,
    cohort_id: 1,
    title: "Guest Lecture: AI in Modern Web Dev",
    description: "",
    event_type: "class",
    start_time: new Date("2025-07-10T16:00:00Z"),
    end_time: new Date("2025-07-10T17:00:00Z"),
    location: "",
  },
]

const placeholderAssignments: AssignmentSubmission[] = [
  {
    id: 1,
    assignment_id: 1,
    user_id: 1,
    file_url: "",
    submitted_at: new Date(),
    status: "pending",
    assignment: {
      id: 1,
      lesson_id: 1,
      title: "Intro to FastAPI",
      description: "Web Development Track",
      due_date: new Date(),
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
    assignment: {
      id: 2,
      lesson_id: 2,
      title: "Robotics Ethics Essay",
      description: "AI & Robotics Track",
      due_date: new Date(),
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
    assignment: {
      id: 3,
      lesson_id: 3,
      title: "Data Structures Quiz",
      description: "Core Concepts",
      due_date: new Date(),
      max_score: 100,
    },
  },
]

function getStatusBadge(status: string) {
  switch (status) {
    case "pending":
      return <Badge variant="outline">To Do</Badge>
    case "submitted":
      return <Badge variant="secondary">Submitted</Badge>
    case "graded":
      return <Badge className="bg-green-600/20 text-green-400 hover:bg-green-600/30">Graded</Badge>
    default:
      return <Badge variant="outline">{status}</Badge>
  }
}

export default async function DashboardPage() {
  // In a real app, user_id and cohort_id would come from the session
  const userId = 1
  const cohortId = 1

  const [eventsResult, assignmentsResult] = await Promise.allSettled([
    getEventsForCohort(cohortId),
    getStudentAssignments(userId),
  ])

  const events =
    eventsResult.status === "fulfilled" && eventsResult.value.length > 0 ? eventsResult.value : placeholderEvents
  const assignments =
    assignmentsResult.status === "fulfilled" && assignmentsResult.value.length > 0
      ? assignmentsResult.value
      : placeholderAssignments

  return (
    <div className="grid auto-rows-max items-start gap-4 md:gap-8 lg:col-span-2">
      <div className="grid gap-4 sm:grid-cols-2 md:grid-cols-4 lg:grid-cols-2 xl:grid-cols-4">
        <Card className="sm:col-span-2">
          <CardHeader className="pb-3">
            <CardTitle>Welcome Back, Alex!</CardTitle>
            <CardDescription className="max-w-lg text-balance leading-relaxed">
              Your central hub for everything at Cosmos Class. Jump back into your learning journey.
            </CardDescription>
          </CardHeader>
          <CardFooter>
            <Button>Continue Learning</Button>
          </CardFooter>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardDescription>Overall Progress</CardDescription>
            <CardTitle className="text-4xl">75%</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-xs text-muted-foreground">+2% from last week</div>
          </CardContent>
          <CardFooter>
            <Progress value={75} aria-label="75% complete" />
          </CardFooter>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardDescription>Assignments Due</CardDescription>
            <CardTitle className="text-4xl">3</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-xs text-muted-foreground">1 due today</div>
          </CardContent>
          <CardFooter>
            <Button asChild size="sm" variant="outline">
              <Link href="/assignments">View Assignments</Link>
            </Button>
          </CardFooter>
        </Card>
      </div>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-1 xl:grid-cols-2">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle>Upcoming Events</CardTitle>
            <Calendar className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {events.slice(0, 3).map((event) => (
                <div key={event.id} className="flex items-center">
                  <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary/10 text-primary">
                    {event.event_type === "class" ? <Clock className="h-5 w-5" /> : <CheckCircle className="h-5 w-5" />}
                  </div>
                  <div className="ml-4 space-y-1">
                    <p className="text-sm font-medium leading-none">{event.title}</p>
                    <p className="text-sm text-muted-foreground">
                      {new Date(event.start_time).toLocaleDateString("en-US", { month: "long", day: "numeric" })}
                      {" at "}
                      {new Date(event.start_time).toLocaleTimeString("en-US", { hour: "numeric", minute: "2-digit" })}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Recent Assignments</CardTitle>
            <CardDescription>Here are your most recent assignments. Keep up the great work!</CardDescription>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Assignment</TableHead>
                  <TableHead className="text-right">Status</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {assignments.slice(0, 3).map((submission) => (
                  <TableRow key={submission.id}>
                    <TableCell>
                      <div className="font-medium">{submission.assignment.title}</div>
                      <div className="hidden text-sm text-muted-foreground md:inline">
                        {submission.assignment.description}
                      </div>
                    </TableCell>
                    <TableCell className="text-right">{getStatusBadge(submission.status)}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
