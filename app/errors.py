from flask import render_template
from app import app, db


@app.errorhandler(404)
def not_found_error(error):
    # Note that both functions return a second value after the template,
    # which is the error code number. For all the view functions that
    # I created so far, I did not need to add a second return value because
    # the default of 200 (the status code for a successful response) is right.
    # In this case these are error pages, so I want the status code for it.
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    # To make sure any failed database sessions do not interfere with any
    # database accesses triggered by the template, I issue a session rollback.
    # This resets the session to a clean state. It does something like
    # cleaning the memory of session, not downgrading the database!
    db.session.rollback()
    return render_template('500.html'), 500
