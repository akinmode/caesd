#GUI classes for the application
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty

#Window.size = (1200, 800)

#FUNCTION classes for the application
from app_functions import AmpFunctions, RoomDesign
from app_constants import AppConstants

#Screens
class LaunchPage(Screen):
    pass

class CctvPage(Screen):
    dropManufacturer = ObjectProperty()
    dropModel = ObjectProperty()
    dropSensor = ObjectProperty()
    distFromCamera = ObjectProperty()
    sceneWidth = ObjectProperty()
    sceneHeight = ObjectProperty()
    sceneArea = ObjectProperty()
    focalLength = ObjectProperty()
    datastore = {
        'Manu_Model_pairs': [],
        'Manufacturer': '',
        'Model': '',
        'Sensor': '',
        'Distance': '',
        'Width': '',
        'Height': '',
        'Focal': '',
        'Area': ''
    }
    def selectedManufacturer(self):
        self.datastore['Manufacturer'] = self.dropManufacturer.text
        self.datastore['Manu_Model_pairs'] = AppConstants().manufacturerModels(self.dropManufacturer.text)
        self.dropModel.values = [i for i in self.datastore['Manu_Model_pairs'].keys()]
        pass
    def selectedModel(self):
        if self.dropModel.text != 'Model':
            self.datastore['Model'] = self.dropModel.text
            self.datastore['Sensor'] = self.datastore['Manu_Model_pairs'][self.dropModel.text]
            self.dropSensor.text = 'Sensor format: '+ self.datastore['Sensor']+'"'
            self.sensor_values = AppConstants().sensorsValues(self.datastore['Sensor'])
    def checkManufacturerModelSelected(self):
        if self.dropManufacturer.text != "" and self.dropModel.text != 'Model':
            return True
    def clearValues(self):
        if self.sceneWidth.text == '':
            self.sceneHeight.text = ''
            self.focalLength.text = ''
            self.sceneArea.text = ''
        elif self.sceneHeight.text == '':
            self.sceneWidth.text = ''
            self.focalLength.text = ''
            self.sceneArea.text = ''
    def calculateSceneDimensions(self, dimension, value):
        app = CAESD()
        if value != '':
            if self.checkManufacturerModelSelected():
                if self.distFromCamera.focus:
                    self.datastore['Distance'] = self.distFromCamera.text
                    if self.sceneWidth.text == '' or self.sceneHeight.text == '':
                        pass
                    else:
                        self.focalLength.text = str(round((float(self.sensor_values[0])*float(self.distFromCamera.text))/float(self.sceneWidth.text), 1))
                        self.sceneArea.text = str(round(float(self.sceneWidth.text)*float(self.sceneHeight.text), 2))
                elif self.sceneWidth.focus:
                    self.datastore['Height'] = ''
                    self.datastore['Width'] = self.sceneWidth.text
                    self.sceneHeight.text = str(round((float(self.sceneWidth.text)*float(self.sensor_values[1]))/float(self.sensor_values[0]), 1))
                    if self.distFromCamera.text != '':
                        self.focalLength.text = str(round((float(self.sensor_values[0])*float(self.distFromCamera.text))/float(self.sceneWidth.text), 1))
                    self.sceneArea.text = str(round(float(self.sceneWidth.text)*float(self.sceneHeight.text), 2))
                elif self.sceneHeight.focus:
                    self.datastore['Width'] = ''
                    self.datastore['Height'] = self.sceneHeight.text
                    self.sceneWidth.text = str(round((float(self.sceneHeight.text)*float(self.sensor_values[0]))/float(self.sensor_values[1]), 1))
                    if self.distFromCamera.text != '':
                        self.focalLength.text = str(round((float(self.sensor_values[1])*float(self.distFromCamera.text))/float(self.sceneHeight.text), 1))
                    self.sceneArea.text = str(round(float(self.sceneHeight.text)*float(self.sceneWidth.text), 2))
                else:
                    pass
            else:
                errorMessage = 'Please, Enter the load of the machine'
                app.popDisplays('Application Error', errorMessage)
        else:
            if self.distFromCamera.text == '':
                self.focalLength.text = ''
                self.clearValues()
            else:
                self.clearValues()

class LanDistributionPage(Screen):
    pass

class PowerPage(Screen):
    pass

class IlluminationPage(Screen):
    pass

#Main Screen Manager
class CAESDApp(ScreenManager):
    pass

main_kv = Builder.load_file("main.kv")
class CAESD(App):
    def build(self):
        self.title = 'Computer Aided Electrical Services Design'
        return main_kv

    def displayInLabelMessage(self, obj, **kwargs):
        obj.color = 1, 0, 0, 1
        obj.italic = False
        if kwargs == {}:
            #Default error message
            obj.text = 'Attention: Application Message'
        else:
            for i in kwargs.keys():
                if i == 'text' or i == 't':
                    obj.text = kwargs[i]
                elif i == 'color' or i == 'c':
                    obj.color = kwargs[i]
                elif i == 'italic' or i == 'i':
                    obj.italic = kwargs[i]

    def popDisplays(self, title, message, hint=(.7, .45)):
        Popup(title=title, title_color=[1,1,1,1],
                content=Label(text=message),
                size_hint=hint,
                separator_color=[1,1,0,.6]).open()

if __name__ == '__main__':
    CAESD().run()
