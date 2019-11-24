"""this module contains function for queries to db"""

def get_comment_list(db, post_id:int):
    """returns list of comments to post by post_id"""
    a = db.execute(
        "SELECT c.id, c.body, c.created, c.author_id, u.username"
         " FROM (comment c LEFT JOIN user u ON c.author_id=u.id) LEFT JOIN post p ON c.post_id=p.id"
         " WHERE p.id={} ORDER BY c.created DESC".format(post_id)).fetchall()
    return a


def get_comment(db, id):
    """return a comment by id"""
    return db.execute(
            "SELECT c.id, body, created, author_id, username"
            " FROM comment c JOIN user u ON c.author_id = u.id"
            " WHERE c.id = ?",
            (id,)
        ).fetchone()


def create_comment(db, body, author_id,post_id):
    """add a comment to post by post_id"""
    db.execute(
        "INSERT INTO comment(body, author_id, post_id) VALUES ( ?, ?,?)",
        (body, author_id, post_id),
    )
    db.commit()


def update_comment(db, body, id):
    """update a comment by id"""
    db.execute(
        "UPDATE comment SET body=? WHERE id=?",
        (body, id)
    )
    db.commit()


def delete_comment(db, id):
    """delete a comment by id"""
    db.execute("DELETE FROM comment WHERE id = ?", (id,))
    db.commit()
