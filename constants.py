# Constant messages used in the app

WELCOME_MESSAGE = "Welcome to Scheduler Bot! I'm here to help you manage your events and meetings efficiently. " \
                  "Feel free to ask me to schedule, reschedule, or inquire about any event details. " \
                  "Let's make your planning easier!"


GPT_PROMPT_FOR_NECESSARY_FORMAT = """ Can you extract key points of schedule from this sentence: {}
                Only give this exact json as an answer even if the fields are empty, nothing else:
                {{
                    "hour":"",
                    "title":"",
                    "minute":"",
                    "am/pm":"",
                    "day":"",
                    "month":"",
                    "year":""
                }}
"""

EXTRACT_TITLE = """Extract event/meeting title from this sentence(Give only the title, nothing else):"{}" """

GPT_PROMPT_FOR_TAG = """ [greeting,goodbye,thanks,ScheduleMeeting,When,CancelMeeting,InquireMeeting,
                        RescheduleMeeting,EventTitle,AskAvailableDays,AskAvailableHours]
                        classify this sentence according to tags above. 
                        Which tag is the best for this sentence. (Give only the tag nothing else): "{}" """

NECESSARY_SCHEDULING_FORMAT = {
    "hour": "",
    "title": "",
    "minute": "",
    "am/pm": "",
    "day": "",
    "month": "",
    "year": ""
}

ASK_UNDEFINED_FIELDS = "Please provide information for these fields: "

SUCCESSFULLY_CREATED = 'Event is successfully created in your Google Calendar!'

FAIL_WHILE_CREATION = 'There has been an error while creating the event :('
