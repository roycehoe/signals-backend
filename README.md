# Overview
https://api.fancybinary.sg/

RestAPI enpoints for a game of hilo written in Python, built with PostgreSQL and FastAPI.

# Play with my application
 1. Download Insomnia [here](https://insomnia.rest/)
 2. Open the [insomnia json file](Insomnia_2022-03-14.json) in Insomnia
 3. Have fun!

# Project Skeleton
 - Created a Card class to implement Card objects that can be compared to other Card objects based on their suit and value attributes. Implemented  with Pydantic dataclasses
 - Created a GameState class to to keep track of GameStates; Implemented methods that alters the GameState object based on player decisions; Implemented with Pydantic dataclasses
 - Implement core game logic by implementing functions that returns altered Gamestate objects


# API
 - Implement a PostgreSQL relational database with SQLAlchemy that stores User authentication details, and the corresponding latest gamestate
 - Utilize FastAPI to create endpoints for my fronend to perform CRUD functions on my database
 - Used Pydantic BaseModel to dictate the request and return structure for each API call

# Security, error handling and testing
![Codecov](https://img.shields.io/codecov/c/github/roycehoe/card_game?flag=unittest&token=RKQABL23VM)
 - Utilized CryptContext to hash passwords when stored in my database
 - Implement the creation of a JWT token whenever a user is successfully authenticated
 - Implement custom Exceptions for all implemented game objecst
 - Implement custom HTTP response status codes for invalid requests sent to my API endpoint with accompanying custom error codes
 - Implement unit tests with Pytest for all backend modules

# Deployment
 - Utilized Docker and docker-compose to deploy a containerize version of my application
 - Implement pre-commit hooks to mantain code integrity
 - Utilize GitHub actions to implement a CI pipeline; push to work branches are automatically rejected should builds fail
 - Used Terraform to automate creation of Virtual Private Servers on DigitalOcean
 - Used Ansible, in conjuction with Terraform, to create a Virtual Private server, download project and system dependencies, and deploy a working backend, with a single command
 - Used Cloudflare to set up a DNS to redirect users from my application domain name to my virtual private server


