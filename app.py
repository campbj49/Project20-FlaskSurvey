from flask import Flask, request, render_template, redirect, flash
from surveys import *
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "chickenz"

#debug = DebugToolbarExtension(app)

responses = []
drv = []

@app.route("/")
def start():
    """Render landing page"""
    return render_template("start.html",
        title = "Landing Page",
        header = "Select Survey",
        options=surveys.keys())
        
@app.route("/questions/<num>")
def run_survey(num):
    """Run survey"""
    survey_key_name = request.args.get("survey","ERR: Bad survey key")
    current_survey = surveys[survey_key_name]
    global responses
    global drv
        
    
    if(num != str(len(responses)+1) and not (responses ==[] and num == "0")): 
        drv +=[str(len(responses))+" is the current len and num is " + num]
        flash("Attempted to go to invalid question")
        return redirect("/questions/"+str(len(responses)+1)+"?survey="+survey_key_name)
    if(num == "0"):
        return render_template("survey.html",
            title = "Survey",
            header = current_survey.title,
            instr = current_survey.instructions,
            next_num = 1,
            survey = survey_key_name,
            button_text="Begin")
            
    elif(int(num) <= len(current_survey.questions)):
        cur_question = current_survey.questions[int(num)-1]
        return render_template("survey.html",
            title = "Survey",
            header = cur_question.question,
            next_num = int(num)+1,
            choices = cur_question.choices,
            question = True,
            survey = survey_key_name,
            button_text="Next Question")
            
    else:
        return render_template("survey.html",
            title = "Survey",
            header = "End of survey",
            instr = "Thank you for finishing the survey",
            next_num = "finish",
            finished = True,
            survey = survey_key_name,
            button_text="Finish")
            
            
@app.route("/answers")
def handle_ans():
    global responses
    if(request.args.get("ans",False)): responses+=[request.args["ans"]]
    return redirect("questions/"+str(len(responses)+1)+"?survey="+request.args.get("survey","ERR: Bad survey key"))
    
@app.route("/resp")
def resp_check():
    global drv
    res = "Errors are currently: " + str(len(drv))+ " "
    for resp in responses: res += resp + " "
    return render_template("resp.html", res = res)
        
        
        
"""
This error catching nonsense is really kicking my teeth in. Sketch as it stands:
instruction page. ignore error if responses are empty
load q1 resp is still empty. 
load q2 resp len = 1
clicking away should redirect to 2, but even if it does it risks re-entering a responses
think that putting the data collection into a redirect will make this more managable
How do I prevent navigating to 1 causing an endless loop of redirecting to 0 while also not 
having navigating to 0 immediatly causing a redirect to 1?

"""
