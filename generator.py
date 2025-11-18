# generator.py

import os
import markdown
import argparse
from jinja2 import Environment, FileSystemLoader

def generate_site(content_dir='content', output_dir='dist', template_dir='templates'):
    """
    Generates a static HTML website from Markdown files.
    """
    print("Starting static site generation...")

    # 1. Setup
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    # Set up Jinja2 template environment
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('base.html')

    # 2. Find all Markdown files in the content directory
    markdown_files = [f for f in os.listdir(content_dir) if f.endswith('.md')]
    if not markdown_files:
        print("No markdown files found in content directory. Exiting.")
        return

    print(f"Found {len(markdown_files)} markdown files to process.")

    # 3. Process each Markdown file
    for md_file in markdown_files:
        # Read the markdown content
        with open(os.path.join(content_dir, md_file), 'r', encoding='utf-8') as f:
            md_content = f.read()

        # Extract title from the first line (e.g., "# My Page Title")
        title = md_content.split('\n', 1)[0].replace('#', '').strip()

        # Convert Markdown to HTML
        html_content = markdown.markdown(md_content)

        # Render the final HTML using the template
        rendered_html = template.render(
            title=title,
            content=html_content
        )

        # Determine the output filename
        base_filename = os.path.splitext(md_file)[0]
        output_filename = os.path.join(output_dir, f"{base_filename}.html")

        # Write the rendered HTML to the output file
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(rendered_html)
        
        print(f"  -> Generated {output_filename}")

    print("\nSite generation complete!")
    print(f"Your static site is ready in the '{output_dir}' directory.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple static site generator.")
    parser.add_argument('--content', default='content', help='Directory containing markdown files.')
    parser.add_argument('--output', default='dist', help='Directory to output the generated HTML files.')
    parser.add_argument('--templates', default='templates', help='Directory containing HTML templates.')
    
    args = parser.parse_args()
    
    generate_site(args.content, args.output, args.templates)