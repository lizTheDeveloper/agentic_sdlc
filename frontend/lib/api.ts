import type { Curriculum, Lesson, AssignmentSubmission, Event } from "@/types/api"

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

async function fetcher<T>(endpoint: string, options?: RequestInit): Promise<T> {
  try {
    // Try to get user email from localStorage/session for demo; fallback to example
    let userEmail = "user@example.com"
    if (typeof window !== "undefined") {
      userEmail = localStorage.getItem("userEmail") || userEmail
    }
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        // TODO: Replace with JWT/session token in production
        "X-User-Email": userEmail,
        ...options?.headers,
      },
    })

    if (!response.ok) {
      console.error(`API error for ${endpoint}: ${response.statusText}`)
      // Return an empty array for list endpoints or throw for single items
      if (endpoint.includes("s/")) return [] as T
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    return response.json()
  } catch (error) {
    console.error(`Failed to fetch from ${endpoint}:`, error)
    // Return empty array for list endpoints to prevent crashes
    if (endpoint.endsWith("s") || endpoint.includes("/user/")) return [] as T
    throw error
  }
}

// --- Auth ---
export const requestAuthCode = (email: string) =>
  fetcher<{ message: string; code?: string }>("/auth/request_code", {
    method: "POST",
    body: JSON.stringify({ email }),
  })

// --- Curriculum & Lessons ---
export const getCurricula = () => fetcher<Curriculum[]>("/curriculum")
export const getLessons = () => fetcher<Lesson[]>("/lessons")

// --- Assignments & Submissions ---
export const getStudentAssignments = (userId: number) =>
  fetcher<AssignmentSubmission[]>(`/student/assignments/${userId}`)

// --- Events ---
export const getEventsForCohort = (cohortId: number) => fetcher<Event[]>(`/events/${cohortId}`)
