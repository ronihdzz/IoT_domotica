# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'itemAlarmaEdit_dise.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.NonModal)
        Dialog.resize(380, 425)
        Dialog.setMinimumSize(QtCore.QSize(380, 425))
        Dialog.setMouseTracking(False)
        Dialog.setAcceptDrops(False)
        Dialog.setWindowTitle("")
        Dialog.setWindowOpacity(1.0)
        Dialog.setAutoFillBackground(False)
        Dialog.setStyleSheet("/*QWidget{\n"
"background-color: #d8d8d8;\n"
"}*/\n"
"\n"
"\n"
"QCheckBox {\n"
"    spacing: 5px;\n"
"}\n"
"\n"
"QCheckBox::indicator {\n"
"    width: 15px;\n"
"    height: 15px;\n"
"}\n"
"\n"
"QCheckBox::indicator:unchecked {\n"
"    border-image: url(:/PYQT5/IMAGENES/pyqt5/checkbox_unchecked.png);\n"
"}\n"
"\n"
"QCheckBox::indicator:unchecked:hover {\n"
"    border-image: url(:/PYQT5/IMAGENES/pyqt5/checkbox_unchecked_hover.png);\n"
"}\n"
"\n"
"QCheckBox::indicator:unchecked:pressed {\n"
"    border-image: url(:/PYQT5/IMAGENES/pyqt5/checkbox_unchecked_pressed.png);\n"
"}\n"
"\n"
"QCheckBox::indicator:checked {\n"
"    border-image: url(:/PYQT5/IMAGENES/pyqt5/checkbox_checked.png);\n"
"}\n"
"\n"
"QCheckBox::indicator:checked:hover {\n"
"    border-image: url(:/PYQT5/IMAGENES/pyqt5/checkbox_checked_hover.png);\n"
"}\n"
"\n"
"QCheckBox::indicator:checked:pressed {\n"
"    border-image: url(:/PYQT5/IMAGENES/pyqt5/checkbox_checked_pressed.png);\n"
"}\n"
"\n"
"QCheckBox::indicator:indeterminate:hover {\n"
"    border-image: url(:/PYQT5/IMAGENES/pyqt5/checkbox_indeterminate_hover.png);\n"
"}\n"
"\n"
"QCheckBox::indicator:indeterminate:pressed {\n"
"   border-image: url(:/PYQT5/IMAGENES/pyqt5 checkbox_indeterminate_pressed.png);\n"
"}")
        Dialog.setWindowFilePath("")
        Dialog.setInputMethodHints(QtCore.Qt.ImhNone)
        Dialog.setSizeGripEnabled(False)
        Dialog.setModal(True)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.layoutHor_2 = QtWidgets.QHBoxLayout()
        self.layoutHor_2.setObjectName("layoutHor_2")
        self.bel_secNombre = QtWidgets.QLabel(Dialog)
        self.bel_secNombre.setMinimumSize(QtCore.QSize(61, 31))
        self.bel_secNombre.setMaximumSize(QtCore.QSize(65, 35))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.bel_secNombre.setFont(font)
        self.bel_secNombre.setObjectName("bel_secNombre")
        self.layoutHor_2.addWidget(self.bel_secNombre)
        self.lineEdit_nombre = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_nombre.setMinimumSize(QtCore.QSize(110, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_nombre.setFont(font)
        self.lineEdit_nombre.setStyleSheet("QLineEdit {\n"
"    border: 1px solid gray;\n"
"    border-radius: 3px;\n"
"    padding: 1px 18px 1px 3px;\n"
"}")
        self.lineEdit_nombre.setObjectName("lineEdit_nombre")
        self.layoutHor_2.addWidget(self.lineEdit_nombre)
        self.bel_secAsunto = QtWidgets.QLabel(Dialog)
        self.bel_secAsunto.setMinimumSize(QtCore.QSize(51, 31))
        self.bel_secAsunto.setMaximumSize(QtCore.QSize(55, 35))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.bel_secAsunto.setFont(font)
        self.bel_secAsunto.setObjectName("bel_secAsunto")
        self.layoutHor_2.addWidget(self.bel_secAsunto)
        self.comBox_asunto = QtWidgets.QComboBox(Dialog)
        self.comBox_asunto.setMinimumSize(QtCore.QSize(114, 40))
        self.comBox_asunto.setMaximumSize(QtCore.QSize(150, 40))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.comBox_asunto.setFont(font)
        self.comBox_asunto.setStyleSheet("QComboBox {\n"
"    border: 1px solid gray;\n"
"    border-radius: 3px;\n"
"    padding: 1px 18px 1px 3px;\n"
"    /*min-width: 7em;*/\n"
"}\n"
"\n"
"QComboBox:editable {\n"
"    background: white;\n"
"}\n"
"\n"
"QComboBox:!editable, QComboBox::drop-down:editable {\n"
"     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                 stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,\n"
"                                 stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);\n"
"}\n"
"\n"
"/* QComboBox gets the \"on\" state when the popup is open */\n"
"QComboBox:!editable:on, QComboBox::drop-down:editable:on {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 #D3D3D3, stop: 0.4 #D8D8D8,\n"
"                                stop: 0.5 #DDDDDD, stop: 1.0 #E1E1E1);\n"
"}\n"
"\n"
"QComboBox:on { /* shift the text when the popup opens */\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid; /* just a single line */\n"
"    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"    border-bottom-right-radius: 3px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"/*/usr/share/icons/crystalsvg/16x16/actions/*/    \n"
"  /* image: url(:/PYQT5/IMAGENES/pyqt5/downarrow.png);*/\n"
" image: url(:/PYQT5/IMAGENES/pyqt5/down_arrow.png);\n"
"}\n"
"\n"
"QComboBox::down-arrow:on { /* shift the arrow when popup is open */\n"
"    top: 1px;\n"
"    left: 1px;\n"
"}")
        self.comBox_asunto.setObjectName("comBox_asunto")
        self.comBox_asunto.addItem("")
        self.comBox_asunto.addItem("")
        self.comBox_asunto.addItem("")
        self.comBox_asunto.addItem("")
        self.layoutHor_2.addWidget(self.comBox_asunto)
        self.verticalLayout_8.addLayout(self.layoutHor_2)
        self.layoutHor_3 = QtWidgets.QHBoxLayout()
        self.layoutHor_3.setObjectName("layoutHor_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.bel_1 = QtWidgets.QLabel(Dialog)
        self.bel_1.setMinimumSize(QtCore.QSize(25, 15))
        self.bel_1.setMaximumSize(QtCore.QSize(30, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.bel_1.setFont(font)
        self.bel_1.setAlignment(QtCore.Qt.AlignCenter)
        self.bel_1.setObjectName("bel_1")
        self.verticalLayout.addWidget(self.bel_1)
        self.cB_1 = QtWidgets.QCheckBox(Dialog)
        self.cB_1.setMinimumSize(QtCore.QSize(20, 20))
        self.cB_1.setMaximumSize(QtCore.QSize(30, 30))
        self.cB_1.setText("")
        self.cB_1.setChecked(False)
        self.cB_1.setAutoRepeat(False)
        self.cB_1.setTristate(False)
        self.cB_1.setObjectName("cB_1")
        self.verticalLayout.addWidget(self.cB_1)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.bel_2 = QtWidgets.QLabel(Dialog)
        self.bel_2.setMinimumSize(QtCore.QSize(25, 15))
        self.bel_2.setMaximumSize(QtCore.QSize(30, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.bel_2.setFont(font)
        self.bel_2.setAlignment(QtCore.Qt.AlignCenter)
        self.bel_2.setObjectName("bel_2")
        self.verticalLayout_3.addWidget(self.bel_2)
        self.cB_2 = QtWidgets.QCheckBox(Dialog)
        self.cB_2.setMinimumSize(QtCore.QSize(20, 20))
        self.cB_2.setMaximumSize(QtCore.QSize(30, 30))
        self.cB_2.setText("")
        self.cB_2.setChecked(False)
        self.cB_2.setAutoRepeat(False)
        self.cB_2.setTristate(False)
        self.cB_2.setObjectName("cB_2")
        self.verticalLayout_3.addWidget(self.cB_2)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.bel_3 = QtWidgets.QLabel(Dialog)
        self.bel_3.setMinimumSize(QtCore.QSize(25, 15))
        self.bel_3.setMaximumSize(QtCore.QSize(30, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.bel_3.setFont(font)
        self.bel_3.setAlignment(QtCore.Qt.AlignCenter)
        self.bel_3.setObjectName("bel_3")
        self.verticalLayout_4.addWidget(self.bel_3)
        self.cB_3 = QtWidgets.QCheckBox(Dialog)
        self.cB_3.setMinimumSize(QtCore.QSize(20, 20))
        self.cB_3.setMaximumSize(QtCore.QSize(30, 30))
        self.cB_3.setText("")
        self.cB_3.setChecked(False)
        self.cB_3.setAutoRepeat(False)
        self.cB_3.setTristate(False)
        self.cB_3.setObjectName("cB_3")
        self.verticalLayout_4.addWidget(self.cB_3)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.bel_4 = QtWidgets.QLabel(Dialog)
        self.bel_4.setMinimumSize(QtCore.QSize(25, 15))
        self.bel_4.setMaximumSize(QtCore.QSize(30, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.bel_4.setFont(font)
        self.bel_4.setAlignment(QtCore.Qt.AlignCenter)
        self.bel_4.setObjectName("bel_4")
        self.verticalLayout_6.addWidget(self.bel_4)
        self.cB_4 = QtWidgets.QCheckBox(Dialog)
        self.cB_4.setMinimumSize(QtCore.QSize(20, 20))
        self.cB_4.setMaximumSize(QtCore.QSize(30, 30))
        self.cB_4.setText("")
        self.cB_4.setChecked(False)
        self.cB_4.setAutoRepeat(False)
        self.cB_4.setTristate(False)
        self.cB_4.setObjectName("cB_4")
        self.verticalLayout_6.addWidget(self.cB_4)
        self.horizontalLayout.addLayout(self.verticalLayout_6)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.bel_5 = QtWidgets.QLabel(Dialog)
        self.bel_5.setMinimumSize(QtCore.QSize(25, 15))
        self.bel_5.setMaximumSize(QtCore.QSize(30, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.bel_5.setFont(font)
        self.bel_5.setAlignment(QtCore.Qt.AlignCenter)
        self.bel_5.setObjectName("bel_5")
        self.verticalLayout_5.addWidget(self.bel_5)
        self.cB_5 = QtWidgets.QCheckBox(Dialog)
        self.cB_5.setMinimumSize(QtCore.QSize(20, 20))
        self.cB_5.setMaximumSize(QtCore.QSize(30, 30))
        self.cB_5.setText("")
        self.cB_5.setChecked(False)
        self.cB_5.setAutoRepeat(False)
        self.cB_5.setTristate(False)
        self.cB_5.setObjectName("cB_5")
        self.verticalLayout_5.addWidget(self.cB_5)
        self.horizontalLayout.addLayout(self.verticalLayout_5)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.bel_6 = QtWidgets.QLabel(Dialog)
        self.bel_6.setMinimumSize(QtCore.QSize(25, 15))
        self.bel_6.setMaximumSize(QtCore.QSize(30, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.bel_6.setFont(font)
        self.bel_6.setAlignment(QtCore.Qt.AlignCenter)
        self.bel_6.setObjectName("bel_6")
        self.verticalLayout_7.addWidget(self.bel_6)
        self.cB_6 = QtWidgets.QCheckBox(Dialog)
        self.cB_6.setMinimumSize(QtCore.QSize(20, 20))
        self.cB_6.setMaximumSize(QtCore.QSize(30, 30))
        self.cB_6.setText("")
        self.cB_6.setChecked(False)
        self.cB_6.setAutoRepeat(False)
        self.cB_6.setTristate(False)
        self.cB_6.setObjectName("cB_6")
        self.verticalLayout_7.addWidget(self.cB_6)
        self.horizontalLayout.addLayout(self.verticalLayout_7)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.bel_7 = QtWidgets.QLabel(Dialog)
        self.bel_7.setMinimumSize(QtCore.QSize(25, 15))
        self.bel_7.setMaximumSize(QtCore.QSize(30, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.bel_7.setFont(font)
        self.bel_7.setAlignment(QtCore.Qt.AlignCenter)
        self.bel_7.setObjectName("bel_7")
        self.verticalLayout_2.addWidget(self.bel_7)
        self.cB_7 = QtWidgets.QCheckBox(Dialog)
        self.cB_7.setMinimumSize(QtCore.QSize(20, 20))
        self.cB_7.setMaximumSize(QtCore.QSize(30, 30))
        self.cB_7.setText("")
        self.cB_7.setChecked(False)
        self.cB_7.setAutoRepeat(False)
        self.cB_7.setTristate(False)
        self.cB_7.setObjectName("cB_7")
        self.verticalLayout_2.addWidget(self.cB_7)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.layoutHor_3.addLayout(self.horizontalLayout)
        self.timeEdit_hora = QtWidgets.QTimeEdit(Dialog)
        self.timeEdit_hora.setMinimumSize(QtCore.QSize(110, 40))
        self.timeEdit_hora.setMaximumSize(QtCore.QSize(150, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.timeEdit_hora.setFont(font)
        self.timeEdit_hora.setStyleSheet("      QTimeEdit {\n"
"            padding-right: 15px; /* make room for the arrows */\n"
"            border-image: url(:/PYQT5/IMAGENES/pyqt5/frame.png) 4;\n"
"            border-width: 3;\n"
"        }\n"
"       QTimeEdit::up-button {\n"
"            subcontrol-origin: border;\n"
"            subcontrol-position: top right; /* position at the top right corner */\n"
"            width: 16px; /* 16 + 2*1px border-width = 15px padding + 3px parent border */\n"
"            border-image: url(:/PYQT5/IMAGENES/pyqt5/spinup.png) 1;\n"
"            border-width: 1px;\n"
"        }\n"
"        QTimeEdit::up-button:hover {\n"
"            border-image: url(:/PYQT5/IMAGENES/pyqt5/spinup_hover.png) 1;\n"
"        }\n"
"        QTimeEdit::up-button:pressed {\n"
"            border-image: url(:/PYQT5/IMAGENES/pyqt5/spinup_pressed.png) 1;\n"
"        }\n"
"        QTimeEdit::up-arrow {\n"
"            image: url(:/PYQT5/IMAGENES/pyqt5/up_arrow.png);\n"
"            width: 7px;\n"
"            height: 7px;\n"
"        }\n"
"        QTimeEdit::up-arrow:disabled, QSpinBox::up-arrow:off { /* off state when value is max */\n"
"        image: url(:/PYQT5/IMAGENES/pyqt5/up_arrow_disabled.png);\n"
"        }\n"
"        QTimeEdit::down-button {\n"
"            subcontrol-origin: border;\n"
"            subcontrol-position: bottom right; /* position at bottom right corner */\n"
"            width: 16px;\n"
"            border-image: url(:/PYQT5/IMAGENES/pyqt5/spindown.png)1;\n"
"            border-width: 1px;\n"
"            border-top-width: 0;\n"
"        }\n"
"        QTimeEdit::down-button:hover {\n"
"            border-image: url(:/PYQT5/IMAGENES/pyqt5spindown_hover.png)1;\n"
"        }\n"
"        QTimeEdit::down-button:pressed {\n"
"            border-image: url(:/PYQT5/IMAGENES/pyqt5/spindown_pressed.png)1;\n"
"        }\n"
"        QTimeEdit::down-arrow {\n"
"            image: url(:/PYQT5/IMAGENES/pyqt5/down_arrow.png);\n"
"            width: 7px;\n"
"            height: 7px;\n"
"        }\n"
"        QTimeEdit::down-arrow:disabled,QSpinBox::down-arrow:off { /* off state when value in min */\n"
"        image: url(:/PYQT5/IMAGENES/pyqt5/down_arrow_disabled.png);\n"
"        }")
        self.timeEdit_hora.setAlignment(QtCore.Qt.AlignCenter)
        self.timeEdit_hora.setObjectName("timeEdit_hora")
        self.layoutHor_3.addWidget(self.timeEdit_hora)
        self.verticalLayout_8.addLayout(self.layoutHor_3)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.bel_secNombre_2 = QtWidgets.QLabel(Dialog)
        self.bel_secNombre_2.setMinimumSize(QtCore.QSize(150, 31))
        self.bel_secNombre_2.setMaximumSize(QtCore.QSize(65, 35))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.bel_secNombre_2.setFont(font)
        self.bel_secNombre_2.setAlignment(QtCore.Qt.AlignCenter)
        self.bel_secNombre_2.setObjectName("bel_secNombre_2")
        self.horizontalLayout_3.addWidget(self.bel_secNombre_2)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.verticalLayout_8.addLayout(self.horizontalLayout_3)
        self.tabWid_sonidosAlarmas = QtWidgets.QTabWidget(Dialog)
        self.tabWid_sonidosAlarmas.setMinimumSize(QtCore.QSize(350, 200))
        self.tabWid_sonidosAlarmas.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tabWid_sonidosAlarmas.setStyleSheet("QTabWidget::pane { /* The tab widget frame */\n"
"/* La linea encabezado que se encuentra abajo de los cuadros de seleccion*/\n"
"    border-top: 2px solid #C2C7CB;\n"
"}\n"
"\n"
"QTabWidget::tab-bar { \n"
"/*Que tan alejado se encuentra el primer cuadro de seleccion de la parte izquierda del TabWiget*/\n"
"   left: 5px; /* move to the right by 5px */\n"
"}\n"
"\n"
"/* Style the tab using the tab sub-control. Note that\n"
"    it reads QTabBar _not_ QTabWidget */\n"
"QTabBar::tab {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,\n"
"                                stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);\n"
"    border: 2px solid #C4C4C3; /*contorno de los cuadros de seleccion*/\n"
"   \n"
" /*linea de abajo del cuadro(s) que no esta(n) seleccionado(s)*/\n"
"    border-bottom-color:#C2C7CB; /* same as the pane color */\n"
"\n"
"    border-top-left-radius: 10px; /*curvatura de los cuadros de seleccion*/\n"
"    border-top-right-radius: 4px; /*curvatura de los cuadros de seleccion*/\n"
"    min-width: 120px; /*ancho de cada casila*/\n"
"    min-height:30px;/*alto de cada casilla*/\n"
"    padding: 2px;\n"
"   font: 12pt \"MS Shell Dlg 2\";\n"
"}\n"
"\n"
"QTabBar::tab:selected, QTabBar::tab:hover {\n"
"background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 #fafafa, stop: 0.4 #f4f4f4,\n"
"                                stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"    border-color:#9B9B9B;/*Color del borde de la casilla que esta seleccionada*/\n"
"   /*borde del suelo del cuadro que esta seleccionado*/ \n"
"   border-bottom-color: #C2C7CB; /* same as pane color */\n"
"}\n"
"\n"
"QTabBar::tab:!selected {\n"
"   /*tamaño de superiodida de alto del cuadro seleccionado y los que no*/\n"
"    margin-top: 2px; /* make non-selected tabs look smaller */\n"
"    font: 12pt \"MS Shell Dlg 2\"; /*Tamaño de letra de los cuadros que no estan\n"
"   seleccionados*/\n"
"}\n"
"\n"
"/* make use of negative margins for overlapping tabs */\n"
"QTabBar::tab:selected {\n"
"    /* expand/overlap to the left and right by 4px */\n"
"    margin-left: -4px;/*longitud que se alejara una casilla de la parte izquierda \n"
"   cuando este seleccionada*/\n"
"    margin-right: -4px;\n"
"}\n"
"\n"
"QTabBar::tab:first:selected {\n"
"    margin-left: 0; /* the first selected tab has nothing to overlap with on the left */\n"
"}\n"
"\n"
"QTabBar::tab:last:selected {\n"
" margin-right: 0; /* the last selected tab has nothing to overlap with on the right */\n"
"}\n"
"\n"
"QTabBar::tab:only-one {\n"
"    margin: 0; /* if there is only one tab, we don\'t want overlapping margins */\n"
"}")
        self.tabWid_sonidosAlarmas.setObjectName("tabWid_sonidosAlarmas")
        self.pistasDefault = QtWidgets.QWidget()
        self.pistasDefault.setObjectName("pistasDefault")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.pistasDefault)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.listWid_soniDef = QtWidgets.QListWidget(self.pistasDefault)
        self.listWid_soniDef.setMinimumSize(QtCore.QSize(0, 100))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.listWid_soniDef.setFont(font)
        self.listWid_soniDef.setStyleSheet("QListWidget {\n"
"    show-decoration-selected: 1; /* make the selection span the entire width of the view */\n"
"}\n"
"\n"
"QListWidget::item:alternate {\n"
"    background: #EEEEEE;\n"
"}\n"
"\n"
"QListWidget::item:selected {\n"
"    border: 1px solid #6a6ea9;\n"
"}\n"
"\n"
"QListWidget::item:selected:!active {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 #ABAFE5, stop: 1 #8588B2);\n"
"}\n"
"\n"
"QListWidget::item:selected:active {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 #6a6ea9, stop: 1 #888dd9);\n"
"}\n"
"\n"
"QListWidget::item:hover {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 #FAFBFE, stop: 1 #DCDEF1);\n"
"}\n"
"\n"
"/*QListWidget\n"
"{\n"
"background : rgb(219, 235, 235);\n"
"}\n"
"\n"
"QListWidget QScrollBar\n"
"{\n"
"background-color: rgb(219, 235, 235);\n"
"}\n"
"\n"
" QListView::item:selected\n"
"{\n"
"background-color: rgb(249, 196, 255);\n"
"color: rgb(0, 0, 0);\n"
"}*/")
        self.listWid_soniDef.setObjectName("listWid_soniDef")
        self.verticalLayout_11.addWidget(self.listWid_soniDef)
        self.tabWid_sonidosAlarmas.addTab(self.pistasDefault, "")
        self.pistasMias = QtWidgets.QWidget()
        self.pistasMias.setObjectName("pistasMias")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.pistasMias)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_6 = QtWidgets.QLabel(self.pistasMias)
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_5.addWidget(self.label_6)
        self.btn_addCancion = QtWidgets.QPushButton(self.pistasMias)
        self.btn_addCancion.setMinimumSize(QtCore.QSize(25, 30))
        self.btn_addCancion.setMaximumSize(QtCore.QSize(30, 35))
        self.btn_addCancion.setStyleSheet("QPushButton {\n"
"    border-image: url(:/ALARMA/IMAGENES/ALARMA/subir_off.png);\n"
" }\n"
"QPushButton:hover {\n"
"border-image: url(:/ALARMA/IMAGENES/ALARMA/subir_on.png);\n"
"}\n"
"QPushButton:pressed {\n"
"border-image: url(:/ALARMA/IMAGENES/ALARMA/subir_off.png);\n"
"}\n"
"")
        self.btn_addCancion.setText("")
        self.btn_addCancion.setObjectName("btn_addCancion")
        self.horizontalLayout_5.addWidget(self.btn_addCancion)
        self.verticalLayout_10.addLayout(self.horizontalLayout_5)
        self.listWid_soniMio = QtWidgets.QListWidget(self.pistasMias)
        self.listWid_soniMio.setMinimumSize(QtCore.QSize(0, 100))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.listWid_soniMio.setFont(font)
        self.listWid_soniMio.setStyleSheet("QListWidget {\n"
"    show-decoration-selected: 1; /* make the selection span the entire width of the view */\n"
"}\n"
"\n"
"QListWidget::item:alternate {\n"
"    background: #EEEEEE;\n"
"}\n"
"\n"
"QListWidget::item:selected {\n"
"    border: 1px solid #6a6ea9;\n"
"}\n"
"\n"
"QListWidget::item:selected:!active {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 #ABAFE5, stop: 1 #8588B2);\n"
"}\n"
"\n"
"QListWidget::item:selected:active {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 #6a6ea9, stop: 1 #888dd9);\n"
"}\n"
"\n"
"QListWidget::item:hover {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 #FAFBFE, stop: 1 #DCDEF1);\n"
"}\n"
"\n"
"/*QListWidget\n"
"{\n"
"background : rgb(219, 235, 235);\n"
"}\n"
"\n"
"QListWidget QScrollBar\n"
"{\n"
"background-color: rgb(219, 235, 235);\n"
"}\n"
"\n"
" QListView::item:selected\n"
"{\n"
"background-color: rgb(249, 196, 255);\n"
"color: rgb(0, 0, 0);\n"
"}*/")
        self.listWid_soniMio.setObjectName("listWid_soniMio")
        self.verticalLayout_10.addWidget(self.listWid_soniMio)
        self.tabWid_sonidosAlarmas.addTab(self.pistasMias, "")
        self.verticalLayout_8.addWidget(self.tabWid_sonidosAlarmas)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setText("")
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.btn_finalizar = QtWidgets.QPushButton(Dialog)
        self.btn_finalizar.setMinimumSize(QtCore.QSize(110, 40))
        self.btn_finalizar.setMaximumSize(QtCore.QSize(150, 50))
        self.btn_finalizar.setStyleSheet("QPushButton:hover {\n"
"    background-color: #DDE8E8; \n"
"    border: 1px solid #DAE7E7;\n"
"    border-radius: 7px;\n"
"}\n"
"\n"
"QPushButton {\n"
"    background-color: #DDE8E8; \n"
"    border: 1px solid #B1BCBC;\n"
"    border-radius: 7px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color:#B8C0C0;\n"
"    border: 1px solid #B8C0C0;\n"
"    border-radius: 7px;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color: rgb(170, 170, 127)\n"
"}")
        self.btn_finalizar.setObjectName("btn_finalizar")
        self.horizontalLayout_2.addWidget(self.btn_finalizar)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.verticalLayout_8.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        self.tabWid_sonidosAlarmas.setCurrentIndex(0)
        self.listWid_soniDef.setCurrentRow(-1)
        self.listWid_soniMio.setCurrentRow(-1)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        self.bel_secNombre.setText(_translate("Dialog", "Nombre:"))
        self.bel_secAsunto.setText(_translate("Dialog", "Asunto:"))
        self.comBox_asunto.setItemText(0, _translate("Dialog", "Despertar"))
        self.comBox_asunto.setItemText(1, _translate("Dialog", "Dormir"))
        self.comBox_asunto.setItemText(2, _translate("Dialog", "Deberes"))
        self.comBox_asunto.setItemText(3, _translate("Dialog", "Otro"))
        self.bel_1.setText(_translate("Dialog", "L"))
        self.cB_1.setShortcut(_translate("Dialog", "Backspace, Backspace"))
        self.bel_2.setText(_translate("Dialog", "Ma"))
        self.cB_2.setShortcut(_translate("Dialog", "Backspace, Backspace"))
        self.bel_3.setText(_translate("Dialog", "Mi"))
        self.cB_3.setShortcut(_translate("Dialog", "Backspace, Backspace"))
        self.bel_4.setText(_translate("Dialog", "Ju"))
        self.cB_4.setShortcut(_translate("Dialog", "Backspace, Backspace"))
        self.bel_5.setText(_translate("Dialog", "Vi"))
        self.cB_5.setShortcut(_translate("Dialog", "Backspace, Backspace"))
        self.bel_6.setText(_translate("Dialog", "Sa"))
        self.cB_6.setShortcut(_translate("Dialog", "Backspace, Backspace"))
        self.bel_7.setText(_translate("Dialog", "Do"))
        self.cB_7.setShortcut(_translate("Dialog", "Backspace, Backspace"))
        self.bel_secNombre_2.setText(_translate("Dialog", "Musica de alarma:"))
        self.tabWid_sonidosAlarmas.setTabText(self.tabWid_sonidosAlarmas.indexOf(self.pistasDefault), _translate("Dialog", "Pistas default"))
        self.tabWid_sonidosAlarmas.setTabText(self.tabWid_sonidosAlarmas.indexOf(self.pistasMias), _translate("Dialog", "Mis pistas"))
        self.btn_finalizar.setText(_translate("Dialog", "GUARDAR"))

import IMAG_rc
