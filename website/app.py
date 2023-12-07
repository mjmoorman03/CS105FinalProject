from flask import Flask, render_template, request
import csv

app = Flask(__name__)

def match(person1: dict, person2: dict):
    ''' true iff fields match '''
    # doesn't just check person1 == person2 bc person2 has a name field
    matched = person1['Concentration 1'] == person2['Concentration 1'] \
                and person1['Concentration 2'] == person2['Concentration 2'] \
                and person1['House'] == person2['House'] \
                and person1['Year'] == person2['Year']
    return matched

def matchWithBlanks(person1: dict, person2: dict):
    ''' true iff fields match '''
    # doesn't just check person1 == person2 bc person2 has a name field
    matched = (person1['Concentration 1'] == person2['Concentration 1'] or not person1['Concentration 1']) \
                and (person1['Concentration 2'] == person2['Concentration 2'] or not person1['Concentration 2']) \
                and (person1['House'] == person2['House'] or not person1['House']) \
                and (person1['Year'] == person2['Year'] or not person1['Year'])
    return matched

def identifyIndividual(person: dict):
    # returns a list of the names of the people who match the person
    # if no one matches, returns an empty list
    
    # open up data file
    facebookFile = '../105facebook_cleaned.csv'
    f = open(facebookFile, 'r', encoding='utf-8-sig')
    data = list(csv.DictReader(f))
    matches = [p for p in data if matchWithBlanks(person, p)]
    f.close()
    return matches

@app.route('/', methods=['GET'])
def index():
    # Render the HTML form template
    return render_template('index.html', numMatches = "?")

@app.route('/result', methods=['POST'])
def result():
    # Retrieve the form values
    concentration1 = request.form['concentration1']
    concentration2 = request.form['concentration2']
    house = request.form['house']
    year = request.form['year']
    # Create the person dictionary
    person = {
        'Concentration 1': concentration1,
        'Concentration 2': concentration2,
        'House': house[:-6],
        'Year': year
    }
    print(person)
    # Call the identifyIndividual() function
    matches = identifyIndividual(person)
    # Render the results template with the matches
    return render_template('result.html', numMatches=str(len(matches)))

if __name__ == '__main__':
    # Define your data
    data = [...]  # Your data goes here
    app.run()