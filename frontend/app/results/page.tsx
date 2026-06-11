'use client'

import Link from 'next/link'
import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { ResultCard } from '@/components/ResultCard'

type ScanData = {
  scan_id: string
  target: string
  timestamp: string
  results: {
    ports: { open_ports: number[]; severity: 'info' | 'warning' | 'critical' }
    ssl: { valid: boolean; expiry_date: string | null; issuer: string; severity: 'info' | 'warning' | 'critical' }
    headers: { missing: string[]; present: string[]; severity: 'info' | 'warning' | 'critical' }
    payloads: { sqli_detected: boolean; xss_detected: boolean; severity: 'info' | 'warning' | 'critical' }
    whois: { registrar: string; creation_date: string | null; severity: 'info' | 'warning' | 'critical' }
  }
  overall_severity: 'info' | 'warning' | 'critical'
}

export default function ResultsPage() {
  const [scan, setScan] = useState<ScanData | null>(null)
  const router = useRouter()

  useEffect(() => {
    const raw = window.sessionStorage.getItem('webguard:lastScan')
    if (raw) {
      setScan(JSON.parse(raw) as ScanData)
    }
  }, [])

  const downloadReport = async () => {
    if (!scan) return
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/report/${scan.scan_id}`)
    if (!response.ok) return
    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `webguard-report-${scan.scan_id}.pdf`
    link.click()
    window.URL.revokeObjectURL(url)
  }

  if (!scan) {
    return (
      <main className="mx-auto flex min-h-screen max-w-3xl items-center justify-center px-6">
        <div className="rounded-3xl border border-slate-200 bg-white p-8 text-center shadow-soft">
          <h1 className="text-2xl font-bold text-slate-900">No scan data found</h1>
          <p className="mt-2 text-slate-600">Run a new scan from the home page or open a saved scan from history.</p>
          <Link className="mt-6 inline-flex rounded-2xl bg-blue-600 px-5 py-3 font-semibold text-white" href="/">
            Go Home
          </Link>
        </div>
      </main>
    )
  }

  return (
    <main className="mx-auto max-w-6xl px-6 py-10">
      <div className="mb-8 flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-sm font-semibold uppercase tracking-wide text-blue-600">Scan Results</p>
          <h1 className="mt-2 text-3xl font-bold text-slate-900">{scan.target}</h1>
          <p className="mt-1 text-slate-500">{scan.timestamp}</p>
        </div>
        <div className="flex gap-3">
          <button onClick={downloadReport} className="rounded-2xl bg-blue-600 px-5 py-3 font-semibold text-white transition hover:bg-blue-700">
            Download PDF Report
          </button>
          <Link href="/history" className="rounded-2xl border border-slate-300 px-5 py-3 font-semibold text-slate-700 transition hover:bg-slate-50">
            View History
          </Link>
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <ResultCard title="Ports" severity={scan.results.ports.severity} items={[{ label: 'Open Ports', value: scan.results.ports.open_ports.length ? scan.results.ports.open_ports.join(', ') : 'No open ports found' }]} />
        <ResultCard title="SSL" severity={scan.results.ssl.severity} items={[{ label: 'Valid Certificate', value: scan.results.ssl.valid ? 'Yes' : 'No' }, { label: 'Expiry Date', value: scan.results.ssl.expiry_date ?? 'Unknown' }, { label: 'Issuer', value: scan.results.ssl.issuer }]} />
        <ResultCard title="Headers" severity={scan.results.headers.severity} items={[{ label: 'Missing', value: scan.results.headers.missing.length ? scan.results.headers.missing.join(', ') : 'None' }, { label: 'Present', value: scan.results.headers.present.length ? scan.results.headers.present.join(', ') : 'None' }]} />
        <ResultCard title="Payloads" severity={scan.results.payloads.severity} items={[{ label: 'SQLi Detected', value: scan.results.payloads.sqli_detected ? 'Yes' : 'No' }, { label: 'XSS Detected', value: scan.results.payloads.xss_detected ? 'Yes' : 'No' }]} />
        <ResultCard title="WHOIS" severity={scan.results.whois.severity} items={[{ label: 'Registrar', value: scan.results.whois.registrar }, { label: 'Creation Date', value: scan.results.whois.creation_date ?? 'Unknown' }]} />
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-soft">
          <h3 className="text-lg font-semibold text-slate-900">Overall Severity</h3>
          <p className="mt-3 text-5xl font-bold text-slate-900">{scan.overall_severity.toUpperCase()}</p>
          <p className="mt-3 text-sm leading-6 text-slate-500">
            Critical issues indicate exposed non-standard ports or detected injection/reflection behavior. Warnings indicate missing headers or an SSL certificate nearing expiry.
          </p>
          <button onClick={() => router.push('/')} className="mt-6 rounded-2xl bg-slate-900 px-5 py-3 font-semibold text-white transition hover:bg-slate-800">
            Start New Scan
          </button>
        </div>
      </div>
    </main>
  )
}
