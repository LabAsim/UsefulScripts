import os
import re
import logging
import parser

# from parser import parse_arguments

logger = logging.getLogger()


def main() -> None:
    args = parser.parse_arguments()
    target_file = args.file
    headers = r"""
---
header-includes:
  - \usepackage{enumitem}
  - \setlistdepth{20}
  - \renewlist{itemize}{itemize}{20}
  - \renewlist{enumerate}{enumerate}{20}
  - \setlist[itemize]{label=$\cdot$}
  - \setlist[itemize,1]{label=\textbullet}
  - \setlist[itemize,2]{label=--}
  - \setlist[itemize,3]{label=*}
output:
  rmarkdown::pdf_document:
      keep_tex: yes
---
\newcommand*\boldborderline[1]{\par\noindent\raisebox{.8ex}{\makebox[\linewidth]{\hrulefill\hspace{1ex}\raisebox{-.8ex}{\textbf{#1}}\hspace{1ex}\hrulefill}}}
            """
    # See the command here: https://tex.stackexchange.com/a/15122
    with open(target_file, 'r+', encoding="utf-8") as f:
        content = f.read()
        f.seek(0, 0)
        f.write(headers.strip('\r\n') + '\n' + content)

    new_content = ""
    with open(target_file, "r+", encoding="utf-8") as file:
        # re.sub needs bytes
        content = bytes(file.read(), encoding="utf-8")
        pattern = b"\$\$"
        repl_pattern = b"$"
        new_content = re.sub(pattern=pattern, repl=repl_pattern, string=content)
        # Replace {c:c:c} with {rrr}
        # {c:c:c:c}

        # pattern = re.compile(pattern=b"[\:]*c[\:]*c[\W]")
        # new_content = re.sub(pattern=pattern, repl=repl_pattern, string=content)
        # if isinstance(new_content, str):
        #     new_content = new_content.encode(encoding="utf-8")#bytes(new_content, encoding="utf-8")
        pattern = re.compile(pattern=b"{c:")
        for match in pattern.finditer(new_content):
            print(f"{len(match.group())} {match.group()}")
        new_content = re.sub(pattern=pattern, repl=b"{r", string=new_content)

        pattern = re.compile(pattern=b"c}")
        for match in pattern.finditer(new_content):
            print(f"{len(match.group())} {match.group()}")
        new_content, num = re.subn(pattern=pattern, repl=b"r}", string=new_content)

        pattern = re.compile(pattern=b"c:")
        for match in pattern.finditer(new_content):
            print(f"{len(match.group())} {match.group()}")
        new_content = re.sub(pattern=pattern, repl=b"r", string=new_content)

        # Replace {r:r} with {rr}
        pattern = re.compile(pattern=b"{r:r}")
        for match in pattern.finditer(new_content):
            print(f"{len(match.group())} {match.group()}")
        new_content = re.sub(pattern=pattern, repl=b"{rr}", string=new_content)

        # Remove \hdashline
        pattern = re.compile(pattern=r"\\hdashline")
        # decode the bytes to str (this way we avoid b"" in the file)
        new_content = re.sub(pattern=pattern, repl="", string=new_content.decode(encoding="utf-8"))

        # Replace `---`
        pattern = re.compile(pattern=r"----")
        new_content = re.sub(
            pattern=pattern,
            repl=r"\\noindent\\hrulefill",  # r"\\noindent\\rule{\\textwidth}{0.6pt}",
            string=new_content
        )

    with open(target_file, "w", encoding="utf-8") as file:
        file.write(new_content)

    os.system(f'pandoc -s {target_file} -o test.pdf --pdf-engine=xelatex  -V mainfont="Arial"')


if __name__ == "__main__":
    main()
