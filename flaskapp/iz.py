from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
 return " <html><head></head> <body> Enter </body></html>"

from flask import render_template

from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField

from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired
import scipy.ndimage.interpolation as interp

SECRET_KEY = 'secret'
app.config['SECRET_KEY'] = SECRET_KEY

app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LcDoScbAAAAANOWBHNB3QnRTxrJvpOItbhMBKsL'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LcDoScbAAAAAB2vlAIbxvkMUqoI90VBDX_Ix7M8'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}

from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)

class NetForm(FlaskForm):

 cho = StringField('Введите угол поворота', validators = [DataRequired()])

 upload = FileField('Load image', validators=[
 FileRequired(),
 FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])

 recaptcha = RecaptchaField()

 submit = SubmitField('send')

from werkzeug.utils import secure_filename
import os

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns


def draw(filename,cho):
 print(filename)
 img= Image.open(filename)
 x, y = img.size
 cho=int(cho)
 ##gra
 fig = plt.figure(figsize=(6, 4))
 ax = fig.add_subplot()
 data = np.random.randint(0, 255, (100, 100))
 ax.imshow(img, cmap='plasma')
 b = ax.pcolormesh(data, edgecolors='black', cmap='plasma')
 fig.colorbar(b, ax=ax)
 gr_path = "./static/newgr.png"
 sns.displot(data)
 plt.savefig(gr_path)
 plt.close()
 
 
 #img = Image.rotate(input=img, angle=cho, axes=(0,1), reshape = False)
 
 img=img.rotate(cho)
 output_filename = filename
 img.save(output_filename)
 
 fig = plt.figure(figsize=(6, 4))
 ax = fig.add_subplot()
 data = np.random.randint(0, 255, (100, 100))
 ax.imshow(img, cmap='plasma')
 b = ax.pcolormesh(data, edgecolors='black', cmap='plasma')
 fig.colorbar(b, ax=ax)
 gr_path2 = "./static/newgr2.png"
 sns.displot(data)
 plt.savefig(gr_path2)
 plt.close()
 return output_filename,gr_path,gr_path2

@app.route("/net",methods=['GET', 'POST'])
def net():

 form = NetForm()

 filename=None
 newfilename=None
 grname=None
 grname2=None
 if form.validate_on_submit():

  filename = os.path.join('./static', secure_filename(form.upload.data.filename))
  ch=form.cho.data
 
  form.upload.data.save(filename)
  newfilename,grname,grname2 = draw(filename,ch)

 
 return render_template('net.html',form=form,image_name=newfilename,gr_name=grname,gr_name2=grname2)


if __name__ == "__main__":
 app.run(host='127.0.0.1',port=5000)
