Project Title: FIFA World Prediction League

Description:
Our project, built using Django Python, is a Progressive Web App (PWA) designed to create an engaging prediction league for FIFA World matches. The primary goal was to provide users with a platform to join a league, predict match outcomes, and compete for the top spot.

Key Features:

    Prediction System: Users could make predictions for each FIFA World match, earning 1 point for correct predictions, losing 1 point for incorrect predictions, and gaining 1 point for staying out.
    API Integration: Utilized API endpoints to fetch live match data, including scores and updates in real-time.
    Backend Automation with Celery: Implemented Celery to automate backend processes, such as fetching live scores during matches and saving points after match completion.
    League Table Calculation: Celery was also employed to calculate and update the league table points at the end of each match, ensuring accuracy and efficiency.
    Winner Determination: At the conclusion of the final match, the person with the highest accumulated points emerged as the winner of the league.

Technology Stack:

    Django (Python)
    Progressive Web App (PWA)
    Celery for Backend Automation
    API Integration for Live Match Data

Outcome:
The project successfully created an interactive and competitive environment for football enthusiasts. Users could actively participate in predicting match outcomes, and the automated backend processes ensured a seamless experience. The use of Celery enhanced the project's efficiency, making it a dynamic and enjoyable FIFA World Prediction League.
