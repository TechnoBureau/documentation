"use client"

import { usePathname } from 'next/navigation'
import React from 'react'

export default function Seo({ meta = {} }) {
  const pathname = usePathname() || '/'
  const siteUrl = meta.url || (meta.openGraph && meta.openGraph.url) || 'https://technobureau.com'
  const canonical = (meta.canonical || `${siteUrl.replace(/\/$/, '')}${pathname}`)

  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': meta.type === 'article' || (meta.openGraph && meta.openGraph.type === 'article') ? 'Article' : 'WebPage',
    headline: meta.title || (meta.openGraph && meta.openGraph.title) || undefined,
    description: meta.description || (meta.openGraph && meta.openGraph.description) || undefined,
    url: canonical,
    author: meta.authors ? meta.authors.map((a) => ({ '@type': 'Person', name: a.name || a })) : meta.author ? [{ '@type': 'Person', name: meta.author }] : undefined,
  }

  return (
    <>
      <link rel="canonical" href={canonical} />
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
    </>
  )
}
