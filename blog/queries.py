"""this module contains function for queries to db"""

def get_post_list(db):
    """returns list of posts, most recent first"""
    return db.execute(
        "SELECT p.id, title, body, created, author_id, u.username FROM post p INNER JOIN user u ON p.author_id=u.id ORDER BY p.created"
    ).fetchall()


def get_post(db, id):
    """return a post by id"""
    return db.execute(
            "SELECT p.id, title, body, created, author_id, username"
            " FROM post p JOIN user u ON p.author_id = u.id"
            " WHERE p.id = ?",
            (id,),
        ).fetchone()


def create_post(db, title, body, author_id):
    """create a post"""
    db.execute(
        "INSERT INTO post(title, body, author_id) VALUES (?, ?, ?)",
        (title, body, author_id),
    )
    db.commit()


def update_post(db, title, body, id):
    """update a post by id"""
    db.execute(
        "UPDATE post SET title=?,body=? WHERE id=?",
        (title, body, id)
    )
    db.commit()


def delete_post(db, id):
    """delete a post by id"""
    db.execute("DELETE FROM post WHERE id = ?", (id,))
    db.commit()
