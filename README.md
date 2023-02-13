# App B

Create a network to be used by both containers (**only once**):

`docker network create crypto`

Run App B:

`docker run --network=crypto --name=flask app-b`