import pandas as pd

"""
# My first app
Here's our first attempt at using data to create a table:
"""

df = pd.DataFrame({
        'first column': [1, 2, 3, 4],
        'second column': [10, 20, 30, 40]
    })

df


# try:
#     df = pd.DataFrame({
#         'first column': [1, 2, 3, 4],
#         'second column': [10, 20, 30, 40]
#     })
#
#     df
#     # Your code that may raise an error
#     # result = 10 / 0  # This will raise a ZeroDivisionError
# except Exception as e:
#     logging.exception("An error occurred:")


