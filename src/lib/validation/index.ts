import * as z from "zod";

export const SignupValidation = z.object({
    first_name : z.string().min(2, { message: 'First Name must be at least 2 characters.' }),
    last_name : z.string().min(2, { message : 'Last name must be at least 2 characters.' }),
    username: z.string().min(2, { message: 'Username must be at least 2 characters.' }),
    email: z.string().email(),
    password: z.string().min(8, { message: 'Password must be at least 8 characters.' }),
    phone_number: z.string().min(10, { message: 'Phone number must be at least 10 characters.' })
  })
  