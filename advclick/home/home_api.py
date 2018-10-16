from flask import Blueprint

bp = Blueprint('home', __name__, url_prefix='/home')


@bp.route("/upload_earn", methods=('GET', 'POST'))
def upload_earn():
    return "UploadEarn"


@bp.route("/get_earn", methods=('GET', 'POST'))
def get_earn():
    return "GetEarn"
