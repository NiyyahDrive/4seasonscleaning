#!/usr/bin/env node

/**
 * Image Optimization Script for 4 Seasons Website
 */

const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const CONFIG = {
  sourcePath: './assets/images',
  outputPath: './assets/images-optimized',
  imageConfigs: {
    hero: { sizes: [390, 768, 1440], aspect: 16/9, quality: 75, type: 'hero' },
    service: { sizes: [340, 400, 500], aspect: 16/9, quality: 75, type: 'service' },
    team: { sizes: [280, 350], aspect: 3/4, quality: 80, type: 'team' },
    gallery: { sizes: [160, 280, 380], aspect: 4/3, quality: 70, type: 'gallery' },
    default: { sizes: [340, 768, 1440], aspect: 16/9, quality: 75, type: 'default' }
  }
};

const log = (msg, type = 'info') => {
  const colors = {
    info: '\x1b[36m',
    success: '\x1b[32m',
    error: '\x1b[31m',
    warn: '\x1b[33m'
  };
  const reset = '\x1b[0m';
  console.log(`${colors[type] || colors.info}[${type.toUpperCase()}]${reset} ${msg}`);
};

const ensureDir = (dir) => {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
};

const getImageConfig = (filename) => {
  if (filename.includes('Nabil') || filename.includes('team')) return CONFIG.imageConfigs.team;
  if (filename.includes('hero') || filename.includes('banner')) return CONFIG.imageConfigs.hero;
  if (filename.includes('service')) return CONFIG.imageConfigs.service;
  if (filename.includes('WhatsApp') || filename.includes('Zonnepanelen') || 
      filename.includes('Dakgoten') || filename.includes('Gevels')) return CONFIG.imageConfigs.gallery;
  return CONFIG.imageConfigs.default;
};

async function generateVariants(inputPath, filename) {
  const config = getImageConfig(filename);
  const baseName = path.parse(filename).name;
  const variants = [];

  log(`Processing: ${filename}`, 'info');

  try {
    for (const size of config.sizes) {
      const width = size;
      const height = Math.round(width / config.aspect);

      const jpgName = `${baseName}-${width}w.jpg`;
      const jpgPath = path.join(CONFIG.outputPath, jpgName);
      await sharp(inputPath)
        .resize(width, height, { fit: 'cover', position: 'center' })
        .jpeg({ quality: config.quality, progressive: true })
        .toFile(jpgPath);

      const webpName = `${baseName}-${width}w.webp`;
      const webpPath = path.join(CONFIG.outputPath, webpName);
      await sharp(inputPath)
        .resize(width, height, { fit: 'cover', position: 'center' })
        .webp({ quality: config.quality })
        .toFile(webpPath);

      const avifName = `${baseName}-${width}w.avif`;
      const avifPath = path.join(CONFIG.outputPath, avifName);
      await sharp(inputPath)
        .resize(width, height, { fit: 'cover', position: 'center' })
        .avif({ quality: config.quality })
        .toFile(avifPath);

      variants.push({ width, jpg: jpgName, webp: webpName, avif: avifName });
      log(`  ✓ ${width}px (JPG: ${Math.round(fs.statSync(jpgPath).size / 1024)}KB)`, 'success');
    }

    return { filename, baseName, type: config.type, variants };
  } catch (err) {
    log(`Error processing ${filename}: ${err.message}`, 'error');
    return null;
  }
}

async function main() {
  log('🚀 Starting image optimization...', 'info');
  ensureDir(CONFIG.outputPath);

  const files = fs.readdirSync(CONFIG.sourcePath)
    .filter(f => /\.(jpg|jpeg|png|webp)$/i.test(f));

  log(`Found ${files.length} images`, 'info');

  const results = [];
  for (const file of files) {
    const inputPath = path.join(CONFIG.sourcePath, file);
    const result = await generateVariants(inputPath, file);
    if (result) results.push(result);
  }

  const mappingFile = path.join(CONFIG.outputPath, 'image-mapping.json');
  fs.writeFileSync(mappingFile, JSON.stringify(results, null, 2));

  log(`\n📊 OPTIMIZATION COMPLETE!`, 'success');
  log(`Processed: ${results.length} images`, 'success');
  log(`Total variants: ${results.reduce((sum, r) => sum + r.variants.length, 0) * 3}`, 'success');
  log(`Output: ${CONFIG.outputPath}/`, 'success');
}

main().catch(err => {
  log(`Fatal error: ${err.message}`, 'error');
  process.exit(1);
});
