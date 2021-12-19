from textwrap import dedent

from marko import Markdown
from marko.ext.latex_renderer import LatexRenderer
from marko.ast_renderer import ASTRenderer


def test_render_paragraph():
    markdown = """\
        This is a paragraph.

        This is
         another paragraph.

        This has line    
           break!
        """
    latex = """\
        \\documentclass{article}
        \\begin{document}
        This is a paragraph.
        
        This is
        another paragraph.
        
        This has line\\\\
        break!
        \\end{document}
        """

    _assert_latex(markdown, latex)


def test_render_special_characters():
    markdown = "\\# This paragraph contains $pecial_characters like: {%, ^, ~ & \\\\}"
    latex = """\
        \\documentclass{article}
        \\begin{document}
        \\# This paragraph contains \\$pecial\\_characters like: \\{\\%, \\^{}, \\~{} \\& \\textbackslash{}\\}
        \\end{document}
        """

    _assert_latex(markdown, latex)


def test_render_format():
    markdown = "This `test case` *tests* **basic** *text **formatting***."
    latex = """\
        \\documentclass{article}
        \\begin{document}
        This \\texttt{test case} \\textit{tests} \\textbf{basic} \\textit{text \\textbf{formatting}}.
        \\end{document}
        """

    _assert_latex(markdown, latex)


def test_render_unordered_list():
    markdown = """\
        Items:
        * Item 1
        * Item 2
        * Item 3
        """
    latex = """\
        \\documentclass{article}
        \\begin{document}
        Items:
        \\begin{itemize}
        \\item Item 1
        \\item Item 2
        \\item Item 3
        \\end{itemize}
        \\end{document}
        """

    _assert_latex(markdown, latex)


def test_render_ordered_list():
    markdown = """\
        Items:
        1. Item 1
        1. Item 2
        1. Item 3
        """
    latex = """\
        \\documentclass{article}
        \\begin{document}
        Items:
        \\begin{enumerate}
        \\item Item 1
        \\item Item 2
        \\item Item 3
        \\end{enumerate}
        \\end{document}
        """

    _assert_latex(markdown, latex)


def test_render_headers():
    markdown = """\
        # Header 1
        Paragraph 1.
        
        ## Header 2
        Paragraph 2.
        
        ### Header 3
        Paragraph 3.
        
        #### Header 4
        Paragraph 4.
        
        ##### Header 5
        Paragraph 5.
        
        ###### Header 6
        Paragraph 6.

        Alternate Header 1
        ==================
        Alternate 1

        Alternate Header 2
        ------------------
        Alternate 2
        """
    latex = """\
        \\documentclass{article}
        \\begin{document}
        \\part*{Header 1}
        Paragraph 1.

        \\section*{Header 2}
        Paragraph 2.

        \\subsection*{Header 3}
        Paragraph 3.

        \\subsubsection*{Header 4}
        Paragraph 4.

        \\paragraph*{Header 5}
        Paragraph 5.

        \\subparagraph*{Header 6}
        Paragraph 6.

        \\part*{Alternate Header 1}
        Alternate 1

        \\section*{Alternate Header 2}
        Alternate 2
        \\end{document}
        """

    _assert_latex(markdown, latex)


def test_render_code():
    markdown = """\
        The following is a code block:

            Text enclosed inside \\texttt{verbatim} environment
            is printed directly and all \\LaTeX{} commands are ignored.

        While the following is a fenced code block:

        ```python
        def do_while():
            while(not_finished):
                print("do something ...")
            print("finished!")
        ```
        """
    latex = """\
        \\documentclass{article}
        \\usepackage{listings}
        \\begin{document}
        The following is a code block:

        \\begin{verbatim}
        Text enclosed inside \\texttt{verbatim} environment
        is printed directly and all \\LaTeX{} commands are ignored.
        \\end{verbatim}

        While the following is a fenced code block:

        \\begin{lstlisting}[language=python]
        def do_while():
            while(not_finished):
                print("do something ...")
            print("finished!")
        \\end{lstlisting}
        \\end{document}
        """

    _assert_latex(markdown, latex)


def test_render_links():
    markdown = """\
        [marko](https://github.com/frostming/marko "marko on GitHub"): A markdown parser with high extensibility.

        Documentation: <https://marko-py.readthedocs.io/en/latest/>.
        """
    latex = """\
        \\documentclass{article}
        \\begin{document}
        \\href{https://github.com/frostming/marko}{marko}: A markdown parser with high extensibility.

        Documentation: \\url{https://marko-py.readthedocs.io/en/latest/}.
        \\end{document}
        """

    _assert_latex(markdown, latex)


def test_render_quote():
    markdown = """\
        They used to say:

        > Take care of
        > important quotes.
        """
    latex = """\
        \\documentclass{article}
        \\usepackage{csquotes}
        \\begin{document}
        They used to say:

        \\begin{displayquote}
        Take care of
        important quotes.
        \\end{displayquote}
        \\end{document}
        """

    _assert_latex(markdown, latex)


def test_render_thematic_break():
    markdown = """\
        This paragraph is above the horizontal line.
        
        * * * 

        While this paragraph is below the horizontal line.
        """
    latex = """\
        \\documentclass{article}
        \\begin{document}
        This paragraph is above the horizontal line.
        
        \\noindent\\rule{\\textwidth}{1pt}

        While this paragraph is below the horizontal line.
        \\end{document}
        """

    _assert_latex(markdown, latex)


def test_render_image():
    markdown = """\
        ## A simple image
        ![This is a sample for an image](sample.jpg "Title is ignored!")
        """
    latex = """\
        \\documentclass{article}
        \\usepackage{graphicx}
        \\begin{document}
        \\section*{A simple image}
        \\includegraphics{sample.jpg}
        \\end{document}
        """

    _assert_latex(markdown, latex)


def _assert_latex(markdown: str, latex: str):
    ast_converter = Markdown(renderer=ASTRenderer)
    print(ast_converter(dedent(markdown)))
    latex_converter = Markdown(renderer=LatexRenderer)
    assert latex_converter(dedent(markdown)) == dedent(latex)
