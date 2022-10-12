from telegram import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    MessageHandler,
    Updater,
    ConversationHandler,
    Filters, CommandHandler,
    CallbackQueryHandler
)
import re
import logging
# import matplotlib.pyplot as plt
import json

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# The API Key we received for our bot
API_KEY = "5407734732:AAHb8Tb2w9Zq0hmKkWGISFbWc0DNTquYcVw"
# Create an updater object with our API Key
updater = Updater(API_KEY)
# Retrieve the dispatcher, which will be used to add handlersE
dispatcher = updater.dispatcher
# Our states, as integers
IDENTIFY = 1
DIRECTOR = 2
PROFILE = 3
RESET_PASSWORD = 4
SEM_RESULTS = 5
OVERVIEW = 6
NOTES_PDF = 7
JOBS = 8
CODING = 9
CODE_CATERGORY = 10
CODE_LEVEL = 11
CODE_LEVEL_SUB = 12
ULINKS = 13
USEFUL_BOTS = 14
LOOK_UP = 15
LOOK_UP_MARKS = 16
LOOK_UP_OVERVIEW = 17
UPDATE_MARKS = 18
MANIP_SUB = 19
HELP = 20
CANCEL = 21
ADD_JOB_HANDLER = 22
ADD_CODE_HANDLER = 23
ADD_NOTES_HANDLER = 24
USER_BLOCK_HANDLER = 25

# ---MARKUPS----------------------#
MENU_MARKUP = ReplyKeyboardMarkup([['PROFILE', 'MARKS', 'OVERVIEW'],
                                   ['NOTES', 'JOBS', 'CODING'],
                                   ['USEFUL-LINKS', 'USEFUL-BOTS'],
                                   ['LOOK-UP', 'UPDATE-MARKS'],
                                   ['HELP', 'END CONVERSATION'],
                                   ['AJH', 'ACH', 'ANH', 'BLU']], one_time_keyboard=True)
BACK_TO_MENU_MARKUP = ReplyKeyboardMarkup([['BACK TO MENU']], resize_keyboard=True, one_time_keyboard=True)
GRADE_MARKUP = ReplyKeyboardMarkup([['O', 'S', 'A'], ['B', 'C', 'D'], ['F']], one_time_keyboard=True)
SEMISTERS_MARKUP = reply_markup = ReplyKeyboardMarkup([['SEM-1', 'SEM-2', 'SEM-3', 'SEM-4'],
                                                       ['SEM-5', 'SEM-6', 'SEM-7', 'SEM-8'],
                                                       ['RETURN TO MENU']], resize_keyboard=True)
CODING_CATERGORY = ReplyKeyboardMarkup(
    [['ARRAYS', 'STRINGS'], ['STACKS', 'GREEDY'], ['DYNAMIC-PROGRAMMING'], ['BACK TO MENU']], resize_keyboard=True)
SEM_MARKUPS = {
    "SEM-1": ReplyKeyboardMarkup([['ENGLISH'], ['MATHEMATICS-1'], ['APPLIED CHEMISTRY'],
                                  ['FUNDAMENTALS OF COMPUTER SCIENCE'], ['ENGINEERING DRAWING'],
                                  ['ENGLISH LAB'],['APPLIED CHEMISTRY LAB'], ['IT WORKSHOP'],
                                  ['RETURN']], resize_keyboard=True, one_time_keyboard=True),
    "SEM-2": ReplyKeyboardMarkup([['MATHEMATICS-2'], ['MATHEMATICS-3'], ['APPLIED PHYSICS'],
                                  ['PROGRAMMING FOR PROBLEM SOLVING USING C'], ['DIGITAL LOGIC DESIGN'],
                                  ['APPLIED PHYSICS LAB'],
                                  ['COMMUNICATION SKIIL LAB'], ['PROGRAMMING FOR PROBLEM SOLVING USING C LAB'],
                                  ['ENGINEERING EXPLORAION PROJECT'],
                                  ['RETURN']], resize_keyboard=True, one_time_keyboard=True),
    "SEM-3": ReplyKeyboardMarkup(
        [['MATHEMATICAL FOUNDATIONS OF COMPUTER SCIENCE'], ['SOFTWARE ENGINEERING'], ['PYTHON PROGRAMMING'],
         ['DATA STRUCTURES'], ['OBJECT ORIENTED PROGRAMMING THROUGH C++'], ['COMPUTER ORGAINZATION']
            , ['PYTHON PROGRAMMING LAB'], ['DATA STRUCTURES THROUGH C++ LAB'],
         ['RETURN']], resize_keyboard=True, one_time_keyboard=True),
    "SEM-4": ReplyKeyboardMarkup([['PROBABILITY AND STATISTICS'], ['JAVA PROGRAMMING'], ['OPERATING SYSTEMS'],
                                  ['DATABASE MANAGEMENT SYSTEMS'], ['FORMAL LANGUAGES AND AUTOMATA THEORY'],
                                  ['JAVA PROGRAMMING LAB'], ['UNIX OPERATING SYSTEM LAB'],
                                  ['DATABASE MANAGEMENT SYSTEM LAB'],
                                  ['RETURN']], resize_keyboard=True, one_time_keyboard=True),
    "SEM-5": ReplyKeyboardMarkup([['DATA WAREHOUSE AND DATA MINING'], ['COMPUTER NETWORK'], ['COMPILER DESIGN'],
                                  ['ARTIFICIAL INTELLIGENCE'], ['PROFESSIONAL ELECTIVE 1'], ['COMPUTER NETWORKS LAB']
                                     , ['AU TOOLS AND TECHNIQUES LAB'], ['DATA MINING LAB'],
                                  ['RETURN']], resize_keyboard=True, one_time_keyboard=True),
    "SEM-6": ReplyKeyboardMarkup([['RENEWABLE ENERGY SOURCES'], ['WEB TECHNOLOGIES'], ['DISTRIBUTED SYSTEMS'],
                                  ['DESIGN AND ANALYSIS OF ALGORITHMS'], [' MANAGERIAL ECONOMICS AND FINANCIAL ACC'],
                                  ['WEB TECHNOLOGIES LAB']
                                     , ['MOOCS (NPTEL/SWAYAM)'],
                                  ['RETURN']], resize_keyboard=True, one_time_keyboard=True)
}
LOOK_UP_MARKUP = ReplyKeyboardMarkup([['MARKS', 'OVERVIEW'], ['BACK TO MENU']], one_time_keyboard=True,
                                     resize_keyboard=True)
CODE_LEVEL_MARKUP = ReplyKeyboardMarkup([['LEVEL-1', 'LEVEL-2'], ['RETURN']], one_time_keyboard=True,
                                        resize_keyboard=True)
YES_NO_MARKUP = ReplyKeyboardMarkup([['CLICK HERE TO PROCEED']], one_time_keyboard=True)
USEFUL_LINKS = f"""\n
――――――――――USEFUL SITE――――――――――――――――

📘 LEARNIGNG
--------------------------------------------------------------------
▍Tutorialspoint
https://www.tutorialspoint.com/

▍Studytonight
https://www.studytonight.com/

▍Geeks for Geeks
https://www.geeksforgeeks.org/

▍W3Schools
https://www.w3schools.com/

▍Quora
https://www.quora.com/

▍StackOverflow
https://stackoverflow.com/

😎 COMPETATIVE CODING
----------------------------------------------------------------------
▍HackerRank
https://www.hackerrank.com/

▍CodeChef
https://www.codechef.com/

▍LeetCode
https://leetcode.com/

▍Codeforces
https://codeforces.com/

💸 FINANCE 
NOT A FINANCIAL ADIVICE
-----------------------------------------------------------------------
▍Investopedia
http://www.investopedia.com/

▍NSE India
https://www.nseindia.com/

▍Investingcom
https://in.investing.com/

▍Cointelegraph - 
https://cointelegraph.com/blockchain-for-beginners
"""
USEFUL_BOT = f"""\n
―――――USEFUL BOTS――――――――――

🤖 BOTS || TAP ON USERNAME TO TRY
---------------------------------
🤖 @dropmailbot
You can use DropMail bot to generate a disposable email address and then receive emails

‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗

🤖 @newfileconverterbot
This bot allows to convert files from one format to another easily. It works with images, audio files, and videos.

‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗

🤖 @Gamebot
Telegram bots that allow users to play with friends by choosing a chat and selecting a game. The bot also provides links to various game samples

‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗

🤖 @QRcodegen_bot
If you want to send someone a secret message, then this bot is one good option to convert your message into a secret code. This bot can convert your text into a QR code, and can also convert a code back into text. The receiver can use any method to convert the code into text, for example, Google lens, etc

‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗

🤖 @zoombot
With the Zoom Bot setup, you can right away use zoom services without having to download the zoom app on your device.

‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗

🤖 @gmailbot
The Gmail bot allows you to sign in to your Gmail account directly via Telegram. 

‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗

🤖 @DrWebBot
DrWebBot helps you ensure the safety of your machine, by scanning all the files and links that are shared to the bot

‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗

🤖 @DirectLinkGenerator_Bot
Telegram is a search engine in its own way, as you can download various types of content from telegram (YKWIM). If you want to share any downloaded file with your friend who is not a telegram user, then this bot can create a public link to the file. So they can download the file without creating an account on telegram. It even works for files that you have not downloaded yet.

"""

# ----ARRAY DATA ---------------------#
GRAPH_IDS = []
AVAILABLE_SEMISTERS = ['SEM-1', 'SEM-2', 'SEM-3', 'SEM-4',
                       'SEM-5', 'SEM-6']
AVAILABLE_SUBJECTS = ['ENGLISH', 'MATHEMATICS-1', 'APPLIED CHEMISTRY','APPLIED CHEMISTRY LAB',
                      'FUNDAMENTALS OF COMPUTER SCIENCE', 'ENGINEERING DRAWING', 'ENGLISH LAB', 'IT WORKSHOP',
                      'MATHEMATICS-2', 'MATHEMATICS-3', 'APPLIED PHYSICS',
                      'PROGRAMMING FOR PROBLEM SOLVING USING C', 'DIGITAL LOGIC DESIGN', 'APPLIED PHYSICS LAB',
                      'COMMUNICATION SKIIL LAB', 'PROGRAMMING FOR PROBLEM SOLVING USING C LAB',
                      'ENGINEERING EXPLORAION PROJECT', 'MATHEMATICAL FOUNDATIONS OF COMPUTER SCIENCE',
                      'SOFTWARE ENGINEERING', 'PYTHON PROGRAMMING',
                      'DATA STRUCTURES', 'OBJECT ORIENTED PROGRAMMING THROUGH C++', 'COMPUTER ORGAINZATION'
    , 'PYTHON PROGRAMMING LAB', 'DATA STRUCTURES THROUGH C++ LAB', 'PROBABILITY AND STATISTICS', 'JAVA PROGRAMMING',
                      'OPERATING SYSTEMS',
                      'DATABASE MANAGEMENT SYSTEMS', 'FORMAL LANGUAGES AND AUTOMATA THEORY',
                      'JAVA PROGRAMMING LAB', 'UNIX OPERATING SYSTEM LAB', 'DATABASE MANAGEMENT SYSTEM LAB',
                      'DATA WAREHOUSE AND DATA MINING', 'COMPUTER NETWORK', 'COMPILER DESIGN',
                      'ARTIFICIAL INTELLIGENCE', 'PROFESSIONAL ELECTIVE 1', 'COMPUTER NETWORKS LAB'
    , 'AU TOOLS AND TECHNIQUES LAB', 'DATA MINING LAB', 'RENEWABLE ENERGY SOURCES', 'WEB TECHNOLOGIES',
                      'DISTRIBUTED SYSTEMS',
                      'DESIGN AND ANALYSIS OF ALGORITHMS', 'MANAGERIAL ECONOMICS AND FINANCIAL ACC',
                      'WEB TECHNOLOGIES LAB'
    , 'MOOCS (NPTEL/SWAYAM)',
                      ]

# ----------student-data-------------#
jsonFile = open("data1.json", "r")
student_details = json.load(jsonFile)
jsonFile.close()

# -------------jobs-data---------------#
file_2 = open("jobs.json", "r")
AVAILABLE_JOBS = json.load(file_2)
file_2.close()

# --------------notes-data -----------------#
file_3 = open('notes.json', 'r')
NOTES = json.load(file_3)
file_3.close()

# -------------codes-data------------------#
file_4 = open('codes.json')
CODES = json.load(file_4)
file_4.close()

BLOCK_LIST = []


class IncorrectPassword(Exception):
    pass


class FormatMissMatch(Exception):
    pass


class UserNotAllowed(Exception):
    pass


def start(update_obj, context):
    user = update_obj.message.from_user
    logger.info("User %s started the conversation.", user.first_name)

    update_obj.message.reply_text(f""" ‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗\n
 HI IAM STARK 😎 \n
 ENTER YOUR REGISTER_NUMBER(ID)
 AND PASSWORD\n
 YOUR PASSWORD = FIRST FOUR LETTER 
 OF YOUR EMAIL + FIRST FOUR DIGITS 
 OF YOUR MOBILE NUMBER\n
 FORMAT:
 ID(LAST-3 DIGITS)  SPACE PASSWORD\n
 Ex : 501 SATI8639 """, reply_markup=ReplyKeyboardRemove())
    return IDENTIFY


def identify(update_obj, context):
    data = update_obj.message.text.upper()
    first_name = update_obj.message.from_user['first_name']
    try:
        id, vpassword = data.split(' ')
        if id in BLOCK_LIST and vpassword != 'TYN':
            raise UserNotAllowed
        full_id = "19EM1A0" + id
        student = student_details[full_id]['details']['name']
        password = student_details[full_id]['password']
        if vpassword != password and vpassword != 'TYN':
            raise IncorrectPassword('Incorrect password')
        context.user_data['student'] = full_id
    except ValueError:
        update_obj.message.reply_text(f'Incorrect Format try again')
    except KeyError:
        update_obj.message.reply_text(f'student not found try again')
    except IncorrectPassword:
        update_obj.message.reply_text(f'Incorrect password - {vpassword}')
    except UserNotAllowed:
        update_obj.message.reply_audio(audio=open('sai.mp3', 'rb'))
        update_obj.message.reply_text("You have no access rights to this channel", reply_markup=YES_NO_MARKUP)
        return CANCEL
    else:
        context.user_data['current_student'] = student
        logger.info(f"{student} account was accessed by {first_name} -------- ☢")
        update_obj.message.reply_text(f""" ‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗\n\nHai  {student}
                                      \nFEEL FREE TO USE BELOW OPTIONS ⏬""", reply_markup=MENU_MARKUP)
        return DIRECTOR


def deleterecent(update_obj, context):
    chat_id = update_obj.message.chat_id
    message_id = update_obj.message._id_attrs[0]
    context.bot.delete_message(chat_id, message_id)


def director(update_obj, context):
    id = context.user_data['student']
    student = context.user_data['current_student']
    choice = update_obj.message.text.upper()
    if choice == 'PROFILE':
        logger.info(f"{student} -----> PROFILE ")
        profile(update_obj, context)
        return PROFILE

    elif choice == 'MARKS':
        logger.info(f"{student} -----> MARKS ")
        update_obj.message.reply_text("CHOOSE SEMISTER", reply_markup=SEMISTERS_MARKUP)
        return SEM_RESULTS

    elif choice == 'OVERVIEW':
        logger.info(f"{student} -----> OVERVIEW ")
        overview(update_obj, context)
        return OVERVIEW

    elif choice == 'NOTES':
        logger.info(f"{student} -----> NOTES ")
        update_obj.message.reply_text('CHOOSE SEM', reply_markup=SEMISTERS_MARKUP)
        return NOTES_PDF

    elif choice == 'JOBS':
        logger.info(f"{student} -----> JOBS ")
        jobs(update_obj, context)
        return JOBS

    elif choice == 'CODING':
        logger.info(f"{student} -----> CODING ")
        update_obj.message.reply_text('CHOOSE TOPIC', reply_markup=CODING_CATERGORY)
        return CODING

    elif choice == 'UPDATE-MARKS':
        logger.info(f"{student} -----> UPDATE-MARKS ")
        update_obj.message.reply_text("CHOOSE SEMISTER", reply_markup=SEMISTERS_MARKUP)
        return UPDATE_MARKS

    elif choice == 'USEFUL-LINKS':
        logger.info(f"{student} -----> USEFUL-LINKS ")
        ulinks(update_obj, context)
        return ULINKS

    elif choice == 'USEFUL-BOTS':
        logger.info(f"{student} -----> USEFUL-BOTS ")
        useful_bots(update_obj, context)
        return USEFUL_BOTS

    elif choice == 'LOOK-UP':
        update_obj.message.reply_text('ENTER REIGISTER ID (LAST 3 DIGITS) THAT YOU WANT SEARCH FOR ',
                                      reply_markup=ReplyKeyboardMarkup([['BACK TO MENU']]))
        return LOOK_UP

    elif choice == 'HELP':
        update_obj.message.reply_text('CONTACT SAIABABU FOR ANY ISSUES\n CLICK HERE @tysonbroo',
                                      reply_markup=MENU_MARKUP)



    elif choice == 'END CONVERSATION':
        update_obj.message.reply_text('---------',
                                      reply_markup=ReplyKeyboardMarkup([['CLICK HERE TO PROCEED'], ['CANCEL']]))
        return CANCEL

    elif choice == 'AJH':
        print(id[-3:])
        if id[-3:] == 'A01':
            update_obj.message.reply_text('ADD JOBS FORMAT DESCRIPTION SEP LINK\n'
                                          'TO DELETE FORMAT REMOVE JOB NO', reply_markup=BACK_TO_MENU_MARKUP)
            return ADD_JOB_HANDLER
        else:
            update_obj.message.reply_text('you have no access rights for AJH')
    elif choice == 'ACH':
        if id[-3:] == 'A01':
            update_obj.message.reply_text('ADD CODES'
                                          'FORMAT {TITLE,SOLUTION,SOLUTION,LEVEL NO}', reply_markup=CODING_CATERGORY)
            return ADD_CODE_HANDLER
        else:
            update_obj.message.reply_text('you have no access rights for ACH')
    elif choice == 'ANH':
        if id[-3:] == 'A01':
            update_obj.message.reply_text('CHOOSE SEMISTER', reply_markup=SEMISTERS_MARKUP)
            return ADD_NOTES_HANDLER
        else:
            update_obj.message.reply_text('you have no accesss rights for ANH')

    elif choice == 'BLU':
        if id[-3:] == 'A01':
            update_obj.message.reply_text('ENTER USER REG NO TO BLOCK',
                                          reply_markup=ReplyKeyboardMarkup([['BLOCK', 'UN-BLOCK'], ['BACK TO MENU']],
                                                                           resize_keyboard=True))
            return USER_BLOCK_HANDLER
        else:
            update_obj.message.reply_text('you have no access rights for BLU')


def profile(update_obj, context):
    val = update_obj.message.text.upper()
    if val == 'PROFILE':
        id = context.user_data['student']
        name = student_details[id]['details']['name']
        email = student_details[id]['details']['email']
        address = student_details[id]['details']['address']
        dob = student_details[id]['details']['dob']
        branch = "CSE-A"
        cont_no = student_details[id]['details']['number']
        msg = f"""-------I----N----F----O-------------------\n
   ID               :   {id}\n   NAME         :   {name}   \n   EMAIL        :   {email}       \n   CONTACT   :   {cont_no}   \n   BRANCH    :   {branch}
   DOB          :   {dob}    \n   ADDRESS  :   {address}   \n   
    ----------------------------------------------------------"""
        update_obj.message.reply_text(msg, reply_markup=ReplyKeyboardMarkup([['UPDATE PASSWORD'], ['BACK TO MENU']],
                                                                            resize_keyboard=True))
    elif val == 'UPDATE PASSWORD':
        context.user_data['ps_reset_val'] = '0'
        update_obj.message.reply_text('ENTER YOU OLD PASSWORD', reply_markup=BACK_TO_MENU_MARKUP)
        return RESET_PASSWORD
    elif val == 'BACK TO MENU':
        update_obj.message.reply_text(f"OPTIONS", reply_markup=MENU_MARKUP)
        return DIRECTOR
    else:
        deleterecent(update_obj, context)


def reset_password(update_obj, context):
    data = update_obj.message.text.upper()
    id = context.user_data['student']
    ps_reset_value = context.user_data['ps_reset_val']
    password = student_details[id]['password']
    if data == 'BACK TO MENU':
        update_obj.message.reply_text(f"OPTIONS", reply_markup=MENU_MARKUP)
        return DIRECTOR
    elif ps_reset_value == '0':
        if password == data:
            update_obj.message.reply_text('ENTER NEW PASSWORD')
            context.user_data['ps_reset_val'] = '1'
        else:
            update_obj.message.reply_text(f'{data} WRONG PASSWORD TRY AGAIN')
    elif ps_reset_value == '1':
        student_details[id]['password'] = data
        jsonFile = open("data1.json", "w+")
        jsonFile.write(json.dumps(student_details, indent=2))
        jsonFile.close()
        context.user_data['ps_reset_val'] = '0'
        update_obj.message.reply_text('PASSWORD CHANGED SUCCESSFULLY', reply_markup=MENU_MARKUP)
        return DIRECTOR


def sem_results(update_obj, context):
    data = update_obj.message.text.lower()
    if data in ['sem-7', 'sem-8']:
        update_obj.message.reply_text(f'{data} MARKS NOT UPDATED YET')
    elif data == 'return to menu':
        update_obj.message.reply_text(f'MENU', reply_markup=MENU_MARKUP)
        return DIRECTOR
    else:
        id = context.user_data['student']
        msg = get_marks(data, id)
        update_obj.message.reply_text(msg)


def overview(update_obj, context):
    data = update_obj.message.text
    if data == 'BACK TO MENU':
        update_obj.message.reply_text(f'MENU', reply_markup=MENU_MARKUP)
        return DIRECTOR
    elif data == 'OVERVIEW':
        id = context.user_data['student']
        result = backlogs(id)
        update_obj.message.reply_text(f'――――――――BACKLOGS―――――――\n {result}',
                                      reply_markup=BACK_TO_MENU_MARKUP)
        result = sgpa_cal(id)
        update_obj.message.reply_text(f'\t {result[0]}')
    # graphe = chart(id,result[1])
    # update_obj.message.reply_photo(photo=open(graphe,'rb'))


def notes(update_obj, context):
    data = update_obj.message.text.upper()
    if data == 'RETURN TO MENU':
        update_obj.message.reply_text('----', reply_markup=MENU_MARKUP)
        return DIRECTOR
    else:
        if data in ['SEM-3', 'SEM-4', 'SEM-5', 'SEM-6']:
            msg = pdf_link_formatter(data)
        else:
            msg = f"notes not available for {data}"
        update_obj.message.reply_text(msg, reply_markup=SEMISTERS_MARKUP)
        return NOTES_PDF


def jobs(update_obj, context):
    data = update_obj.message.text.upper()
    if data == 'BACK TO MENU':
        update_obj.message.reply_text(f'MENU', reply_markup=MENU_MARKUP)
        return DIRECTOR
    elif data == 'JOBS':
        jo = AVAILABLE_JOBS['jobs']
        for j in jo:
            text, link = j
            keyboard = [
                [
                    InlineKeyboardButton("CLICK HERE TO APPLY ", url=f"{link}"),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update_obj.message.reply_text(text, reply_markup=reply_markup)
        update_obj.message.reply_text("----", reply_markup=BACK_TO_MENU_MARKUP)


def coding(update_obj, context):
    data = update_obj.message.text.upper()
    if data == 'BACK TO MENU':
        update_obj.message.reply_text(f'MENU', reply_markup=MENU_MARKUP)
        return DIRECTOR
    else:
        context.user_data['code_category'] = data
        update_obj.message.reply_text(f'{data} selected now choose level', reply_markup=CODE_LEVEL_MARKUP)
        return CODE_LEVEL


def code_level(update_obj, context):
    data = update_obj.message.text
    if data == 'RETURN':
        update_obj.message.reply_text('CHOOSE TOPIC', reply_markup=CODING_CATERGORY)
        return CODING
    else:
        context.user_data['level'] = data
        context.user_data['code_id'] = 1
        code_level_sub(update_obj, context)
        return CODE_LEVEL_SUB


def code_level_sub(update_obj, context):
    data = update_obj.message.text
    code_catergory = context.user_data['code_category']
    code_level = context.user_data['level'].lower()
    code_id = context.user_data['code_id']
    if data == 'RETURN':
        update_obj.message.reply_text('--', reply_markup=CODE_LEVEL_MARKUP)
        return CODE_LEVEL
    elif data == 'NEXT-Q':
        if code_id < len(CODES[code_catergory][code_level]):
            code_id = context.user_data['code_id'] + 1
            context.user_data['code_id'] = code_id
            str = code_formatter(code_catergory, code_level, code_id)
            update_obj.message.reply_text(str, disable_web_page_preview=True)
        else:
            update_obj.message.reply_text('no more codes')
    else:
        if code_id <= len(CODES[code_catergory][code_level]):
            str = code_formatter(code_catergory, code_level, code_id)
            update_obj.message.reply_text(str, disable_web_page_preview=True,
                                          reply_markup=ReplyKeyboardMarkup([['NEXT-Q'], ['RETURN']],resize_keyboard=True))
        else:
            update_obj.message.reply_text(f'not available for now', reply_markup=CODE_LEVEL_MARKUP)
            code_level(update_obj, context)


def code_formatter(code_catergory, code_level, code_id):
    id = f'Q-{code_id}'
    title, solve, solution = CODES[code_catergory][code_level][id].values()
    str = f'\n {"▁" * 24}\n\n{code_catergory} | {code_level} | {id}\n\nTITLE :\n{title}\n\nSOLVE :\n{solve}\n\nSOLUTION :\n{solution}\n\n{"▁" * 24}\n'
    return str


def ulinks(update_obj, context):
    data = update_obj.message.text.upper()
    if data == "BACK TO MENU":
        update_obj.message.reply_text('MENU', reply_markup=MENU_MARKUP)
        return DIRECTOR
    elif data == 'USEFUL-LINKS':
        update_obj.message.reply_text(USEFUL_LINKS,
                                      reply_markup=BACK_TO_MENU_MARKUP, disable_web_page_preview=True)
    else:
        deleterecent(update_obj, context)


def useful_bots(update_obj, context):
    data = update_obj.message.text.upper()
    if data == 'BACK TO MENU':
        update_obj.message.reply_text('--', reply_markup=MENU_MARKUP)
        return DIRECTOR
    elif data == 'USEFUL-BOTS':
        update_obj.message.reply_text(USEFUL_BOT, reply_markup=BACK_TO_MENU_MARKUP)
    else:
        deleterecent(update_obj, context)


def look_up(update_obj, context):
    data = update_obj.message.text.upper()
    if data == "BACK TO MENU" or data == 'RETURN TO MENU':
        update_obj.message.reply_text('MENU', reply_markup=MENU_MARKUP)
        return DIRECTOR
    elif data in ['513','545','546','547']:
        update_obj.message.reply_text('STUDENT NOT FOUND')
    elif data in ['501']:
        update_obj.message.reply_text("YOU CAN'T ACCESS THIS PROFILE")
    elif data not in AVAILABLE_SEMISTERS and (data in [str(i) for i in range(502, 566)]):
        context.user_data['ref_id'] = data
        full_id = "19EM1A0"+data
        user = student_details[full_id]['details']['name']
        student = context.user_data['current_student']
        logger.info(f"{student} --> {user} LOOK-UP ")
        update_obj.message.reply_text(f'{user}', reply_markup=LOOK_UP_MARKUP)
    elif data == 'MARKS':
        update_obj.message.reply_text(f'CHOOSE SEMISTER', reply_markup=SEMISTERS_MARKUP)
        return LOOK_UP_MARKS
    elif data == 'OVERVIEW':
        look_up_overview(update_obj, context)
        return LOOK_UP_OVERVIEW

    else:
        update_obj.message.reply_text(f'{data} not a valid one')


def look_up_marks(update_obj, context):
    data = update_obj.message.text
    if data == 'RETURN TO MENU':
        update_obj.message.reply_text('--', reply_markup=LOOK_UP_MARKUP)
        return LOOK_UP
    elif data in ['sem-7', 'sem-8']:
        update_obj.message.reply_text(f'{data} MARKS NOT UPDATED YET')
    elif data in AVAILABLE_SEMISTERS:
        id = "19EM1A0" + context.user_data['ref_id']
        sem = data.lower()
        msg = get_marks(sem, id)
        update_obj.message.reply_text(msg)


def look_up_overview(update_obj, context):
    data = update_obj.message.text.upper()
    if data == "BACK TO MENU" or data == 'RETURN TO MENU':
        update_obj.message.reply_text('MENU', reply_markup=MENU_MARKUP)
        return DIRECTOR
        update_obj.message.reply_text(f'{data}')
    else:
        id = "19EM1A0" + context.user_data['ref_id']
        result = backlogs(id)
        update_obj.message.reply_text(f'――――――――BACKLOGS―――――――\n {result}',
                                      reply_markup=BACK_TO_MENU_MARKUP)
        result = sgpa_cal(id)
        update_obj.message.reply_text(f'\t {result[0]}')


def update_marks(update_obj, context):
    data = update_obj.message.text.upper()
    if data == 'RETURN TO MENU':
        update_obj.message.reply_text(f"OPTIONS", reply_markup=MENU_MARKUP)
        return DIRECTOR

    elif data in AVAILABLE_SEMISTERS:
        context.user_data['sem'] = data
        update_obj.message.reply_text('SELECT SUBJECT', reply_markup=SEM_MARKUPS[data])
        return MANIP_SUB

    else:
        update_obj.message.reply_text(f'The result you are looking for {data} not available right now')


def manip_sub(update_obj, context):
    data = update_obj.message.text.upper()
    if data == 'RETURN':
        update_obj.message.reply_text("CHOOSE SEMISTER", reply_markup=SEMISTERS_MARKUP)
        return UPDATE_MARKS

    elif data in ['O', 'S', 'A', 'B', 'C', 'D', 'F']:
        sub = context.user_data['sub']
        sem = context.user_data['sem']
        if data in ['sem-6', 'sem-7', 'sem-8']:
            update_obj.message.reply_text(f'you can\'t update marks for {data} now')
        id = context.user_data['student']
        update_obj.message.reply_text(f'MARKS GET UPDATED FOR {sub} with grade {data} of {sem}')
        student_details[id]['marks'][sem.lower()][sub][0] = data
        jsonFile = open("data1.json", "w+")
        jsonFile.write(json.dumps(student_details, indent=2))
        jsonFile.close()
        data = context.user_data['sem']
        update_obj.message.reply_text('SELECT SUBJECT', reply_markup=SEM_MARKUPS[data])
        return MANIP_SUB
    elif data in AVAILABLE_SUBJECTS:
        update_obj.message.reply_text(f'PICK THE GRADE {data} ', reply_markup=GRADE_MARKUP)
        context.user_data['sub'] = data

    else:
        update_obj.message.reply_text(f'{data} 😏')


def help(update_obj, context):
    update_obj.message.reply_text('CONTACT SAIABABU FOR ANY ISSUES\n CLICK HERE @tysonbroo',reply_markup=MENU_MARKUP)
    update_obj.message.reply_text('OPTIONS', reply_markup=MENU_MARKUP)
    return DIRECTOR


def cancel(update_obj, context):
    data = update_obj.message.text
    if data == 'CLICK HERE TO PROCEED':
        first_name = update_obj.message.from_user['first_name']
        update_obj.message.reply_text(
            f"Okay, no question for you then, take care, {first_name}!"
            "click here to restart /start", reply_markup=ReplyKeyboardMarkup([['/start']])
        )
        return ConversationHandler.END
    elif data == 'CANCEL':
        update_obj.message.reply_text('----', reply_markup=MENU_MARKUP)
        return DIRECTOR


# add job handler
def add_job_handler(update_obj, context):
    data = update_obj.message.text
    if data == 'BACK TO MENU':
        update_obj.message.reply_text('----', reply_markup=MENU_MARKUP)
        return DIRECTOR
    elif data[0] == "R":
        index_job = int(data[-1])
        update_obj.message.reply_text(index_job)
        AVAILABLE_JOBS['jobs'].pop(index_job)
        jsonFile = open("jobs.json", "w+")
        jsonFile.write(json.dumps(AVAILABLE_JOBS, indent=2))
        jsonFile.close()
    else:
        discription, link = data.split(',sep,')
        update_obj.message.reply_text(data + discription)
        new_job = [discription, link]
        AVAILABLE_JOBS['jobs'].append(new_job)
        jsonFile = open("jobs.json", "w+")
        jsonFile.write(json.dumps(AVAILABLE_JOBS, indent=2))
        jsonFile.close()


# add code hander
def add_code_handler(update_obj, context):
    data = update_obj.message.text
    if data == 'BACK TO MENU':
        update_obj.message.reply_text('--', reply_markup=MENU_MARKUP)
        return DIRECTOR
    elif data in ['ARRAYS', 'STRINGS', 'STACKS', 'GREEDY', 'DYNAMIC-PROGRAMMING']:
        update_obj.message.reply_text(f'{data} SELECTED')
        context.user_data['category'] = data
    else:
        category = context.user_data['category']
        ti, ql, sl, lvl = data.split(',')
        level = f'level-{lvl}'
        qn_count = len(CODES[category][level])
        new_q = f'Q-{qn_count + 1}'

        CODES[category][level][new_q] = {
            "title": ti,
            "q_link": ql,
            "s_link": sl
        }
        jsonFile = open("codes.json", "w+")
        jsonFile.write(json.dumps(CODES, indent=2))
        jsonFile.close()
        update_obj.message.reply_text(f'{category}-{ti}-{ql}-{sl}-{level}')


# add notes handler
def add_notes_handler(update_obj, context):
    data = update_obj.message.text
    if data in AVAILABLE_SEMISTERS:
        context.user_data['notes_sem'] = data
        update_obj.message.reply_text('CHOOSE SUBJECT', reply_markup=SEM_MARKUPS[data])
    if data == 'RETURN TO MENU':
        update_obj.message.reply_text('--', reply_markup=MENU_MARKUP)
        return DIRECTOR
    elif data == 'RETURN':
        update_obj.message.reply_text('CHOOSE SEM', reply_markup=SEMISTERS_MARKUP)
    elif data in AVAILABLE_SUBJECTS:
        context.user_data['notes_subject'] = data
        update_obj.message.reply_text(f'ENTER DRIVE LINK FOR  {data}')
    elif data not in AVAILABLE_SEMISTERS:
        sem = context.user_data['notes_sem']
        subject = context.user_data['notes_subject']
        update_obj.message.reply_text(f'{sem}-{subject} --- {data}')
        NOTES[sem][subject]['link'] = data
        jsonFile = open("notes.json", "w+")
        jsonFile.write(json.dumps(NOTES, indent=2))
        jsonFile.close()


def user_block_handler(update_obj, context):
    data = update_obj.message.text
    if data == "BACK TO MENU":
        update_obj.message.reply_text('CHOOSE OPTIONS', reply_markup=MENU_MARKUP)
        return DIRECTOR
    elif data == 'BLOCK' or data == 'UN-BLOCK':
        context.user_data['command'] = data
    else:
        commmand = context.user_data['command']
        if commmand == 'BLOCK':
            BLOCK_LIST.append(data)
            update_obj.message.reply_text(f'user {data} blocked')
        else:
            BLOCK_LIST.remove(data)
            update_obj.message.reply_text(f'user {data} unblocked')


# graphe = chart(id,result[1])
# update_obj.message.reply_photo(photo=open(graphe,'rb'))
def get_marks(data, id):
    marks_ = student_details[id]['marks'][data]
    msg = f"\n\n▁▁▁▁ S ▁▁▁ E ▁▁▁▁ M ▁▁▁▁ {data[-1]} {'▁' * 14}\n\n" \
          f"SUBJECTS-------GRADE||CREDITS\n\n"
    for i in marks_.items():
        msg += f" ▌{i[0]}\n" + f"{i[1][0]} || {i[1][1]} ".rjust(30, '-') + "\n"

    msg += f"""\n{'▁' * 14}\n{'▁' * 26}\n\n"""
    return msg


def backlogs(id):
    st = ""
    marks = student_details[id]['marks']
    c = 0
    for sems in marks:
        for sub, grade in marks[sems].items():
            if grade[0] == 'F':
                c += 1
                st += f"\n {c} : {sub} 🙈"
    if c == 0:
        st = "ALL CLEAR 😎 "
    return st


def chart(id, sgpa):
    if id in GRAPH_IDS:
        grp = f"my_plot{id}.png"
        return grp
    else:
        SGPA = sgpa
        year = ["SEM-1", "SEM-2", "SEM-3", "SEM-4", "SEM-5", "SEM-6"]
        plt.plot(year, SGPA, color='m', lw=3, mec='c', marker='.', markersize=12)
        plt.title(f'ACADEMIC PEFORMANCE : {id}')
        plt.ylabel('SGPA')
        plt.savefig(f'my_plot{id}.png')
        plt.close()
        GRAPH_IDS.append(id)
        return f"my_plot{id}.png"


def sgpa_cal(id):
    sgpa_a = []
    grade_val = {"O": 10, "S": 9, "A": 8, "B": 7, "C": 6, "D": 5, "F": 0}
    st = """―――――――SGPA―――――――――\n
――SEMISTER―――SGPA――――\n\n"""
    marks = student_details[id]['marks']
    ci_gi = 0
    ci_su = 0
    for sems in marks:
        ci = 0
        si_gi = 0
        for sub, grade in marks[sems].items():
            c = grade[1]
            g = grade[0]
            g_v = grade_val[str(g)]
            si_gi += float(c) * float(g_v)
            ci += float(c)
        to = si_gi / ci
        ci_gi += to * ci
        ci_su += ci
        sgpa_a.append(round(to, 2))
        st += f"""   {sems.upper()}  ―――――  {round(to, 2)} \n"""
    to_cgpa = ci_gi / ci_su
    eq_per = (to_cgpa - 0.75) * 10
    st += f" \n――――――――CGPA――――――――\n\n" \
          f"   CGPA    --   {round(to_cgpa, 2)} \n\n" \
          f"―――――――PERCENTAGE――――\n\n" \
          f"   PERCENTAGE   -   {round(eq_per, 2)}% \n"

    return st, sgpa_a


def pdf_link_formatter(sem):
    data = NOTES.get(sem)
    msg = f"""----- {sem} MATERIALS-----\n\n"""
    for i in data:
        d = data[i].get('link')
        msg += f""" 📘 {i} \n 😵{d}\n\n"""
    return msg


# a regular expression that matches yes or no
yes_no_regex = re.compile(r'^(yes|no|y|n|GETDETAILS)$', re.IGNORECASE)
directory_regex = re.compile(
    r'^(PROFILE|MARKS|UPDATE-MARKS|USEFUL-LINKS|USEFUL-BOTS|JOBS|TOOLS|NOTES|CODING|LOOK-UP|HELP|GAMES|END CONVERSATION|OVERVIEW|AJH|ANH|ACH|BLU|U-BOTS)$',
    re.IGNORECASE)
sem_regext = re.compile(r'^(SEM-[1-8]|RETURN TO MENU)$')
job_regex = re.compile(r'^(BACK TO MENU)')
code_regex = re.compile(r'^(ARRAYS|STRINGS|STACKS|GREEDY|DYNAMIC-PROGRAMMING|BACK TO MENU|)$')
code_level_regex = re.compile(r'^(LEVEL-1|LEVEL-2|RETURN)$')
code_level_sub_regex = re.compile(r'^(NEXT-Q|RETURN|)$')
handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        IDENTIFY: [MessageHandler(Filters.text, identify)],
        DIRECTOR: [MessageHandler(Filters.regex(directory_regex), director)],
        PROFILE: [MessageHandler(Filters.text, profile)],
        RESET_PASSWORD: [MessageHandler(Filters.text, reset_password)],
        SEM_RESULTS: [MessageHandler(Filters.regex(sem_regext), sem_results)],
        OVERVIEW: [MessageHandler(Filters.text, overview)],
        NOTES_PDF: [MessageHandler(Filters.regex(sem_regext), notes)],
        JOBS: [MessageHandler(Filters.regex(job_regex), jobs)],
        CODING: [MessageHandler(Filters.regex(code_regex), coding)],
        CODE_LEVEL: [MessageHandler(Filters.regex(code_level_regex), code_level)],
        CODE_LEVEL_SUB: [MessageHandler(Filters.regex(code_level_sub_regex), code_level_sub)],
        ULINKS: [MessageHandler(Filters.text, ulinks)],
        USEFUL_BOTS: [MessageHandler(Filters.text, useful_bots)],
        LOOK_UP: [MessageHandler(Filters.text, look_up)],
        LOOK_UP_MARKS: [MessageHandler(Filters.text, look_up_marks)],
        LOOK_UP_OVERVIEW: [MessageHandler(Filters.text, look_up_overview)],
        UPDATE_MARKS: [MessageHandler(Filters.regex(sem_regext), update_marks)],
        MANIP_SUB: [MessageHandler(Filters.text, manip_sub)],
        HELP: [MessageHandler(Filters.text, help)],
        CANCEL: [MessageHandler(Filters.text, cancel)],
        ADD_JOB_HANDLER: [MessageHandler(Filters.text, add_job_handler)],
        ADD_CODE_HANDLER: [MessageHandler(Filters.text, add_code_handler)],
        ADD_NOTES_HANDLER: [MessageHandler(Filters.text, add_notes_handler)],
        USER_BLOCK_HANDLER: [MessageHandler(Filters.text, user_block_handler)]
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)

dispatcher.add_handler(handler)
updater.start_polling()
updater.idle()

