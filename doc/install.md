# 安装

```
mkdir mysite
cd mysite
# virtualenv  venv(虚拟环境名称，可自行定义.采用 python2，MySQL-python不支持3)
python3 -m venv venv(环境名称)
source venv/bin/activate
pip install -r modules.txt
django-admin startproject mysite
python3 manage.py startapp stock
```

在 mysite/mysite 下添加 celery.py
```
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

app = Celery('mysite')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
```

在__init_.py文件添加如下配置(MySQL-python不支持3)
```
from __future__ import absolute_import, unicode_literals

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__all__ = ['celery_app']

import pymysql
pymysql.install_as_MySQLdb()
```

修改settings.py配置
```
INSTALLED_APPS = (
        ...,
        'django_celery_beat',
    )

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

初始化数据库
```
python manage.py migrate
```

创建管理员用户
```
python manage.py createsuperuser（admin:test123456）
```

启动服务
```
python manage.py runserver [0.0.0.0:8000]
```

启动beat（manage.py所在目录）
```
celery -A mysite(模块名) beat -l info -S django
```

启动worker（manage.py所在目录）
```
celery -A mysite(模块名) worker -l info
```

模块 task shell 调试
```
python manage.py shell
from test_celery.tasks import test
test()
```

### 参考
 * https://github.com/celery/celery