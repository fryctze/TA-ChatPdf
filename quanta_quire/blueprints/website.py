import os

from flask import Blueprint, render_template, current_app, flash, session, redirect, url_for, send_from_directory

from quanta_quire.app.vectorstore import splitter, generate_vectorstore
from quanta_quire.helper import delete_all_pdfs, get_first_pdf_file, get_pdf_page_num, get_session_id
from quanta_quire.forms import UploadForm

blueprint = Blueprint("website", __name__)


@blueprint.route("/", methods=['GET', 'POST'])
def chat():
  current_app.logger.info("Rendered homepage chat")
  user = get_session_id()
  return render_template("menu/chat.html", page_name='chat', session_id=user)


@blueprint.route("/document", methods=['GET', 'POST'])
def document():
  size = 1000
  overlap = 200

  #if get_first_pdf_file() is not None:


  form = UploadForm()
  if form.validate_on_submit():
    delete_all_pdfs()
    f = form.document.data
    filename = f.filename
    f.save(os.path.join(current_app.config['UPLOAD_PATH'], filename))
    flash('Upload success.')

    chunks = splitter(size, overlap)
    current_app.chunks = len(chunks)
    generate_vectorstore(chunks)
    # create_chroma(chunks)

    return redirect(url_for('website.document'))

  # Get the first PDF file in UPLOAD_FOLDER
  pdf_file = get_first_pdf_file()
  pdf_pages = get_pdf_page_num()
  chunks = 0 if pdf_file is None else len(splitter(size, overlap)) if current_app.chunks == 0 else current_app.chunks
  current_app.chunks = chunks


  context = {
    'page_name': 'document',
    'pdf_file': pdf_file,
    'pdf_pages': pdf_pages,
    'form': form,
    'size': size,
    'overlap': overlap,
    'chunks': chunks
  }
  return render_template("menu/document.html", **context)


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
