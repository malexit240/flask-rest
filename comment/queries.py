

def comment_list(db, post_id):
    return db.execute(
        "SELECT c.id, body, created, author_id, username FROM comment c INNER JOIN user u ON c.author_id=u.id"
    ).fetchall()


def get_comment(db, id):
    return db.execute(
            "SELECT comment.id, title, body, created, author_id, username"
            " FROM comment JOIN user u ON comment.author_id = u.id"
            " WHERE comment.id = ?",
            (id,),
        ).fetchone()


def create_comment(db, body, author_id,post_id):
    db.execute(
        "INSERT INTO comment(body, author_id, post_id) VALUES ( ?, ?,?)",
        (body, author_id, post_id),
    )
    db.commit()


def update_comment(db, title, body, id):
    db.execute(
        "UPDATE comment SET body=? WHERE id=?",
        (body, id)
    )
    db.commit()


def delete_comment(db, id):
    db.execute("DELETE FROM comment WHERE id = ?", (id,))
    db.commit()
