"use client";

import { createAuthClient } from "better-auth/react";
import { auth } from "./auth";

export const authClient = createAuthClient({
  baseURL: process.env.BETTER_AUTH_URL || "http://localhost:3000",
});

export function AuthProvider({ children }: { children: React.ReactNode }) {
  return <>{children}</>; // Better-Auth handles session management
}