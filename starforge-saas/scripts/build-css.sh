#!/bin/bash

echo "🚀 Building Tailwind CSS → globals.css"
npx tailwindcss -i ./app/static/css/input.css -o ./app/static/css/globals.css --minify

if [ $? -eq 0 ]; then
  echo "✅ Tailwind CSS built successfully!"
else
  echo "❌ Tailwind CSS build failed. Check errors above."
  exit 1
fi
