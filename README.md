# Project: surfs-up

## **Steps for development:**
0. Install:
    - python 3.9.7 [[click here](https://realpython.com/installing-python)]

    - Generate an environment for development (only once)
    ```bash
    $ python3 -m venv dev_env
    ```

1. Activate the virtual environment:
    ```bash
    $ source dev_env/bin/activate
    ```
    Your shell prompt should indicate the `dev_env`:
    ```bash
    (dev_env) $
    ```

2. Install requirements:
    ```bash
    (dev_env) $ pip3 install -r requirements.txt
    ```


## **Running Tests:**
- Run all tests in `test/`

    ```bash
    (dev_env) $ python3 -m pytest test/*
    ```

## **Running Coverage Report:**
1. Run coverage using tests as entry point

    ```bash
    (dev_env) $ coverage run -m pytest test/*
    ```

2. Show coverage report to terminal

    ```bash
    (dev_env) $ coverage report
    ```

3. Show coverage report to html

    ```bash
    (dev_env) $ coverage html
    (dev_env) $ open coverage_html/index.html
    ```

## **Playground Instructions:**

    ```bash
    (dev_env) $ SURFLINE_USERNAME=XXXXX SURFLINE_PASSWORD=XXXXX python3 playground.py
    <class 'requests.models.Response'>
    parsing took 0.06013798713684082 seconds
    {   'forecast': {
        ...
        }
    }
    ```

## **Generate Spot URL Lookup Database**

    ```bash
    (dev_env) $ python3 scripts/populate_spot_db.py -h
    usage: populate_spot_db.py [-h] [--ow] filename

    Process to build report URLs

    positional arguments:
      filename    file to store table (CSV format)

    optional arguments:
      -h, --help  show this help message and exit
      --ow        overwrite file at argument filename
    ```
This could take a long while. It searches every page of the surfline domain, building a
list of valid report urls and scraping basic information about each spot.

