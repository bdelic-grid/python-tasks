import json
import sys
import requests

def load_data():
    user_in = input("Please enter a path to survey file in JSON format and a list of emails separated by a space: ")
    
    json_path = user_in.split(" ")[0]
    emails_path = user_in.split(" ")[1]

    try:
        with open(json_path, 'r') as f:
            json_data = json.load(f)

        with open(emails_path, 'r') as f:
            emails_list = []
            for line in f:
                emails_list.append(line)
    except FileNotFoundError:
        raise FileNotFoundError("Error: file was not found")

    return json_data, emails_list


def parse_json(data):
    survey_name = list(data.keys())[0]

    questions = []
    answers = []

    for page_name, q in data[survey_name].items():
        page_info = {
            "Page_name" : page_name
        }

        for q_name, q_data in q.items():
            q_payload = {
                "Question_name" : q_name,
                "Description" : q_data["Description"],
                "Answers" : q_data["Answers"]
            }

            questions.append(q_payload["Description"])
            answers.append(q_payload["Answers"])

    return survey_name, questions, page_info, answers


def load_token():
    try:
        with open("token.txt", "r") as f:
            token = f.readline()
    except FileNotFoundError:
        raise FileNotFoundError("Error: file was not found")

    return token


def get_all_surveys(url, access_token):
    headers = {
        'Accept': "application/json",
        'Authorization': f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print(response.text)
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


def create_survey(url, access_token, survey_name):
    headers = {
        'Content-Type': "application/json",
        'Accept': "application/json",
        'Authorization': f"Bearer {access_token}"
    }  

    data = json.dumps({"title": survey_name})

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 201:
        return json.loads(response.text)["id"]
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


def add_page(url, access_token, page_info):
    headers = {
        'Content-Type': "application/json",
        'Accept': "application/json",
        'Authorization': f"Bearer {access_token}"
    }

    data = json.dumps({"title": page_info["Page_name"]})

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 201:
        return json.loads(response.text)["id"]
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


def add_questions(url, access_token, questions, answers):
    headers = {
        'Content-Type': "application/json",
        'Accept': "application/json",
        'Authorization': f"Bearer {access_token}"
    }

    for question, ans in zip(questions, answers):
        data = {"headings": [{"heading": question}], "family": "single_choice", "subtype": "horiz", "answers": {"choices": [{"text": choice} for choice in ans]}}
        data = json.dumps(data)

        response = requests.post(url, headers=headers, data=data)
        if response.status_code != 201:
            print(f"Error: {response.status_code}")
            print(response.text)

def create_collector(url, access_token):
    headers = {
        'Content-Type': "application/json",
        'Accept': "application/json",
        'Authorization': f"Bearer {access_token}"
    }

    data = json.dumps({"type": "weblink", "name": "Collector"})
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 201:
        return json.loads(response.text)["url"]
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


if __name__ == "__main__":
    try:
        json_data, emails = load_data()
        access_token = load_token().strip()
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)

    survey_name, questions, page_info, answers = parse_json(json_data)

    base_url = "https://api.surveymonkey.com/v3"
    
    survey_id = create_survey(base_url + "/surveys", access_token, survey_name)
    page_id = add_page(base_url + f"/surveys/{survey_id}/pages", access_token, page_info)
    add_questions(base_url + f"/surveys/{survey_id}/pages/{page_id}/questions", access_token, questions, answers)

    survey_url = create_collector(base_url + f"/surveys/{survey_id}/collectors", access_token)
    print(survey_url)

    
    #print("------------------------ALL SURVEYS------------------------")
    #get_all_surveys(base_url + "/surveys", access_token)
