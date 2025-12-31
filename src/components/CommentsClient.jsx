"use client"

import dynamic from 'next/dynamic'
import { Suspense } from 'react'

const Giscus = dynamic(() => import('@/components/Giscus'), { ssr: false })

export default function CommentsClient(props) {
  return (
    <Suspense fallback={null}>
      <Giscus {...props} />
    </Suspense>
  )
}
