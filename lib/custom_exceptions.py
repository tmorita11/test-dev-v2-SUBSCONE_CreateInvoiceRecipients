class S3Error(Exception):
    """基本的なS3エラー"""
    pass


class DatabaseError(Exception):
    """基本的なデータベースエラー"""
    pass


class DatabaseQueryError(DatabaseError):
    """データベースクエリ実行時のエラー"""
    pass
