import os, datetime
from flask import Flask, render_template, send_from_directory, request

# lazy config
username = os.getlogin()
if username == 'pi':
    FOLDER_TO_SAVE_IMAGES_TO = '/media/usb'
elif username == 'manoj':
    FOLDER_TO_SAVE_IMAGES_TO = '/Users/manoj/Downloads/usbstick'

app = Flask(__name__)


@app.route('/')
def hello():
    files = os.listdir(FOLDER_TO_SAVE_IMAGES_TO)
    files = sorted(files, reverse=True)
    total_image_count = 0
    images = []
    for image in files:
        if '.jpg' in image:
            images.append('/image/{}'.format(image))
            total_image_count += 1
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template(
        'index.html',
        images=images[:30],
        total_image_count=total_image_count,
        timestamp=timestamp)

@app.route('/image/<path:filename>')
def base_static(filename):
    return send_from_directory(FOLDER_TO_SAVE_IMAGES_TO, filename)

@app.route('/image/delete/', methods=['POST'])
def delete_image():
    image = request.form["image"].split("/")[2]
    move_from = FOLDER_TO_SAVE_IMAGES_TO + "/" + image
    move_to = FOLDER_TO_SAVE_IMAGES_TO + "/deleted/" + image
    os.rename(move_from, move_to)
    return "Deleting img: {}".format(image)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
