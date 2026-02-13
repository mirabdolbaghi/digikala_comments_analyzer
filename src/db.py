import sqlite3
from typing import Optional, List, Tuple, Any


class CommentDB:
    def __init__(self, db_path: str = "comments.db") -> None:
        self.db_path = db_path
        self._create_table()

    def _get_conn(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _create_table(self) -> None:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS comments (
                id     INTEGER PRIMARY KEY AUTOINCREMENT,
                comment TEXT NOT NULL,
                rate    INTEGER NOT NULL
            )
            """
        )
        conn.commit()
        conn.close()

    def create_comment(self, comment: str, rate: int) -> int:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO comments (comment, rate) VALUES (?, ?)",
            (comment, rate),
        )
        conn.commit()
        new_id = cur.lastrowid
        conn.close()
        return new_id
    
    def create_comments_batch(
        self,
        rows: List[Tuple[str, int]],
    ) -> int:
        """
        rows: list of (comment, rate)
        returns: number of inserted rows
        """
        if not rows:
            return 0

        conn = self._get_conn()
        cur = conn.cursor()
        cur.executemany(
            "INSERT INTO comments (comment, rate) VALUES (?, ?)",
            rows,
        )
        conn.commit()
        count = cur.rowcount
        conn.close()
        return count

    def get_comment(self, comment_id: int) -> Optional[Tuple[Any, ...]]:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, comment, rate FROM comments WHERE id = ?",
            (comment_id,),
        )
        row = cur.fetchone()
        conn.close()
        return row

    def get_all_comments(self) -> List[Tuple[Any, ...]]:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT comment, rate FROM comments")
        rows = cur.fetchall()
        conn.close()
        return rows


    def delete_all_comment(self) -> bool:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM comments")
        conn.commit()
        deleted = cur.rowcount > 0
        conn.close()
        return deleted