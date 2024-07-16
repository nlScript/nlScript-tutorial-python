from PySide2.QtWidgets import QApplication
from nlScript.evaluator import Evaluator

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

    # 1. Define the type "units" as the string literal "pixel(s)"
    #    Here we use a lambda expression to define the evaluator
    parser.defineType("units", "pixel(s)", evaluator=Evaluator(lambda pn: False))
    # 2. Define the type "units" as the string literal "calibrated units"
    parser.defineType("units", "calibration units", evaluator=Evaluator(lambda pn: True))


    def evaluateFilterSize(pn):
        stddev = pn.evaluate("stddev")

        # Note that the "units" type evaluates to a Boolean, which is true if "calibrated units" was
        # parsed, and false if "pixel(s)" was parsed
        units = pn.evaluate("units")

        # Convert stddev to pixel units in case it was specified in calibrated units
        if units:
            stddev /= preprocessing.getPixelWidth()
        return stddev


    parser.defineType(
        "filter-size",
        "{stddev:float} {units:units}",
        evaluator=Evaluator(evaluateFilterSize),
        autocompleter=True
    )

    def evaluateSentence(pn):
        stddev = pn.evaluate("stddev")
        preprocessing.gaussianBlur(stddev)

    parser.defineSentence(
        "Apply Gaussian blurring with a standard deviation of {stddev:filter-size}.",
        evaluator=Evaluator(evaluateSentence))

    editor = ACEditor(parser)
    editor.show()

    # Needed for running a PySide application
    exit(app.exec_())
