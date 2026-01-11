import { visit } from 'unist-util-visit'

export function remarkMapFrontmatterMetadata() {
    return (tree) => {
        let hasMetadataExport = false
        let frontmatterMetadataNode = null
        let frontmatterMetadataIdentifier = null

        // First pass: Check for existing metadata export and find the frontmatterMetadata identifier
        visit(tree, 'mdxjsEsm', (node) => {
            const program = node.data?.estree
            if (!program || !program.body) return

            for (const statement of program.body) {
                if (
                    statement.type === 'ExportNamedDeclaration' &&
                    statement.declaration?.type === 'VariableDeclaration'
                ) {
                    for (const decl of statement.declaration.declarations) {
                        if (decl.id?.type === 'Identifier') {
                            if (decl.id.name === 'metadata') {
                                hasMetadataExport = true
                            }
                            if (decl.id.name === 'frontmatterMetadata') {
                                frontmatterMetadataNode = node
                                frontmatterMetadataIdentifier = decl.id
                            }
                        }
                    }
                }
            }
        })

        // Second pass: Rename if safe
        if (!hasMetadataExport && frontmatterMetadataIdentifier) {
            frontmatterMetadataIdentifier.name = 'metadata'
            // Sync value string to ensure tools not using ESTree also see the change
            if (frontmatterMetadataNode.value) {
                frontmatterMetadataNode.value = frontmatterMetadataNode.value.replace(
                    /\bfrontmatterMetadata\b/,
                    'metadata'
                )
            }
        }
    }
}
