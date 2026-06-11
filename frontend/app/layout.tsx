import type { Metadata } from 'next'
import type { ReactNode } from 'react'
import { Manrope } from 'next/font/google'
import './globals.css'

const manrope = Manrope({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'WebGuard — Web Vulnerability Scanner',
  description: 'Scan web targets for common security issues with WebGuard.',
}

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body className={manrope.className}>{children}</body>
    </html>
  )
}
