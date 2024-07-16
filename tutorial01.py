from PySide2.QtWidgets import QApplication

from nlScript.parser import Parser
from nlScript.ui.ui import ACEditor

"""
This is a basic example how NLS works in principle. It demonstrates the three steps involved:
- Creating a parser
- Teach the parser the sentences to accept
- Show a dedicated editor with autocompletion adjusted to the defined language

Please note that the 2nd argument to 'defineSentence' is null, so that nothing actually happens
when the user clicks on the editor's Run button.

This will be addressed in Tutorial02

For details, see
https://nlScript.github.io/nlScript-java/#implement-an-interface-that-understands-a-first-sentence
https://nlScript.github.io/nlScript-java/variables.html
"""

if __name__ == '__main__':
    # Needed for running a PySide application
    app = QApplication([])

    # Step 1: Create a parser
    parser = Parser()

    # Step 2: Define the sentences to parse
    #         A sentence may contain one or more variables, which are specified
    #         as {name:type:quantifier}.
    #
    #         The quantifier is optional.
    #
    #         More information about how to declare variables can be found at
    #         https://nlScript.github.io/nlScript-java/variables.html.
    #
    #         More information about other built-in types, apart from 'float', can be found at
    #         https://nlScript.github.io/nlScript-java/#built-in-types
    parser.defineSentence(
        "Apply Gaussian blurring with a standard deviation of {stddev:float} pixel(s).",
        None)

    # Step 3: Display an editor for the user to enter the input text
    editor = ACEditor(parser)
    editor.show()

    # Needed for running a PySide application
    exit(app.exec_())
