import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Hedge Fund Agent',
  description: 'AI-powered trading guidance and scenario analysis',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
