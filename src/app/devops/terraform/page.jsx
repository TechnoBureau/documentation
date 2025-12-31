import { SimpleLayout } from '@/components/SimpleLayout'
import { getAllArticles } from '@/lib/articles'
import { PaginatedArticles } from '@/components/PaginatedArticles'

export const metadata = {
  title: 'DevOps Tutorials',
  description:
    'we introduce you to the world of DevOps – a game-changing approach to software development and IT operations.',
}

export default async function ArticlesIndex() {
  const folder = 'devops/terraform'
  let allArticles = await getAllArticles(folder)

  return (
    <SimpleLayout
      title="DevOps Tutorials"
      intro="we introduce you to the world of DevOps – a game-changing approach to software development and IT operations."
    >
      <div className="md:pl-2">
        <PaginatedArticles
          allArticles={allArticles}
          pageSize={10}
          basePath="/devops/terraform"
        />
      </div>
    </SimpleLayout>
  )
}
