from flask import Blueprint, request, send_file

bp = Blueprint('image', __name__, url_prefix='/image')


@bp.route("/get_image", methods=('GET', 'POST'))
def image():
    name = request.args.get('name')
    if name is not None and name != '':
        try:
            return send_file('../images/' + name)
        except FileNotFoundError as e:
            print(e)
    return send_file('../images/' + 'logo.png')
