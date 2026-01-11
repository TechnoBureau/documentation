import { mdxAnnotations } from 'mdx-annotations'
import remarkFrontmatter from 'remark-frontmatter'
import remarkMdxFrontmatter from 'remark-mdx-frontmatter'
import { remarkMapFrontmatterMetadata } from './remark-frontmatter-metadata.mjs'
import { remarkAutoMetadata } from './remark-auto-metadata.mjs'
import remarkGfm from 'remark-gfm'

export const remarkPlugins = [
  mdxAnnotations.remark,
  remarkFrontmatter,
  [remarkMdxFrontmatter, { name: 'frontmatterMetadata' }],
  remarkMapFrontmatterMetadata,
  remarkAutoMetadata,
  remarkGfm,
]
