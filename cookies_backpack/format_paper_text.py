import re


def format_sentences(text):
    lines = text.split('\n')
    s = ''
    for line in lines:
        if line.endswith('-'):
            s += line[:-1]
        else:
            s += line + ' '
    return s.strip()


def extract_sections(raw_file, title):
    sections = {}
    author = []
    abstract = []
    last_section_no = 0
    section_no = None
    in_title = False
    passed_title = False
    in_author = False
    in_abstract = False
    in_section_no = None
    section_contents = []

    with open(raw_file, encoding='utf8', newline='\n') as ifile:
        for line in ifile:
            s = line.strip()
            if not passed_title:
                if s in title:
                    in_title = True
                    continue
                if in_title and (s not in title):
                    passed_title = True
                    in_author = True
            if in_author:
                if s == 'Abstract':
                    in_author = False
                    in_abstract = True
                    continue
                author.append(s)
            if section_no is not None:
                if re.fullmatch(r'[\d\.]+', s) is not None:
                    section_no = None
                    continue
                sections[section_no] = {'title': s}
                last_section_no = section_no
                in_section_no = section_no
                section_no = None
                continue
            if in_section_no is not None:
                section_contents.append(s)
                if s.endswith('.'):
                    sections[in_section_no]['content'] = format_sentences('\n'.join(section_contents))
                    in_section_no = None
                    section_contents = []
            if s == str(last_section_no + 1):
                in_abstract = False
                section_no = int(s)
            if in_abstract:
                abstract.append(s)
    return '\n'.join(author), format_sentences('\n'.join(abstract)), sections


def format_paper_text(raw_file, formatted_file, title):
    author, abstract, sections = extract_sections(raw_file, title)
    with open(formatted_file, mode='w', encoding='utf8', newline='\n') as ofile:
        ofile.write(f'### Title\n{title}\n\n')
        ofile.write(f'### Author\n{author}\n\n')
        ofile.write(f'### Abstract\n{abstract}\n\n')
        for k, v in sections.items():
            ofile.write(f'### Section {k}: {v["title"]}\n{v["content"]}\n\n')
