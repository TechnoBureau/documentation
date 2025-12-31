"use client"

import { useEffect } from 'react'

export default function Giscus(props) {
  // Read defaults from  env vars (exposed to client by Next.js)
  const defaults = {
    repo: process.env.NEXT_PUBLIC_GISCUS_REPO || 'OWNER/REPO',
    repoId: process.env.NEXT_PUBLIC_GISCUS_REPO_ID || undefined,
    category: process.env.NEXT_PUBLIC_GISCUS_CATEGORY || 'General',
    categoryId: process.env.NEXT_PUBLIC_GISCUS_CATEGORY_ID || undefined,
    mapping: process.env.NEXT_PUBLIC_GISCUS_MAPPING || 'pathname',
    reactionsEnabled:
      process.env.NEXT_PUBLIC_GISCUS_REACTIONS_ENABLED ?? '1',
    emitMetadata: process.env.NEXT_PUBLIC_GISCUS_EMIT_METADATA ?? '0',
    inputPosition: process.env.NEXT_PUBLIC_GISCUS_INPUT_POSITION || 'bottom',
    theme: process.env.NEXT_PUBLIC_GISCUS_THEME || 'light',
    lang: process.env.NEXT_PUBLIC_GISCUS_LANG || 'en',
    crossorigin: 'anonymous',
    id: 'giscus-script',
  }

  const cfg = { ...defaults, ...props }

  useEffect(() => {
    // avoid double-loading
    if (document.getElementById(cfg.id)) return

    const container = document.getElementById('giscus_thread')
    if (!container) return

    const script = document.createElement('script')
    script.src = 'https://giscus.app/client.js'
    script.async = true
    script.crossOrigin = cfg.crossorigin
    script.setAttribute('data-repo', cfg.repo)
    if (cfg.repoId) script.setAttribute('data-repo-id', cfg.repoId)
    script.setAttribute('data-category', cfg.category)
    if (cfg.categoryId) script.setAttribute('data-category-id', cfg.categoryId)
    script.setAttribute('data-mapping', cfg.mapping)
    script.setAttribute('data-reactions-enabled', cfg.reactionsEnabled)
    script.setAttribute('data-emit-metadata', cfg.emitMetadata)
    script.setAttribute('data-input-position', cfg.inputPosition)
    script.setAttribute('data-theme', cfg.theme)
    script.setAttribute('data-lang', cfg.lang)
    script.id = cfg.id

    container.appendChild(script)

    return () => {
      // cleanup script and iframe when unmounting
      const s = document.getElementById(cfg.id)
      if (s) s.remove()
      container.innerHTML = ''
    }
  }, [
    cfg.repo,
    cfg.repoId,
    cfg.category,
    cfg.categoryId,
    cfg.mapping,
    cfg.reactionsEnabled,
    cfg.emitMetadata,
    cfg.inputPosition,
    cfg.theme,
    cfg.lang,
    cfg.crossorigin,
    cfg.id,
  ])

  return <div id="giscus_thread" />
}
