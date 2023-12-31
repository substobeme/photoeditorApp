from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.core.window import Window
from plyer import filechooser
from PIL import Image,ImageFilter
from io import BytesIO
from kivy.core.image import Image as I
Window.size=(800,600)
class Interface(MDBoxLayout):
    #open and select image
    def import1(self):
        self.img = filechooser.open_file(title="Import image", filters=[("Image Files", "*.png;*.jpg;*.jpeg")]) #filers inside a tupple inside a list
        if self.img:
            self.ids.screen.source = self.img[0] #update source of Image with id= img_screen to the choosen image which is first member of list img
            self.ids.Rotate.text='0' #default value of rotation
            self.ids.Rotate.focus=True #prevent overlapp
            self.edit=Image.open(self.img[0])#to get the imported image to become editable using PIL library, self to access variable outside function
            self.ids.WDH.text= str(self.edit.width)
            self.ids.WDH.focus= True
            self.ids.H8.text= str(self.edit.height)
            self.ids.H8.focus= True

    def apply(self):
        #Editing
        
        resized=self.edit.resize((int(self.ids.WDH.text),int(self.ids.H8.text)))#input height and width from text input in textfield
        #Rotation
        rotated= resized.rotate(int(self.ids.Rotate.text))#taking input from user in textfield,converting to integer and rotating
        #options on image
         # List to store selected effects
        selected_effects = []
        if self.ids.e1.active:
            selected_effects.append(ImageFilter.FIND_EDGES)
        if self.ids.e2.active:
            selected_effects.append(ImageFilter.CONTOUR)
        if self.ids.e3.active:
            selected_effects.append(ImageFilter.BLUR)
        if self.ids.e4.active:
            selected_effects.append(ImageFilter.DETAIL)
        if self.ids.e5.active:
            selected_effects.append(ImageFilter.SHARPEN)
        if self.ids.e6.active:
            selected_effects.append("grayscale")
        
        
        
        # Apply selected effects
        self.final_edit = rotated
        for effect in selected_effects:
            if effect == "grayscale":
                self.final_edit = self.final_edit.convert("L")  # Convert to grayscale
            else:
                self.final_edit = self.final_edit.filter(effect)
       


        data=BytesIO()
        self.final_edit.save(data,format='png') #pointer at end after saving so need to move to front using seek function
        data.seek(0) #0 is beggining, 1 is current position, 2 is end
        b= BytesIO(data.read())#reading the data and converting to Bytes object
        img1=I(b,ext='png')#convert byte object to kivy object which is image/texture
        self.ids.screen.texture=img1.texture
    def select(self,location):
        l= str(location[0])+ '\\Customname.jpg'
        self.final_edit.save(l) #saving in the location l
    def exportImage(self):
        filechooser.choose_dir(title="Save to?",on_selection=self.select)#choosing directory





        

class PhotoEditorApp(MDApp):
    def build(self):
        pass

PhotoEditorApp().run()
