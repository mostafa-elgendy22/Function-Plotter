# imports
import sys
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtCore, QtGui, QtWidgets


# Constants
TEXT_COLOR = "#0B04DA"
WINDOW_BACKGROUND_COLOR = "white"
TEXT_FONT = QtGui.QFont("Times", 14)
STYLE_SHEET = "background-color:" + WINDOW_BACKGROUND_COLOR + "; font: bold; color:" + TEXT_COLOR
BUTTON_STYLE_SHEET = "background-color: #0BB419; color: white; font-size: 30px; font-weight: bold"
TEXT_FIELD_WIDTH = 800
TEXT_FIELD_HEIGHT = 60
BUTTON_WIDTH = 400
BUTTON_HEIGHT = 100



class Plotter(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle("Function Plotter")
        self.showMaximized()
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.setWindowIcon(QtGui.QIcon("assets/app_icon.png"))
        self.setStyleSheet("background-color:" + WINDOW_BACKGROUND_COLOR + ";");
        self.autoFillBackground = True
        self.backgroundColor = WINDOW_BACKGROUND_COLOR
        plt.style.use('seaborn-whitegrid')

        # error messages 
        self.messageBox = QtWidgets.QMessageBox() 
        self.errorMessage = None
        self.errorMessageEmptyFields = "Please, complete all the input fields"
        self.errorMessageLimitsNotNumbers = "Limits must be numbers only"
        self.errorMessageInvalidLimits = "The maximum value must be greater than the minimum value"
        self.errorMessageInvalidFunction = "Invalid function"
        
        # create the application layout
        self.__createLayout()


    # create a new canvas to show the plot of the function
    def __createCanvas(self):
        self.figure = plt.figure(figsize=(8, 8))
        self.canvas = FigureCanvas(self.figure)
        self.canvas.axes = self.figure.add_subplot(1, 1, 1)
        self.__styleCanvas()


    def __styleCanvas(self, outputFunction=None):
        if outputFunction is not None:
            addedTitle = " [" + outputFunction + "]"
            addedTitle = addedTitle.replace("np.", "")
        else:
            addedTitle = ""
        self.figure.suptitle("Output Plot" + addedTitle, fontsize=30, color=TEXT_COLOR)
        self.canvas.axes.tick_params(axis='x', colors=TEXT_COLOR)
        self.canvas.axes.tick_params(axis='y', colors=TEXT_COLOR)
        self.canvas.axes.set_xlabel('x', fontsize=30)
        self.canvas.axes.set_ylabel('f(x)', fontsize=30)
        self.canvas.axes.xaxis.label.set_color(TEXT_COLOR)
        self.canvas.axes.yaxis.label.set_color(TEXT_COLOR)
        

    # create the function [f(x)] text field and its label
    def __createInputFunction(self):
        self.inputFunctionLabel = QtWidgets.QLabel("f(x)")
        self.inputFunctionLabel.setStyleSheet(STYLE_SHEET)
        self.inputFunctionLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.inputFunctionLabel.setFont(TEXT_FONT)

        self.inputFunctionTextField = QtWidgets.QLineEdit(self)
        self.inputFunctionTextField.setFixedWidth(TEXT_FIELD_WIDTH)
        self.inputFunctionTextField.setFixedHeight(TEXT_FIELD_HEIGHT)
        self.inputFunctionTextField.setFont(TEXT_FONT)
        self.inputFunctionTextField.setTextMargins(12, 0, 12, 0)


    # create the input text fields and the labels for the limits of x
    def __createLimits(self):
        self.minXLabel = QtWidgets.QLabel("Minimum value of x")
        self.minXLabel.setStyleSheet(STYLE_SHEET)
        self.minXLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.minXLabel.setFont(TEXT_FONT)

        self.minXTextField = QtWidgets.QLineEdit(self)
        self.minXTextField.setFixedWidth(TEXT_FIELD_WIDTH)
        self.minXTextField.setFixedHeight(TEXT_FIELD_HEIGHT)
        self.minXTextField.setFont(TEXT_FONT)
        self.minXTextField.setTextMargins(12, 0, 12, 0)

        self.maxXLabel = QtWidgets.QLabel("Maximum value of x")
        self.maxXLabel.setStyleSheet(STYLE_SHEET)
        self.maxXLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.maxXLabel.setFont(TEXT_FONT)

        self.maxXTextField = QtWidgets.QLineEdit(self)
        self.maxXTextField.setFixedWidth(TEXT_FIELD_WIDTH)
        self.maxXTextField.setFixedHeight(TEXT_FIELD_HEIGHT)
        self.maxXTextField.setFont(TEXT_FONT)
        self.maxXTextField.setTextMargins(12, 0, 12, 0)


    def __createPlotButton(self):
        self.plotButton = QtWidgets.QPushButton("Plot Function") 
        self.plotButton.setFixedWidth(BUTTON_WIDTH)
        self.plotButton.setFixedHeight(BUTTON_HEIGHT)
        self.plotButton.setStyleSheet(BUTTON_STYLE_SHEET)
        # Add an event handler to the button
        self.plotButton.clicked.connect(self.__plotButtonHandler) 


    def __plotButtonHandler(self):
        if self.__validateInput(self.inputFunctionTextField.text().lower(),
                                self.maxXTextField.text(), 
                                self.minXTextField.text()) == True:
            try:
                x = np.linspace(self.minXValue, self.maxXValue) # create the data on the x-axis
                y = eval(self.inputFunction) # evalute the function
                self.__plot(x, y) 
            except Exception as e:
                self.errorMessage = self.errorMessageInvalidFunction + ", " + str(e)
                self.__showErrorMessage()


    def __createClearButton(self):
        self.clearButton = QtWidgets.QPushButton("Clear") 
        self.clearButton.setFixedWidth(BUTTON_WIDTH)
        self.clearButton.setFixedHeight(BUTTON_HEIGHT)
        self.clearButton.setStyleSheet(BUTTON_STYLE_SHEET)
        # Add an event handler to the button
        self.clearButton.clicked.connect(self.__clearButtonHandler) 


    def __clearButtonHandler(self):
        self.inputFunctionTextField.clear()
        self.minXTextField.clear()
        self.maxXTextField.clear()
        self.figure.clear()
        self.canvas.axes = self.figure.add_subplot(111)
        self.__styleCanvas()
        self.canvas.draw()


    def __styleLayout(self): 
        # create the window layout
        layout = QtWidgets.QFormLayout()
        layout.setSpacing(40)
        
        # add the canvas to the main layout 
        layout.addRow(self.canvas)

        # create the input fields layout
        inputLayout = QtWidgets.QFormLayout()
        inputLayout.setFormAlignment(QtCore.Qt.AlignCenter)
        inputLayout.setSpacing(40)

        # add the input function text field and its label to the window
        inputLayout.addRow(self.inputFunctionLabel, self.inputFunctionTextField)

        # add the text field of the minimum value of x and its label to the window
        inputLayout.addRow(self.minXLabel, self.minXTextField)

        # Add the text field of the maximum value of x and its label to the window
        inputLayout.addRow(self.maxXLabel, self.maxXTextField)

        # create a horizontal layout for the two buttons (plot & clear buttons)
        buttons = QtWidgets.QHBoxLayout()
        buttons.setSpacing(50)
        buttons.addWidget(self.plotButton)
        buttons.addWidget(self.clearButton)

        # create a form layout for to position the buttons correctly
        buttonsLayout = QtWidgets.QFormLayout()
        buttonsLayout.setFormAlignment(QtCore.Qt.AlignCenter)
        buttonsLayout.setSpacing(40)
        buttonsLayout.addRow(buttons)

        # add the input layout and buttons layout to the main layout
        layout.addItem(inputLayout)
        layout.addItem(buttonsLayout)
        self.setLayout(layout)


    # plots the function on the figure
    def __plot(self, x, y):
        self.figure.clear()
        self.canvas.axes = self.figure.add_subplot(111)
        self.__styleCanvas(outputFunction=self.inputFunction)
        self.canvas.axes.plot(x, y, 'red')
        self.canvas.draw()


    def __createLayout(self): 
        self.__createCanvas()
        self.__createPlotButton()
        self.__createClearButton()
        self.__createInputFunction()
        self.__createLimits()
        self.__styleLayout()


    def __validateInput(self, fx, max, min):
        # check if any text field is empty
        if fx == "" or max == "" or min == "":
            self.errorMessage = self.errorMessageEmptyFields
            self.__showErrorMessage()
            return False

        # check if the input function f(x) is valid
        self.inputFunction = fx
        try:
            self.inputFunction = self.inputFunction.replace(" ", "").replace("^", "**").replace("sqrt", "np.sqrt")
            self.inputFunction = self.inputFunction.replace("e**", "np.exp").replace("log", "np.log10")  
            self.inputFunction = self.inputFunction.replace("sin", "np.sin").replace("cos", "np.cos").replace("tan", "np.tan")

        except:
            self.errorMessage = self.errorMessageInvalidFunction
            self.__showErrorMessage()
            return False
        

        # check if the min and max values of x are numbers
        self.minXValue = min
        self.maxXValue = max
        try:
            self.minXValue = float(self.minXValue)
            self.maxXValue = float(self.maxXValue)
        except:
            self.errorMessage =  self.errorMessageLimitsNotNumbers
            self.__showErrorMessage()
            return False
        
 
        if self.minXValue >= self.maxXValue:
            self.errorMessage = self.errorMessageInvalidLimits
            self.__showErrorMessage()
            return False

        return True


    # shows the error messages in a message box
    def __showErrorMessage(self):
        if self.errorMessage is not None:    
            self.setStyleSheet("QMessageBox{background:  self.backgroundColor; }"); # change the color theme in case of an error
            self.messageBox.warning(self, "Error", self.errorMessage, QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
            self.setStyleSheet("background-color:" + WINDOW_BACKGROUND_COLOR + ";"); # return the color theme to its original
            self.errorMessage = None
            self.__clearButtonHandler()


def run():
    # create the app
    app = QtWidgets.QApplication(sys.argv)

    main = Plotter()
    main.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()