import os
import subprocess
import re
from pathlib import Path


def convert_latex_to_html(latex_file, output_dir):
    # Convert LaTeX to HTML
    html_file = os.path.splitext(os.path.basename(latex_file))[0] + ".html"
    output_path = os.path.join(output_dir, html_file)
    #
    # NOTE: latexmlc command may be combined to latexml command in the future. See below.
    # https://math.nist.gov/~BMiller/LaTeXML/ussage.html
    subprocess.run(["latexmlc", latex_file, "--destination=" + output_path])

    # Load the converted HTML file
    with open(output_path, "r") as f:
        content = f.read()

    # Add front matter of Hugo
    front_matter = "---\n"
    front_matter += f'title: "{os.path.splitext(os.path.basename(latex_file))[0]}"\n'
    front_matter += (
        "date: "
        + subprocess.check_output(["date", "+%Y-%m-%d"]).decode().strip()
        + "\n"
    )
    front_matter += "---\n\n"

    # Extract the body content
    body_content = re.search("<body>(.*?)</body>", content, re.DOTALL)
    if body_content:
        content = body_content.group(1)

    # Merge front matter and body content
    final_content = front_matter + content

    # Save the final content
    with open(output_path, "w") as f:
        f.write(final_content)


def process_latex_files(src_dir, output_dir):
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith(".tex"):
                latex_file = os.path.join(root, file)
                relative_path = os.path.relpath(latex_file, src_dir)
                output_subdir = os.path.join(output_dir, os.path.dirname(relative_path))

                Path(output_subdir).mkdir(parents=True, exist_ok=True)

                convert_latex_to_html(latex_file, output_subdir)


if __name__ == "__main__":
    src_dir = "src"  # LaTeXファイルのソースディレクトリ
    output_dir = "content"  # 変換後のHTMLファイルの出力ディレクトリ

    process_latex_files(src_dir, output_dir)
