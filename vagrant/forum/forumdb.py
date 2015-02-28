#
# Database access functions for the web forum.
#

import time
import psycopg2
import bleach

## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    ## Database connection
    db = psycopg2.connect("dbname=forum")
    cursor = db.cursor()
    # fetch all posts with their timestamps:
    cursor.execute("select time, content from posts order by time")
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    posts = [{'content': str(row[1]), 'time': str(row[0])} for row in rows]
    return posts

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    ## Database connection
    db = psycopg2.connect("dbname=forum")
    cursor = db.cursor()
    clean_content = bleach.clean(content, strip=True)
    cursor.execute("insert into posts (content) values (%s)", (clean_content,))
    db.commit()
    cursor.close()
    db.close()
