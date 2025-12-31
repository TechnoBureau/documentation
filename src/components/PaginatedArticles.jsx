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
            <div className="flex max-w-4xl flex-col space-y-2">
                {articles.length > 0 ? (
                    articles.map((article) => (
                        <Article key={article.slug} article={article} basePath={basePath} />
                    ))
                ) : (
                    <p className="text-center text-zinc-600 dark:text-zinc-400 pt-8">
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
        <Suspense fallback={<div>Loading articles...</div>}>
            <PaginatedArticlesInner
                allArticles={allArticles}
                pageSize={pageSize}
                basePath={basePath}
            />
        </Suspense>
    )
}
