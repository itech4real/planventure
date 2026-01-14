import './globals.css'
import type { ReactNode } from 'react'

export const metadata = {
  title: 'PlanVenture',
  description: 'Plan your perfect trip',
}

export default function RootLayout({
  children,
}: {
  children: ReactNode
}) {
  return (
    <html lang="en">
      <body className="bg-gray-50">{children}</body>
    </html>
  )
}
