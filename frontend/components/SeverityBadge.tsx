type Severity = 'info' | 'warning' | 'critical'

const severityMap: Record<Severity, string> = {
  info: 'bg-blue-50 text-blue-700 ring-blue-200',
  warning: 'bg-amber-50 text-amber-700 ring-amber-200',
  critical: 'bg-red-50 text-red-700 ring-red-200',
}

export function SeverityBadge({ severity }: { severity: Severity }) {
  const label = severity.charAt(0).toUpperCase() + severity.slice(1)
  return <span className={`inline-flex rounded-full px-3 py-1 text-xs font-semibold ring-1 ${severityMap[severity]}`}>{label}</span>
}
