import { SimpleLayout } from '@/components/SimpleLayout'
import { getAllArticles } from '@/lib/articles'
import { PaginatedArticles } from '@/components/PaginatedArticles'

export const metadata = {
  title: 'Kubernetes Tutorials',
  description:
    'Unlock the full potential of container orchestration with our in-depth coverage of Kubernetes. Dive into the intricacies of Kubernetes architecture, deployment strategies, scalability, monitoring, and management techniques.',
}

export default async function ArticlesIndex() {
  const folder = 'kubernetes/deployment'
  let allArticles = await getAllArticles(folder)

  return (
    <SimpleLayout
      title="Kubernetes Tutorials"
      intro="Unlock the full potential of container orchestration with our in-depth coverage of Kubernetes. Dive into the intricacies of Kubernetes architecture, deployment strategies, scalability, monitoring, and management techniques."
    >
      <div className="md:pl-2">
        <PaginatedArticles
          allArticles={allArticles}
          pageSize={10}
          basePath="/kubernetes/deployment"
        />
      </div>
    </SimpleLayout>
  )
}
