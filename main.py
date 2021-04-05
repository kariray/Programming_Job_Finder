"""
https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs

"""
from flask import Flask, render_template, request,redirect, send_file
from remote import get_jobs as remote_jobs
from we_work import get_jobs as we_work_jobs
from stackoverflow import get_jobs as stack_jobs
from save import save_to_file

app = Flask("ProgrammingJobFinder")

db={}

@app.route("/")
def home():
  return render_template("index.html")


@app.route("/report")
def report():
  word=request.args.get("word")
  jobs=[]
  if word:
    word=word.lower()
    existingJobs=db.get(word)
    if existingJobs:
      jobs=existingJobs
    else:
      jobs=remote_jobs(word)+we_work_jobs(word)+stack_jobs(word)
      db[word]=jobs
    print(jobs)
  else:
    return redirect("/")
  return render_template("report.html",searchingBy=word, resultsNumber=len(jobs),jobs=jobs)

@app.route("/export")
def export():
  try:
    word=request.args.get("word")
    if not word:
      raise Exception()
    word=word.lower()
    jobs=db.get(word)
    if not jobs:
      raise Exception()
    save_to_file(jobs,word)
    return send_file(f"{word}.csv",mimetype='text/csv',attachment_filename=f'{word}.csv',as_attachment=True)
  except:
    return redirect("/")

app.run(host="0.0.0.0")