import { SeverityBadge } from '@/components/SeverityBadge'

type ResultCardProps = {
  title: string
  severity: 'info' | 'warning' | 'critical'
  items: Array<{ label: string; value: string }>
}

export function ResultCard({ title, severity, items }: ResultCardProps) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-soft transition hover:-translate-y-0.5 hover:shadow-lg">
      <div className="mb-4 flex items-start justify-between gap-4">
        <div>
          <h3 className="text-lg font-semibold text-slate-900">{title}</h3>
          <p className="mt-1 text-sm text-slate-500">Summary of the latest check</p>
        </div>
        <SeverityBadge severity={severity} />
      </div>
      <div className="space-y-3">
        {items.map((item) => (
          <div key={item.label} className="rounded-xl bg-slate-50 px-4 py-3">
            <div className="text-xs font-medium uppercase tracking-wide text-slate-500">{item.label}</div>
            <div className="mt-1 text-sm text-slate-800 break-words">{item.value}</div>
          </div>
        ))}
      </div>
    </div>
  )
}
