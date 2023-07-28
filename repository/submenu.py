


def get_all(session = Depends(get_db)):
    return session.query(Submenu).all()