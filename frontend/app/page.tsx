import Link from 'next/link'
import { ScanForm } from '@/components/ScanForm'

export default function HomePage() {
  return (
    <main className="min-h-screen px-6 py-12">
      <div className="mx-auto flex min-h-[calc(100vh-6rem)] max-w-5xl flex-col justify-center">
        <div className="mb-8 max-w-2xl">
          <div className="mb-4 inline-flex rounded-full bg-blue-50 px-4 py-2 text-sm font-semibold text-blue-700 ring-1 ring-blue-100">
            WebGuard — Web Vulnerability Scanner
          </div>
          <h1 className="text-4xl font-bold tracking-tight text-slate-900 sm:text-6xl">Scan a target for security gaps in one clean workflow.</h1>
          <p className="mt-4 text-lg leading-8 text-slate-600">
            WebGuard runs a focused set of checks for ports, SSL, headers, payload reflection, and WHOIS data, then stores every scan for later review.
          </p>
        </div>
        <ScanForm />
        <div className="mt-6 flex gap-4 text-sm font-medium text-slate-600">
          <Link className="text-blue-700 hover:underline" href="/history">
            View history
          </Link>
          <span>•</span>
          <span>FastAPI backend, Next.js frontend, MongoDB storage</span>
        </div>
      </div>
    </main>
  )
}
