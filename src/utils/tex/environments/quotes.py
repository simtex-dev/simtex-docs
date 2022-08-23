from typing import TextIO

from src.config import Rules


def quotation(
        rules: Rules,
        sources: list[str],
        start: int,
        out_file: TextIO
    ) -> int:
    """For typesetting of block quotes using csquotes package.

    Args:
        line -- line that will be analyzed and translated.
        start -- where the parser/translator would start.
        out_file -- where the translated line will be written.

    Returns:
        An integer that marks the lines that should be skipped.
    """

    end: int; quote: str
    for end, quote in enumerate(sources[start:]):
        if not quote.startswith(rules.bquote):
            return end+start
        else:
            out_file.write(
                f"\t{quote.replace(rules.bquote, '').strip()}\n"
            )