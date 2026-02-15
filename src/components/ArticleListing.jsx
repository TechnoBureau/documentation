import Link from 'next/link'
import { formatDate } from '@/lib/formatDate'

export function Article({ article, basePath }) {
    const articleHref = `${basePath}/${article.slug}`
    const parsedDate = new Date(`${article.date}T00:00:00`)
    const month = parsedDate.toLocaleDateString('en-US', { month: 'short' }).toUpperCase()
    const day = parsedDate.toLocaleDateString('en-US', { day: 'numeric' })
    const year = parsedDate.toLocaleDateString('en-US', { year: 'numeric' })

    return (
        <article className="group relative">
            <div className="relative overflow-hidden rounded-3xl border border-zinc-200 bg-zinc-50/70 p-6 shadow-sm ring-1 ring-zinc-900/5 dark:border-zinc-700 dark:bg-zinc-900/70 dark:ring-white/10 sm:p-8">
                <div className="relative z-10 flex flex-col gap-5 sm:flex-row sm:items-start sm:gap-6">
                    <div className="flex items-start sm:shrink-0">
                        <time
                            dateTime={article.date}
                            title={formatDate(article.date)}
                            className="inline-flex w-[4.5rem] flex-col overflow-hidden rounded-2xl border border-zinc-200 bg-white shadow-sm ring-1 ring-zinc-900/5 dark:border-zinc-700 dark:bg-zinc-900 dark:ring-white/10"
                        >
                            <span className="bg-red-500 px-2 py-1 text-center text-[0.62rem] font-bold tracking-[0.08em] text-white">
                                {month}
                            </span>
                            <span className="px-2 pt-2 pb-1 text-center text-2xl font-bold leading-none text-zinc-900 dark:text-zinc-100">
                                {day}
                            </span>
                            <span className="px-2 pb-2 text-center text-[0.62rem] font-semibold tracking-[0.08em] text-zinc-500 dark:text-zinc-400">
                                {year}
                            </span>
                        </time>
                    </div>

                    <div className="min-w-0 flex-1">
                        <h2 className="text-2xl font-semibold tracking-tight text-zinc-900 dark:text-zinc-100">
                            <Link
                                href={articleHref}
                                className="outline-none"
                            >
                                {article.title}
                            </Link>
                        </h2>

                        <p className="mt-4 text-base leading-8 text-zinc-600 dark:text-zinc-400">
                            {article.description}
                        </p>

                        <div className="mt-6">
                            <Link
                                href={articleHref}
                                className="inline-flex items-center gap-1.5 text-base font-semibold text-teal-600 dark:text-teal-400"
                            >
                                Read article
                                <svg
                                    viewBox="0 0 16 16"
                                    fill="none"
                                    aria-hidden="true"
                                    className="h-4 w-4 stroke-current"
                                >
                                    <path
                                        d="M6.75 5.75 9.25 8l-2.5 2.25"
                                        strokeWidth="1.5"
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                    />
                                </svg>
                            </Link>
                        </div>
                    </div>
                </div>
            </div>
        </article>
    )
}
