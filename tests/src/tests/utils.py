def extract_between(text, start_tag, end_tag):
    try:
        start = text.index(start_tag) + len(start_tag)
        end = text.index(end_tag, start)
        return text[start:end]
    except ValueError:
        return None
