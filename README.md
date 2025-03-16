# Automate your HIS workflow at CCH
using `python` and [`selenium`](https://www.selenium.dev/)

## Install from git

```sh
pip install git+https://github.com/vuongkienthanh/cch_his_auto
```

or using [`uv`](https://docs.astral.sh/uv/)

```sh
uv add git+https://github.com/vuongkienthanh/cch_his_auto
```

## Build your own workflow

- Initialize driver (also a [selenium driver](https://www.selenium.dev/documentation/overview/), with some convenient methods)
```python
from cch_his_auto.driver import Driver
driver = Driver()
```

- Set up logger as needed
```python
import logging
_logger = logging.getLogger()

def add_file_handler_to_logger(filename: str, mode="w"):
    file = logging.FileHandler(filename, mode=mode, encoding="utf-8-sig")
    file.setFormatter(logging.Formatter("{asctime}: {msg}", style="{"))
    _logger.addHandler(file)
```

- Pick the tasks you want
```python
from cch_his_auto.tasks.auth import login
login(driver, username, password)
```

- Close the driver when finished
```python
driver.close()
```

## Or use GUI which is built for my daily tasks
```sh
uv run src/cch_his_auto/app/main.py
```
