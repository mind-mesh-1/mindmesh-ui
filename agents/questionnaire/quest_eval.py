from langchain_core.prompts import ChatPromptTemplate
ph9_q=["Over the last two weeks, how often have you been bothered by little interest or pleasure in doing things? (0 = Not at all, 1 = Several days, 2 = More than half the days, 3 = Nearly every day): ",
        "Over the last two weeks, how often have you been bothered by feeling down, depressed, or hopeless? (0 = Not at all, 1 = Several days, 2 = More than half the days, 3 = Nearly every day): ",
        "Over the last two weeks, how often have you been bothered by trouble falling or staying asleep, or sleeping too much? (0 = Not at all, 1 = Several days, 2 = More than half the days, 3 = Nearly every day): ",
        "Over the last two weeks, how often have you been bothered by feeling tired or having little energy? (0 = Not at all, 1 = Several days, 2 = More than half the days, 3 = Nearly every day): ",
        "Over the last two weeks, how often have you been bothered by poor appetite or overeating? (0 = Not at all, 1 = Several days, 2 = More than half the days, 3 = Nearly every day): ",
        "Over the last two weeks, how often have you been bothered by feeling bad about yourself – or that you are a failure or have let yourself or your family down? (0 = Not at all, 1 = Several days, 2 = More than half the days, 3 = Nearly every day): ",
        "Over the last two weeks, how often have you been bothered by trouble concentrating on things, such as reading the newspaper or watching television? (0 = Not at all, 1 = Several days, 2 = More than half the days, 3 = Nearly every day): ",
        "Over the last two weeks, how often have you been bothered by moving or speaking so slowly that other people could have noticed? Or the opposite – being so restless that you have to move around a lot more than usual? (0 = Not at all, 1 = Several days, 2 = More than half the days, 3 = Nearly every day): ",
        "Over the last two weeks, how often have you been bothered by thoughts that you would be better off dead or of hurting yourself in some way? (0 = Not at all, 1 = Several days, 2 = More than half the days, 3 = Nearly every day): "
]
responses={}
for i, q in enumerate(ph9_q):
    while True:
        try:
            user_response=input(f"Q{i+1}:{q}")
            user_response_int=int(user_response)
            if 0<=user_response_int <=3:
                responses[f"Q{i+1}"]=user_response_int
                break
            else:
                print("Please enter a number between 0 and 3")
        except ValueError:
            print("Invalid number")
                
score=sum(responses.values())
suicidal_score = responses.get("Q9", 0) > 0

def interpret_score(score):
    if 0 <= score <= 4: 
        return "Minimal"
    elif 5 <= score <= 9: 
        return "Mild"
    elif 10 <= score <= 14: 
        return "Moderate"
    elif 15 <= score <= 19: 
        return "Moderately Severe"
    elif 20 <= score <= 27: 
        return "Severe"
    else:
        return "Invalid"

total_score=interpret_score(score)

llm_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a highly empathetic and professional mental health assistant. Your task is to provide a compassionate and informative summary of a patient's PHQ-9 questionnaire responses, including their total score, severity level, and any indication of suicidal thoughts. Do not provide a diagnosis. Always recommend seeking professional help."),
    ("human", """The patient has completed the PHQ-9 questionnaire with the following responses:
Q1 (Little interest): {q1_val}
Q2 (Feeling down): {q2_val}
Q3 (Trouble sleeping): {q3_val}
Q4 (Feeling tired): {q4_val}
Q5 (Poor appetite): {q5_val}
Q6 (Feeling bad): {q6_val}
Q7 (Trouble concentrating): {q7_val}
Q8 (Being restless): {q8_val}
Q9 (Suicidal thought): {q9_val}

Based on these responses, the calculated total score is {score}, indicating a severity level of {total_score}.
Suicidal thoughts are {suicidal_score} based on Q9.

Please provide a compassionate summary of these findings and a clear recommendation for seeking professional help.
"""),
])
formatted_prompt = llm_prompt.format_messages(
    q1_val=responses.get('Q1'),
    q2_val=responses.get('Q2'),
    q3_val=responses.get('Q3'),
    q4_val=responses.get('Q4'),
    q5_val=responses.get('Q5'),
    q6_val=responses.get('Q6'),
    q7_val=responses.get('Q7'),
    q8_val=responses.get('Q8'),
    q9_val=responses.get('Q9'),
    score=score,
    total_score=total_score,
    suicidal_score='indicated' if suicidal_score else 'not indicated'
)
#dotenv.load_dotenv()
os.environ['OPENAI_API_KEY']=os.getenv("OPENAI_API_KEY")
client = OpenAI(
    api_key = os.environ.get("OPENAI_API_KEY")
)
llm = ChatOpenAI(
    model="gpt-4o-mini", temperature =0.5
)
llm_response = llm(formatted_prompt)
print("\nLLM Analysis:")
print(llm_response.content)
