'use client'

import type { FormEvent } from 'react'
import { useState } from 'react'
import { useRouter } from 'next/navigation'

type ScanResponse = {
  scan_id: string
  target: string
  timestamp: string
  results: Record<string, unknown>
  overall_severity: 'info' | 'warning' | 'critical'
}

export function ScanForm() {
  const [url, setUrl] = useState('https://example.com')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const router = useRouter()

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setError('')
    setLoading(true)

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/scan`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url }),
      })

      if (!response.ok) {
        throw new Error('Unable to complete scan')
      }

      const data = (await response.json()) as ScanResponse
      window.sessionStorage.setItem('webguard:lastScan', JSON.stringify(data))
      router.push('/results')
    } catch (submitError) {
      setError(submitError instanceof Error ? submitError.message : 'Scan failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-2xl rounded-3xl border border-slate-200 bg-white p-6 shadow-soft">
      <label htmlFor="url" className="mb-2 block text-sm font-medium text-slate-700">
        Enter target URL
      </label>
      <div className="flex flex-col gap-3 sm:flex-row">
        <input
          id="url"
          type="url"
          value={url}
          onChange={(event) => setUrl(event.target.value)}
          placeholder="https://example.com"
          className="flex-1 rounded-2xl border border-slate-300 px-4 py-3 text-slate-900 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
          required
        />
        <button
          type="submit"
          disabled={loading}
          className="inline-flex items-center justify-center rounded-2xl bg-blue-600 px-6 py-3 font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-slate-400"
        >
          {loading ? 'Scanning...' : 'Scan Now'}
        </button>
      </div>
      {error ? <p className="mt-3 text-sm text-red-600">{error}</p> : null}
      {loading ? <p className="mt-3 text-sm text-slate-500">Running checks in parallel...</p> : null}
    </form>
  )
}
