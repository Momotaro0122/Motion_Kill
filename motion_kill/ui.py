from PySide2 import QtWidgets
from PySide2 import QtCore
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance
import functions


def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class MotionKillerUI(QtWidgets.QDialog):
    def __init__(self, parent=maya_main_window()):
        super(MotionKillerUI, self).__init__(parent)

        self.setWindowTitle("Motion Killer")
        self.setMinimumWidth(200)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.choose_point_mode_radio_btn = QtWidgets.QRadioButton("Choose Point Mode")
        self.default_radio_btn = QtWidgets.QRadioButton("Default")
        self.head_radio_btn = QtWidgets.QRadioButton("Head")
        self.body_radio_btn = QtWidgets.QRadioButton("Body")
        self.choose_point_btn = QtWidgets.QPushButton("Choose Point")
        self.kill_motion_btn = QtWidgets.QPushButton("Kill Motion")

        self.default_radio_btn.setChecked(True)

    def create_layouts(self):
        mode_radio_btn_layout = QtWidgets.QHBoxLayout()
        mode_radio_btn_layout.addWidget(self.choose_point_mode_radio_btn)
        mode_radio_btn_layout.addWidget(self.default_radio_btn)

        default_radio_btn_layout = QtWidgets.QHBoxLayout()

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(mode_radio_btn_layout)
        main_layout.addLayout(default_radio_btn_layout)
        main_layout.addWidget(self.choose_point_btn)
        main_layout.addWidget(self.kill_motion_btn)

    def create_connections(self):
        self.choose_point_mode_radio_btn.toggled.connect(self.update_default_radio_buttons)
        self.default_radio_btn.toggled.connect(self.update_default_radio_buttons)
        self.choose_point_btn.clicked.connect(self.on_choose_point)
        self.kill_motion_btn.clicked.connect(self.on_kill_motion)

    def on_choose_point(self):
        self.mk = motion_killer()
        self.mk.run_steps()

    def on_kill_motion(self):
        if self.default_radio_btn.isChecked():
            if self.head_radio_btn.isChecked():
                point_to_kill = "head"  # Replace this with your actual method to get head
            else:
                point_to_kill = "body"  # Replace this with your actual method to get body
        else:  # Choose point mode button is clicked
            point_to_kill = self.chosen_point

        for obj in selected_objects:
            self.kill_motion_on_point(obj, point_to_kill)

    def kill_motion_on_point(self, obj, point):


    def show(self):
        self.mk = None
        super(MotionKillerUI, self).show()


def main():
    ui = MotionKillerUI()
    ui.show()


if __name__ == "__main__":
    main()