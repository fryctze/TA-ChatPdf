from quanta_quire.extensions import db
from quanta_quire.models import ChatLog
from sqlalchemy import func
import json


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


def count_total():
  result = db.session.query(
    ChatLog.point,
    func.count(ChatLog.id).label('total')
  ).group_by(ChatLog.point).all()

  # Convert result to a dictionary or list of dicts
  counts = {str(point) if point is not None else 'None': total for point, total in result}
  return counts


def count_by_user():
  # Count messages grouped by user
  # result = db.session.query(
  #   ChatLog.user,
  #   func.count(ChatLog.id).label('total')
  # ).group_by(ChatLog.user).all()
  #
  # # Convert result to a dictionary or list of dicts
  # counts = {user: total for user, total in result}
  # return counts
  # Count messages grouped by user, excluding those with category = None
  result = ((db.session.query(
    ChatLog.user,
    func.count(ChatLog.id).label('total')
  ).filter(ChatLog.point.isnot(None))
             .group_by(ChatLog.user))
            .all())

  # Convert result to a dictionary or list of dicts
  counts = {user: total for user, total in result}
  return counts


def sum_by_user_and_category():
  # Query to sum each category for each user
  result = ((db.session.query(
    ChatLog.user,
    ChatLog.point,
    func.count(ChatLog.id).label('total')
  ).filter(ChatLog.point.isnot(None))
             .group_by(ChatLog.user, ChatLog.point))
            .all())

  # Convert result to a dictionary or list of dicts
  sums = {}
  for user, point, total in result:
    if user not in sums:
      sums[user] = {}
    sums[user][point] = total

  return sums


def exporting_data():
  results = db.session.query(ChatLog).all()
  data = [
    {
      'id': log.id,
      'timestamp': log.timestamp.isoformat() if log.timestamp else None,
      'user': log.user,
      'question': log.question,
      'answer': log.answer,
      'category': log.point
    }
    for log in results
  ]
  with open('data.json', 'w') as file:
    json.dump(data, file, indent=4, default=str)
  return data