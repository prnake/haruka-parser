import re
import os
from haruka_parser.latex_processing import replace_math_tags_with_dollar_signs

edit_regex = r"\[(e|E)dit\]"

boilerplate_words_path = os.path.join(
    os.path.dirname(__file__), "dictionary/boilerplate_words.txt"
)
with open(boilerplate_words_path, "r") as f:
    boilerplate_words = {}
    for line in f:
        words = line.replace("\n", "")
        n_words = len(words.split())
        boilerplate_words[words] = n_words


def remove_empty_headers(lines, replacement_manager):
    output_lines = []
    is_heading = [0] * len(lines)
    for k in range(1, 7):
        for i in range(len(lines)):
            if replacement_manager.has_tag(lines[i], tag="h" + str(k)):
                is_heading[i] = k
    for i in range(len(lines)):
        # Check if this line is a heading
        if is_heading[i] != 0:
            remove = False
            # Go through the next lines until we find a line that is not a heading
            j = i + 1
            while j < len(lines):
                if is_heading[j] == 0 and len(lines[j]) > 16:
                    break
                elif is_heading[j] != 0 and is_heading[j] <= is_heading[i]:
                    remove = True
                    break
                j += 1
            # If we found a line that is not a heading, then we have a section
            if j < len(lines) and not remove:
                output_lines.append(lines[i])
        else:
            output_lines.append(lines[i])
            # If there is at least one non-heading line, then we have a section

    return output_lines


def remove_edit_buttons(lines):
    output_lines = []
    for line in lines:
        if re.search(edit_regex, line):
            output_lines.append(re.sub(edit_regex, "", line))
        else:
            output_lines.append(line)
    return output_lines


def have_chinese_characters(text):
    return bool(re.search("[\u4e00-\u9fff]", text))


def remove_chinese_characters(lines):
    output_lines = []
    for line in lines:
        if re.match("[\u4e00-\u9fff]", line):
            output_lines.append("")
        else:
            output_lines.append(line)
    return output_lines


def remove_boilerplate(lines, boilerplate_config, replacement_manager):
    output_lines = []
    maths = [replacement_manager.has_tag(line, tag="math") for line in lines]
    codes = [replacement_manager.has_tag(line, tag="code") for line in lines]
    for i in range(len(lines)):
        lowered = lines[i].lower()
        without_tags = replacement_manager.remove_tags(lowered)
        s = sum(
            [
                without_tags.count(word) * boilerplate_words[word]
                for word in boilerplate_words
            ]
        )
        # Compute the ratio of boilerplate words over the length of the line, and remove the line if this ratio is larger than the threshold
        ratio = s / (len(without_tags.split()) + 0.001)
        if (
            (
                ratio > boilerplate_config["ratio_threshold"]
                or s > boilerplate_config["absolute_threshold"]
            )
            and not maths[i]
            and not codes[i]
        ):
            if len(lines) - i < boilerplate_config["end_threshold"]:
                for j in range(i, len(lines)):
                    if maths[j] or codes[j]:
                        output_lines.append(lines[j])
                break
        else:
            output_lines.append(lines[i])
    return output_lines


def remove_headings(text):
    """Delete [heading_i], which also handling in post_process_headings"""
    for i in range(6, 0, -1):
        text = text.replace("[heading_%d]" % i, "")
    return text


def restore_replacements(text, replacement_manager, config, info):
    text = remove_headings(text)
    if config["extract_latex"] and config["escape_dollars"] and info["found_math"]:
        # Escape any dollar signs in the text if we add some $ for math equations
        text = text.replace("[extract_single_dollar]", "\\$")
    else:
        text = text.replace("[extract_single_dollar]", "$")

    # Now, add the dollar signs for math
    text = replace_math_tags_with_dollar_signs(text)

    text = replacement_manager.remove_tags(text)
    text = text.replace("[extract_single_chapter]", "§")
    return text.strip()
