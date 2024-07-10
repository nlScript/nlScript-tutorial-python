from PyQt5.QtWidgets import QApplication
from nlScript.evaluator import Evaluator

from nlScript.parser import Parser
from nlScript.ui.ui import ACEditor

from preprocessing import Preprocessing

"""
Tutorial02 extends the previous one by specifying a 2nd parameter to
'defineSentence', an object of type Evaluator. Evaluator is an interface with a
single function evaluate(), which is called upon parsing the corresponding sentence.

For details, see
https://nlScript.github.io/nlScript-java/#evaluating-the-parsed-text
"""

if __name__ == '__main__':
    app = QApplication([])

    # Create an instance of the processing backend.
    preprocessing = Preprocessing(None)

    # Load an example image
    preprocessing.open('http://imagej.net/images/clown.jpg')
    preprocessing.show()

    parser = Parser()

    # Define a function to evaluate the sentence below.
    def evaluateSentence(pn):
        # The argument given to evaluate(), a ParsedNode, can be used to
        # evaluate the value of the sentence's variables, here 'stddev'.
        # They are accessed by name.
        stddev = pn.evaluate("stddev")

        # Do the actual blurring, using the processing backend.
        preprocessing.gaussianBlur(stddev)


    parser.defineSentence(
        "Apply Gaussian blurring with a standard deviation of {stddev:float} pixel(s).",
        # The function specified here will be called upon parsing the sentence above
        Evaluator(evaluateSentence))

    editor = ACEditor(parser)
    editor.show()

    exit(app.exec_())
