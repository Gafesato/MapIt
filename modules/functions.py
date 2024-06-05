db_topics, db_total_topics = None, None
db_total_rel_topics = int

relevance_status = False

def update_root_screen(process=1, relevance_status=False):
    global db_topics
    global db_total_topics
    global db_total_rel_topics

    db_topics, db_total_topics = getTopicList()
    if process == 1:
        try:
            if db_total_topics > 5:
                db_total_rel_topics = 6
            else:
                db_total_rel_topics = db_total_topics
        except TypeError:
            pass
    
    


def relevance_up_to_date():
    # Especificar relevancia al día
    try:
        cursor, con = openDB('user.db')
        cursor.execute('UPDATE user_info SET relevancia = ? WHERE id = ?', (relevance_status, 1,))
        con.commit()
        con.close()
        return True
    except Exception:
        return False