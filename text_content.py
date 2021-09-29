import cv2
import docx2txt
import fitz
import imutils
import os
from pytesseract import image_to_string

class Document(object):
    def __init__(self, file_path):
        self.file = file_path
    
    def file_extension(self, file_name):
        '''return the extension or file type'''
        name, extension = os.path.splitext(file_name)
        return extension

    def file_text_content(self):
        '''return the text content of the file'''
        extension = self.file_extension(self.file)
        text_content = ''
        file = self.file
        if extension == ".docx":
             text_content = docx2txt.process(file)
        elif extension == ".doc":
            # we need run apt-get install -y antiword
            doc_file = file 
            docx_file = file +'x'    
            os.system('antiword ' + doc_file + ' > ' + docx_file)
            with open(docx_file) as f:
                    text_content = f.read()
            os.remove(docx_file)
        elif extension == ".pdf":
            read_pdf = fitz.open(file)
            number_of_pages = read_pdf.pageCount
            for i in range(number_of_pages):
                page_text = read_pdf.loadPage(i).getText("text")
                text_content += page_text
        elif extension in ['.jpg', '.png', '.jpeg', '.webp']:
            lang = "spa"
            image = self.transform_image(self.file)
            text_content = image_to_string(image, lang=lang)
        return text_content

    def transform_image(self, src_image):
        '''Return the transform image'''
        img = cv2.imread(src_image)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, img = cv2.threshold(img, 127, 255, cv2.THRESH_TRUNC)
        image_width, image_height = img.shape[:2]
        if image_height > 900:
            img = imutils.resize(img, height=900)
        return img
    
if __name__== '__main__':
    my_document = Document('my_document.pdf')
    text = my_document.file_text_content()
    print('Text Result: ', text)