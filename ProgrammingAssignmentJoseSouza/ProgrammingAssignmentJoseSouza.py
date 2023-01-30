import ctk
import logging
import qt
import slicer
import vtk
from slicer.ScriptedLoadableModule import *

class ProgrammingAssignmentJoseSouza(ScriptedLoadableModule):
    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        applicant_name = "Jose Souza"
        self.parent.title = "Programming Assignment: {}".format(applicant_name)
        self.parent.categories = ["Programming Assignment"]
        self.parent.dependencies = []
        self.parent.contributors = [applicant_name]
        self.parent.helpText = ""
        self.parent.acknowledgementText = ""


class ProgrammingAssignmentJoseSouzaWidget(ScriptedLoadableModuleWidget):
    def setup(self):
        ScriptedLoadableModuleWidget.setup(self)

        # Instantiate and connect widgets ...
        self.logic = ProgrammingAssignmentJoseSouzaLogic()

        #
        # Parameters Area
        #
        parameters_collapsible_button = ctk.ctkCollapsibleButton()
        parameters_collapsible_button.text = "Parameters"
        self.layout.addWidget(parameters_collapsible_button)

        # Layout within the dummy collapsible button
        parameters_form_layout = qt.QFormLayout(parameters_collapsible_button)

        #
        # input volume selector
        #
        self.input_selector = slicer.qMRMLNodeComboBox()
        self.input_selector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
        self.input_selector.selectNodeUponCreation = True
        self.input_selector.addEnabled = False
        self.input_selector.removeEnabled = False
        self.input_selector.noneEnabled = False
        self.input_selector.showHidden = False
        self.input_selector.showChildNodeTypes = False
        self.input_selector.setMRMLScene(slicer.mrmlScene)
        self.input_selector.setToolTip("Pick the input to the algorithm.")
        parameters_form_layout.addRow("Input Volume: ", self.input_selector)

        #
        # output volume selector
        #
        self.output_selector = slicer.qMRMLNodeComboBox()
        self.output_selector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
        self.output_selector.selectNodeUponCreation = True
        self.output_selector.addEnabled = True
        self.output_selector.renameEnabled = True
        self.output_selector.removeEnabled = True
        self.output_selector.noneEnabled = False
        self.output_selector.showHidden = False
        self.output_selector.showChildNodeTypes = False
        self.output_selector.setMRMLScene(slicer.mrmlScene)
        self.output_selector.setToolTip("Pick the output to the algorithm.")
        parameters_form_layout.addRow("Output Volume: ", self.output_selector)

        #
        # threshold value
        #
        self.image_threshold_slider_vidget = ctk.ctkSliderWidget()
        self.image_threshold_slider_vidget.singleStep = 0.01
        self.image_threshold_slider_vidget.minimum = 0
        self.image_threshold_slider_vidget.maximum = 1
        self.image_threshold_slider_vidget.value = 0.5
        parameters_form_layout.addRow("Image threshold", self.image_threshold_slider_vidget)
        
        #
        # Invert classification checkbox
        #
        self.invert_check_box = qt.QCheckBox()
        parameters_form_layout.addRow("Invert", self.invert_check_box)

        #
        # Apply Button
        #
        self.apply_button = qt.QPushButton("Apply")
        self.apply_button.toolTip = "Run the algorithm."
        self.apply_button.enabled = False
        parameters_form_layout.addRow(self.apply_button)

        # connections
        self.enter()
        self.apply_button.connect('clicked()', self.onApplyButton)
        self.input_selector.connect('currentNodeChanged(vtkMRMLNode*)', self.onInputChanged)
        self.output_selector.connect('currentNodeChanged(vtkMRMLNode*)', self.onOutputChanged)

        # Add vertical spacer
        self.layout.addStretch(1)

    def enter(self):
        if self.input_selector.currentNode() is not None:
            self.logic.updateRange(self.input_selector.currentNode(), self.image_threshold_slider_vidget)

    def onApplyButton(self):
        with slicer.util.tryWithErrorDisplay("Failed to compute results.", waitCursor=True):

            self.logic.run(
                self.input_selector.currentNode(),
                self.output_selector.currentNode(),
                self.image_threshold_slider_vidget.value,
                self.invert_check_box.isChecked()
            )

            slicer.util.setSliceViewerLayers(background = self.output_selector.currentNode())
            slicer.util.resetSliceViews()

    def onInputChanged(self):
        self.apply_button.enabled = self.input_selector.currentNode() is not None

        if self.apply_button.enabled:
            self.logic.updateRange(self.input_selector.currentNode(), self.image_threshold_slider_vidget)

    def onOutputChanged(self):
        self.apply_button.enabled = self.output_selector.currentNode() is not None and (self.input_selector.currentNode().GetID() !=
                            self.output_selector.currentNode().GetID())    

    def cleanup(self):
        pass


class ProgrammingAssignmentJoseSouzaLogic(ScriptedLoadableModuleLogic):
    def has_image_data(self, volume_node):
        if not volume_node:
            logging.debug("has_image_data failed: no volume node")
            return False
        if volume_node.GetImageData() is None:
            logging.debug("has_image_data failed: no image data in volume node")
            return False
        return True

    def is_valid_input_output_data(self, input_volume_node, output_volume_node):
        if not input_volume_node:
            logging.debug("is_valid_input_output_data failed: no input volume node defined")
            return False
        if not output_volume_node:
            logging.debug("is_valid_input_output_data failed: no output volume node defined")
            return False
        if input_volume_node.GetID() == output_volume_node.GetID():
            logging.debug(
                "is_valid_input_output_data failed: input and output volume is the same. Create a new volume for output to avoid this error."
            )
            return False
        return True

    def updateRange(self, input_volume, slider):
        input_range = input_volume.GetImageData().GetScalarRange()
        slider.minimum = input_range[0]
        slider.maximum = input_range[1]
        slider.value = (input_range[1] + input_range[0])/2
        slider.singleStep = (input_range[1] - input_range[0])/100

    def run(self, input_volume, output_volume, image_threshold, invert):
        if not self.is_valid_input_output_data(input_volume, output_volume):
            slicer.util.errorDisplay("Input volume is the same as output volume. Choose a different output volume.")
            return False

        if image_threshold < input_volume.GetImageData().GetScalarRange()[0] or image_threshold > input_volume.GetImageData().GetScalarRange()[1]:
            slicer.util.errorDisplay("Invalid threshold selected. Choose a valid value")
            return False        

        output_image = vtk.vtkImageData()
        output_image.SetDimensions(input_volume.GetImageData().GetDimensions())
        output_image.AllocateScalars(vtk.VTK_UNSIGNED_CHAR, 1)
        output_image.GetPointData().GetScalars().Fill(0)

        output_volume.SetOrigin(input_volume.GetOrigin())
        output_volume.SetSpacing(input_volume.GetSpacing())
        dirs = [[0,0,1],[-1,0,0],[0,-1,0]]
        output_volume.SetIJKToRASDirections(dirs)
        output_volume.SetAndObserveImageData(output_image)
        output_volume.CreateDefaultDisplayNodes()
        output_volume.CreateDefaultStorageNode()

        threshold_mask = slicer.util.arrayFromVolume(input_volume) < image_threshold if invert else \
                            slicer.util.arrayFromVolume(input_volume) > image_threshold

        slicer.util.arrayFromVolume(output_volume)[threshold_mask] = 1

        output_volume.Modified()

        return True


class ProgrammingAssignmentJoseSouzaTest(ScriptedLoadableModuleTest):
    def setUp(self):
        slicer.mrmlScene.Clear(0)

    def runTest(self):
        self.setUp()
        self.test_assignment_logic()

    def test_assignment_logic(self):
        self.delayDisplay("Starting the test")
        
        import SampleData
        self.delayDisplay("Load source volume")

        input_volume = SampleData.downloadSample('MRHead')
        output_volume = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLScalarVolumeNode", 'test_node')

        inputScalarRange = input_volume.GetImageData().GetScalarRange()
        minTreshold = inputScalarRange[0]
        maxTreshold = inputScalarRange[1]
        medianThreshold = (inputScalarRange[1] + inputScalarRange[1])/2

        logic = ProgrammingAssignmentJoseSouzaLogic()
        
        # Invalid threshold args
        self.assertFalse(logic.run(input_volume, output_volume, minTreshold - 10, False))
        self.assertFalse(logic.run(input_volume, output_volume, maxTreshold + 10, False))

        # Invalid volume args
        self.assertFalse(logic.run(None, None, 100, False))
        self.assertFalse(logic.run(input_volume, input_volume, 100, False))
        
        # Correct arguments for binary thresholding
        self.assertTrue(logic.run(input_volume, output_volume, medianThreshold, False))
        self.assertTrue(logic.run(input_volume, output_volume, medianThreshold, True))
            
        self.delayDisplay('test_Threshold passed!')

        pass
