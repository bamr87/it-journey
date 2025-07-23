#!/bin/bash
# /script/jupyter-to-markdown.sh
# Define the path to your Jekyll site's _posts directory
POSTS_DIR="/_posts/notebooks"

# Get the current date in the format required by Jekyll
DATE=$(date +"%Y-%m-%d")

# Loop over all .ipynb files in the current directory and its subdirectories
for notebook in $(find . -name "*.ipynb")
do
  # Convert the Jupyter notebook to a markdown file
  jupyter nbconvert --to markdown $notebook

  # Get the name of the markdown file
  md_file="${notebook%.ipynb}.md"

  # Rename the markdown file to match Jekyll's naming convention
  jekyll_md_file="${DATE}-${md_file}"

  # Extract the front matter from the Jupyter notebook
  # front_matter=$(jq -r '.cells[0].source | join("\n")' $notebook)

  # Create a temporary file
  temp_file=$(mktemp)

  # Write the front matter to the temporary file
  # echo "$front_matter" > $temp_file

  # Append the contents of the markdown file to the temporary file
  cat $md_file >> $temp_file

  # Replace the markdown file with the temporary file
  mv $temp_file $jekyll_md_file

  # Move the markdown file to the _posts directory
  mv $jekyll_md_file $POSTS_DIR
done