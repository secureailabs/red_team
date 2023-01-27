# Prerequisite

1. Install flask:
https://flask.palletsprojects.com/en/2.2.x/installation/

2. Install mongodb:
https://www.mongodb.com/docs/manual/installation/

3. Other packages used in projects

```
# Install openai-whisper for voice to text
pip install git+https://github.com/openai/whisper.git

# Install keybert for keyword extraction
pip install keybert
```

# Run the project

```
flask --app server --debug run
```

# Patient register:

username -- need to be unique, different from what you have used before(include failed registration attempts)
password -- no restriction
email -- no restriction
firstname -- no restriction
lastname -- no restriction
address -- no restriction
age -- needs to be an adult, greater than 20
gender -- string, "male" or "female"
height -- normal human height
weight -- normal human weight
bloodtype -- A, B, AB or O

