'use client'

import Link from 'next/link'
import { useEffect, useState } from 'react'

type HistoryRow = {
  scan_id: string
  target: string
  timestamp: string
  overall_severity: 'info' | 'warning' | 'critical'
  results?: unknown
}

export default function HistoryPage() {
  const [rows, setRows] = useState<HistoryRow[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const loadHistory = async () => {
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/history`)
        const data = await response.json()
        setRows(data.scans ?? [])
      } finally {
        setLoading(false)
      }
    }

    loadHistory()
  }, [])

  const openScan = (row: HistoryRow) => {
    window.sessionStorage.setItem('webguard:lastScan', JSON.stringify(row))
    window.location.href = '/results'
  }

  return (
    <main className="mx-auto max-w-6xl px-6 py-10">
      <div className="mb-8 flex items-end justify-between">
        <div>
          <p className="text-sm font-semibold uppercase tracking-wide text-blue-600">History</p>
          <h1 className="mt-2 text-3xl font-bold text-slate-900">Past scans</h1>
        </div>
        <Link href="/" className="rounded-2xl border border-slate-300 px-5 py-3 font-semibold text-slate-700 transition hover:bg-slate-50">
          New Scan
        </Link>
      </div>

      <div className="overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-soft">
        <table className="min-w-full divide-y divide-slate-200">
          <thead className="bg-slate-50">
            <tr>
              <th className="px-6 py-4 text-left text-sm font-semibold text-slate-600">Target URL</th>
              <th className="px-6 py-4 text-left text-sm font-semibold text-slate-600">Timestamp</th>
              <th className="px-6 py-4 text-left text-sm font-semibold text-slate-600">Overall Severity</th>
              <th className="px-6 py-4 text-left text-sm font-semibold text-slate-600">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {loading ? (
              <tr>
                <td className="px-6 py-8 text-slate-500" colSpan={4}>
                  Loading history...
                </td>
              </tr>
            ) : rows.length ? (
              rows.map((row) => (
                <tr key={row.scan_id}>
                  <td className="px-6 py-4 text-sm font-medium text-slate-900">{row.target}</td>
                  <td className="px-6 py-4 text-sm text-slate-600">{row.timestamp}</td>
                  <td className="px-6 py-4 text-sm capitalize text-slate-700">{row.overall_severity}</td>
                  <td className="px-6 py-4 text-sm">
                    <button onClick={() => openScan(row)} className="rounded-xl bg-blue-600 px-4 py-2 font-semibold text-white hover:bg-blue-700">
                      View
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td className="px-6 py-8 text-slate-500" colSpan={4}>
                  No scans available yet.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </main>
  )
}
