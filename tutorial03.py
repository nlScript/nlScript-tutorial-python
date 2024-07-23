from PySide2.QtWidgets import QApplication

from nlScript.parser import Parser
from nlScript.ui.ui import ACEditor

from preprocessing import Preprocessing

"""
Tutorial03 introduces custom types.

Custom types are specified similar to sentences, but
- an explicit type name is given
- their evaluator typically doesn't return null, but an arbitrary object representing that type

In this particular example, using a custom type for the filter size doesn't provide any advantage. In general, one
would use custom types to
- reuse them in multiple sentences or other types
- to fine-tune the way they are auto-completed in the editor.

This will be demonstrated in subsequent tutorials.

For details, see
https://nlScript.github.io/nlScript-java/#built-in-types
https://nlScript.github.io/nlScript-java/#custom-types-and-type-hierarchy
https://nlScript.github.io/nlScript-java/custom-types.html
https://nlScript.github.io/nlScript-java/type-hierarchy.html
"""

if __name__ == '__main__':
    app = QApplication([])

    preprocessing = Preprocessing(None)
    preprocessing.open('http://imagej.net/images/clown.jpg')
    preprocessing.show()

    parser = Parser()

    # Define a function which will be used to evaluate the 'filter-size' type below
    def evaluateFilterSize(pn):
        return pn.evaluate("stddev")

    # Create a custom type 'filter-size'
    parser.defineType(
        # The name of the type
        "filter-size",
        # The pattern to parse  (i.e. a floating point number, followed by the literal " pixel(s)".
        "{stddev:float} pixel(s)",
        # An Evaluator, which in this case just returns the parsed standard deviation as a Double.
        # In principle, a custom type can evaluate to any object
        evaluator=evaluateFilterSize
    )

    def evaluateSentence(pn):
        stddev = pn.evaluate("stddev")
        preprocessing.gaussianBlur(stddev)

    parser.defineSentence(
        "Apply Gaussian blurring with a standard deviation of {stddev:filter-size}.",
        evaluator=evaluateSentence)

    editor = ACEditor(parser)
    editor.show()

    exit(app.exec_())
