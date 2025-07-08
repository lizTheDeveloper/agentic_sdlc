"use client"

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Table, TableHeader, TableRow, TableHead, TableBody, TableCell } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import type { AssignmentSubmission } from "@/types/api"

const statusStyles: { [key: string]: string } = {
  pending: "border-yellow-400/50 text-yellow-400",
  submitted: "border-blue-400/50 text-blue-400",
  graded: "border-green-400/50 text-green-400",
}

function getGradeDisplay(submission: AssignmentSubmission) {
  if (submission.status === "graded" && submission.grade) {
    const percentage = (submission.grade.score / submission.assignment.max_score) * 100
    return `${submission.grade.score}/${submission.assignment.max_score} (${percentage.toFixed(0)}%)`
  }
  if (submission.status === "submitted") {
    return "Pending"
  }
  return "N/A"
}

export default function AssignmentsTabs({ assignments }: { assignments: AssignmentSubmission[] }) {
  const renderTable = (filteredAssignments: AssignmentSubmission[]) => (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Assignment</TableHead>
          <TableHead className="hidden sm:table-cell">Course</TableHead>
          <TableHead className="hidden md:table-cell">Due Date</TableHead>
          <TableHead>Status</TableHead>
          <TableHead className="text-right">Grade</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {filteredAssignments.map((submission) => (
          <TableRow key={submission.id}>
            <TableCell className="font-medium">{submission.assignment.title}</TableCell>
            <TableCell className="hidden sm:table-cell">{submission.assignment.description}</TableCell>
            <TableCell className="hidden md:table-cell">
              {new Date(submission.assignment.due_date).toLocaleDateString()}
            </TableCell>
            <TableCell>
              <Badge variant="outline" className={statusStyles[submission.status]}>
                {submission.status.charAt(0).toUpperCase() + submission.status.slice(1)}
              </Badge>
            </TableCell>
            <TableCell className="text-right">{getGradeDisplay(submission)}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )

  return (
    <Tabs defaultValue="all">
      <TabsList>
        <TabsTrigger value="all">All</TabsTrigger>
        <TabsTrigger value="todo">To Do</TabsTrigger>
        <TabsTrigger value="submitted">Submitted</TabsTrigger>
        <TabsTrigger value="graded">Graded</TabsTrigger>
      </TabsList>
      <TabsContent value="all">{renderTable(assignments)}</TabsContent>
      <TabsContent value="todo">{renderTable(assignments.filter((a) => a.status === "pending"))}</TabsContent>
      <TabsContent value="submitted">{renderTable(assignments.filter((a) => a.status === "submitted"))}</TabsContent>
      <TabsContent value="graded">{renderTable(assignments.filter((a) => a.status === "graded"))}</TabsContent>
    </Tabs>
  )
}
