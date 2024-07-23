from PySide2.QtWidgets import QApplication

from nlScript.parser import Parser
from nlScript.ui.ui import ACEditor

from preprocessing import Preprocessing

"""
The previous tutorial introduced custom types.
In Tutorial04, they will be used to change how they are autocompleted in the editor

For details, see
https://nlScript.github.io/nlScript-java/#fine-tuning-autocompletion-parameterized-autocompletion
"""

if __name__ == '__main__':
    # Needed for running a PySide application
    app = QApplication([])

    preprocessing = Preprocessing(None)
    preprocessing.open('http://imagej.net/images/clown.jpg')
    preprocessing.show()

    parser = Parser()

    def evaluateFilterSize(pn):
        return pn.evaluate("stddev")

    # In contrast to the previous tutorial, a third parameter is given, which specifies whether to
    # insert the entire sequence when auto-completing or not.
    #
    # The default is false, which means that once the user input reaches the filter size, the editor will wait
    # until a number is entered. This might be unintuitive, because it might not be clear to the user what is
    # expected (e.g. in which units to enter the value).
    #
    # If set to 'true', the entire sequence will be inserted, i.e. a placeholder for 'stddev' (which is selected
    # so that the user can readily overwrite it), concatenated with the literal 'pixel(s)'.
    parser.defineType(
        "filter-size",
        "{stddev:float} pixel(s)",
        evaluator=evaluateFilterSize,
        autocompleter=True
    )

    def evaluateSentence(pn):
        stddev = pn.evaluate("stddev")
        preprocessing.gaussianBlur(stddev)

    parser.defineSentence(
        "Apply Gaussian blurring with a standard deviation of {stddev:filter-size}.",
        evaluator=evaluateSentence)

    editor = ACEditor(parser)
    editor.show()

    # Needed for running a PySide application
    exit(app.exec_())
