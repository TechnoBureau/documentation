import { SimpleLayout } from '@/components/SimpleLayout'
import { getAllArticles } from '@/lib/articles'
import { PaginatedArticles } from '@/components/PaginatedArticles'

export const metadata = {
  title: 'Linux Tutorials',
  description:
    'Immerse yourself in the world of Linux, where boundaries are shattered, and limitations are mere illusions. With Linux, every user becomes a pioneer, equipped with an arsenal of customizable tools and a robust foundation that empowers them to create, explore, and push the boundaries of what is possible.',
}

export default async function ArticlesIndex() {
  const folder = 'linux/administration'
  let allArticles = await getAllArticles(folder)

  return (
    <SimpleLayout
      title="Linux Tutorials"
      intro="Immerse yourself in the world of Linux, where boundaries are shattered, and limitations are mere illusions. With Linux, every user becomes a pioneer, equipped with an arsenal of customizable tools and a robust foundation that empowers them to create, explore, and push the boundaries of what is possible."
    >
      <div className="md:pl-2">
        <PaginatedArticles
          allArticles={allArticles}
          pageSize={10}
          basePath="/linux/administration"
        />
      </div>
    </SimpleLayout>
  )
}
