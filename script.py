import pdfplumber
import csv
import time
PDF_PATH = '/Users/akifislam/PycharmProjects/PlumberTest/Resources/AS  Biology (9700)/2011/9700_s11_qp_11.pdf'
PAGE_NUMBER = 6

SL_COLUMN_A = []  # For SL Input in Excels
QUES_TEXT_COLUMN_B = [] # For Question in Excels
OPTIONS_COLUMN_I_J_K_L = [] # Collecting Options
HAS_ANY_QTABLE= []
HAS_ANY_ANSWER_TABLE = []
ALL_TABLE_DATA = []
ANSWER_TABLE_DATA = []
OPTION_TABLE_DATA = []

def updateQTABLEStatus(index,status):
    if(HAS_ANY_QTABLE[index]==False):
        HAS_ANY_QTABLE[index] = status


def countSerial():
    count = 16 #Start of Page Count
    with pdfplumber.open(PDF_PATH) as pdf:
        page_all_texts = (pdf.pages[PAGE_NUMBER].extract_text())
        page_all_texts = page_all_texts
        spllited_page_all_texts = (page_all_texts.splitlines(False))
        # print(spllited_page_all_texts.count("?"))

        # Checking How Many Questions are in a Page
        for line in spllited_page_all_texts:
            # print(line)
            if(line.__contains__("?")):
                count+=1
                SL_COLUMN_A.append(count)

        # print("Question Serial : ",SL_COLUMN_A)






def collectQuestions():
    with pdfplumber.open(PDF_PATH) as pdf:
        questionSerialiterator = 0
        page_all_texts = (pdf.pages[PAGE_NUMBER].extract_text())
        page_all_texts = page_all_texts
        spllited_page_all_texts = (page_all_texts.splitlines(False))
        cur_question = ""
        gotAnswerOptions = True
        gotQTable = False
        # Checking for Questions
        for line in spllited_page_all_texts:

            # Whiteline Ignore
            if(line.isspace()):
                continue

            #Breaking Condition
            if (questionSerialiterator == len(SL_COLUMN_A)):
                break

            #Graph Detection
            # if(line.__contains__("graph") or line.__contains__("diagram") ):
            #     print("\nGraph Detected\n")

            #Table Detection
            # if(line.count("  ")>=2):
            #     print("\nTable Detected\n")

            # Logic
            if (gotAnswerOptions and line.startswith(str(SL_COLUMN_A[questionSerialiterator]))):

                cur_question+=line.lstrip(str(SL_COLUMN_A[questionSerialiterator]))+"\n"

                # print(line)
                if(line.__contains__("A  ")):
                    gotAnswerOptions = True

                    questionSerialiterator+=1
                    QUES_TEXT_COLUMN_B.append(cur_question)
                    cur_question=""

                else:
                    gotAnswerOptions = False

            elif(gotAnswerOptions==False):
                if (line.strip("").__contains__("A  ")):
                    gotAnswerOptions = True
                    questionSerialiterator += 1
                    QUES_TEXT_COLUMN_B.append(cur_question)
                    cur_question = ""
                else:
                    if (line.count("  ") >= 2 or line.isspace()):
                        continue
                    else:
                        cur_question += line + "\n"









def collectOptions():
    with pdfplumber.open(PDF_PATH) as pdf:
        questionSerialiterator = 0
        page_all_texts = (pdf.pages[PAGE_NUMBER].extract_text())
        page_all_texts = page_all_texts
        spllited_page_all_texts = (page_all_texts.splitlines(False))
        options_for_cur_question = []
        possible_options=['A  ', 'B  ', 'C  ', 'D  ']
        # Checking for Questions
        for line in spllited_page_all_texts:

            # Whiteline Ignore
            if(line.isspace()):
                continue

            #Graph Detection
            # if(line.__contains__("graph") or line.__contains__("diagram") ):
            #     print("\nGraph Detected\n")

            # #Table Detection
            # if(line.count("  ")>=2):
            #     print("\nTable Detected\n")

            # Logic
            for i in range (0,4):
                if line.__contains__(possible_options[i]):
                    optionStartIndex = line.find(possible_options[i])
                    if(i<3):
                        optionEndIndex = line.find(possible_options[i+1])
                        options_for_cur_question.append(line[optionStartIndex+3:optionEndIndex])
                    else:
                        options_for_cur_question.append(line[optionStartIndex+3:])

                if(len(options_for_cur_question)==4):
                    OPTIONS_COLUMN_I_J_K_L.append(options_for_cur_question)
                    options_for_cur_question = []




def getAnswerTableLocation():
    # print(len(OPTIONS_COLUMN_I_J_K_L))
    for i in range (0,len(OPTIONS_COLUMN_I_J_K_L)):
        if(OPTIONS_COLUMN_I_J_K_L[i][1].count("  "))>=1:
            LEN = len(OPTIONS_COLUMN_I_J_K_L[i][1])
            IND = OPTIONS_COLUMN_I_J_K_L[i][1].find("  ")
            if(LEN-IND>2):
                HAS_ANY_ANSWER_TABLE.append(True)
            else:
                HAS_ANY_ANSWER_TABLE.append(False)
        else:
            HAS_ANY_ANSWER_TABLE.append(False)

def getAnswerTableData():
    with pdfplumber.open(PDF_PATH) as pdf:
        # print(pdf.pages[PAGE_NUMBER].extract_tables())
        ALL_TABLE_DATA.append(pdf.pages[PAGE_NUMBER].extract_tables())
    # if(len(ALL_TABLE_DATA[0])!=len(OPTIONS_COLUMN_I_J_K_L)):
    #         # print("Q TABLE FOUND")



countSerial()
collectQuestions()
collectOptions()

getAnswerTableLocation()
getAnswerTableData()
# print(OPTIONS_COLUMN_I_J_K_L)


for i in range (0,len(ALL_TABLE_DATA[0])):
    AB_counter = 0
    # print(ALL_TABLE_DATA[0][i]) #First Table
    #Now check if it is a option table
    for j in range (0,len(ALL_TABLE_DATA[0][i])):
        if ('A' in ALL_TABLE_DATA[0][i][j] or 'B' in ALL_TABLE_DATA[0][i][j] or 'C' in ALL_TABLE_DATA[0][i][j] or 'D' in ALL_TABLE_DATA[0][i][j]):
            AB_counter+=1
        if 'A \nB \nC \nD' in ALL_TABLE_DATA[0][i][j]:
            AB_counter=4

    if(AB_counter==4):
        ANSWER_TABLE_DATA.append(ALL_TABLE_DATA[0][i])



newCSVfile = open('/Users/akifislam/Desktop/summary.csv', 'w')
writer = csv.writer(newCSVfile)

#CSV Processing Part
# Adding Header
writer.writerow(['SL.','Question Name*','Question Text*','Question Table <QTABLE>','Answer Format*','Answer Column header/s Level1*','Answer Column header/s Level2','Answer Row header/s Level2','Option A*','Option B*','Option C*','Option D*','Correct Answer*','Tags-Topic','Tag-Difficulty*','Tag-UniqueID*','General Feedback','Grade(Default =1)','Penalty (default = none)','Shuffle Answers (default = no)','Answer numbering (default = abcd..)'])
# Adding Data

for i in range (0,len(SL_COLUMN_A)):
    cur_seral = SL_COLUMN_A[i];
    cur_qus_name = PDF_PATH.split('/')[-1].split('.')[0] + "_" + str(i)
    cur_question_text = QUES_TEXT_COLUMN_B[i]
    cur_Q_TABLE = ""
    cur_ans_row_header_l2 = "";
    cur_options = []
    cur_ans_col_header_l2 = ""
    cur_ans_col_header_l1 = ""
    cur_answer_format = ""

    # print(ALL_TABLE_DATA)
    # print(ANSWER_TABLE_DATA)
    # Answer Format
    # print(HAS_ANY_ANSWER_TABLE)

    if(HAS_ANY_ANSWER_TABLE[i]==True):
        # Getting Table Format
        cur_answer_format = "With Table"

        # Check for L1 Headers

        if "A" not in ANSWER_TABLE_DATA[i][0]:
            for item in ANSWER_TABLE_DATA[i][0]:
                if(str(item).isspace() or item=="," or item==None):
                    continue
                cur_ans_col_header_l1+= item + ","

        #Check for L2 Headers
        if "A" not in ANSWER_TABLE_DATA[i][1]:
            for item in ANSWER_TABLE_DATA[i][1]:
                if (str(item).isspace() or item == "," or item == None):
                    continue
                cur_ans_col_header_l2 += item + ","

    else:
        cur_ans_col_header_l2=""
        cur_ans_col_header_l1=""
        cur_answer_format = "No Table"

    # print(ALL_TABLE_DATA)
    #Filliing Up Options
    if(HAS_ANY_ANSWER_TABLE[i]==True):
        # print("Table Found")
        for data in ANSWER_TABLE_DATA[i]:
            # print("data: ", data)
            if("A" in data or "B" in data or "C" in data or "D" in 'A \nB \nC \nD' in data ):
                cur_options = ["ANSWER TABLE DATA 1", "ANSWER TABLE DATA 2", "ANSWER TABLE DATA 3", "ANSWER TABLE DATA 4"]
    else:
        cur_options = [OPTIONS_COLUMN_I_J_K_L[i][0], OPTIONS_COLUMN_I_J_K_L[i][1], OPTIONS_COLUMN_I_J_K_L[i][2],OPTIONS_COLUMN_I_J_K_L[i][3]]

    print(cur_options)
    #Current Option Processing
    # cur_options_processed = []
    #
    # for eachOption in cur_options:
    #     tempstr=""
    #     for item in eachOption:
    #         tempstr+=item+"##"
    #     cur_options_processed.append(tempstr)
    writer.writerow([cur_seral,cur_qus_name,cur_question_text, cur_Q_TABLE,cur_answer_format,cur_ans_col_header_l1,cur_ans_col_header_l2,cur_ans_row_header_l2,cur_options[0],cur_options[1],cur_options[2],cur_options[3]])
#


newCSVfile.close()