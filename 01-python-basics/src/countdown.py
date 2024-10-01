from datetime import *
import traceback


def transformAndReturnUserInput():
  provided_datetime = datetime(year, month, day)
  sysdate = datetime.now()
  time_difference = provided_datetime - sysdate
  print(f"Time until deadline:\n" \
        f"Days {time_difference.days}\n" \
        f"Hours {int(time_difference.seconds / 3600)}\n" \
        f"Minutes {int((time_difference.seconds % 3600) / 60)}\n" \
        f"Seconds {time_difference.seconds % 60}\n" \
        "")

def isUserInputValid():
  try:
    user_input_list = user_input.split(':')
    if len(user_input_list) <= 1 or len(user_input_list) > 2:
      print("List of size 2 could not be created. Provided input does not conform to the format.")
      return False
    elif len(user_input_list) == 2:
      provided_user_date = user_input_list[1].split('.')
      if len(provided_user_date) != 3:
        print("Date provided does not conform to the format DD.MM.YYYY")
        return False
      else:
        global day, month, year
        day = int(provided_user_date[0])
        month = int(provided_user_date[1])
        year = int(provided_user_date[2])
        if day > 31 or day < 1:
          print("DD not between 1-31")
          return False
        if month > 12 or month < 1:
          print("MM not between 1-12")
          return False
        if year > 2050 or year < 2024:
          print("YYYY not between 2024-2050")
          return False
        # Length is three and date is between 01.01.2024-12.12.2050
        print("User Input is valid. Processing...")
        return True
    else:
      print("User Input could not be parsed.")
      return False
  except Exception as e:
    traceback.print_exc()
    print(e)
    return False

user_input = ""
while user_input != "done":
  user_input = input("\n~\n>Provide a future task:date in the format <string>:<date'DD.MM.YYYY'> to see remaining time to completion (TTC):\n\n" \
                    ">Example:\n" \
                    ">master thesis:30.11.2028\n" \
                    "------------------------- [to exit write 'done']\n")
  if user_input == "done":
    quit()
  elif isUserInputValid() == True:
    transformAndReturnUserInput()
  else:
    print("User Input invalid. Exiting Loop...")
