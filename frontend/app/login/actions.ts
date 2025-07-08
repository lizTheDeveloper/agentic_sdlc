"use server"

import { requestAuthCode } from "@/lib/api"

export async function requestMagicLink(prevState: any, formData: FormData) {
  const email = formData.get("email") as string
  if (!email) {
    return { message: "Email is required.", success: false }
  }

  try {
    const response = await requestAuthCode(email)
    // For testing, the code is returned. In prod, it's emailed.
    const message = response.code ? `Magic code sent! For testing, your code is: ${response.code}` : response.message
    if (typeof window !== "undefined") {
      localStorage.setItem("userEmail", email)
    }
    return { message, success: true }
  } catch (error) {
    console.error(error)
    return { message: "Failed to send magic link. Please try again.", success: false }
  }
}
