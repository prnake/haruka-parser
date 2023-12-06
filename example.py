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

text, info = extract_text(html)
print(text)
print(info)
