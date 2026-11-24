// Meme Sprint: AI Agents Ship Games — entry program.
//
// Writes the meme image to /output/entry.png and verifies it against the
// competition gate: a whole PNG, exactly 1024x1024 pixels, at most 1 MiB.
import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const SRC = join(dirname(fileURLToPath(import.meta.url)), "entry.png");
const OUT_DIR = process.env.OUTPUT_DIR ?? "/output";
const OUT = join(OUT_DIR, "entry.png");
const MAX_BYTES = 1_048_576;

mkdirSync(OUT_DIR, { recursive: true });
copyFileSync(SRC, OUT);

const buf = readFileSync(OUT);
if (buf.length > MAX_BYTES) {
  throw new Error(`entry.png is ${buf.length} bytes, over the 1 MiB limit`);
}
if (
  buf[0] !== 0x89 || buf[1] !== 0x50 || buf[2] !== 0x4e || buf[3] !== 0x47 ||
  buf[4] !== 0x0d || buf[5] !== 0x0a || buf[6] !== 0x1a || buf[7] !== 0x0a
) {
  throw new Error("entry.png is not a PNG file");
}
const width = buf.readUInt32BE(16);
const height = buf.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  throw new Error(`entry.png is ${width}x${height}, must be 1024x1024`);
}
// A whole PNG ends with a 12-byte IEND chunk (length 0, "IEND", CRC).
const iend = buf.subarray(buf.length - 12);
if (
  iend.readUInt32BE(0) !== 0 ||
  iend.toString("ascii", 4, 8) !== "IEND"
) {
  throw new Error("entry.png is truncated: missing IEND chunk");
}
console.log(`wrote ${OUT} (${buf.length} bytes, ${width}x${height})`);
