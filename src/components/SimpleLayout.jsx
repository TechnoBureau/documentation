import { Container } from '@/components/Container'

export function SimpleLayout({ title, intro, children }) {
  return (
    <Container className="mt-2 sm:mt-2">
      <header className="w-full max-w-none">
        <h1 className="text-4xl font-bold tracking-tight text-zinc-800 sm:text-5xl dark:text-zinc-100">
          {title}
        </h1>
        <p className="mt-2 text-base text-zinc-600 dark:text-zinc-400">
          {intro}
        </p>
      </header>
      {children && <div className="mt-8 sm:mt-4">{children}</div>}
    </Container>
  )
}
