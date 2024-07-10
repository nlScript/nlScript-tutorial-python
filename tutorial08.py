from PyQt5.QtWidgets import QApplication
from nlScript.autocompleter import Autocompleter
from nlScript.core.autocompletion import Autocompletion
from nlScript.ebnf.ebnfparser import ParseStartListener
from nlScript.evaluator import Evaluator

from nlScript.parser import Parser
from nlScript.ui.ui import ACEditor

from preprocessing import Preprocessing

"""
The previous tutorial showed how to use a custom Autocompleter. Using a ParseStartListener, the pixel
calibration unit string is saved. The 'units' autocompleter then suggests the two options 'pixel(s)'
and the actual calibration unit string.

A much better solution would be, if the 'units' type could be defined as 'pixel(s)' and as 'mm' in the
first place (similar to Tutorial05), and this would work here because the image to be processed is fixed.

However, in a more general case, the designed language should work on any image, and therefore, at the
time of designing the language the actual pixel units are not known yet, and this is why Tutorial05
used the fixed literal 'calibrated units' instead of the actual units string.

This tutorial shows how the 'units' type can be re-defined dynamically, and this is again best done
within in the ParseStartListener's parsingStarted() function.

The result will be similar to that of Tutorial05, but instead of the general 'calibrated units'
autocompletion option, the actual units string will be shown as an option.

For details, see
https://nlScript.github.io/nlScript-java/#dynamically-re-defining-types
"""

if __name__ == '__main__':
    # Needed for running a PyQt application
    app = QApplication([])

    preprocessing = Preprocessing(None)
    preprocessing.open('http://imagej.net/images/clown.jpg')
    preprocessing.show()

    preprocessing.setPixelWidth(0.25, "mm")

    parser = Parser()

    def parsingStarted():
        unitsString = preprocessing.getUnits()

        # At the start of parsing (remember this is done whenever auto-completion
        # needs to be performed), the 'units' type is undefined and then
        # re-defined, according to the pixel calibration unit string of the current image:
        parser.undefineType("units")

        parser.defineType("units", "pixel(s)", Evaluator(lambda pn: False))
        parser.defineType("units", unitsString, Evaluator(lambda pn: True))


    parser.addParseStartListener(listener=ParseStartListener(parsingStarted))

    parser.defineType("units", "pixel(s)", Evaluator(lambda pn: False))
        
    def evaluateFilterSize(pn):
        stddev = pn.evaluate("stddev")
        units = pn.evaluate("units")
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

    # Needed for running a PyQt application
    exit(app.exec_())
