Learning Management System (LMS) Requirements

1. Introduction

1.1 Purpose

The purpose of the LMS is to provide a central platform for managing and delivering educational content at The Multiverse School. It will support dynamic, cohort-based instruction, flexible curriculum publishing from markdown sources, student engagement tracking, and streamlined instructor workflows. The platform is designed to serve both highly technical students and non-technical learners exploring AI, robotics, web development, and related fields. A potential name for the application may be Multiverse LMS or Cosmos Class.

1.2 Scope

Included Features:
	•	Cohort-based class organization
	•	Markdown-based curriculum publishing via Quartz
	•	Assignment submission and grading
	•	Student, instructor, and role management
	•	Scheduling and calendar integration
	•	Notifications and changelogs
	•	Stripe-based payment processing
	•	Jitsi-based video conferencing

Excluded Features (for now):
	•	Dedicated mobile apps (web-responsive only)
	•	Integrated forum/discussion boards (managed outside LMS for now)
	•	Automatic AI grading (future enhancement)

1.3 Target Audience
	•	Internal Stakeholders: Multiverse instructors, administrators, and course designers.
	•	End Users: Students enrolled in technical or non-technical tracks, ranging from AI engineers to low-code creators and self-guided learners.
	•	Technical Implementers: Developers and IT staff building and maintaining the system.

1.4 Definitions and Acronyms
	•	LMS: Learning Management System
	•	Obsidian: Markdown-based note-taking and knowledge management tool
	•	Quartz: Static site generator for publishing Obsidian content
	•	Cohort: A group of students assigned to progress through a class together
	•	Jitsi: Open-source video conferencing platform
	•	Stripe: Online payment processing platform
	•	Markdown: Lightweight markup language used to format curriculum documents
	•	Magic Link: A passwordless authentication method using time-limited email links

1.5 References
	•	The Multiverse School Product Matrix
	•	Curriculum content hosted in Obsidian vaults
	•	Quartz documentation: https://github.com/jackyzha0/quartz
	•	Stripe API docs: https://stripe.com/docs/api
	•	Jitsi Meet API docs: https://jitsi.github.io/handbook/docs/dev-guide/dev-guide-iframe
	•	Quartz theme used: Quartz v4 custom layout

⸻

2. Goals and Objectives

2.1 Business Goals
	•	Reduce instructional overhead by streamlining curriculum and cohort management.
	•	Increase access to high-quality tech education through self-paced and live instruction.
	•	Facilitate scalable and repeatable course deployment across multiple learning tracks.
	•	Support internal revenue generation via Stripe and tier-based access models.

2.2 User Goals
	•	Students: Access curriculum, submit assignments, attend classes, and track progress.
	•	Instructors: Manage cohorts, post assignments, track submissions, and update curriculum.
	•	Admins: Configure class schedules, process payments, and manage user roles and enrollment.

2.3 Success Metrics
	•	Time to onboard a new instructor: < 1 hour
	•	Curriculum update propagation time: < 5 minutes
	•	Student daily active usage: > 70% per cohort
	•	Completion rate per cohort: ≥ 60%
	•	Support ticket resolution time: < 48 hours
	•	Payment success rate: ≥ 98%

⸻

3. User Stories/Use Cases

3.1 User Stories
	•	As a student, I want to see my schedule so that I know when live classes and assignment deadlines are.
	•	As an instructor, I want to assign and grade student submissions so that I can give timely feedback.
	•	As an admin, I want to configure the curriculum and calendar for each cohort so that sessions stay organized.
	•	As a student, I want to log in without a password so that I don’t have to manage login credentials.
	•	As an instructor, I want to view student progress to identify who needs help.

3.2 Use Cases
	•	Use Case 1: Schedule Class
	•	Actor: Instructor
	•	Precondition: Logged in, assigned to a cohort
	•	Flow: Instructor selects lesson → sets date/time → system updates calendar
	•	Postcondition: Students receive a notification with updated calendar
	•	Use Case 2: Submit Assignment
	•	Actor: Student
	•	Precondition: Logged in, assignment assigned
	•	Flow: Student uploads work → clicks submit → system confirms receipt
	•	Postcondition: Assignment appears as “submitted” in dashboard

⸻

4. Functional Requirements

(No changes; already well-structured and comprehensive.)

⸻

5. Non-Functional Requirements
	•	Performance: Page loads must complete within 2 seconds under 95% of expected load.
	•	Security:
	•	No password storage (magic link only)
	•	TLS encryption for all traffic
	•	Role-based access control
	•	Usability: Interfaces must follow accessibility standards (WCAG 2.1 AA).
	•	Reliability: 99.9% uptime guarantee.
	•	Maintainability: All components modular.
	•	Portability: System should run on any Linux server or be deployable on major cloud platforms (e.g., DigitalOcean, AWS).
	•	Error Handling: All errors must be logged with timestamps and retrievable by admin interface.
	•	Internationalization (i18n): All static strings externalized for localization (English-only in v1).
	•	Compliance: Stripe and email integration must follow GDPR where applicable.

⸻

6. Technical Requirements
	•	Frontend: React, Tailwind CSS, and Shadcn UI
	•	Backend: Python FastAPI
	•	Database: PostgreSQL (hosted on Neon.tech)
	•	Hosting: Google Cloud
	•	Content Hosting: Quartz-powered static curriculum site (with Obsidian vault as source)
	•	Authentication: Magic link via Supabase or custom implementation
	•	Video Integration: Jitsi Meet API iframe embed
	•	Payment Integration: Stripe Checkout + Webhooks for enrollment access
	•	APIs: RESTful or GraphQL for internal data exchange
	•	Email Delivery: SendGrid is used for sending magic link authentication codes from the backend. Configure SENDGRID_API_KEY and SENDGRID_FROM_EMAIL in the environment.

⸻

7. Design Considerations
	•	Branding should align with The Multiverse School’s design language: vibrant, clear, inclusive, and purpose-driven.
	•	Ensure curriculum view is readable on small screens.
	•	Navigation should include: Dashboard, Assignments, Calendar, Curriculum, Profile
	•	Reference styles from Quartz theme and Multiverse’s existing class pages

⸻

8. Testing and Quality Assurance
	•	Unit Testing: Required for backend endpoints and UI components.
	•	End-to-End Testing: Automated flows using Puppeteer.
	•	Performance Testing: Baseline load tests simulating 200 concurrent users.
	•	Security Testing: Run OWASP ZAP scans before release.
	•	Acceptance Criteria: Each feature must pass test cases defined in the functional spec.

⸻

9. Deployment and Release
	•	Deployment via GitHub Actions CI/CD to Google Cloud.
	•	Blue-green deployments for backend releases.
	•	Manual approval for production pushes.
	•	Rollback strategy: automated reversion to prior container build

⸻

10. Maintenance and Support
	•	Bug triage weekly
	•	Critical fixes within 24 hours
	•	Monthly content sync check
	•	Admin interface for basic maintenance (resync curriculum, manage users)

⸻

11. Future Considerations (Optional)
	•	AI-based tutoring agents
	•	Peer feedback and review workflows
	•	Curriculum recommendation engine
	•	In-LMS analytics dashboards
	•	Native mobile apps


⸻

12. Stakeholder Responsibilities and Approvals (Optional)
	•	Liz Howard (CEO, Founder): Product Owner, Final Approval
	•	TK: Technical Admin, Implementation Oversight
	•	Chad (GPT): Assistant content support (automated)

⸻

13. Change Management Process (Optional)
	•	All requirement changes submitted via GitHub Issues.
	•	Major scope changes require Liz’s approval.
	•	Versioned document maintained in project repo under /docs.

⸻

Appendix (Optional)
	•	Quartz configuration
	•	Example curriculum structure (Obsidian vault sample)
	•	Dashboard wireframe (pending)
	•	Calendar sync concept (Google Calendar example)

