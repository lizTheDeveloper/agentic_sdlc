"use client"

import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Rocket } from "lucide-react"
import Link from "next/link"
import { useFormState, useFormStatus } from "react-dom"
import { requestMagicLink } from "./actions"

function SubmitButton() {
  const { pending } = useFormStatus()
  return (
    <Button className="w-full" type="submit" disabled={pending}>
      {pending ? "Sending..." : "Send Magic Link"}
    </Button>
  )
}

export default function LoginPage() {
  const [state, formAction] = useFormState(requestMagicLink, { message: "", success: false })

  return (
    <div className="flex items-center justify-center min-h-screen bg-background">
      <Card className="w-full max-w-sm">
        <CardHeader className="text-center">
          <div className="flex justify-center items-center mb-4">
            <Rocket className="h-8 w-8 text-primary" />
          </div>
          <CardTitle className="text-2xl">Cosmos Class</CardTitle>
          <CardDescription>Enter your email to receive a magic link to sign in.</CardDescription>
        </CardHeader>
        <form action={formAction}>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input id="email" name="email" type="email" placeholder="alex@example.com" required />
            </div>
            {state.message && (
              <p className={`text-sm ${state.success ? "text-green-500" : "text-red-500"}`}>{state.message}</p>
            )}
          </CardContent>
          <CardFooter className="flex flex-col gap-4">
            <SubmitButton />
            <p className="text-xs text-muted-foreground text-center">
              By signing in, you agree to our Terms of Service.
            </p>
            <Button variant="link" asChild className="mt-4">
              <Link href="/dashboard">Proceed to Dashboard (Demo)</Link>
            </Button>
          </CardFooter>
        </form>
      </Card>
    </div>
  )
}
