import fs from 'fs'
import path from 'path'
import { pipeline } from 'stream/promises'
import zlib from 'zlib'
import fg from 'fast-glob'

async function gzipFile(filePath) {
  const gzipPath = `${filePath}.gz`
  await pipeline(fs.createReadStream(filePath), zlib.createGzip({ level: 9 }), fs.createWriteStream(gzipPath))
  console.log('gzipped', path.basename(filePath), '→', path.basename(gzipPath))
}

async function main() {
  const outDir = path.resolve(process.cwd(), 'out')
  const patterns = ['sitemap*.xml', '**/sitemap*.xml']
  const entries = await fg(patterns, { cwd: outDir, absolute: true })
  if (!entries.length) {
    console.warn('No sitemap XML files found in', outDir)
    return
  }
  await Promise.all(entries.map(gzipFile))
}

main().catch((err) => {
  console.error(err)
  process.exitCode = 1
})
