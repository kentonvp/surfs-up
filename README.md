# Project: surfs-up

The name's Kenton. I'm an ocean lover. My primary activity of choice is shortboarding, but I also love taking out the log or twinny, running on the beach with my wife, or just setting up a chair and opening a good book.

The Problem: Whatever activity I was feeling on a particular day, I'd have to search through my favorite spots and try and find the best conditions for that activity. For example sorting by size and good winds when shortboarding, maybe smaller surf for when I wanted a cruisier day on the log, or maybe a drained tide if my wife wanted to go for a run on the beach... So also being a programmer I decied to automate it.

The Solution: SurfsUp_Bot is an interactive bot which can store custom preferences based on activity. These preferences are then used to filter and sort surf reports, giving you the best spots for your activity.

I hope this can be used as a tool to streamline the difficult decision of deciding which beach to go to.

Thanks for reading, now get out there and remember to have fun!

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

## **Running Coverage Report:**

1. Run coverage using tests as entry point

   ```bash
   (dev_env) $ coverage run -m unittest
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
