1 - structure:

├── Development_promptly
    ├── Docker
    │   ├── docker-compose.yml
    │   └── init-scripts
    │   │   └── init.sql
    ├── documentation.yaml
    └── python_scripts
    │   ├── .env
    │   ├── db_utils.py
    │   ├── ingest_data.py
    │   ├── requirements.txt
    │   ├── source_files
    │       └── patient.csv
    │   └── transform_data.py
├── Readme.md
├── data_engineering_exercise.pdf
└── patient.csv

2 - How to run Scripts:
    2.1: Docker:
        2.1.1: Install docker.
        2.1.2: Run docker-compose.yml: docker-compose -f Development_promptly/Docker/docker-compose.yml up -d
            This command start image docker and run script to create tables.
    2.2: Run ingest_data.py
            Comand: python3 Development_promptly/python_scripts/ingest_data.py --file patient.csv
            Is necessary to have a file in python_scripts folder.
    2.3: Run transform_data.py
            Comand: python3 Development_promptly/python_scripts/transform_data.py