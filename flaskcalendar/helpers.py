# TODO: Move this to helpers?
def addToHistory(instance,action):
    hist = History(time = datetime.utcnow(), entry=(instance), action=action)
    db.session.add(hist)
    db.session.commit()


def save_pictures(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = str(current_user.id) + '_' + random_hex + f_ext
    picture_path = os.path.join(app.root_path,'static\pics', picture_fn)

    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn
