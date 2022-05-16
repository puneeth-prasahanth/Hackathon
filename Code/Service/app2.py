from gtts import gTTS
from flask import Flask, send_file, request, json, render_template
from pygame import mixer
import psycopg2


connection = psycopg2.connect(user = "postgres",
                                  password = "Puneeth@2",
                                  host = "localhost",
                                  database = "Hatcathon")


app = Flask(__name__)


@app.route("/user", methods=['POST', 'GET'])
def phonetic_name_prononce():
     """

     :return:
     """
     print(request.method)
     if request.method == 'POST':
          emp_id=json.dumps(request.form['emp_id'])
          emp_id=emp_id[1:-1]
          emp_id="'"+emp_id+"'"
          select_statment=f'select * from emp where emp_id={emp_id}'
          print(f'select_statment:{select_statment}')
          try:
              c = connection.cursor()
              # c.autocommit = True
              c.execute(select_statment)
          except Exception as e:
              print(f'Failed becouse of {e}')
          finally:
              data=c.fetchall()
              print(data)
              first_name=data[0][0]
              last_name=data[0][1]
              emp_id=data[0][2]
              audio=data[0][3]
              with open("sample.txt", "wb") as f:
                  f.write(audio)
              with open("sample.txt", "r") as f:
                  file_name = f.readline()
              print(file_name)
              mixer.init()
              mixer.music.load(file_name)
              mixer.music.play()

          return render_template('user_data.html', first_name=first_name,last_name=last_name,emp_id=emp_id)
     else:
         return render_template('user.html')




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
          entry_type=json.dumps(request.form['entry'])
          first_name=first_name[1:-1]
          last_name=last_name[1:-1]
          language=language[1:-1]
          emp_id=emp_id[1:-1]
          entry_type=entry_type[1:-1]
          t2s(first_name,last_name,language,emp_id,entry_type )
          return render_template('admin.html')
     else:
         return render_template('admin.html')

def t2s(*args):
    first_name=args[0]
    last_name=args[1]
    langu=args[2]
    emp_id=args[3]
    entry=args[4]
    name = first_name + last_name

    print(name,langu,entry)
    obj = gTTS(text = name, slow = False, lang = langu)
    audio=emp_id + '.mp3'
    obj.save(audio)
    print(obj)
    #mixer.init()
    #mixer.music.load(audio)
    #mixer.music.play()
    if entry.upper()=="INSERT":
        emp_insert_statment = f'INSERT INTO public.emp (first_name, last_name, emp_id, audio) ' \
                              f'VALUES {first_name,last_name,emp_id, audio}'
        print(f'emp_insert_statment:{emp_insert_statment}')
        try:
            c = connection.cursor()
            #c.autocommit = True
            c.execute(emp_insert_statment)
            connection.commit()
        except Exception as e:
            print(f'Failed becouse of {e}')
        finally:
            c.execute('''SELECT audio FROM emp''')
            mview = c.fetchone()
            print(mview[0])
            #data = open(mview[0]+'.'+mview[1], 'wb').write(mview[2])
            #song = AudioSegment.from_file(io.BytesIO(data), format="mp3")
            #play(song)
            #song = AudioSegment.from_file(io.BytesIO(data), format="mp3")
            #play(song)
            with open("test.mp3", "wb") as f:
                f.write(mview[0])
            with open("test.mp3", "r") as f:
                file_name=f.readline()
            print(file_name)
            mixer.init()
            mixer.music.load(file_name)
            mixer.music.play()
            #print(mview)

            if (connection):
                c.close()
                # connection.close()
    elif (entry).upper()=="UPDATE":
        emp_update_statment = f'UPDATE public.emp set audio='+audio+' where emp_id=emp_id '
        print(f'LDCS_insert_statment:{emp_update_statment}')
        try:
            cursor = connection.cursor()
            cursor.execute(emp_update_statment)
            connection.commit()
            #  connection.commit()
        except Exception as e:
            print(f'Failed becouse of {e}')
        finally:
            if (connection):
                cursor.close()
                # connection.close()


if __name__ == "__main__":
    app.run(debug=True)

