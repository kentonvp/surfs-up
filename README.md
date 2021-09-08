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
    (dev_env) $ pip install -r requirements.txt
    ```


## **Running Tests:**
- Run all tests in `test/`

    ```bash
    (dev_env) $ python3 -m unittest -v
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