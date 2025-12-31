import { SimpleLayout } from '@/components/SimpleLayout'
import { getAllArticles } from '@/lib/articles'
import { PaginatedArticles } from '@/components/PaginatedArticles'

export const metadata = {
  title: 'Career Articles',
  description:
    'Our comprehensive guides, career-focused articles, and expert advice offer practical insights and strategies to help you achieve your professional goals.',
}

export default async function ArticlesIndex() {
  const folder = 'career/general'
  let allArticles = await getAllArticles(folder)

  return (
    <SimpleLayout
      title="Career Articles"
      intro="Our comprehensive guides, career-focused articles, and expert advice offer practical insights and strategies to help you achieve your professional goals."
    >
      <div className="md:pl-2">
        <PaginatedArticles
          allArticles={allArticles}
          pageSize={10}
          basePath="/career/general"
        />
      </div>
    </SimpleLayout>
  )
}
