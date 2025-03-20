1 - How to run Scripts:

1.1: Docker:
1.1.1: Install docker.

1.1.2: Run docker-compose.yml: " docker-compose -f Development_promptly/Docker/docker-compose.yml up -d "
    This command start image docker and run script to create tables.

1.2: Run requirements.txt

1.3: Run ingest_data.py
    Comand: "python3 Development_promptly/python_scripts/ingest_data.py --file patient.csv "
    Is necessary to have a file in python_scripts folder.
    
1.4: Run transform_data.py
    Comand: " python3 Development_promptly/python_scripts/transform_data.py "
