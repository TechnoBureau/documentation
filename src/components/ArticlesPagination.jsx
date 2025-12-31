import {
    Pagination,
    PaginationList,
    PaginationPage,
} from '@/components/pagination'

export function ArticlesPagination({ totalArticles, pageSize, currentPage, basePath }) {
    const totalPages = Math.ceil(totalArticles / pageSize)

    if (totalPages <= 1) {
        return null
    }

    const pages = Array.from({ length: totalPages }, (_, i) => i + 1)

    return (
        <Pagination className="mt-12 justify-center">
            <PaginationList>
                {pages.map((page) => {
                    const href = `${basePath}?page=${page}`
                    const isCurrent = page === currentPage
                    return (
                        <PaginationPage
                            key={page}
                            href={href}
                            current={isCurrent}
                        >
                            {page}
                        </PaginationPage>
                    )
                })}
            </PaginationList>
        </Pagination>
    )
}
