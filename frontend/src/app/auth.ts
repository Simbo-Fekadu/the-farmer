import { betterAuth } from "better-auth";
// import { mongodbAdapter } from "better-auth/adapters/mongodb";
// import { MongoClient } from "mongodb";

// For now, use memory adapter for testing
import { memoryAdapter } from "better-auth/adapters/memory";

// const client = new MongoClient(process.env.MONGODB_URI || "mongodb://localhost:27017");
// const db = client.db(process.env.MONGODB_DB_NAME || "the_farmer_dev");

export const auth = betterAuth({
  // database: mongodbAdapter(db),
  database: memoryAdapter(),
  emailAndPassword: {
    enabled: true,
  },
  socialProviders: {
    // Add providers if needed, e.g., google, github
  },
  user: {
    additionalFields: {
      role: {
        type: "string",
        required: true,
        defaultValue: "buyer", // default role
        validate: (value: string) => ["farmer", "buyer", "admin"].includes(value),
      },
    },
  },
  baseURL: process.env.BETTER_AUTH_URL || "http://localhost:3000",
  secret: process.env.BETTER_AUTH_SECRET || "your-secret-key",
});