#!/usr/bin/env python3

import re
from pathlib import Path

# Cell-block regex
cell_start = re.compile(r"^:{3,}\s*cell.*$", re.MULTILINE)
cell_end = re.compile(r"^:{3,}\s*$", re.MULTILINE)
code_fence = re.compile(r"``` *\{\.([a-zA-Z0-9_]+)[^}]*\}")

# Cell-output regex
cell_output_start = re.compile(
    r"^\s*:{3,}\s*\{[^}]*\.cell-output[^\}]*\}", re.IGNORECASE
)
cell_output_end = re.compile(r"^\s*:{3,}\s*$")


def on_pre_build(config):

    docs_dir = Path(config["docs_dir"])

    for md_file in docs_dir.rglob("*.md"):
        text = md_file.read_text(encoding="utf-8")

        # remove fenced code blocks. These are supported in qmd but not in mkdocs
        text = cell_start.sub("", text)
        text = cell_end.sub("", text)

        # Convert ``` {.r .cell-code} → ```r
        text = code_fence.sub(lambda m: f"```{m.group(1)}", text)

        # Convert cell-output divs to MkDocs info admonitions
        lines = text.splitlines()
        new_lines = []

        # replace code blocks (:::) with info admonitions and put
        # the output in a text code block so formatting is not
        # interpreted as markdown
        i = 0
        while i < len(lines):

            line = lines[i]

            if cell_output_start.search(line):
                # Start of output → replace with info admonition
                new_lines.append('!!! info "Output"')
                # new_lines.append("    ```text")  # Start code fence
                new_lines.append("    ```")  # Start code fence
                i += 1

                # consume consecutive indented lines as part of output
                while i < len(lines):
                    next_line = lines[i]
                    # stop of the next line is not indented
                    # or if it is another cell-output start
                    if not next_line.startswith(
                        "    "
                    ) and not cell_output_start.search(next_line):
                        break
                    new_lines.append(next_line)
                    i += 1

                # close the code fence
                new_lines.append("    ```")
                continue

            # Not a cell-output start, so just copy the line
            new_lines.append(line)
            i += 1

        # Write cleaned Markdown back
        md_file.write_text("\n".join(new_lines), encoding="utf-8")

    print(
        f"[strip_quarto_cells] Cleaned Quarto cell wrappers and converted outputs in {docs_dir}"
    )
