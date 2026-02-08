'use client'

import clsx from 'clsx'
import { motion } from 'framer-motion'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useSidebarStore } from '@/hooks/useSidebarStore'

import { Footer } from '@/components/Footer'
import { Header } from '@/components/Header'
import { Logo } from '@/components/Logo'
import { Navigation } from '@/components/Navigation'
import { SectionProvider } from '@/components/SectionProvider'

export function Layout({ children, allSections }) {
  let pathname = usePathname()
  let { isOpen } = useSidebarStore()

  return (
    <SectionProvider sections={allSections[pathname] ?? []}>
      <div
        className="group relative flex flex-auto flex-col"
        data-sidebar-collapsed={!isOpen ? '' : undefined}
      >
        <Header />

        <aside
          data-nosnippet
          className="fixed bottom-0 left-0 top-14 z-40 w-72 -translate-x-full overflow-y-auto border-r border-zinc-900/10 bg-white px-6 pt-6 pb-8 transition-transform duration-300 ease-in-out lg:not-group-data-sidebar-collapsed:translate-x-0 max-lg:hidden xl:w-80 lg:dark:border-white/10 dark:bg-zinc-900"
        >
          <Navigation />
        </aside>

        <div
          className={clsx(
            'flex flex-auto flex-col transition-all duration-300 ease-in-out',
            'lg:pl-0 lg:not-group-data-sidebar-collapsed:pl-72 xl:not-group-data-sidebar-collapsed:pl-80',
          )}
        >
          <div className="relative flex flex-auto flex-col px-4 pt-14 sm:px-6 lg:px-8">
            <main className="flex-auto">{children}</main>
            <Footer />
          </div>
        </div>
      </div>
    </SectionProvider>
  )
}
