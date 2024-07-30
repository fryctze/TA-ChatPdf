from quanta_quire.extensions import db
from quanta_quire.models import ChatLog


def clean_up_duplicates():
  # Subquery to get the latest entry for each user, question, and answer combination
  latest_entries = db.session.query(
    ChatLog.id,
    ChatLog.user,
    ChatLog.question,
    ChatLog.answer,
    ChatLog.timestamp
  ).distinct(ChatLog.user, ChatLog.question, ChatLog.answer).order_by(
    ChatLog.user, ChatLog.question, ChatLog.answer, ChatLog.timestamp.desc()
  ).subquery()

  # Delete entries that are not the latest
  db.session.query(ChatLog).filter(
    ~ChatLog.id.in_(
      db.session.query(latest_entries.c.id)
    )
  ).delete(synchronize_session=False)

  # Commit the changes
  db.session.commit()


# Call the cleanup function
# clean_up_duplicates()

def recreate_table():
  db.drop_all()
  db.create_all()
