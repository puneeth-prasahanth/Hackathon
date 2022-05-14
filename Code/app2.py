from gtts import gTTS
from flask import Flask, send_file, request, json, render_template
from pygame import mixer
import csv

app = Flask(__name__)

@app.route("/admin", methods=['POST', 'GET'])
def phonetic_name_update():
     """

     :return:
     """
     if request.method == 'POST':
          first_name = json.dumps(request.form['first_name'])
          # first_name=vals['first_name']
          last_name = json.dumps(request.form['last_name'])
          language = json.dumps(request.form['language'])
          emp_id=json.dumps(request.form['emp_id'])
          full_name = first_name + last_name
          t2s(full_name,language,emp_id )
          return render_template('admin.html')
     else:
         return render_template('admin.html')

def t2s(*args):
    name=args[0]
    langu=args[1]
    emp_id=args[2]

    print(name,langu)
    obj = gTTS(text = name, slow = False, lang = 'en')
    #audio_file=first+'.mp3'
    obj.save(emp_id+'.mp3')
    mixer.init()
    mixer.music.load(emp_id+'.mp3')
    mixer.music.play()
    #obj.runAndWait()
    #return send_file(emp_id+'.mp3')

if __name__ == "__main__":
    app.run(debug=True)

