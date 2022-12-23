# Debugging

## Backend debugging

The app can be debugged using [pdb](https://docs.python.org/3/library/pdb.html). You can do this in several ways.

1. Use Postman to test the API without a frontend instance
2. Use the frontend instance to interact with the API
3. Run specific `pytest` unit test inside the backend container `docker exec -it climatemind-backend_web_1 pytest -xs --pdb YOURTEST_PATH`

For either test, you need to add a breakpoint() into the code where you want the application to pause for debugging.

For more information about PDB review their [documentation](https://docs.python.org/3/library/pdb.html).

### **To test with Postman**

Navigate to the climatemind-backend directory and run:

```
docker-compose -p climatemind-backend -f docker/docker-compose.yml up -d
docker attach climatemind-backend
```

{% hint style="info" %}
In case of mac with M1 chip `docker-compose.m1.yml`file should be used instead.
{% endhint %}

The terminal/command-line can now be used to interact with PDB. Once the code hits a stopping point, you will see (pdb) in this terminal/command-line instance.

The application should now be running on localhost. In Postman you can make requests to http://127.0.0.1:5000

### **To test with the frontend**

Verify the `webapp` is up and running with `docker ps` or Docker Desktop. Open http://localhost:3000/ in your browser to access the app.
