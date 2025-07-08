This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.

## Backend Integration

This frontend is integrated with the FastAPI backend (see ../app/main.py). To run both together:

1. Start the backend (from the project root):
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
2. Start the frontend (from the frontend directory):
   ```bash
   npm install
   npm run dev
   ```
3. The frontend will make API requests to the backend at `http://localhost:8000` by default. To change this, set the environment variable `NEXT_PUBLIC_API_URL` in a `.env.local` file in the frontend directory.

4. Authentication uses a magic link flow. Enter your email on the login page; the backend will return a code for testing. The frontend stores your email in localStorage and sends it as `X-User-Email` in API requests for role-based access.

5. For production, replace this with a secure session or JWT-based authentication.
