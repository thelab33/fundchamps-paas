# starforge_patch_tailwind_opacity_all.sh

find app/templates -type f \( -name '*.html' -o -name '*.jinja*' \) | while read -r file; do
  # Patch text-, bg-, border-, fill-, stroke-, outline-, ring-, shadow-
  sed -i -E \
    -e 's/(text-[a-zA-Z0-9\-]+)\/([0-9]{2})/\1 opacity-\2/g' \
    -e 's/(bg-[a-zA-Z0-9\-]+)\/([0-9]{2})/\1 opacity-\2/g' \
    -e 's/(border-[a-zA-Z0-9\-]+)\/([0-9]{2})/\1 opacity-\2/g' \
    -e 's/(fill-[a-zA-Z0-9\-]+)\/([0-9]{2})/\1 opacity-\2/g' \
    -e 's/(stroke-[a-zA-Z0-9\-]+)\/([0-9]{2})/\1 opacity-\2/g' \
    -e 's/(outline-[a-zA-Z0-9\-]+)\/([0-9]{2})/\1 opacity-\2/g' \
    -e 's/(ring-[a-zA-Z0-9\-]+)\/([0-9]{2})/\1 opacity-\2/g' \
    -e 's/(shadow-[a-zA-Z0-9\-]+)\/([0-9]{2})/\1 opacity-\2/g' \
    "$file"
done
