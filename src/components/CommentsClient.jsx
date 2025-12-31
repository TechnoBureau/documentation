"use client"

import dynamic from 'next/dynamic'
import { Suspense } from 'react'
import { usePathname } from 'next/navigation'

const Giscus = dynamic(() => import('@/components/Giscus'), { ssr: false })

export default function CommentsClient(props) {
  const pathname = usePathname() || ''
  const depth = pathname.split('/').filter(Boolean).length

  // Only render Giscus for deeper/article-like paths (e.g. /category/subcategory/article)
  if (depth < 3) return null

  return (
    <Suspense fallback={null}>
      <Giscus {...props} />
    </Suspense>
  )
}
