from datetime import datetime
from typing import IO, Any, NoReturn, TextIO

from src.utils.logger import Logger
from src.config import Config


def headings(
        log: Logger,
        conf: Config,
        title: str,
        out_file: TextIO
    ) -> int | NoReturn:
    """Create the headings of the LaTeX file."""

    SECTIONS: dict[str, str] = {
            "main": (
                    "\n"
                    r"% size config of sections"
                    "\n\sectionfont{\\fontsize{"
                    "<SECTION_SIZES>}{15}\selectfont}"
                ),
            "sub": (
                    "\subsectionfont{\\fontsize{"
                    "<SECTION_SIZES>}{15}\selectfont}"
                ),
            "subsub": (
                    "\subsubsectionfont{\\fontsize{"
                    "<SECTION_SIZES>}{15}\selectfont}"
                ),
        }

    headings: list[str] = [
            f"\documentclass[{conf.font_size}pt]{{{conf.doc_class}}}\n",
            f"% font\n\\usepackage{{{conf.doc_font}}}\n\n% packages"
        ]

    if "<NOW>" in conf.date:
        conf.__setattr__("date", datetime.now().strftime("%B %d, %Y"))

    pkgs: str
    for pkgs in conf.packages:
        if "margin" in pkgs:
            pkgs = (
                    pkgs
                        .replace("<MARGIN>", f"{conf.margin}in")
                        .replace("<PAPER_SIZE>", conf.paper_size)
                )
        elif "colorlinks" in pkgs:
            pkgs = pkgs.replace("<LINK_COLORS>", conf.link_color)

        headings.append(f"\\usepackage{pkgs}")

    headings.append(
        f"\\usepackage[scaled={conf.cfont_scale}]{{{conf.code_font}}}"
    )

    sec_sizes: int; sec_val: str
    for sec_sizes, sec_val in zip(
            conf.section_sizes.values(), SECTIONS.values()
        ):
        headings.append(sec_val.replace("<SECTION_SIZES>", str(sec_sizes)))

    headings.append(
        f"\n% basic config\n\setlength\parindent{{{conf.indent_size}pt}}"
    )
    headings.append(
        f"\\renewcommand{{\\thefootnote}}{{\\fnsymbol{{{conf.footnote}}}}}"
    )

    if conf.sloppy:
        headings.append(r"\sloppy")

    lstconf: IO[Any]
    with open(conf.code_conf, "r", encoding="utf-8") as lstconf:
        headings.append(f"\n% lst listings config")
        for lines in lstconf.readlines():
            headings.append(lines.replace("\n", ""))

    items: str
    for items in [
            f"\n% paper info\n\\title{{{title}}}",
            f"\\author{{{conf.author}}}",
            f"\date{{{conf.date}}}"
        ]:
        headings.append(items)

    try:
        log.logger("I", "Writing headings to file ...")
        for items in headings:
            out_file.write(f"{items}\n")
    except (
        IOError,
        SystemError,
        BlockingIOError,
        PermissionError
    ) as Err:
        log.logger("E", f"Encountered {Err}, aborting ...")
    else:
        return len(headings)+11 # 11 is the number of newlines created.
