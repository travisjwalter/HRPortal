from flask import Flask, render_template, url_for, request, redirect, flash
from script import createUser, assign_user_group, assign_user_attribute, deactivate_user, reactivate_user, getUserAttribute
#from drive import add_user, update_permissions, remove_user
from admin import suspendUser, reactivateUser, addUserToGroup, removeUserFromGroup, removeUser


# This script was created by Travis Walter on October 10th, 2020

app = Flask(__name__)
#app.secret_key = 
#team_drive_id = 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/onboarding/', methods=['POST', 'GET'])
def onboarding():
    if request.method == 'POST':
        # Read input from html form submission
        username = request.form['username']
        first = request.form['firstName']
        last = request.form['lastName']
        display = str(first) + " " + str(last)
        mail = request.form['email']
        phone = request.form['phoneNumber']
        major = request.form['major']
        grad = request.form['gradeYear']
        subteam = request.form['subteam']

        # Create user within the Crowd
        createRet = createUser(username, first, last, display, mail)

        # Assigning user attributes
        assign_user_attribute(username, "Phone Number", phone)
        assign_user_attribute(username, "Major", major)
        assign_user_attribute(username, "Graduating Year", grad)

        # Assigning user to subteam group
        if subteam == "Avionics":
            assign_user_group(username, "Avionics")
            assign_user_group(username, "Engineering")
        elif subteam == "Propulsion":
            assign_user_group(username, "Propulsion")
            assign_user_group(username, "Engineering")
        elif subteam == "Programming":
            assign_user_group(username, "Software")
            assign_user_group(username, "Engineering")
        elif subteam == "Structures":
            assign_user_group(username, "Structures")
            assign_user_group(username, "Engineering")
        elif subteam == "Business":
            assign_user_group(username, "Business")

        # Flash user password
        flash(str(createRet))

        # Return to the index page
        return redirect(url_for('index'))
    
    # Render onboarding html
    return render_template('onboarding.html')

@app.route('/offboarding/', methods=['POST', 'GET'])
def offboarding():
    if request.method == 'POST':
        # Read input from html form submission
        username = request.form['username']

        # Deactivate user within the Crowd
        deactivateRet = deactivate_user(username)

        # Remove user from drive
        # Add @lrl.com to username before calling this
        removeUser(username)

        # Flash user password
        flash(str(deactivateRet))

        # Return to the index page
        return redirect(url_for('index'))
    
    # Render onboarding html
    return render_template('offboarding.html')

@app.route('/leave/')
def leave():
    return render_template('leave.html')

@app.route('/onleave/', methods=['POST', 'GET'])
def onLeave():
    if request.method == 'POST':
        # Read input from html form submission
        username = request.form['username']

        # Deactivate user within the Crowd
        deactivateRet = deactivate_user(username)

        # Set onLeave attribute to true
        assign_user_attribute(username, "onLeave", "true")

        # Suspend user
        lrlEmail = str(username) + "@liquidrocketry.com"
        suspendUser(lrlEmail)

        # Flash user password
        flash(str(deactivateRet))

        # Return to the index page
        return redirect(url_for('index'))
    
    # Render onboarding html
    return render_template('leave.html')

@app.route('/offleave/', methods=['POST', 'GET'])
def offLeave():
    if request.method == 'POST':
        # Read input from html form submission
        username = request.form['username']

        # Deactivate user within the Crowd
        reactivateRet = reactivate_user(username)

        # Set onLeave attribute to false
        assign_user_attribute(username, "onLeave", "false")

        # Make user a content manager in drive
        lrlEmail = str(username) + "@liquidrocketry.com"
        reactivateUser(lrlEmail)

        # Flash user password
        flash(str(reactivateRet))

        # Return to the index page
        return redirect(url_for('index'))
    
    # Render onboarding html
    return render_template('leave.html')

if __name__ == "__main__":
    app.run(debug=True)