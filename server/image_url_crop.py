from PIL import Image
import requests
from io import BytesIO
import base64


def pillow_image_to_base64_string(img):
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


def base64_string_to_pillow_image(base64_str):
    return Image.open(BytesIO(base64.decodebytes(bytes(base64_str, "utf-8"))))
    
    
def read_image_from_url(url, left=0, top=0, right=0, bottom=0):
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    x1, y1 = 0, 0
    x2, y2 = image.size
    # Setting the points for cropped image
    left = x1 + left
    if left >= x2:
        print("please check left value.")
        return image, ''
    top = y1 + top
    if top >= y2:
        print("please check top value.")
        return image, ''
    right = x2 - right
    if right <= left:
        print("please check right value.")
        return image, ''
    bottom = y2 - bottom
    if bottom <= top:
        print("please check bottom value.")
        return image, ''
    image = image.crop((left, top, right, bottom))
    data_url = 'data:image/jpeg;base64,' + pillow_image_to_base64_string(image)
    # You can put this data URL in the address bar of your browser to view the image
    cropped_image_html = '<img src={}>'.format(data_url) 
    return image, cropped_image_html 


if __name__ == '__main__':
    # Cropping from different values
    url = 'https://image.shutterstock.com/image-photo/man-his-30s-shows-disdain-260nw-2167588581.jpg'
    image, cropped_image_html  = read_image_from_url(url, left=-30, top=-50, right=-30, bottom=-50)
    image
    image, cropped_image_html  = read_image_from_url(url, left=30, top=50, right=30, bottom=50)
    image
    image, cropped_image_html  = read_image_from_url(url, left=0, top=0, right=0, bottom=20)
    image