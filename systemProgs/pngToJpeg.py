
#importing the required package 
from PIL import Image 
  
#open image in png format 
img_png = Image.open("C:/Users/DELL/Downloads/free.png") 
if img_png.mode == 'RGBA':
    img_png = img_png.convert('RGB')
#The image object is used to save the image in jpg format 
img_png.save('C:/Users/DELL/Downloads/outputPng.jpeg',format='JPEG')