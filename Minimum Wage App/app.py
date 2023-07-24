from flask import Flask, redirect, render_template, request, session, url_for, Response, send_file
import os
import io
import sqlite3 as sl
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import date, datetime

app = Flask(__name__)
db = "minimum-wage.db"


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/submit_focus", methods=["POST"])
def submit_focus():
    session["focus"] = request.form["focus"]
    if 'focus' not in session or session["focus"] == "":
        return redirect(url_for("home"))
    if session["focus"] == "Federal":
        session["state"] = "California"
        return redirect(url_for("display_vis", focus=session["focus"], state=session["state"]))
    else:
        return redirect(url_for("select_state"))


@app.route("/state")
def select_state():
    print(db_get_states())
    return render_template('state.html', states=db_get_states())


@app.route("/submit_state", methods=["POST"])
def submit_state():
    session["state"] = request.form["state"]
    print(request.form["state"])
    if 'state' not in session or session["state"] == "":
        return redirect(url_for("state"))
    return redirect(url_for("display_vis", focus=session["focus"], state=session["state"]))


@app.route("/<focus>/minimum-wage/<state>")
def display_vis(focus, state):
    return render_template('display.html', focus=focus, state=state, project=False)


@app.route("/submit_projection", methods=["POST"])
def submit_projection():
    session["year"] = request.form["year"]
    if session["state"] == "" or session["focus"] == "" or session["year"] == "":
        return redirect(url_for("home"))
    return redirect(url_for("display_proj", focus=session["focus"], state=session["state"]))


@app.route("/<focus>/minimum-wage/projection/<state>")
def display_proj(focus, state):
    return render_template("display.html", focus=focus, state=state, project=True, year=session["year"])


@app.route("/fig/<focus>/<state>")
def fig(focus, state):
    fig = create_figure(focus, state)

    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    return send_file(img, mimetype="image/png")


def create_figure(focus, state):
    df = db_create_dataframe(focus, state)
    print(session)
    if 'year' not in session:
        fig = Figure()
        ax = fig.add_subplot(1, 1, 1)
        if focus == "Federal":
            fig.suptitle(focus.capitalize() + " Minimum Wage")
        else:
            fig.suptitle(state + " Minimum Wage")
        ax.plot(df["year"], df["wage"])
        ax.set(xlabel="Year", ylabel="Minimum Wage ($)")
        return fig
    else:
        df['yearmod'] = df["year"].map(datetime.toordinal)
        y = df['wage'][-30:].values
        X = df['yearmod'][-30:].values.reshape(-1, 1)
        # ogdt = "01/01/" + str(session['year'])
        dt = [[datetime.strptime("01/01/" + session["year"], '%m/%d/%Y')]]
        print('dt:', dt)
        draw = datetime.toordinal(dt[0][0])
        dord = datetime.fromordinal(int(draw))
        regr = LinearRegression(fit_intercept=True, normalize=True, copy_X=True, n_jobs=2)
        regr.fit(X, y)
        pred = int(regr.predict([[draw]])[0])
        df = df.append({'year': dord,
                        'wage': pred,
                        'yearmod': draw}, ignore_index=True)
        fig = Figure()
        ax = fig.add_subplot(1, 1, 1)
        fig.suptitle('By ' + session['year'] + ', the ' + focus + ' minimum wage will be $' + str(pred))
        ax.plot(df["year"], df["wage"])
        ax.set(xlabel="Year", ylabel="Minimum Wage ($)")
        return fig


def db_create_dataframe(focus, state):
    conn = sl.connect(db)
    curs = conn.cursor()

    df = pd.DataFrame()
    table = "min_wage"
    stmt = "SELECT * from " + table + " where `State`=?"
    data = curs.execute(stmt, (state, ))
    items = curs.fetchall()
    df["year"] = [datetime(item[0], 1, 1, 1, 1) for item in items]
    if focus == "Federal":
        df["wage"] = [item[4] for item in items]
    else:
        df["wage"] = [item[2] for item in items]
    print(df["wage"])
    conn.close()
    return df

def db_get_states():
    conn = sl.connect(db)
    curs = conn.cursor()
    table = "min_wage"
    stmt = "SELECT DISTINCT State from " + table
    data = curs.execute(stmt)
    states = sorted({result[0] for result in data})
    conn.close()
    return states


if __name__ == "__main__":
    # print(db_get_states())
    app.secret_key = os.urandom(12)
    app.run(debug=True)
