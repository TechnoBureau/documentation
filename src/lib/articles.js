import glob from 'fast-glob'

async function importArticle(articleFilename, folder) {
  let { metadata } = await import(`../app/${folder}/${articleFilename}`)

  return {
    slug: articleFilename.replace(/(\/page)?\.mdx$/, ''),
    ...metadata,
  }
}

export async function getAllArticles(folder) {
  let articleFilenames = await glob('**/page.mdx', {
    cwd: `./src/app/${folder}`,
  })

  let articles = await Promise.all(articleFilenames.map(filename => importArticle(filename, folder)))

  return articles.sort((a, z) => {
    // Primary sort: by date (newest first)
    const dateDiff = +new Date(z.date) - +new Date(a.date)
    if (dateDiff !== 0) return dateDiff

    // Secondary sort: by slug (alphabetical) for stable ordering when dates match
    return a.slug.localeCompare(z.slug)
  })
}