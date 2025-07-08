import { getEventsForCohort } from "@/lib/api"
import type { Event } from "@/types/api"
import CalendarView from "@/components/calendar-view"

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
  {
    id: 4,
    cohort_id: 1,
    title: "Neural Network Basics Assignment Due",
    description: "",
    event_type: "deadline",
    start_time: new Date("2025-07-15T23:59:00Z"),
    end_time: new Date("2025-07-15T23:59:00Z"),
    location: "",
  },
]

export default async function CalendarPage() {
  // In a real app, cohort_id would come from the session
  const cohortId = 1
  let events = await getEventsForCohort(cohortId)

  if (!events || events.length === 0) {
    events = placeholderEvents
  }

  const eventsByDate = events.reduce(
    (acc, event) => {
      const date = new Date(event.start_time).toISOString().split("T")[0]
      if (!acc[date]) {
        acc[date] = []
      }
      acc[date].push(event)
      return acc
    },
    {} as Record<string, Event[]>,
  )

  return <CalendarView eventsByDate={eventsByDate} />
}
