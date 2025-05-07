Title: Hands-on Learn Python Celery In 30 Minutes - Li Pei - Medium

URL Source: https://lip17.medium.com/hands-on-learn-python-celery-in-30-minutes-9544aabb70b1

Published Time: 2024-06-07T04:12:54.768Z

Markdown Content:
Hands-on Learn Python Celery In 30 Minutes | by Li Pei | Medium
===============
 

[Open in app](https://rsci.app.link/?%24canonical_url=https%3A%2F%2Fmedium.com%2Fp%2F9544aabb70b1&%7Efeature=LoOpenInAppButton&%7Echannel=ShowPostUnderUser&source=post_page---top_nav_layout_nav-----------------------------------------)

Sign up

[Sign in](https://medium.com/m/signin?operation=login&redirect=https%3A%2F%2Flip17.medium.com%2Fhands-on-learn-python-celery-in-30-minutes-9544aabb70b1&source=post_page---top_nav_layout_nav-----------------------global_nav------------------)

[](https://medium.com/?source=post_page---top_nav_layout_nav-----------------------------------------)

[Write](https://medium.com/m/signin?operation=register&redirect=https%3A%2F%2Fmedium.com%2Fnew-story&source=---top_nav_layout_nav-----------------------new_post_topnav------------------)

[](https://medium.com/search?source=post_page---top_nav_layout_nav-----------------------------------------)

Sign up

[Sign in](https://medium.com/m/signin?operation=login&redirect=https%3A%2F%2Flip17.medium.com%2Fhands-on-learn-python-celery-in-30-minutes-9544aabb70b1&source=post_page---top_nav_layout_nav-----------------------global_nav------------------)

![Image 2](https://miro.medium.com/v2/resize:fill:64:64/1*dmbNkD5D-u45r44go_cf0g.png)

Hands-on Learn Python Celery In 30 Minutes
==========================================

[![Image 3: Li Pei](https://miro.medium.com/v2/resize:fill:64:64/1*NCmMr30MpR8sOUgGRwfgvw.jpeg)](https://lip17.medium.com/?source=post_page---byline--9544aabb70b1---------------------------------------)

[Li Pei](https://lip17.medium.com/?source=post_page---byline--9544aabb70b1---------------------------------------)

Follow

3 min read

·

Jun 7, 2024

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Fp%2F9544aabb70b1&operation=register&redirect=https%3A%2F%2Flip17.medium.com%2Fhands-on-learn-python-celery-in-30-minutes-9544aabb70b1&user=Li+Pei&userId=72bca72fca5b&source=---header_actions--9544aabb70b1---------------------clap_footer------------------)

22

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F9544aabb70b1&operation=register&redirect=https%3A%2F%2Flip17.medium.com%2Fhands-on-learn-python-celery-in-30-minutes-9544aabb70b1&source=---header_actions--9544aabb70b1---------------------bookmark_footer------------------)

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D9544aabb70b1&operation=register&redirect=https%3A%2F%2Flip17.medium.com%2Fhands-on-learn-python-celery-in-30-minutes-9544aabb70b1&source=---header_actions--9544aabb70b1---------------------post_audio_button------------------)

Share

Recently my team was assigned a task to compare and demo the difference between [**Celery**](https://docs.celeryq.dev/en/stable/index.html) and [**Kafka**](https://kafka.apache.org/)**.** As someone totally new to Celery (and Python), I spent several days on it and here I want to share what I learned with hands on experiment in the shortest length. As someone new to Python as well, this should be rookie friendly with good coverage. So, let’s go.

What Is Celery?
===============

Celery is a distributed task queue.

How Does Celery Work?
=====================

1.  Client submit a predefined task to broker (commonly [**Redis Pubsub**](https://redis.io/docs/latest/develop/interact/pubsub/))
2.  Celery worker poll from **Redis** and execute the predefined task.
3.  \[Bonus\] For scheduled or recuring task, [**Celery beat**](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html) will schedule and trigger the task.
4.  \[A little more detail\] **Redis PubSub** is working on pull mode, if there is no worker, client submitted task will stay in Redis.

Time To Play
============

All the code is available [**here**](https://github.com/LIP17/kafka-blog-series/tree/main/celery-and-kafka).

1.  Create a new project with [Poetry](https://python-poetry.org/). We only need [basic usage](https://python-poetry.org/docs/basic-usage/) here for dependency management.
2.  Install dependency, add [celery](https://pypi.org/project/celery/) and [redis](https://pypi.org/project/redis/5.0.5/) to your **_pyproject.toml_**, create virtual environment by running `python -m venv venv` and run `poetry install` in your project’s root directory.
3.  Prepare Celery worker, beat and tasks.

\# celery\_app.py  
from celery import Celery  
from celery.schedules import crontab  
  
app = Celery('celery\_app', broker='redis://localhost:6379/0')  
app.conf.update(  
    result\_backend='redis://localhost:6379/0',  
    beat\_schedule={  
        'add-every-30-seconds': {  
            'task': 'tasks.add',  
            'schedule': 10.0, \# run every 10 seconds  
            'args': (10, 10)  
        },  
        'multiply-at-noon': {  
            'task': 'tasks.multiply',  
            'schedule': crontab(hour='12', minute='6'),  
            'args': (4, 5)  
        }  
    },  
    include=\['tasks'\]  
)  
  
  
\# tasks.py  
from celery\_app import app  
  
  
@app.task  
def add(x: int, y: int) -\> int:  
    result = x + y  
    print("add task result ", result)  
    return result  
  
  
@app.task  
def multiply(x: int, y: int) -\> int:  
    result = x \* y  
    print("multiply task ", result)  
    return result  
  
\# main.py  
from tasks import add   
  
if \_\_name\_\_ == "\_\_main\_\_":  
    result = add.delay(4, 5)  
    print('Task result: ', result.get())

4\. Prepare Redis with docker-compose file. You can also use `docker exec` on that image.

services:  
  redis:  
    image: docker.io/bitnami/redis:7.2  
    environment:  
      \- ALLOW\_EMPTY\_PASSWORD=yes  
      \- REDIS\_DISABLE\_COMMANDS=FLUSHDB,FLUSHALL  
    ports:  
      \- '6379:6379'  
    volumes:  
      \- 'redis\_data:/bitnami/redis/data'  
  
volumes:  
  redis\_data:  
    driver: local

5\. Run Celery worker first by `celery -A celery_app worker --loglevel=info`

6\. \[Optional\] Run Celery beat if you want to see the scheduled job running `celery -A celery_app beat --loglevel=info`

7\. You can also manually trigger a task by running a script

from tasks import add   
  
if \_\_name\_\_ == "\_\_main\_\_":  
    result = add.delay(4, 5)  
    print('Task result: ', result.get())

Thoughts After Play
===================

There are several tricks that I spend some time to figure out

1.  You have to register all the tasks to Celery by **_include_** Celery app’s conf.
2.  There are 2 ways to manually create task, **_delay_** vs **_apply\_async_**. From my understanding **_delay_** is a simple version of **_apply\_async_**, where in **_apply\_async_** you can pass in parameters to fine tune the task. To list possible parameters and its description below

**_countdown_**: Delay execution for a specified number of seconds.  
**_eta_**: Execute the task at a specific time.  
**_eta_** and **countdown** are mutually complementary.   
**_countdown_** is for relative time from now and **_eta_** is for specifc time.  
  
**_expires_**: Set an expiration time for the task.  
**_retry_**: Enable or disable automatic retries.  
**_priority_**: Set the priority of the task.  
**_routing\_key_**: Specify a routing key to control which queue the task is sent to.  
**_queue_**: Specify the queue to send the task to.

3\. Both **_delay_** and **_apply\_async_** return **_AsyncResult_**, and if you do not call blocking method on it, it will not block caller thread. Method on AsyncResult is listed below

**_get():_** Waits for the task to complete and returns the result.  
**_status()_**: Returns the current status of the task (e.g., PENDING, STARTED, SUCCESS, FAILURE).  
**_ready()_**: Returns True if the task has finished processing.  
**_successful()_**: Returns True if the task completed successfully.  
**_failed()_**: Returns True if the task raised an exception.  
**_traceback()_**: Returns the traceback of the task if it failed.

4\. Celery and Kafka are similar but designed for totally different purpose, I will write another blog to compare the difference in depth.

Hope you enjoy and see you later.

![Image 4](https://miro.medium.com/v2/da:true/resize:fit:0/5c50caa54067fd622d2f0fac18392213bf92f6e2fae89b691e62bceb40885e74)

Sign up to discover human stories that deepen your understanding of the world.
------------------------------------------------------------------------------

Free
----

Distraction-free reading. No ads.

Organize your knowledge with lists and highlights.

Tell your story. Find your audience.

Sign up for free

Membership
----------

Read member-only stories

Support writers you read most

Earn money for your writing

Listen to audio narrations

Read offline with the Medium app

Try for $5/month

[Celery](https://medium.com/tag/celery?source=post_page-----9544aabb70b1---------------------------------------)

[Python](https://medium.com/tag/python?source=post_page-----9544aabb70b1---------------------------------------)

[Task Queues](https://medium.com/tag/task-queues?source=post_page-----9544aabb70b1---------------------------------------)

[Distributed Computing](https://medium.com/tag/distributed-computing?source=post_page-----9544aabb70b1---------------------------------------)

[Programming](https://medium.com/tag/programming?source=post_page-----9544aabb70b1---------------------------------------)

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Fp%2F9544aabb70b1&operation=register&redirect=https%3A%2F%2Flip17.medium.com%2Fhands-on-learn-python-celery-in-30-minutes-9544aabb70b1&user=Li+Pei&userId=72bca72fca5b&source=---footer_actions--9544aabb70b1---------------------clap_footer------------------)

22

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Fp%2F9544aabb70b1&operation=register&redirect=https%3A%2F%2Flip17.medium.com%2Fhands-on-learn-python-celery-in-30-minutes-9544aabb70b1&user=Li+Pei&userId=72bca72fca5b&source=---footer_actions--9544aabb70b1---------------------clap_footer------------------)

22

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F9544aabb70b1&operation=register&redirect=https%3A%2F%2Flip17.medium.com%2Fhands-on-learn-python-celery-in-30-minutes-9544aabb70b1&source=---footer_actions--9544aabb70b1---------------------bookmark_footer------------------)

[![Image 5: Li Pei](https://miro.medium.com/v2/resize:fill:96:96/1*NCmMr30MpR8sOUgGRwfgvw.jpeg)](https://lip17.medium.com/?source=post_page---post_author_info--9544aabb70b1---------------------------------------)

[![Image 6: Li Pei](https://miro.medium.com/v2/resize:fill:128:128/1*NCmMr30MpR8sOUgGRwfgvw.jpeg)](https://lip17.medium.com/?source=post_page---post_author_info--9544aabb70b1---------------------------------------)

Follow

[Written by Li Pei -----------------](https://lip17.medium.com/?source=post_page---post_author_info--9544aabb70b1---------------------------------------)

[29 followers](https://lip17.medium.com/followers?source=post_page---post_author_info--9544aabb70b1---------------------------------------)

·[51 following](https://lip17.medium.com/following?source=post_page---post_author_info--9544aabb70b1---------------------------------------)

Everything can be built in event driven way

Follow

No responses yet
----------------

[](https://policy.medium.com/medium-rules-30e5502c4eb4?source=post_page---post_responses--9544aabb70b1---------------------------------------)

![Image 7](https://miro.medium.com/v2/resize:fill:32:32/1*dmbNkD5D-u45r44go_cf0g.png)

Write a response

[What are your thoughts?](https://medium.com/m/signin?operation=register&redirect=https%3A%2F%2Flip17.medium.com%2Fhands-on-learn-python-celery-in-30-minutes-9544aabb70b1&source=---post_responses--9544aabb70b1---------------------respond_sidebar------------------)

Cancel

Respond

More from Li Pei
----------------

![Image 8: Zero Loss: Debezium Connector Migration For PostgresDB Upgrades](https://miro.medium.com/v2/resize:fit:679/1*5wbuCwq4OOXPScP0E6hRGw.png)

[![Image 9: Li Pei](https://miro.medium.com/v2/resize:fill:20:20/1*NCmMr30MpR8sOUgGRwfgvw.jpeg)](https://lip17.medium.com/?source=post_page---author_recirc--9544aabb70b1----0---------------------3424b799_734f_401a_b417_b168b3030492--------------)

[Li Pei](https://lip17.medium.com/?source=post_page---author_recirc--9544aabb70b1----0---------------------3424b799_734f_401a_b417_b168b3030492--------------)

[Zero Loss: Debezium Connector Migration For PostgresDB Upgrades --------------------------------------------------------------- ### A concise solution to upgrade Postgres with Debezium connector. This solution has minimal downtime and guerantee no loss of CDC message.](https://lip17.medium.com/zero-loss-debezium-connector-migration-for-postgresdb-upgrades-af16d2acb1fd?source=post_page---author_recirc--9544aabb70b1----0---------------------3424b799_734f_401a_b417_b168b3030492--------------)

Feb 22, 2024

[7](https://lip17.medium.com/zero-loss-debezium-connector-migration-for-postgresdb-upgrades-af16d2acb1fd?source=post_page---author_recirc--9544aabb70b1----0---------------------3424b799_734f_401a_b417_b168b3030492--------------)

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2Faf16d2acb1fd&operation=register&redirect=https%3A%2F%2Flip17.medium.com%2Fzero-loss-debezium-connector-migration-for-postgresdb-upgrades-af16d2acb1fd&source=---author_recirc--9544aabb70b1----0-----------------bookmark_preview----3424b799_734f_401a_b417_b168b3030492--------------)

![Image 10: Building Chat Server With Kafka](https://miro.medium.com/v2/resize:fit:679/1*QXapdLYowHlUQ6a1LxMbKg.png)

[![Image 11: Li Pei](https://miro.medium.com/v2/resize:fill:20:20/1*NCmMr30MpR8sOUgGRwfgvw.jpeg)](https://lip17.medium.com/?source=post_page---author_recirc--9544aabb70b1----1---------------------3424b799_734f_401a_b417_b168b3030492--------------)

[Li Pei](https://lip17.medium.com/?source=post_page---author_recirc--9544aabb70b1----1---------------------3424b799_734f_401a_b417_b168b3030492--------------)

[Building Chat Server With Kafka ------------------------------- ### A simplified ChatServer design and demo based on Kafka and WebSocket.](https://lip17.medium.com/building-chat-server-with-kafka-2c988f74beb8?source=post_page---author_recirc--9544aabb70b1----1---------------------3424b799_734f_401a_b417_b168b3030492--------------)

Jan 12

[](https://lip17.medium.com/building-chat-server-with-kafka-2c988f74beb8?source=post_page---author_recirc--9544aabb70b1----1---------------------3424b799_734f_401a_b417_b168b3030492--------------)

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F2c988f74beb8&operation=register&redirect=https%3A%2F%2Flip17.medium.com%2Fbuilding-chat-server-with-kafka-2c988f74beb8&source=---author_recirc--9544aabb70b1----1-----------------bookmark_preview----3424b799_734f_401a_b417_b168b3030492--------------)

![Image 12: Local Development With Kafka Connect](https://miro.medium.com/v2/resize:fit:679/1*yuVzMhCJyDENbyhwAsrkwA.png)

[![Image 13: Li Pei](https://miro.medium.com/v2/resize:fill:20:20/1*NCmMr30MpR8sOUgGRwfgvw.jpeg)](https://lip17.medium.com/?source=post_page---author_recirc--9544aabb70b1----2---------------------3424b799_734f_401a_b417_b168b3030492--------------)

[Li Pei](https://lip17.medium.com/?source=post_page---author_recirc--9544aabb70b1----2---------------------3424b799_734f_401a_b417_b168b3030492--------------)

[Local Development With Kafka Connect ------------------------------------ ### A practical setup of Docker images for developers working with Kafka Connect everywhere](https://lip17.medium.com/local-development-with-kafka-connect-e93f34ce0590?source=post_page---author_recirc--9544aabb70b1----2---------------------3424b799_734f_401a_b417_b168b3030492--------------)

May 31, 2024

[1](https://lip17.medium.com/local-development-with-kafka-connect-e93f34ce0590?source=post_page---author_recirc--9544aabb70b1----2---------------------3424b799_734f_401a_b417_b168b3030492--------------)

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2Fe93f34ce0590&operation=register&redirect=https%3A%2F%2Flip17.medium.com%2Flocal-development-with-kafka-connect-e93f34ce0590&source=---author_recirc--9544aabb70b1----2-----------------bookmark_preview----3424b799_734f_401a_b417_b168b3030492--------------)

![Image 14: Hands-On Tutorial: Test Kubernetes Java Client In Local Environment](https://miro.medium.com/v2/resize:fit:679/1*yuVzMhCJyDENbyhwAsrkwA.png)

[![Image 15: Li Pei](https://miro.medium.com/v2/resize:fill:20:20/1*NCmMr30MpR8sOUgGRwfgvw.jpeg)](https://lip17.medium.com/?source=post_page---author_recirc--9544aabb70b1----3---------------------3424b799_734f_401a_b417_b168b3030492--------------)

[Li Pei](https://lip17.medium.com/?source=post_page---author_recirc--9544aabb70b1----3---------------------3424b799_734f_401a_b417_b168b3030492--------------)

[Hands-On Tutorial: Test Kubernetes Java Client In Local Environment ------------------------------------------------------------------- ### A handes on tutorial on how to use Java client manipulating Kubernetes resources.](https://lip17.medium.com/hands-on-tutorial-test-kubernetes-java-client-in-local-environment-c36df2bf2983?source=post_page---author_recirc--9544aabb70b1----3---------------------3424b799_734f_401a_b417_b168b3030492--------------)

Feb 16, 2024

[38](https://lip17.medium.com/hands-on-tutorial-test-kubernetes-java-client-in-local-environment-c36df2bf2983?source=post_page---author_recirc--9544aabb70b1----3---------------------3424b799_734f_401a_b417_b168b3030492--------------)

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2Fc36df2bf2983&operation=register&redirect=https%3A%2F%2Flip17.medium.com%2Fhands-on-tutorial-test-kubernetes-java-client-in-local-environment-c36df2bf2983&source=---author_recirc--9544aabb70b1----3-----------------bookmark_preview----3424b799_734f_401a_b417_b168b3030492--------------)

[See all from Li Pei](https://lip17.medium.com/?source=post_page---author_recirc--9544aabb70b1---------------------------------------)

Recommended from Medium
-----------------------

![Image 16: This new IDE from Google is an absolute game changer](https://miro.medium.com/v2/resize:fit:679/1*f-1HQQng85tbA7kwgECqoQ.png)

[![Image 17: Coding Beauty](https://miro.medium.com/v2/resize:fill:20:20/1*ViyWUoh4zqx294no1eENxw.png)](https://medium.com/coding-beauty?source=post_page---read_next_recirc--9544aabb70b1----0---------------------46994d16_11c4_4c11_a34c_a1ecac24ff92--------------)

In

[Coding Beauty](https://medium.com/coding-beauty?source=post_page---read_next_recirc--9544aabb70b1----0---------------------46994d16_11c4_4c11_a34c_a1ecac24ff92--------------)

by

[Tari Ibaba](https://medium.com/@tariibaba?source=post_page---read_next_recirc--9544aabb70b1----0---------------------46994d16_11c4_4c11_a34c_a1ecac24ff92--------------)

[This new IDE from Google is an absolute game changer ---------------------------------------------------- ### This new IDE from Google is seriously revolutionary.](https://medium.com/@tariibaba/new-google-project-idx-fae1fdd079c7?source=post_page---read_next_recirc--9544aabb70b1----0---------------------46994d16_11c4_4c11_a34c_a1ecac24ff92--------------)

Mar 11

[5.1K 293](https://medium.com/@tariibaba/new-google-project-idx-fae1fdd079c7?source=post_page---read_next_recirc--9544aabb70b1----0---------------------46994d16_11c4_4c11_a34c_a1ecac24ff92--------------)

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2Ffae1fdd079c7&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fcoding-beauty%2Fnew-google-project-idx-fae1fdd079c7&source=---read_next_recirc--9544aabb70b1----0-----------------bookmark_preview----46994d16_11c4_4c11_a34c_a1ecac24ff92--------------)

![Image 18: Ensuring Fair Processing with Celery — Part I](https://miro.medium.com/v2/resize:fit:679/1*ftA6qam2NSbrhwRCqjMDug.png)

[![Image 19: Dev Whisper](https://miro.medium.com/v2/resize:fill:20:20/1*5FxFZRyX962ICFmByi3yAQ.png)](https://medium.com/dev-whisper?source=post_page---read_next_recirc--9544aabb70b1----1---------------------46994d16_11c4_4c11_a34c_a1ecac24ff92--------------)

In

[Dev Whisper](https://medium.com/dev-whisper?source=post_page---read_next_recirc--9544aabb70b1----1---------------------46994d16_11c4_4c11_a34c_a1ecac24ff92--------------)

by

[Yuyi Kimura](https://medium.com/@yuyik46?source=post_page---read_next_recirc--9544aabb70b1----1---------------------46994d16_11c4_4c11_a34c_a1ecac24ff92--------------)

[Ensuring Fair Processing with Celery — Part I --------------------------------------------- ### Taming Celery: Fair Task Processing with Rate Limits](https://medium.com/@yuyik46/ensuring-fair-processing-with-celery-part-i-5fb7f67f91f9?source=post_page---read_next_recirc--9544aabb70b1----1---------------------46994d16_11c4_4c11_a34c_a1ecac24ff92--------------)

Nov 14, 2024

[11](https://medium.com/@yuyik46/ensuring-fair-processing-with-celery-part-i-5fb7f67f91f9?source=post_page---read_next_recirc--9544aabb70b1----1---------------------46994d16_11c4_4c11_a34c_a1ecac24ff92--------------)

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F5fb7f67f91f9&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fdev-whisper%2Fensuring-fair-processing-with-celery-part-i-5fb7f67f91f9&source=---read_next_recirc--9544aabb70b1----1-----------------bookmark_preview----46994d16_11c4_4c11_a34c_a1ecac24ff92--------------)

![Image 20: Mastering Celery: A Guide to Background Tasks, Workers, and Parallel Processing in Python](https://miro.medium.com/v2/resize:fit:679/1*o6KkvSA-i6j4DMBfAZzzsg.png)

[![Image 21: Khairi BRAHMI](https://miro.medium.com/v2/resize:fill:20:20/1*KWsMag4PRZ8RcSpv9n9Avg.jpeg)](https://khairi-brahmi.medium.com/?source=post_page---read_next_recirc--9544aabb70b1----0---------------------46994d16_11c4_4c11_a34c_a1ecac24ff92--------------)

[Khairi BRAHMI](https://khairi-brahmi.medium.com/?source=post_page---read_next_recirc--9544aabb70b1----0---------------------46994d16_11c4_4c11_a34c_a1ecac24ff92--------------)

[Mastering Celery: A Guide to Background Tasks, Workers, and Parallel Processing in Python ----------------------------------------------------------------------------------------- ### Introduction to Celery and Its Uses](https://khairi-brahmi.medium.com/mastering-celery-a-guide-to-background-tasks-workers-and-parallel-processing-in-python-eea575928c52?source=post_page---read_next_recirc--9544aabb70b1----0---------------------46994d16_11c4_4c11_a34c_a1ecac24ff92--------------)

Nov 11, 2024

[95 2](https://khairi-brahmi.medium.com/mastering-celery-a-guide-to-background-tasks-workers-and-parallel-processing-in-python-eea575928c52?source=post_page---read_next_recirc--9544aabb70b1----0---------------------46994d16_11c4_4c11_a34c_a1ecac24ff92--------------)

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2Feea575928c52&operation=register&redirect=https%3A%2F%2Fkhairi-brahmi.medium.com%2Fmastering-celery-a-guide-to-background-tasks-workers-and-parallel-processing-in-python-eea575928c52&source=---read_next_recirc--9544aabb70b1----0-----------------bookmark_preview----46994d16_11c4_4c11_a34c_a1ecac24ff92--------------)

![Image 22: If You Can Answer These 7 Concepts Correctly, You’re Decent at Python](https://miro.medium.com/v2/resize:fit:679/1*N5aLwwgTv6lRIxvhYwDKJw.png)

[![Image 23: Sabrina Carpenter 🐍](https://miro.medium.com/v2/resize:fill:20:20/1*PJD22-YlRcikHSqMF2sOIw.png)](https://medium.com/@Sabrina-Carpenter?source=post_page---read_next_recirc--9544aabb70b1----1---------------------46994d16_11c4_4c11_a34c_a1ecac24ff92--------------)

[Sabrina Carpenter 🐍](https://medium.com/@Sabrina-Carpenter?source=post_page---read_next_recirc--9544aabb70b1----1---------------------46994d16_11c4_4c11_a34c_a1ecac24ff92--------------)

[If You Can Answer These 7 Concepts Correctly, You’re Decent at Python --------------------------------------------------------------------- ### Perfect for anyone wanting to prove their Python expertise!](https://medium.com/@Sabrina-Carpenter/if-you-can-answer-these-7-concepts-correctly-youre-decent-at-python-8a21391e5911?source=post_page---read_next_recirc--9544aabb70b1----1---------------------46994d16_11c4_4c11_a34c_a1ecac24ff92--------------)

Feb 3

[1.2K 15](https://medium.com/@Sabrina-Carpenter/if-you-can-answer-these-7-concepts-correctly-youre-decent-at-python-8a21391e5911?source=post_page---read_next_recirc--9544aabb70b1----1---------------------46994d16_11c4_4c11_a34c_a1ecac24ff92--------------)

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F8a21391e5911&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40Sabrina-Carpenter%2Fif-you-can-answer-these-7-concepts-correctly-youre-decent-at-python-8a21391e5911&source=---read_next_recirc--9544aabb70b1----1-----------------bookmark_preview----46994d16_11c4_4c11_a34c_a1ecac24ff92--------------)

![Image 24: How to Distribute Tasks in Kubernetes Using Celery](https://miro.medium.com/v2/resize:fit:679/1*gX9zVTT564uu_DiRxRzXOw.jpeg)

[![Image 25: Emmanuel Davidson](https://miro.medium.com/v2/resize:fill:20:20/1*DNnf4CUA84O1HHDRBSlRbw.png)](https://medium.com/@emmanueldavidson?source=post_page---read_next_recirc--9544aabb70b1----2---------------------46994d16_11c4_4c11_a34c_a1ecac24ff92--------------)

[Emmanuel Davidson](https://medium.com/@emmanueldavidson?source=post_page---read_next_recirc--9544aabb70b1----2---------------------46994d16_11c4_4c11_a34c_a1ecac24ff92--------------)

[How to Distribute Tasks in Kubernetes Using Celery -------------------------------------------------- ### Kubernetes Pods. This article will guide you through leveraging the KubernetesPodOperatorCallback to dynamically create and manage Celery…](https://medium.com/@emmanueldavidson/how-to-distribute-tasks-in-kubernetes-using-celery-ac564f8813d2?source=post_page---read_next_recirc--9544aabb70b1----2---------------------46994d16_11c4_4c11_a34c_a1ecac24ff92--------------)

Nov 29, 2024

[1](https://medium.com/@emmanueldavidson/how-to-distribute-tasks-in-kubernetes-using-celery-ac564f8813d2?source=post_page---read_next_recirc--9544aabb70b1----2---------------------46994d16_11c4_4c11_a34c_a1ecac24ff92--------------)

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2Fac564f8813d2&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40emmanueldavidson%2Fhow-to-distribute-tasks-in-kubernetes-using-celery-ac564f8813d2&source=---read_next_recirc--9544aabb70b1----2-----------------bookmark_preview----46994d16_11c4_4c11_a34c_a1ecac24ff92--------------)

![Image 26: 5 Python Decorators That Will Transform Your Coding Workflow](https://miro.medium.com/v2/resize:fit:679/0*bbDuRtK_uxAkpGUT)

[![Image 27: Python in Plain English](https://miro.medium.com/v2/resize:fill:20:20/1*VA3oGfprJgj5fRsTjXp6fA@2x.png)](https://python.plainenglish.io/?source=post_page---read_next_recirc--9544aabb70b1----3---------------------46994d16_11c4_4c11_a34c_a1ecac24ff92--------------)

In

[Python in Plain English](https://python.plainenglish.io/?source=post_page---read_next_recirc--9544aabb70b1----3---------------------46994d16_11c4_4c11_a34c_a1ecac24ff92--------------)

by

[Kevin Meneses González](https://medium.com/@kevinmenesesgonzalez?source=post_page---read_next_recirc--9544aabb70b1----3---------------------46994d16_11c4_4c11_a34c_a1ecac24ff92--------------)

[5 Python Decorators That Will Transform Your Coding Workflow ------------------------------------------------------------ ### In the realm of programming, efficiency often lies in how elegantly we can reuse and extend code. Python decorators are a powerful tool…](https://medium.com/@kevinmenesesgonzalez/5-python-decorators-that-will-transform-your-coding-workflow-38a9c199f7d9?source=post_page---read_next_recirc--9544aabb70b1----3---------------------46994d16_11c4_4c11_a34c_a1ecac24ff92--------------)

Dec 27, 2024

[1K 12](https://medium.com/@kevinmenesesgonzalez/5-python-decorators-that-will-transform-your-coding-workflow-38a9c199f7d9?source=post_page---read_next_recirc--9544aabb70b1----3---------------------46994d16_11c4_4c11_a34c_a1ecac24ff92--------------)

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F38a9c199f7d9&operation=register&redirect=https%3A%2F%2Fpython.plainenglish.io%2F5-python-decorators-that-will-transform-your-coding-workflow-38a9c199f7d9&source=---read_next_recirc--9544aabb70b1----3-----------------bookmark_preview----46994d16_11c4_4c11_a34c_a1ecac24ff92--------------)

[See more recommendations](https://medium.com/?source=post_page---read_next_recirc--9544aabb70b1---------------------------------------)

[Help](https://help.medium.com/hc/en-us?source=post_page-----9544aabb70b1---------------------------------------)

[Status](https://medium.statuspage.io/?source=post_page-----9544aabb70b1---------------------------------------)

[About](https://medium.com/about?autoplay=1&source=post_page-----9544aabb70b1---------------------------------------)

[Careers](https://medium.com/jobs-at-medium/work-at-medium-959d1a85284e?source=post_page-----9544aabb70b1---------------------------------------)

[Press](mailto:pressinquiries@medium.com)

[Blog](https://blog.medium.com/?source=post_page-----9544aabb70b1---------------------------------------)

[Privacy](https://policy.medium.com/medium-privacy-policy-f03bf92035c9?source=post_page-----9544aabb70b1---------------------------------------)

[Rules](https://policy.medium.com/medium-rules-30e5502c4eb4?source=post_page-----9544aabb70b1---------------------------------------)

[Terms](https://policy.medium.com/medium-terms-of-service-9db0094a1e0f?source=post_page-----9544aabb70b1---------------------------------------)

[Text to speech](https://speechify.com/medium?source=post_page-----9544aabb70b1---------------------------------------)
