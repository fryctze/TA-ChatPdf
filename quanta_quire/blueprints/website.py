import os
from flask import Blueprint, render_template, current_app, flash, session, redirect, url_for, send_from_directory
from quanta_quire.helper import delete_all_pdfs, get_first_pdf_file

from quanta_quire.forms import UploadForm

blueprint = Blueprint("menus", __name__)


@blueprint.route("/")
def chat():
  return render_template("menu/chat.html", page_name='chat')


@blueprint.route("/document", methods=['GET', 'POST'])
def document():
  form = UploadForm()
  if form.validate_on_submit():
    delete_all_pdfs()
    f = form.document.data
    filename = f.filename
    f.save(os.path.join(current_app.config['UPLOAD_PATH'], filename))
    flash('Upload success.')
    session['filename'] = [filename]
    return redirect(url_for('menus.document'))

  # Get the first PDF file in UPLOAD_FOLDER
  pdf_file = get_first_pdf_file()
  return render_template("menu/document.html",
                         page_name='document', pdf_file=pdf_file,
                         form=form)


@blueprint.route('/document/<path:filename>', methods=['GET', 'POST'])
def document_download(filename):
  uploads = os.path.join(current_app.root_path, current_app.config['UPLOAD_PATH'])
  return send_from_directory(uploads, filename)


@blueprint.route('/data')
def data():
  return render_template("menu/data.html", page_name='data')


@blueprint.route('/token')
def change_token():
  return render_template("menu/token.html", page_name='token')
