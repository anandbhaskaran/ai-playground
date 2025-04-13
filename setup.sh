#!/bin/bash

# Find folders that contain at least one .ipynb file
notebook_dirs=$(find . -type f -name "*.ipynb" -exec dirname {} \; | sort -u)

if [ -z "$notebook_dirs" ]; then
  echo "❌ No Jupyter notebooks found in this repository."
  exit 1
fi

# Display a numbered menu to the user
echo "📒 Select a notebook folder to set up:"
select dir in $notebook_dirs; do
  if [ -n "$dir" ]; then
    echo "✅ Selected folder: $dir"
    cd "$dir" || exit 1
    pwd

    env_name=$(basename "$dir")

    echo "📦 Setting up uv environment in $dir ..."
    uv venv  || { echo "❌ Failed to create venv"; exit 1; }
    uv pip install -r pyproject.toml || { echo "❌ Failed to install dependencies"; exit 1; }

    echo "🐍 Activating virtual environment and registering Jupyter kernel..."
    source .venv/bin/activate
    python -m ipykernel install --user --name "$env_name" --display-name "Python ($env_name)"

    echo "✅ Environment setup complete for $env_name"
    echo "➡️ To activate it, run:"
    echo "cd $dir && source .venv/bin/activate"
    break
  else
    echo "❗ Invalid selection"
  fi
done
