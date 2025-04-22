#!/usr/bin/env bash
#
# Remove unwanted / temporary files from a tree.
# Supports dry‑run preview and age filter.

source ./lib/utils.sh

show_help() {
  echo "Usage:"
  echo "  shellman clean_files [options]"
  echo ""
  echo "Description:"
  echo "  Deletes unwanted files (by name, extension or age)."
  echo ""
  echo "Options:"
  echo "  --path <dir>          Directory to scan   (default: .)"
  echo "  --ext <extension>     Delete files with this extension      (*.log)"
  echo "  --name <pattern>      Delete files whose name contains pattern (e.g. ~ or .bak) "
  echo "  --older-than <days>   Delete only files older than N days"
  echo "  --dry-run             Preview: list files but do NOT delete"
  echo "  --confirm             Ask Y/n before deleting each file"
  echo "  --help                Show this help message"
  echo ""
  echo "Examples:"
  echo "  shellman clean_files --ext tmp --older-than 7 --dry-run"
  echo "  shellman clean_files --path ./build --name '~' --confirm"
}

# ---------- defaults ----------
SCAN_PATH="."
EXT_FILTER=""
NAME_FILTER=""
AGE_DAYS=""
DRY_RUN=false
CONFIRM=false
# --------------------------------

while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --help) show_help; exit 0 ;;
    --path) SCAN_PATH="$2";        shift ;;
    --ext)  EXT_FILTER="$2";       shift ;;
    --name) NAME_FILTER="$2";      shift ;;
    --older-than) AGE_DAYS="$2";   shift ;;
    --dry-run) DRY_RUN=true ;;
    --confirm) CONFIRM=true ;;
    -*)
      error "Unknown option: $1"
      show_help; exit 1 ;;
    *)
      error "Unexpected argument: $1"; exit 1 ;;
  esac
  shift
done

# ----- validation -----
[[ ! -d "$SCAN_PATH" ]] && { error "Invalid path: $SCAN_PATH"; exit 1; }
if [[ -z "$EXT_FILTER" && -z "$NAME_FILTER" ]]; then
  error "Need --ext or --name (or both) to know what to delete!"
  exit 1
fi
# -----------------------

# Build find command
FIND_CMD=(find "$SCAN_PATH" -type f)
[[ -n "$EXT_FILTER"  ]] && FIND_CMD+=(-name "*.${EXT_FILTER}")
[[ -n "$NAME_FILTER" ]] && FIND_CMD+=(-name "*${NAME_FILTER}*")
[[ -n "$AGE_DAYS"    ]] && FIND_CMD+=(-mtime +"$AGE_DAYS")

MAPFILE -t CANDIDATES < <("${FIND_CMD[@]}")

if [[ ${#CANDIDATES[@]} -eq 0 ]]; then
  info "No files matched the criteria – nothing to do."
  exit 0
fi

echo "🧹  ${#CANDIDATES[@]} file(s) match the criteria:"
for f in "${CANDIDATES[@]}"; do echo "  $f"; done
echo ""

if [[ "$DRY_RUN" == true ]]; then
  info "Dry‑run mode – nothing deleted."
  exit 0
fi

for FILE in "${CANDIDATES[@]}"; do
  DELETE=true
  if [[ "$CONFIRM" == true ]]; then
    read -rp "Delete $FILE ? (Y/n): " CHOICE
    [[ "$CHOICE" =~ ^[Nn]$ ]] && DELETE=false
  fi
  if [[ "$DELETE" == true ]]; then
    rm -f -- "$FILE" && info "Deleted: $FILE"
  fi
done

info "Clean‑up complete."
