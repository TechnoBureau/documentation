'use client'

import { useSearchParams } from 'next/navigation'
import { Suspense } from 'react'
import { ArticlesPagination } from '@/components/ArticlesPagination'
import { Article } from '@/components/ArticleListing'

function PaginatedArticlesInner({ allArticles, pageSize, basePath }) {
    const searchParams = useSearchParams()
    const currentPage = parseInt(searchParams.get('page') || '1', 10)

    const totalArticles = allArticles.length
    const articles = allArticles.slice(
        (currentPage - 1) * pageSize,
        currentPage * pageSize
    )

    return (
        <>
            <div className="flex w-full max-w-none flex-col gap-6 pb-8 sm:pb-10">
                {articles.length > 0 ? (
                    articles.map((article) => (
                        <Article key={article.slug} article={article} basePath={basePath} />
                    ))
                ) : (
                    <p className="rounded-2xl border border-zinc-200/80 bg-zinc-50/80 p-8 text-center text-zinc-600 dark:border-zinc-700 dark:bg-zinc-800/60 dark:text-zinc-400">
                        No articles found.
                    </p>
                )}
            </div>

            <ArticlesPagination
                totalArticles={totalArticles}
                pageSize={pageSize}
                currentPage={currentPage}
                basePath={basePath}
            />
        </>
    )
}

export function PaginatedArticles({ allArticles, pageSize, basePath }) {
    return (
        <Suspense
            fallback={
                <div className="rounded-2xl border border-zinc-200/80 bg-zinc-50/80 p-8 text-center text-zinc-600 dark:border-zinc-700 dark:bg-zinc-800/60 dark:text-zinc-400">
                    Loading articles...
                </div>
            }
        >
            <PaginatedArticlesInner
                allArticles={allArticles}
                pageSize={pageSize}
                basePath={basePath}
            />
        </Suspense>
    )
}
