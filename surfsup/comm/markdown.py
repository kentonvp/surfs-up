def fmt_text(text):
    return (
        text.replace("(", "\\(")
        .replace(")", "\\)")
        .replace(".", "\\.")
        .replace("-", "\\-")
        .replace("_", " ")
    )


def gen_link(text, link):
    return f"[{fmt_text(text)}]({fmt_text(link)})"
