from PySide2.QtWidgets import QApplication
from nlScript.autocompleter import Autocompleter
from nlScript.core.autocompletion import Autocompletion
from nlScript.ebnf.ebnfparser import ParseStartListener
from nlScript.evaluator import Evaluator

from nlScript.parser import Parser
from nlScript.ui.ui import ACEditor

from preprocessing import Preprocessing

"""
The previous tutorial showed how to use a custom Autocompleter, but suffered from one
autocompletion issue:

Once the user starts typing the text for the unit (let's say a 'p' for 'pixel(s)'), completion
should stop (or even better, only suggest 'pixel(s)', because 'mm' doesn't start with 'p').
However, here it will just continue to suggest 'pixel(s)' as well as 'mm'.

This tutorial demonstrates how to stop autocompletion once the user started typing a value.

In the case here, it would actually be better to filter suggested options according to what the user typed,
(and this will be shown in the next tutorial), but there are cases where stopping auto-completion after the
user started to type is important: This is particularly the case if e.g. entering numbers: As long as nothing
is entered, auto-completion should indicate what needs to be entered (e.g. a placeholder with a name), but once
the user started typing a number, auto-completion should be quiet. BTW: This is not only true for numbers, but
for also e.g. when entering a name for something.

For details, see
https://nlScript.github.io/nlScript-java/#prohibit-further-autocompletion-autocompleterveto
"""

if __name__ == '__main__':
    # Needed for running a PySide application
    app = QApplication([])

    preprocessing = Preprocessing(None)
    preprocessing.open('http://imagej.net/images/clown.jpg')
    preprocessing.show()

    preprocessing.setPixelWidth(0.25, "mm")

    parser = Parser()

    imageUnits = ""

    def parsingStarted():
        global imageUnits
        imageUnits = preprocessing.getUnits()

    parser.addParseStartListener(listener=ParseStartListener(parsingStarted))

    # The only change here, compared to the previous version, is
    # to check whether the user has started typing for 'units', in
    # which case pn.getParsedString() returns what's already entered.
    # If something was entered, a special 'veto' autocompleter is returned,
    # which prohibits further auto-completion.
    def getAutocompletion(pn, justCheck):
        if len(pn.getParsedString()) == 0:
            return Autocompletion.literal(pn, ["pixel(s)", imageUnits])
        return Autocompletion.veto(pn)

    parser.defineType("units", "{unistring:[a-zA-Z()]:+}",
              evaluator=Evaluator(lambda pn: pn.getParsedString() != "pixel(s)"),
              autocompleter=Autocompleter(getAutocompletion))

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

    # Needed for running a PySide application
    exit(app.exec_())
