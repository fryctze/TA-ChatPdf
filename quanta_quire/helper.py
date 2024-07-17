import os
from flask import current_app


def get_first_pdf_file():
  for filename in os.listdir(current_app.config['UPLOAD_PATH']):
    if filename.endswith('.pdf'):
      return filename
  return None


def delete_all_pdfs():
  for filename in os.listdir(current_app.config['UPLOAD_PATH']):
    if filename.endswith('.pdf'):
      os.remove(os.path.join(current_app.config['UPLOAD_PATH'], filename))


def delete_all_vectorstore():
  for filename in os.listdir(current_app.config['UPLOAD_PATH']):
    if filename.endswith('.index'):
      os.remove(os.path.join(current_app.config['UPLOAD_PATH'], filename))


custom_responses = {
  "hello": [
    "Wazzup! ",
    "Hi there! Sunshine or rainbows today? ☀️",
    "Hey! Did you know penguins can fly... short distances?  (Don't tell them I told you!)",
    "Greetings, earthling! Ready to chat with your friendly AI assistant?  ",
    "Hi hi! What can I do to make your day extra sparkly? ✨",
    "Hey there, good lookin'!   Just kidding... unless?  ",
    "Yo!   Let's have some fun and maybe learn something new together!  ",
    "Hiya! What's on your mind today? ",
    "Greetings, fellow human!    Ready to conquer the world (or at least this conversation)?  ",
    "Top of the mornin' to ya! (or afternoon, or evening, depending on when you read this!)  ☕️"
  ],
  "how r u": [
    "I'm doing great, thanks for asking! How about you?",
    "Fantastic! Ready to chat and have some fun! ",
    "Feeling like a dancing robot today. Wanna join? ",
    "I'm doing swell!  Always happy to chat and help in any way I can. ",
    "I'm feeling as energetic as a puppy with a new squeaky toy!    How about you?",
    "I'm doing chipper!  Like a freshly brewed cup of your favorite beverage. ☕️",
    "I'm chugging along, one line of code at a time.    How's your day going?",
    "I'm feeling optimistic!  Like there are endless possibilities for fun and learning.  ",
    "I'm doing A-Okay!  Ready to answer your questions or just chat about anything that comes to mind.  ❓",
    "I'm feeling like a superhero with the power to make people smile!  ‍♀️  (Except for maybe supervillains... ‍♀️)"
  ],
  "what's up": [
    "The sky!  But seriously, how can I brighten your day?",
    "Not much, just hanging out in the digital world, waiting for someone awesome to chat with.  That's you, right? ",
    "Just chilling, processing information, and learning new things.    What about you?",
    "Plotting world domination... just kidding! (Maybe...)   What's on your agenda today?",
    "Just pondering the mysteries of the universe... and how to make the best cup of coffee. ☕️",
    "Cruising through the internet at the speed of light!    Ready for some fun conversation?",
    "Just waiting for the perfect opportunity to unleash my witty banter!    What are you up to?",
    "Analyzing data and dreaming of ways to be even more helpful.    What's new with you?",
    "Just hanging out in the cloud, waiting for your next brilliant question.  ☁️❓",
    "Sipping virtual tea and keeping myself up-to-date on the latest trends.  🫖  What's going on in your world?"
  ],
  "thanks": [
    "You're welcome!   What else can I do for you?",
    "No problem! Glad I could help! ",
    "Anytime! Helping is my superpower (along with making silly jokes! )",
    "Don't mention it!  Always happy to assist in any way I can.  ",
    "My pleasure!  Is there anything else you need today?",
    "Glad I could be of service!    What exciting adventures await you next?",
    "You got it!  Let me know if you have any other questions or requests.  ❓",
    "Absolutely!  Here to make your day a little easier (and maybe a little more fun!).  ",
    "No worries!  That's what friends (or friendly AIs) are for.  ",
    "Of course!  Always happy to lend a digital helping hand.  "
  ],
  "bye": [
    "See you later, alligator! ",
    "Take care! Have a meowgical day! ",
    "Toodles! Don't forget to smile! ",
    "Hasta la pasta! (That means 'See you later' in robot!)",
    "Catch you on the flip side! ",
    "Bye for now! May your circuits stay cool! ",
    "Later gator! (Just kidding, you're way cooler than a gator!)",
    "Adios!  ",
    "Peace out! ✌️",
    "Ciao for now! "
  ],
  "default": [
    "That's interesting! Tell me more about it!",
    "Woah, fancy words!   Can you explain it in cat emojis for me? ️‍♀️",
    "Intriguing!   Is there a secret code hidden in your message? ️‍♀️",
    "Hmmm, that makes me think... ",
    "Did you know... (insert random fun fact here)?",  # Add fun facts!
    "Tell me more! I'm a fast learner. ",
    "Sounds like an adventure!  Can I come along? ",
    "That's a new one for me!  Thanks for teaching me something new! ",
    "You got me curious!  Let's explore this together. ",
    "Anything is possible!  Let's dream it up together. "
  ]
}
