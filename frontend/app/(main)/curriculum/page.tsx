import { Card, CardContent } from "@/components/ui/card"
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"
import { FileText, Video } from "lucide-react"
import { getCurricula, getLessons } from "@/lib/api"
import type { Curriculum, Lesson } from "@/types/api"
import Link from "next/link"
import { cn } from "@/lib/utils"

const placeholderCurricula: Curriculum[] = [
  {
    id: 1,
    title: "Web Development Track",
    description: "",
    cohort_id: 1,
    published: true,
    lessons: [
      { id: 1, curriculum_id: 1, title: "Module 1: Frontend Foundations", content_markdown: "", order_index: 1 },
    ],
  },
]

const placeholderLessons: Lesson[] = [
  { id: 1, curriculum_id: 1, title: "1.1 Intro to React", content_markdown: "...", order_index: 1 },
  { id: 2, curriculum_id: 1, title: "1.2 JSX and Components", content_markdown: "...", order_index: 2 },
  {
    id: 3,
    curriculum_id: 1,
    title: "1.3 State and Props (Video)",
    content_markdown: "...",
    order_index: 3,
    is_video: true,
  },
  { id: 4, curriculum_id: 1, title: "1.4 Component Lifecycle", content_markdown: "...", order_index: 4 },
  { id: 5, curriculum_id: 2, title: "2.1 CSS-in-JS", content_markdown: "...", order_index: 1 },
  { id: 6, curriculum_id: 2, title: "2.2 Tailwind CSS Deep Dive", content_markdown: "...", order_index: 2 },
  { id: 7, curriculum_id: 2, title: "2.3 Building with shadcn/ui", content_markdown: "...", order_index: 3 },
]

const placeholderArticle = {
  title: "1.1 Introduction to React",
  content: `
<p className="text-lg text-muted-foreground">
  Welcome to the first lesson in your web development journey. React is a powerful JavaScript library for
  building user interfaces. Let's dive in.
</p>

<h2>What is React?</h2>
<p>
  React, sometimes referred to as a frontend JavaScript framework, is a JavaScript library created by
  Facebook. React is a tool for building UI components.
</p>

<h2>Key Concepts</h2>
<p>Before we start writing code, let's understand a few core concepts:</p>
<ul>
  <li>
    <strong>Components:</strong> The building blocks of any React app. They are like JavaScript functions
    that return HTML.
  </li>
  <li>
    <strong>JSX (JavaScript XML):</strong> A syntax extension for JavaScript. It allows you to write
    HTML-like code in your JavaScript files.
  </li>
  <li>
    <strong>Props (Properties):</strong> How components talk to each other. They are passed to components
    like function arguments.
  </li>
  <li>
    <strong>State:</strong> Data that a component maintains. When a component's state changes, React
    re-renders the component.
  </li>
</ul>

<h2>Your First Component</h2>
<p>Here's what a simple React component looks like using JSX:</p>
<pre><code>{\`function Welcome(props) {
return <h1>Hello, {props.name}</h1>;
}\`}</code></pre>

<blockquote>
  <p>
    <strong>Note:</strong> This is a simplified example. In a real project, you'd use tools like Next.js or
    Create React App to set up your development environment.
  </p>
</blockquote>

<p>In the next lesson, we'll explore JSX and components in more detail and set up our first project.</p>
`,
}

export default async function CurriculumPage({ searchParams }: { searchParams: { lesson: string } }) {
  const [curriculaResult, lessonsResult] = await Promise.allSettled([getCurricula(), getLessons()])

  const curricula =
    curriculaResult.status === "fulfilled" && curriculaResult.value.length > 0
      ? curriculaResult.value
      : placeholderCurricula
  const allLessons =
    lessonsResult.status === "fulfilled" && lessonsResult.value.length > 0 ? lessonsResult.value : placeholderLessons

  const activeLessonId = searchParams.lesson ? Number.parseInt(searchParams.lesson) : allLessons[0]?.id
  const activeLesson = allLessons.find((l) => l.id === activeLessonId) || allLessons[0]

  // In a real app, you'd fetch the specific lesson content or use a markdown parser
  const article = activeLesson ? { title: activeLesson.title, content: placeholderArticle.content } : placeholderArticle

  return (
    <div className="grid md:grid-cols-[280px_1fr] gap-8">
      <div className="flex flex-col gap-4">
        {curricula.map((curriculum) => (
          <div key={curriculum.id}>
            <h2 className="text-xl font-bold">{curriculum.title}</h2>
            <Accordion type="multiple" defaultValue={[`curriculum-${curriculum.id}`]} className="w-full">
              <AccordionItem value={`curriculum-${curriculum.id}`}>
                <AccordionTrigger>Modules</AccordionTrigger>
                <AccordionContent>
                  <ul className="space-y-2 pl-4">
                    {allLessons
                      .filter((l) => l.curriculum_id === curriculum.id)
                      .map((lesson) => (
                        <li key={lesson.id}>
                          <Link
                            href={`/curriculum?lesson=${lesson.id}`}
                            className={cn(
                              "flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors",
                              activeLessonId === lesson.id && "text-primary font-semibold",
                            )}
                          >
                            {lesson.is_video ? <Video size={16} /> : <FileText size={16} />}
                            {lesson.title}
                          </Link>
                        </li>
                      ))}
                  </ul>
                </AccordionContent>
              </AccordionItem>
            </Accordion>
          </div>
        ))}
      </div>
      <Card>
        <CardContent className="p-6">
          <article
            className="prose prose-invert max-w-none"
            dangerouslySetInnerHTML={{ __html: `<h1>${article.title}</h1>${article.content}` }}
          ></article>
        </CardContent>
      </Card>
    </div>
  )
}
