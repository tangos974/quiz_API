import requests
from requests.auth import HTTPBasicAuth

# Set the base URL for FastAPI app
base_url = "http://localhost:8000" 

credentials = HTTPBasicAuth("alice", "wonderland")

# Test the health check endpoint
response = requests.get(f"{base_url}/health", auth=credentials)
print("L'API tourne: {}". format(response.json()))

# Test the random_question endpoint
response = requests.get(f"{base_url}/random_question", auth=credentials)
print("\n\n Voilà une question aléatoire: {}". format(response.json()))

# Test the random_filtered_question endpoint with use parameter
response = requests.get(f"{base_url}/random_filtered_question?use=Test de positionnement", auth=credentials)
print("\n\n Voilà une question issue des Tests de Positionnement: {}". format(response.json()))

# Test the multiple_responses endpoint with use and num_responses parameters
response = requests.get(f"{base_url}/multiple_responses?use=Test de positionnement&num_responses=5", auth=credentials)
print("\n\n Voilà cinq questions issues des Tests de Positionnement: {}". format(response.json()))

# Test the generate_qcm endpoint with num_questions parameter
response = requests.get(f"{base_url}/generate_qcm?use=Test de validation&num_questions=3&subjects=Automation&subjects=Streaming de données", auth=credentials)
print("\n\n Voilà 3 questions issues des Tests de Validation ayant pour subject Automation ou Streaming de donées: {}". format(response.json()))

# Test the create_question endpoint (admin only)
admin_credentials = HTTPBasicAuth("admin", "4dm1N")
new_question_data = {
    "question": "What is the capital of France?",
    "subject": "Geography",
    "use": "Test",
    "correct": "Paris",
    "responseA": "London",
    "responseB": "Berlin",
    "responseC": "Madrid",
    "responseD": "Paris",
    "remark": "None"
}
response = requests.post(f"{base_url}/create_question", json=new_question_data, auth=admin_credentials)
print("\n\n Message issu de la création d'une nouvelle question {}". format(response.json()))
