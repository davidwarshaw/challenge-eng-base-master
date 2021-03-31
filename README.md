# challenge-eng-base

Run the backend tests:

    cd backend-python
    docker-compose up

Start the project:

    docker-compose up backend site

Download and load the movielens data to elasticsearch:

    docker-compose exec backend flask load-movielens

The app is at: http://localhost:8090

Drop the elasticsearch data:

    docker-compose down -v
