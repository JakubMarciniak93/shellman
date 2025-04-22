#!/usr/bin/env bash
#
# Generate or verify checksums for many files.
# Default algo: sha256.  Other supported: md5, sha1.

source ./lib/utils.sh

show_help() {
  echo "Usage: "
  echo "  shellman checksum_files [options]"
  echo ""
  echo "Description:"
  echo "  Creates *.sha256sum (or md5/sha1) for files, or verifies existing list."
  echo ""
  echo "Options:"
  echo "  --path <dir>        Directory to scan (default .)"
  echo "  --ext <extension>   Only include files with this extension"
  echo "  --algo <sha256|md5|sha1>   Hash algorithm (default sha256)"
  echo "  --out <file>        Output list name (default checksums.<algo>)"
  echo "  --verify            Verify instead of generate (reads --out list)"
  echo "  --help              Show this help message"
  echo ""
  echo "Examples:"
  echo "  shellman checksum_files --ext zip --algo sha256 --out builds.sha256sum"
  echo "  shellman checksum_files --path ./dist --verify --out builds.sha256sum"
}

# ---------- defaults ----------
SCAN_PATH="."
EXT_FILTER=""
ALGO="sha256"
OUT_FILE=""
VERIFY=false
# --------------------------------

while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --help) show_help; exit 0 ;;
    --path) SCAN_PATH="$2"; shift ;;
    --ext)  EXT_FILTER="$2"; shift ;;
    --algo) ALGO="$2"; shift ;;
    --out)  OUT_FILE="$2"; shift ;;
    --verify) VERIFY=true ;;
    -*)
      error "Unknown option: $1"
      show_help; exit 1 ;;
    *)
      error "Unexpected argument: $1"; exit 1 ;;
  esac
  shift
done

[[ ! -d "$SCAN_PATH" ]] && { error "Invalid path: $SCAN_PATH"; exit 1; }

[[ -z "$OUT_FILE" ]] && OUT_FILE="checksums.${ALGO}sum"
HASH_CMD=""
case "$ALGO" in
  sha256) HASH_CMD="sha256sum" ;;
  md5)    HASH_CMD="md5sum" ;;
  sha1)   HASH_CMD="sha1sum" ;;
  *)      error "Unsupported algo $ALGO"; exit 1 ;;
esac
command -v "$HASH_CMD" >/dev/null || { error "$HASH_CMD not installed"; exit 1; }

# ---------- VERIFY MODE ----------
if [[ "$VERIFY" == true ]]; then
  [[ ! -f "$OUT_FILE" ]] && { error "Checksum list $OUT_FILE not found"; exit 1; }
  echo "🔎 Verifying files via $HASH_CMD list $OUT_FILE ..."
  $HASH_CMD -c "$OUT_FILE"
  exit $?
fi

# ---------- GENERATE MODE ----------
FILES=()
while IFS= read -r -d '' f; do
  [[ -n "$EXT_FILTER" && "${f##*.}" != "$EXT_FILTER" ]] && continue
  FILES+=("$f")
done < <(find "$SCAN_PATH" -type f -print0)

[[ ${#FILES[@]} -eq 0 ]] && { warn "No files matched."; exit 0; }

echo "✍️  Writing ${#FILES[@]} checksums to $OUT_FILE ..."
> "$OUT_FILE"
for f in "${FILES[@]}"; do
  $HASH_CMD "$f" >> "$OUT_FILE"
done
info "Done."
