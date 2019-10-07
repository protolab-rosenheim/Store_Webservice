# Store Webservice


## Building and running the Docker Container

    docker build -t storews .
    docker run -d -p 5000:5000 storews

Mount configuration files (the application expects a file named `conf.yaml` in `/usr/src/app/conf` otherwise it'll 
fall back to dev configuration from `dev.yaml`): 

    docker run -d -p 5000:5000 --mount type=bind,source="$(pwd)"/test_conf,target=/usr/src/app/conf storews
    
## Importing data
There is some demo data in `\Import\Demodata.csv`, import it to a local webservice instance via: 

    python CsvImport.py