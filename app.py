from flask import Flask, request, render_template, redirect, flash, session
from surveys import *
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "chickenz"

#debug = DebugToolbarExtension(app)

#responses = []

@app.route("/")
def start():
    """Render landing page"""
    if(session.get("survey", None) != None):del session["survey"]
    return render_template("start.html",
        title = "Landing Page",
        header = "Select Survey",
        options=surveys.keys())
        
@app.route("/questions/<num>")
def run_survey(num):
    """Run survey"""
    survey_key_name = session.get("survey",False)
    if(not survey_key_name):
        flash("No survey selected. Redirecting")
        return redirect("/")
    current_survey = surveys[survey_key_name]
        
    
    if(num != str(len(session["responses"])+1) and not (session["responses"] ==[] and num == "0")): 
        flash("Attempted to go to invalid question")
        return redirect("/questions/"+str(len(session["responses"])+1))
    if(num == "0"):
        return render_template("survey.html",
            title = "Survey",
            header = current_survey.title,
            instr = current_survey.instructions,
            next_num = 1,
            button_text="Begin")
            
    elif(int(num) <= len(current_survey.questions)):
        cur_question = current_survey.questions[int(num)-1]
        return render_template("survey.html",
            title = "Survey",
            header = cur_question.question,
            next_num = int(num)+1,
            choices = cur_question.choices,
            question = True,
            button_text="Next Question")
            
    else:
        return render_template("survey.html",
            title = "Survey",
            header = "End of survey",
            instr = "Thank you for finishing the survey",
            next_num = "finish",
            finished = True,
            button_text="Finish")
            
            
@app.route("/answers")
def handle_ans():
    if(request.args.get("ans",False)): session["responses"]+=[request.args["ans"]]
    return redirect("questions/"+str(len(session["responses"])+1))
    
@app.route("/init")
def initialize():
    session["survey"] =  request.args.get("survey","ERR: Bad survey key")
    session["responses"] = []
    return redirect("/questions/0")
@app.route("/resp")
def resp_check():
    res = "Survey is currently: " + session.get("survey","undefined")+ " "
    for resp in session["responses"]: res += resp + " "
    return render_template("resp.html", res = res)
