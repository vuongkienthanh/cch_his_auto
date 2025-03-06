# Automate your HIS workflow at CCH
using `python` and [`selenium`](https://www.selenium.dev/)

### Install from git

```sh
pip install git+https://github.com/vuongkienthanh/cch_his_auto
```

or using [`uv`](https://docs.astral.sh/uv/)

```sh
uv add git+https://github.com/vuongkienthanh/cch_his_auto
```

### Usage:

- Initialize driver (also a selenium driver, with some convenient methods)
```python
from cch_his_auto import Driver
driver = Driver()
```

- Set up logger as needed
```python
import logging
logger = logging.getLogger()

def add_file_handler_to_logger(filename: str, mode="w"):
    file = logging.FileHandler(filename, mode=mode, encoding="utf-8-sig")
    file.setFormatter(logging.Formatter("{asctime}: {msg}", style="{"))
    logger.addHandler(file)
```

- Pick the tasks you want
```python
from cch_his_auto.tasks import login
login(driver, username, password)
```

- Close the driver when finished
```python
driver.close()
```
