"use client"

import React from "react"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Calendar } from "@/components/ui/calendar"
import { Badge } from "@/components/ui/badge"
import { Clock, CheckCircle } from "lucide-react"
import type { Event } from "@/types/api"

interface CalendarViewProps {
  eventsByDate: Record<string, Event[]>
}

export default function CalendarView({ eventsByDate }: CalendarViewProps) {
  const [date, setDate] = React.useState<Date | undefined>(new Date("2025-07-07"))

  const selectedDateString = date ? date.toISOString().split("T")[0] : ""
  const selectedEvents = eventsByDate[selectedDateString] || []

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      <Card className="lg:col-span-2">
        <CardContent className="p-0 flex justify-center">
          <Calendar
            mode="single"
            selected={date}
            onSelect={setDate}
            className="p-4"
            modifiers={{
              event: Object.keys(eventsByDate).map((d) => new Date(d)),
            }}
            modifiersStyles={{
              event: {
                color: "hsl(var(--primary-foreground))",
                backgroundColor: "hsl(var(--primary))",
              },
            }}
          />
        </CardContent>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle>
            Schedule for {date ? date.toLocaleDateString("en-US", { month: "long", day: "numeric" }) : "Select a date"}
          </CardTitle>
        </CardHeader>
        <CardContent>
          {selectedEvents.length > 0 ? (
            <div className="space-y-4">
              {selectedEvents.map((event) => (
                <div key={event.id} className="flex items-start">
                  <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary/10 text-primary mt-1">
                    {event.event_type === "class" ? <Clock className="h-5 w-5" /> : <CheckCircle className="h-5 w-5" />}
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium">{event.title}</p>
                    <p className="text-sm text-muted-foreground">
                      {new Date(event.start_time).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                    </p>
                    <Badge
                      variant="outline"
                      className={`mt-1 ${event.event_type === "class" ? "border-blue-400/50 text-blue-400" : "border-yellow-400/50 text-yellow-400"}`}
                    >
                      {event.event_type === "class" ? "Live Class" : "Deadline"}
                    </Badge>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-sm text-muted-foreground">No events for this day.</p>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
