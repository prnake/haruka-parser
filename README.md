# Haruka Parser

A simple HTML Parser

## Usage

```python3
from haruka_parser.extract import extract_text

html = """<!DOCTYPE html>
<html>
<body>
<!-- Using MathML -->
<p>Using MathJax:</p>
<script type="math/tex; mode=display" id="MathJax-Element-1">{e}^{i\pi }=-1</script>
<!-- Using MathML -->
<p>Using MathML:</p>
<math xmlns="http://www.w3.org/1998/Math/MathML">
  <msup>
    <mi>e</mi>
    <mrow>
      <mi>i</mi>
      <mi>&#x03C0;</mi>
    </mrow>
  </msup>
  <mo>=</mo>
  <mn>-1</mn>
</math>

<!-- Using AsciiMath -->
<p>Using AsciiMath:</p>
<script type="math/asciimath">
e^(i*pi) = -1
</script>
</body>
</html>"""

configuration = {
    "readability": False,
    "skip_large_links": False,
    "extract_latex": True,
    "extract_cnki_latex": False,
    "escape_dollars": True,
    "remove_buttons": True,
    "remove_edit_buttons": True,
    "remove_image_figures": True,
    "markdown_code": True,
    "markdown_headings": True,
    "table_config": {
        "format": "html",
        "min_rows": 3,
        "min_cols": 2,
    },
    "remove_chinese": False,
    "boilerplate_config": {
        "enable": False,
        "ratio_threshold": 0.18,
        "absolute_threshold": 10,
        "end_threshold": 15,
    },
}

text, info = extract_text(html, configuration)
print(text)
print(info)
```
