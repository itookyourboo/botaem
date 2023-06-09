"""
Run redis:

$ docker build . t redis-task
$ docker run -d -p 6380:6380 redis-task

Install py-redis:

$ pip install redis
"""
import functools
import json
import re
import time
from typing import Callable, Any

from redis import Redis, ConnectionPool

pool = ConnectionPool(port=6380)
redis_client = Redis(connection_pool=pool)

H_BLOG_POST = "blog_post"


# Data Storage and Retrieval

def store_post(redis: Redis, post_id: int, content: str) -> None:
    """
    Implement a function to store a blog post in Redis.
    The function should take the blog post ID and content as input
    and store them as a hash data structure in Redis.
    """
    redis.hset(f"{H_BLOG_POST}:{post_id}", "content", content)


def get_post(redis: Redis, post_id: int) -> str:
    """
    Implement a function to retrieve a blog post from Redis based on its ID.
    """
    return redis.hget(f"{H_BLOG_POST}:{post_id}", "content").decode("utf8")


def delete_post(redis: Redis, post_id: int) -> None:
    """
    Implement a function to delete a blog post from Redis based on its ID.
    """
    redis.hdel(f"{H_BLOG_POST}:{post_id}")


# Indexing and Searching

def index_post(redis: Redis, post_id: int, content: str) -> None:
    """
    Implement a function to index the blog posts' content using Redis's Sorted Sets.
    Each word in the blog post's content should be a member of a Sorted Set,
    with its score representing the occurrence frequency.
    """
    words: list[str] = re.findall(r"\w+", content)
    for word in words:
        redis.zincrby(f"index:{word}", 1, post_id)


def search_posts(redis: Redis, keyword: str) -> list[int]:
    """
    Implement a function to search for blog posts based on a given keyword.
    The function should return a list of blog post IDs ranked by relevance to the keyword.
    """
    index_key: str = f"index:{keyword}"
    if not redis.exists(index_key):
        return []

    return list(map(int, redis.zrevrangebyscore(index_key, "+inf", "-inf")))


# Expiration

def set_expire_time(redis: Redis, post_id: int, seconds: int) -> None:
    """
    Implement a function to set an expiration time for a blog post in Redis.
    The function should take the blog post ID and expiration time in seconds
    as input and set the expiration for that key accordingly.
    """
    redis.expire(f"{H_BLOG_POST}:{post_id}", seconds)


# Data Retrieval

def get_all_posts(redis: Redis) -> list[tuple[int, str]]:
    posts: list[tuple[int, str]] = []
    for key in redis.scan_iter(f"{H_BLOG_POST}:*"):
        id_: int = int(key.split(b":")[1])
        post = redis.hgetall(key)
        posts.append((id_, post[b"content"].decode("utf8")))
    return posts


def get_post_count(redis: Redis) -> int:
    return len(tuple(redis.scan_iter(f"{H_BLOG_POST}:*")))


# Caching and Invalidations


def fetch_from_storage(post_id: int) -> str:
    time.sleep(0.250)
    return "Lorem ipsum dolor sit amet, consectetur adipiscing elit"


def get_post_cached(redis: Redis, post_id: int) -> str:
    """
    Implement a caching mechanism using Redis for frequently accessed blog posts.
    Whenever a blog post is retrieved, it should be cached in Redis.
    Subsequent requests for the same blog post should first check the cache
    before fetching the data from the database or any other persistent storage.
    """
    post: str
    if redis.exists(f"{H_BLOG_POST}:{post_id}"):
        post = get_post(redis_client, post_id)
    else:
        post = fetch_from_storage(post_id)
        store_post(redis_client, post_id, post)
    return post


def invalidate_post_cache(redis: Redis, post_id: int) -> None:
    """
    Implement a function to invalidate the cache for a specific blog post.
    This function should be called whenever a blog post is updated or deleted.
    """
    redis.delete(f"{H_BLOG_POST}:{post_id}")


# Pub/Sub

POSTS_CHANNEL = "posts_channel"


def publish_post(redis: Redis, post_id: int, content: str) -> None:
    """
    Implement a pub/sub mechanism using Redis. Whenever a new blog post is created,
    publish a message to a specific channel.
    Subscribers should receive the message containing the blog post ID and content.
    """
    store_post(redis, post_id, content)
    message = dict(post_id=post_id, content=content)
    redis.publish(POSTS_CHANNEL, json.dumps(message).encode("utf8"))


def handle_message(message: dict) -> None:
    """
    Implement a subscriber that listens to the channel and logs the received blog post information.
    """
    received_message = message["data"]
    print(f"Received message: {received_message}")


def run_subscriber():
    for i_message in pubsub.listen():
        if i_message["type"] == "message":
            handle_message(i_message)


pubsub = redis_client.pubsub()
pubsub.subscribe(POSTS_CHANNEL)


# Transactions

def atomacity(func: Callable) -> Callable:
    """
    Implement a transaction to ensure atomicity
    when updating a blog post's content and its associated indexes.
    Rollback the transaction if any operation fails within the transaction.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        transaction = redis_client.pipeline()
        result = func(transaction, *args[1:], **kwargs)
        transaction.execute()
        return result

    return wrapper


index_post = atomacity(index_post)
