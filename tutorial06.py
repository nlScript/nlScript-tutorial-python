from PySide2.QtWidgets import QApplication
from nlScript.core.autocompletion import Autocompletion, Purpose
from nlScript.ebnf.ebnfparser import ParseStartListener
from nlScript.parseexception import ParseException

from nlScript.parser import Parser
from nlScript.ui.ui import ACEditor

from preprocessing import Preprocessing

"""
Tutorial06 shows how to use a fully custom Autocompleter, with the goal to replace the
static "calibrated units" option for the "units" type with the actual units string of
the currently open image.

There is one (autocompletion) issue here, which will be addressed in the next tutorial:
Once the user starts typing the text for the unit (let's say a 'p' for 'pixel(s)'), completion
should stop (or even better, only suggest 'pixel(s)', because 'mm' doesn't start with 'p').
However, here it will just continue to suggest 'pixel(s)' as well as 'mm'.

For details, see
https://nlScript.github.io/nlScript-java/#dynamic-autocompletion-at-runtime-using-a-custom-autocompleter
"""

if __name__ == '__main__':
    # Needed for running a PySide application
    app = QApplication([])

    preprocessing = Preprocessing(None)
    preprocessing.open('http://imagej.net/images/clown.jpg')
    preprocessing.show()

    # Unfortunately, the clown image doesn't have calibrated pixels. For demonstration
    # purposes, we artificially set a calibration here
    preprocessing.setPixelWidth(0.25, "mm")

    parser = Parser()

    # The new feature is the use of the ParseStartListener, whose parsingStarted() function
    # gets called when parsing is started. At that time, the image to process is known, so its
    # pixel calibration unit string can be stored, to be used for autocompletion later.
    # Note: Parsing is not only performed once the user clicks on 'Run', but whenever the user's
    # text changes, for auto-completion.
    imageUnits = ""

    def parsingStarted():
        global imageUnits
        print("Parsing started")
        imageUnits = preprocessing.getUnits()

    parser.addParseStartListener(listener=ParseStartListener(parsingStarted))

    def getAutocompletion(pn, justCheck):
        print("getAutocompletion: imageUnits = " + imageUnits)
        return Autocompletion.literal(pn, ["pixel(s)", imageUnits])

    parser.defineType("units", "{unitstring:[a-zA-Z()]:+}",
                      evaluator=lambda pn: pn.getParsedString() != "pixel(s)",
                      autocompleter=getAutocompletion)


    def evaluateFilterSize(pn):
        stddev = pn.evaluate("stddev")
        units = pn.evaluate("units")
        if units:
            stddev /= preprocessing.getPixelWidth()
        return stddev

    parser.defineType("filter-size",
                      "{stddev:float} {units:units}",
                      evaluator=evaluateFilterSize,
                      autocompleter=True)

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
