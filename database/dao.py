from database.DB_connect import DBConnect
from model.artist import Artist

class DAO:

    @staticmethod
    def get_all_artists():

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT *
                FROM artist a
                """
        cursor.execute(query)
        for row in cursor:
            artist = Artist(id=row['id'], name=row['name'])
            result.append(artist)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_artisti_filtrati(n_min_album):

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                    select a.id, a.name
                    from artist a, album b
                    where a.id = b.artist_id 
                    group by a.id 
                    having count(b.id) > %s
                """
        cursor.execute(query, (n_min_album,))
        for row in cursor:
            artist = Artist(id=row['id'], name=row['name'])
            result.append(artist)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_connesioni():

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                    select distinct b1.artist_id as a1, b2.artist_id as a2, count(DISTINCT t1.genre_id) as peso
                    from album b1, album b2, track t1, track t2
                    where b1.artist_id < b2.artist_id 
                    and b1.id = t1.album_id 
                    and b2.id = t2.album_id 
                    and t1.genre_id = t2.genre_id 
                    group by b1.artist_id, b2.artist_id 

                    """
        cursor.execute(query)
        for row in cursor:
            result.append((row['a1'], row['a2'], row['peso']))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_art_validi(d_min):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ 
                select distinct b.artist_id as id, a.name
                from album b, track t, artist a
                where a.id = b.artist_id 
                and (t.milliseconds / 60000) > %s
                """
        cursor.execute(query, (d_min,))
        for row in cursor:
            artist = Artist(id=row['id'], name=row['name'])
            result.append(artist)
        cursor.close()
        conn.close()
        return result