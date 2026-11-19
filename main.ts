// THE WORLD — Wednesday, 18 November 2026.
// Copies the committed front-page image to /output/entry.png.
// Deterministic: the output is a byte-for-byte copy of entry.png.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
mkdirSync("/output", { recursive: true });
copyFileSync(join(here, "entry.png"), "/output/entry.png");
console.log("wrote /output/entry.png");
