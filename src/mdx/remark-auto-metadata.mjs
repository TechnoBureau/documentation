import { visit } from 'unist-util-visit'
import { toString } from 'mdast-util-to-string'
import * as fs from 'node:fs'
import * as path from 'node:path'

export function remarkAutoMetadata() {
  return (tree, file) => {
    let title = null
    let description = null
    let metadataExportNode = null
    
    // 1. Find Title (H1) and Description (First Paragraph)
    let foundH1 = false
    visit(tree, (node) => {
      if (!title && node.type === 'heading' && node.depth === 1) {
        title = toString(node)
        foundH1 = true
        return 'skip'
      }

      if (foundH1 && !description && node.type === 'paragraph') {
        description = toString(node).slice(0, 160).trim()
        if (description.length === 160) description += '...'
        return 'skip'
      }
      
      // Check ESTree for exports
      if (node.type === 'mdxjsEsm') {
         const program = node.data?.estree
         if (program?.body) {
             for (const statement of program.body) {
                 if (statement.type === 'ExportNamedDeclaration' && statement.declaration?.declarations) {
                     for (const decl of statement.declaration.declarations) {
                         if (decl.id.name === 'metadata' || decl.id.name === 'frontmatterMetadata') {
                             metadataExportNode = node
                         }
                     }
                 }
             }
         }
      }
    })
    
    // Get file dates from file.history or file.path
    let filePath = file.history?.[0] || file.path
    let dateCreated = null
    let dateModified = null
    
    if (filePath && typeof filePath === 'string') {
      // Ensure path is absolute for fs.statSync to avoid issues with different loaders
      if (!path.isAbsolute(filePath)) {
          filePath = path.resolve(process.cwd(), filePath)
      }

      try {
        if (fs.existsSync(filePath)) {
            const stats = fs.statSync(filePath)
            dateCreated = stats.birthtime.toISOString().split('T')[0]
            dateModified = stats.mtime.toISOString().split('T')[0]
        }
      } catch (e) {
        // Silently fail if we can't read file stats
      }
    }
    
    // Use dateModified as the primary 'date' if available, otherwise dateCreated
    const primaryDate = dateModified || dateCreated
    
    if (metadataExportNode) {
        // We need to inject into the ESTree
        const program = metadataExportNode.data?.estree
        if (program?.body) {
            for (const statement of program.body) {
                if (statement.type === 'ExportNamedDeclaration' && statement.declaration?.declarations) {
                     for (const decl of statement.declaration.declarations) {
                        if (decl.id.name === 'metadata' || decl.id.name === 'frontmatterMetadata') {
                            // Handle undefined or null init (empty frontmatter case)
                            if (!decl.init || (decl.init.type === 'Identifier' && decl.init.name === 'undefined')) {
                                decl.init = {
                                    type: 'ObjectExpression',
                                    properties: []
                                }
                            }
                            
                            if (decl.init?.type === 'ObjectExpression') {
                                const properties = decl.init.properties
                                
                                const hasTitle = properties.some(p => (p.key?.name === 'title' || p.key?.value === 'title'))
                                const hasDescription = properties.some(p => (p.key?.name === 'description' || p.key?.value === 'description'))
                                const hasDate = properties.some(p => (p.key?.name === 'date' || p.key?.value === 'date'))
                                const hasDateCreated = properties.some(p => (p.key?.name === 'dateCreated' || p.key?.value === 'dateCreated'))
                                const hasDateModified = properties.some(p => (p.key?.name === 'dateModified' || p.key?.value === 'dateModified'))
                                
                                // Auto-infer title and description
                                if (!hasTitle && title) {
                                    properties.push({
                                        type: 'Property',
                                        key: { type: 'Identifier', name: 'title' },
                                        value: { type: 'Literal', value: title },
                                        kind: 'init'
                                    })
                                }
                                
                                if (!hasDescription && description) {
                                     properties.push({
                                        type: 'Property',
                                        key: { type: 'Identifier', name: 'description' },
                                        value: { type: 'Literal', value: description },
                                        kind: 'init'
                                    })
                                }
                                
                                // Add file dates if available
                                if (!hasDate && primaryDate) {
                                    properties.push({
                                        type: 'Property',
                                        key: { type: 'Identifier', name: 'date' },
                                        value: { type: 'Literal', value: primaryDate },
                                        kind: 'init'
                                    })
                                }

                                if (!hasDateCreated && dateCreated) {
                                    properties.push({
                                        type: 'Property',
                                        key: { type: 'Identifier', name: 'dateCreated' },
                                        value: { type: 'Literal', value: dateCreated },
                                        kind: 'init'
                                    })
                                }
                                
                                if (!hasDateModified && dateModified) {
                                    properties.push({
                                        type: 'Property',
                                        key: { type: 'Identifier', name: 'dateModified' },
                                        value: { type: 'Literal', value: dateModified },
                                        kind: 'init'
                                    })
                                }

                                // Sync value string if possible
                                if (metadataExportNode.value) {
                                    // This is a naive sync, but better than nothing
                                    if (!hasTitle && title && !metadataExportNode.value.includes('title:')) {
                                        metadataExportNode.value = metadataExportNode.value.replace(/}\s*$/, `, title: ${JSON.stringify(title)} }`)
                                    }
                                    if (!hasDescription && description && !metadataExportNode.value.includes('description:')) {
                                        metadataExportNode.value = metadataExportNode.value.replace(/}\s*$/, `, description: ${JSON.stringify(description)} }`)
                                    }
                                    if (!hasDate && primaryDate && !metadataExportNode.value.includes('date:')) {
                                        metadataExportNode.value = metadataExportNode.value.replace(/}\s*$/, `, date: ${JSON.stringify(primaryDate)} }`)
                                    }
                                    // Clean up potential ", }" at start of object
                                    metadataExportNode.value = metadataExportNode.value.replace(/\{\s*,\s*/, '{ ')
                                }
                            }
                        }
                     }
                }
            }
        }
    } else if (title || description || primaryDate) {
         const properties = []
         
         if (title) {
             properties.push({
                 type: 'Property',
                 key: { type: 'Identifier', name: 'title' },
                 value: { type: 'Literal', value: title },
                 kind: 'init'
             })
         }
         
         if (description) {
             properties.push({
                 type: 'Property',
                 key: { type: 'Identifier', name: 'description' },
                 value: { type: 'Literal', value: description },
                 kind: 'init'
             })
         }

         if (primaryDate) {
            properties.push({
                type: 'Property',
                key: { type: 'Identifier', name: 'date' },
                value: { type: 'Literal', value: primaryDate },
                kind: 'init'
            })
         }
         
         if (dateCreated) {
             properties.push({
                 type: 'Property',
                 key: { type: 'Identifier', name: 'dateCreated' },
                 value: { type: 'Literal', value: dateCreated },
                 kind: 'init'
             })
         }
         
         if (dateModified) {
             properties.push({
                 type: 'Property',
                 key: { type: 'Identifier', name: 'dateModified' },
                 value: { type: 'Literal', value: dateModified },
                 kind: 'init'
             })
         }
         
         const valueString = properties.map(p => `${p.key.name}: ${JSON.stringify(p.value.value)}`).join(', ')
         
         tree.children.unshift({
            type: 'mdxjsEsm',
            value: `export const metadata = { ${valueString} }`,
            data: {
                estree: {
                    type: 'Program',
                    sourceType: 'module',
                    body: [
                        {
                            type: 'ExportNamedDeclaration',
                            specifiers: [],
                            source: null,
                            declaration: {
                                type: 'VariableDeclaration',
                                kind: 'const',
                                declarations: [
                                    {
                                        type: 'VariableDeclarator',
                                        id: { type: 'Identifier', name: 'metadata' },
                                        init: {
                                            type: 'ObjectExpression',
                                            properties: properties
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
         })
    }
  }
}
