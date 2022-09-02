from typing import Any, TextIO

from src.config import Config, Rules
from src.utils.tex.parser.headings import headings
from src.utils.tex.parser.body import body
from src.mutils.format_body import format_body
from src.mutils.fix_file_path import fix_file_path
from src.mutils.fix_title import fix_title
from src.mutils.finalize import finalize
from src.utils.logger import Logger


def convert(
        log: Logger,
        args: Any,
        rules: Rules,
        config: Config,
        title: str,
        in_file: str,
        filenametitle: bool
    ) -> None:
    """This unifies all the modules.

    Args:
        log -- for logging.
        args -- overrides received from arguments.
        rules -- rules that needs to be followed in translation.
        config -- configuration of the document metadata, which includes,
            formatting, packages to use among others, refer to simtex.json.
        title -- title of the document.
        in_file -- path of the file to be converted to LaTeX.
    """

    log.logger("I", f"Converting {in_file} ...")

    title: str = fix_title(log, title, in_file, filenametitle)
    OFILE_PATH: str = fix_file_path(
            log, in_file, config.output_folder, args.filename
        )

    out_file: TextIO
    with open(OFILE_PATH, "w", encoding="utf-8") as out_file:
        start: int = headings(log, config, title, out_file)
        files: list[str] = body(log, rules, in_file, out_file)

    format_body(log, config, start, OFILE_PATH)
    finalize(log, files, config.output_folder, in_file)
