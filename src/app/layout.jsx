import glob from 'fast-glob'

import { Providers } from '@/app/providers'
import { Layout } from '@/components/Layout'
import { HeroPattern } from '@/components/HeroPattern'

import '@/styles/tailwind.css'

export const metadata = {
  title: {
    template: '%s - Your Gateway to Tech Excellence',
    default: 'Your Gateway to Tech Excellence',
  },
  siteName: 'TechnoBureau',
  generator: 'TechnoBureau',
  locale: 'en_US',
  type: 'article',
  url: 'https://ganapathichidambaram.github.io',
  description: 'We offers a wealth of information, news, and insights into the ever-evolving world of technology. Whether you are a tech enthusiast, professional, or simply curious about the latest trends, TechnoBureau provides you with a one-stop hub to stay up-to-date and explore the fascinating realm of innovation',
  keywords: "documentation,technical guides,development,programming",
  authors: [{ name: 'Ganapathi Chidambaram', url: 'https://github.com/GanapathiChidambaram' }],
  referrer: 'origin-when-cross-origin',
  creator: 'Ganapathi Chidambaram',
  publisher: 'TechnoBureau',
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  openGraph: {
    url: 'https://ganapathichidambaram.github.io',
    siteName: 'TechnoBureau',
    locale: 'en_US',
    type: 'article',
    authors: ['Ganapathi Chidambaram'],
  },
  twitter: {
    card: 'summary_large_image',
    creator: '@ganapathirj',
  },
  robots: {
    index: true,
    follow: true,
    nocache: false,
    googleBot: {
      index: true,
      follow: true,
      noimageindex: false,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
}

export default async function RootLayout({ children }) {
  let pages = await glob('**/*.mdx', { cwd: 'src/app' })
  let allEntries = await Promise.all(
    pages.map(async (filename) => {
      let route = '/' + filename.replace(/(^|\/)page\.mdx$/, '')
      let mod = await import(`./${filename}`)
      return [route, { sections: mod.sections, metadata: mod.metadata }]
    }),
  )

  let allSections = Object.fromEntries(allEntries.map(([k, v]) => [k, v.sections]))
  let allMetadata = Object.fromEntries(allEntries.map(([k, v]) => [k, v.metadata]))

  return (
    <html lang="en" className="h-full" suppressHydrationWarning>
      <body className="flex min-h-full bg-white antialiased dark:bg-zinc-900">
        <Providers>
          <div className="flex min-h-full w-full flex-col">
            <HeroPattern />
            <Layout allSections={allSections} allMetadata={allMetadata}>
              {children}
            </Layout>
          </div>
        </Providers>
      </body>
    </html>
  )
}
