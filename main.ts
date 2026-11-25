import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const source = join(here, "entry.png");
const target = join(outDir, "entry.png");
if (!existsSync(source)) {
  throw new Error(`entry.png not found next to main.ts: ${source}`);
}
copyFileSync(source, target);
console.log(`wrote ${target}`);

// Post-write read-back verification: re-read the file we just wrote and
// confirm it is byte-for-byte the entry.png shipped in this repository,
// so a silent or partial copy can never pass as a successful run.
import { readFileSync } from "node:fs";
const written = readFileSync(target);
const shipped = readFileSync(source);
if (!written.equals(shipped)) {
  throw new Error(
    `entry.png verification failed: wrote ${written.length} bytes, ` +
      `expected ${shipped.length} bytes from ${source}`,
  );
}
console.log(`verified ${target} (${written.length} bytes, identical to repo entry.png)`);
