# Manual Testing

## Local API

If you'd like to test the endpoints, you can do this with Postman.

Register for and install Postman from their [website](https://www.postman.com).

We have a collection of tests already available that you can run. Request access from any of the backend team members to our collections.

## Local App

If you'd like to test the application locally with the front-end interface, you need to do the following:

### First Time

1. Use terminal/command-line to navigate to any directory located outside of the climatemind-backend
2. Clone the front-end repo

```
git clone https://github.com/ClimateMind/climatemind-frontend.git
```

1. Install NPM

```
npm -i
```

### Every Time

1. Navigate to the /climatemind-backend directory
2. Start the Docker Instance and attach to it

```
docker-compose -p climatemind-backend -f docker/docker-compose.yml up -d
docker attach climate-backend_web_1
```

1. Open up a second terminal/command-line instance
2. Navigate to the /climatemind-frontend directory
3. Start NPM

```
npm start
```

You should now be able to open [http://localhost:3000/](http://localhost:3000/) or [http://127.0.0.1:3000/](http://127.0.0.1:3000/) and have access to the fully functioning application locally!
