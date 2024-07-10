from PyQt5.QtWidgets import QApplication
from nlScript.ebnf.ebnfparser import ParseStartListener
from nlScript.evaluator import Evaluator

from nlScript.parser import Parser
from nlScript.ui.ui import ACEditor

from preprocessing import Preprocessing

"""
 * This tutorial extends the previous functionality by median filtering, background subtraction and intensity
 * normalization, simply by adding more sentence definitions similar to the existing one for Gaussian blurring.
 *
 * The new sentences also re-use the 'filter-size' type.
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

    # Gaussian Blurring
    parser.defineSentence(
        "Apply Gaussian blurring with a standard deviation of {stddev:filter-size}.",
        evaluator=Evaluator(lambda pn: preprocessing.gaussianBlur(pn.evaluate("stddev"))))

    # Median filtering
    parser.defineSentence(
        "Apply Median filtering with a window of radius {window-size:filter-size}.",
        evaluator=Evaluator(lambda pn: preprocessing.medianFilter(pn.evaluate("window-size"))))

    # Intensity normalization
    parser.defineSentence(
        "Normalize intensities.",
        evaluator=Evaluator(lambda pn: preprocessing.intensityNormalization()))

    # Background subtraction
    parser.defineSentence(
        "Subtract the background with a standard deviation of {window-size:filter-size}.",
        evaluator=Evaluator(lambda pn: preprocessing.gaussianBlur(pn.evaluate("window-size"))))

    editor = ACEditor(parser)
    editor.show()

    # Needed for running a PyQt application
    exit(app.exec_())
