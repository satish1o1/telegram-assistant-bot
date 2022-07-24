from telegram import ReplyKeyboardMarkup,ReplyKeyboardRemove
from telegram.ext import MessageHandler,Updater,ConversationHandler,Filters,CommandHandler
import re
import logging
import pandas as pd
import json
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# The API Key we received for our bot
API_KEY = "5589662713:AAFn5KtajeAwVGTmf9j0Q18E3lp1c19XDlQ"
# Create an updater object with our API Key
updater = Updater(API_KEY)
# Retrieve the dispatcher, which will be used to add handlers
dispatcher = updater.dispatcher
# Our states, as integers
IDENTIFY = 1
DIRECTOR = 2
DETAILS = 3
MARKS = 4
SEM_RESULTS =5
EDITMARKS = 6
MANIP_SUB = 7
JOBS = 8
ULINKS = 9
TOOLS = 10
HELP = 11
CANCEL = 12


MENU_MARKUP = ReplyKeyboardMarkup([['DETAILS', 'MARKS', 'EDITMARKS'],
                                            ['TOOLS','JOBS','U-LINKS'],
                                            ['HELP','END CONVERSATION']], one_time_keyboard=True)

GRADE_MARKUP = ReplyKeyboardMarkup([['O','S','A'],['B','C','D']])
sem_markups = {
"SEM-1" : ReplyKeyboardMarkup([ ['ENGLISH', 'MATHEMATICS-1', 'APPLIED CHEMISTRY'],
                                             ['FUNDAMENTALS OF COMPUTER SCIENCE', 'ENGINEERING DRAWING'],
                                             ['ENGLISH LAB', 'IT WORKSHOP'],
                                         ['RETURN']]),
"SEM-2" : ReplyKeyboardMarkup([['MATHEMATICS-2', 'MATHEMATICS-3', 'APPLIED PHYSICS'],
                                             ['PROGRAMMING FOR PROBLEM SOLVING USING C', 'DIGITAL LOGIC DESIGN', 'APPLIED PHYSICS LAB'],
                                             ['COMMUNICATION SKIIL LAB', 'PROGRAMMING FOR PROBLEM SOLVING USING C LAB', 'ENGINEERING EXPLORAION PROJECT'],
                                         ['RETURN']]),
"SEM-3" : ReplyKeyboardMarkup([['MATHEMATICAL FOUNDATIONS OF COMPUTER SCIENCE', 'SOFTWARE ENGINEERING', 'PYTHON PROGRAMMING'],
                                             ['DATA STRUCTURES', 'OBJECT ORIENTED PROGRAMMING THROUGH C++', 'COMPUTER ORGAINZATION']
                                                ,[ 'PYTHON PROGRAMMING LAB', 'DATA STRUCTURES THROUGH C++ LAB'],
                                         ['RETURN']]),
"SEM-4" : ReplyKeyboardMarkup([['PROBABILITY AND STATISTICS', 'JAVA PROGRAMMING', 'OPERATING SYSTEMS'],
                                             ['DATABASE MANAGEMENT SYSTEMS', 'FORMAL LANGUAGES AND AUTOMATA THEORY', 'JAVA PROGRAMMING LAB']
                                                , ['UNIX OPERATING SYSTEM LAB', 'DATABASE MANAGEMENT SYSTEM LAB'],
                                         ['RETURN']]),
"SEM-5" : ReplyKeyboardMarkup([['DATA WAREHOUSE AND DATA MINING', 'COMPUTER NETWORK', 'COMPILER DESIGN'],
                                             ['ARTIFICIAL INTELLIGENCE', 'PROFESSIONAL ELECTIVE 1', 'COMPUTER NETWORKS LAB']
                                                , ['AU TOOLS AND TECHNIQUES LAB', 'DATA MINING LAB'],
                                         ['RETURN']])
}
SEM_6_MARKUP = ReplyKeyboardMarkup([])

YES_NO_MARKUP = ReplyKeyboardMarkup([['YES']], one_time_keyboard=True)



jsonFile = open("data1.json", "r")  # Open the JSON file for reading
student_details = json.load(jsonFile)  # Read the JSON into the buffer
jsonFile.close()

# df = pd.read_json('details.json')


def start(update_obj, context):
    user = update_obj.message.from_user
    logger.info("User %s started the conversation e.", user.first_name)
    update_obj.message.reply_text(f"\tHai {user.first_name} iam student assisstant bot"
     "\n Enter you register number to proceed",
                                  reply_markup=ReplyKeyboardRemove()
                                  )
    return IDENTIFY


def identify(update_obj, context):
    id = update_obj.message.text.upper()
    if id == '19em1a0524':
        update_obj.message.reply_audio()
    try:
      student = student_details[id]['details']['name']
      context.user_data['student'] = id
    except:
        update_obj.message.reply_text(f'Student not found try again')
    update_obj.message.reply_text(f" Hai {student}"
                                  "\n choose any option below to procceed",
                                  reply_markup= MENU_MARKUP)
    return DIRECTOR


def director(update_obj, context):
    choice = update_obj.message.text.upper()
    if choice == 'DETAILS':
        update_obj.message.reply_text("Press yes to continue",
                                      reply_markup=YES_NO_MARKUP)
        return DETAILS
    elif choice == 'MARKS':
        update_obj.message.reply_text("""
              CHOOSE SEMISTER
            """, reply_markup=ReplyKeyboardMarkup(
            [['SEM-1', 'SEM-2', 'SEM-3', 'SEM-4'], ['SEM-5', 'SEM-6', 'SEM-7', 'SEM-8'], ['Return to menu']]))

        return SEM_RESULTS
    elif choice == 'EDITMARKS':
        update_obj.message.reply_text("""
             CHOOSE SEMISTER
           """, reply_markup=ReplyKeyboardMarkup(
            [['SEM-1', 'SEM-2', 'SEM-3', 'SEM-4'], ['SEM-5', 'SEM-6', 'SEM-7', 'SEM-8'], ['Return to menu']]))

        return EDITMARKS
    elif choice == 'END CONVERSATION':
        update_obj.message.reply_text('Press yes to continue', reply_markup=YES_NO_MARKUP)
        return CANCEL
    elif choice == 'JOBS':
        update_obj.message.reply_text('Press yes to continue', reply_markup=YES_NO_MARKUP)
        return JOBS
    elif choice == 'U-LINKS':
        update_obj.message.reply_text('Press yes to continue', reply_markup=YES_NO_MARKUP)
        return ULINKS
    elif choice == 'TOOLS':
        update_obj.message.reply_text('Press yes to continue', reply_markup=YES_NO_MARKUP)
        return TOOLS
    elif choice == 'HELP':
        update_obj.message.reply_text('Press yes to continue', reply_markup=YES_NO_MARKUP)
        return HELP


def details(update_obj, context):
    val = update_obj.message.text
    if val == 'YES':
     id = context.user_data['student']
     # df = pd.DataFrame.from_dict(student_details[id]['details'], orient='index')
     name = student_details[id]['details']['name']
     email = student_details[id]['details']['email']
     address = student_details[id]['details']['address']
     dob = student_details[id]['details']['dob']
     branch = "CSE-A"
     cont_no = student_details[id]['details']['number']
     msg = f"""-------I------N--------F--------O-------------------\n
      NAME          :    {name}   \n      EMAIL          :    {email}     \n      CONTRACT       :    {cont_no}   \n      BRANCH    :    {branch}
      DOB           :    {dob}    \n      ADDRESS         :    {address}   \n
    ----------------------------------------------------------"""
     update_obj.message.reply_text(msg
  , reply_markup=ReplyKeyboardRemove())
     update_obj.message.reply_text(f"OPTIONS",
                                   reply_markup=MENU_MARKUP)
     return DIRECTOR
    else:
        return CANCEL

#
# def marks(update_obj, context):
#     update_obj.message.reply_text("""
#       CHOOSE SEMISTER
#     """,reply_markup=telegram.ReplyKeyboardMarkup([['SEM-1','SEM-2','SEM-3','SEM-4'],['SEM-5','SEM-6','SEM-7','SEM-8'],['Return to menu']]))
#
#     return SEM_RESULTS


def help(update_obj, context):
    update_obj.message.reply_text("contact saibabu for any issues \n saibabu@123gamil.com")
    update_obj.message.reply_text(f"OPTIONS",
                                  reply_markup=MENU_MARKUP)
    return DIRECTOR

def sem_results(update_obj,context):
    data = update_obj.message.text.lower()
    if data in ['sem-6', 'sem-7', 'sem-8']:
        update_obj.message.reply_text(f'{data} marks not updated yet')
    if data == 'return to menu':
        update_obj.message.reply_text(f'redirecting to menu', reply_markup=MENU_MARKUP)
        return DIRECTOR
    else:
      stu = context.user_data['student']
      id = context.user_data['student']
      marks_ = student_details[id]['marks'][data]
      # df = pd.DataFrame(student_details[id]['marks'][data])
      msg = f"""\n-------S----E-----M------ - ------{data[-1]}------\n\n """
      for i in marks_.items():
          msg += f"""   {i[0]}""" + " "*(15-len(i[0])) +f""" :     {i[1]} \n"""
          # {}f"     {i[0]}{" "*(len(i[0])-15)}:     {i[1][0]}  {i[1][1]}  \n "
      msg += """\n-------------------------------------"""
      update_obj.message.reply_text(msg)



def editmarks(update_obj,context):
    data = update_obj.message.text
    if data == 'RETURN':
        update_obj.message.reply_text("""
                    CHOOSE SEMISTER
                  """, reply_markup=ReplyKeyboardMarkup(
            [['SEM-1', 'SEM-2', 'SEM-3', 'SEM-4'], ['SEM-5', 'SEM-6', 'SEM-7', 'SEM-8'], ['Return to menu']]))
    elif data == 'Return to menu':
        update_obj.message.reply_text(f"OPTIONS",
                                      reply_markup=MENU_MARKUP)
        return DIRECTOR
    id = context.user_data['student']
    context.user_data['sem'] = data
    update_obj.message.reply_text('SELECT SUBJECT',reply_markup=sem_markups[data])
    return MANIP_SUB



def manip_sub(update_obj,context):
    data = update_obj.message.text
    if data in ['O','S','A','B','C','D','F']:
        sub = context.user_data['sub']
        sem = context.user_data['sem']
        if sem in ['SEM-6', 'SEM-7', 'SEM-8']:
            update_obj.message.reply_text(f'{sem} marks are not updates yet')
        id = context.user_data['student']
        update_obj.message.reply_text(f'MARKS GET UPDATED FOR {sub} with grade {data} of {sem}')
        student_details[id]['marks'][sem.lower()][sub][0] = data
        jsonFile = open("data1.json", "w+")
        jsonFile.write(json.dumps(student_details,indent=2))
        jsonFile.close()

        update_obj.message.reply_text("""
                            CHOOSE SEMISTER
                          """, reply_markup=ReplyKeyboardMarkup(
            [['SEM-1', 'SEM-2', 'SEM-3', 'SEM-4'], ['SEM-5', 'SEM-6', 'SEM-7', 'SEM-8'], ['Return to menu']]))
        return EDITMARKS

    update_obj.message.reply_text(f'PICK THE GRADE {data} ')
    update_obj.message.reply_text('--------',reply_markup=GRADE_MARKUP)
    context.user_data['sub'] = data


def jobs(update_obj,context):
    update_obj.message.reply_text('CURRENTLY NO JOBS AVAILABLE',reply_markup= MENU_MARKUP)
    return DIRECTOR
def ulinks(update_obj,context):
    update_obj.message.reply_text('links will be added soon',reply_markup= MENU_MARKUP)
    return DIRECTOR
def tools(update_obj,context):
    update_obj.message.reply_text('tools will be added soon',reply_markup= MENU_MARKUP)
    return DIRECTOR


def cancel(update_obj, context):
    # get the user's first name
    first_name = update_obj.message.from_user['first_name']
    update_obj.message.reply_text(
        f"Okay, no question for you then, take care, {first_name}!"
        "click here to restart /start", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


# a regular expression that matches yes or no
yes_no_regex = re.compile(r'^(yes|no|y|n|GETDETAILS)$', re.IGNORECASE)
# Create our ConversationHandler, with only one state
id_check = re.compile(r'')
handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        IDENTIFY: [MessageHandler(Filters.text, identify)],
        DIRECTOR: [MessageHandler(Filters.text, director)],
        DETAILS: [MessageHandler(Filters.text, details)],
        # MARKS: [telegram.ext.MessageHandler(telegram.ext.Filters.text, marks)],
        SEM_RESULTS:[MessageHandler(Filters.text,sem_results)],
        EDITMARKS: [MessageHandler(Filters.text, editmarks)],
        MANIP_SUB:[MessageHandler(Filters.text,manip_sub)],
        JOBS:[MessageHandler(Filters.text,jobs)],
        ULINKS:[MessageHandler(Filters.text,ulinks)],
        TOOLS: [MessageHandler(Filters.text, tools)],
        HELP: [MessageHandler(Filters.text,help)],
        CANCEL: [MessageHandler(Filters.regex(yes_no_regex), cancel)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)
# add the handler to the dispatcher


dispatcher.add_handler(handler)
# start polling for updates from Telegram
updater.start_polling()
# block until a signal (like one sent by CTRL+C) is sent
updater.idle()


