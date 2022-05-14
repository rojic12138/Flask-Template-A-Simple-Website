#罗皓
#2022年5月14日
from flask import Flask, render_template, request, redirect, url_for, make_response,jsonify,flash
import os
from wtforms import StringField, SelectMultipleField, RadioField,SubmitField
from flask_wtf import Form

#设置允许的文件格式
ALLOWED_EXTENSIONS = set(['jpg'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = "123456"
app.secret_key = "123456"

@app.route('/upload', methods=['POST', 'GET'])  # 添加路由
def upload():
#    path='static/images/6.png'
#    img = cv2.imread(path)
#    cv2.imwrite('static/images/test.jpg', img)
    
    if request.method == 'POST':
        f = request.files['file']
 
        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于mri"})
 
        user_input = request.form.get("name")#文件只能是英文名
 
        upload_path = os.path.join('static/images'+'/'+f.filename)  
        f.save(upload_path)
        
        img=Image.open(upload_path)
        if(f.filename.rsplit('.', 1)[1]=='png' or f.filename.rsplit('.', 1)[1]=='PNG'):
            img = img.convert("RGB")
        img_new=img.convert('L')
        img.save('static/images/pre.jpg')
        img_new.save('static/images/new.jpg')
        
        return render_template('patient_ok.html')
 
    return render_template('patient.html')

#计算数值
def cal(model):
    pCR=1
    TRG=2
    TNM_Stage=3
    return pCR,TRG,TNM_Stage

#计算计划
def get_plan():
    pass

class ModelForm(Form):
    model=RadioField('Model',choices=['Model1','Model2'])
    submit = SubmitField('Got')
    
pre,post=False,False
dose_has,time_has=False,False
analysis_has=False
@app.route('/patient',methods=['POST', 'GET'])
def patient():
    global pre,post,dose_has,time_has,analysis_has
    if request.method=='POST':
        print(request.form)
        if("model" in request.form):
            model=request.form['model']
            if(pre and post):
                pCR,TRG,TNM_Stage=cal(model)
                return render_template('test_ok.html', pCR=pCR,TRG=TRG,TNM_Stage=TNM_Stage)
            else:
                flash('Please choose files')
                
        if ("analysis" in request.form):
                analysis_has=True
                return render_template('analysis.html',lines=[])
            
        if("plan" in request.form):
            print(dose_has,time_has)
            if(dose_has and time_has):
                get_plan()
                f=open('static/files/plan.txt','r',encoding='utf-8')
                lines=f.readlines()
                f.close()
                return render_template('analysis_ok.html',lines=lines)
            else:
                return render_template('analysis.html',lines=[])
        
        try:
            dosefile=request.files['dosefile']
            dosefile.save('static/files/dosefile.txt')
            dose_has=True
        except:
            pass
        
        try:
            timefile=request.files['timefile']
            timefile.save('static/files/timefile.txt')
            time_has=True
        except:
            pass
        
        try:
            pre_image=request.files['prefile']
            pre_data=request.form.get('name')
            pre_image.save('static/images/pre_test.jpg')
            pre=True
        except:
            pass
        
        try:
            post_image=request.files['postfile']
            post_data=request.form.get('name')
            post_image.save('static/images/post_test.jpg')
            post=True
        except:
            pass
    
    if(analysis_has):
        return render_template('analysis.html',lines=[])
    #选择框
    form=ModelForm()
    return render_template('test.html',form=form)

if __name__ == '__main__':
    app.run()