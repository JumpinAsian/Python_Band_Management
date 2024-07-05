from flask_app.config.mysqlconnection import connect
from flask_app.models import user
from flask import flash
mydb = "band_together"


class Band:
    def __init__(self, data):
        self.id = data['id']
        self.band_name = data['band_name']
        self.music_genre = data['music_genre']
        self.home_city = data['home_city']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None

    @classmethod
    def save(cls, data):
        query = """
                INSERT INTO bands (band_name, music_genre, home_city, user_id)
                VALUES (%(band_name)s,%(music_genre)s,%(home_city)s,%(user_id)s);
                """
        return connect(mydb).query_db(query, data)

    @classmethod
    def get_all_bands(cls):
        query = """
                SELECT * FROM bands
                JOIN users on bands.user_id = users.id;
                """
        results = connect(mydb).query_db(query)
        bands = []
        for row in results:
            this_band = cls(row)
            user_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": "",
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            this_band.creator = user.User(user_data)
            bands.append(this_band)
        return bands

    @classmethod
    def get_band_by_id(cls, data):
        query = """
                SELECT * FROM bands
                JOIN users on bands.user_id = users.id
                WHERE bands.id = %(id)s;
                """
        result = connect(mydb).query_db(query, data)
        # print('results', result)
        if not result:
            return False
        result = result[0]
        this_band = cls(result)
        user_data = {
            "id": result['users.id'],
            "first_name": result['first_name'],
            "last_name": result['last_name'],
            "email": result['email'],
            "password": "",
            "created_at": result['users.created_at'],
            "updated_at": result['users.updated_at']
        }
        this_band.creator = user.User(user_data)
        # print('this_band', this_band)
        return this_band

    @classmethod
    def update_band(cls, form_data):
        query = """
                UPDATE bands
                SET band_name = %(band_name)s,
                music_genre = %(music_genre)s,
                home_city = %(home_city)s
                WHERE id = %(id)s;
                """
        results = connect(mydb).query_db(query, form_data)
        print(results)
        return results

    @classmethod
    def delete(cls, data):
        query = """
                DELETE FROM bands
                WHERE id = %(id)s;
                """
        return connect(mydb).query_db(query, data)

    @staticmethod
    def validate_band(request):
        is_valid = True
        if len(request['band_name']) < 1:
            is_valid = False
            flash('*Band Name required')
        elif len(request['band_name']) <= 1:
            is_valid = False
            flash('*Band Name must be at least 2 characters long')
        if len(request['music_genre']) < 1:
            is_valid = False
            flash('*Music Genre required')
        elif len(request['music_genre']) <= 1:
            is_valid = False
            flash('*Music Genre must be at least 2 characters long')
        if len(request['home_city']) < 1:
            is_valid = False
            flash('*Home City required')
        elif len(request['home_city']) <= 1:
            is_valid = False
            flash('*Home City must be at least 2 characters long')
        return is_valid
