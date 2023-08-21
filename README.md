Run `flask --app api run --debug`  in the terminal to start developmental server.

### Endpoints

`/symptom/<response>`

Donwload symptom report. Responses to climacteric questionnaire encoded as string of 21 numbers in URL.

TODO: change to URL parameter

`/risk`

Calculate health risks. Questionnaire answers sent in JSON as POST request payload.
