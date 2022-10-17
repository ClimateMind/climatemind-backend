# Debugging

## Backend Debugging

The app can be debugged using pdb. You can do this several ways.

1. Use Postman to test the API without a front-end instance
2. Use the front-end instance to interact with the API
3. Run specific `pytest` unit test inside the backend container `docker exec -it climatemind-backend_web_1 pytest -xs --pdb YOURTEST`

For either test, you need to add a breakpoint() into the code where you want the application to pause for debugging.

For more information about PDB review their [documentation](https://docs.python.org/3/library/pdb.html).

**To test with Postman**

Navigate to the climatemind-backend directory and run:

```
docker-compose -p climatemind-backend -f docker/docker-compose.yml up -d
docker attach climatemind-backend
```

The terminal/command-line can now be used to interact with PDB. Once the code hits a stopping point, you will see (pdb) in this terminal/command-line instance.

**To test with Front-End**

Run the same commands listed above. Then open up a second terminal and run:

```
npm start
```

The terminal/command-line can now be used to interact with PDB. Once the code hits a stopping point, you will see (pdb) in this terminal/command-line instance.
