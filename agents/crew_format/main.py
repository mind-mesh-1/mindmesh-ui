import sys
from crew import Sentiment

def run():
    """
    Run the crew.
    """
    inputs ={"text": "Im feeling depressed and Im not happy",
            "user":"Diana",
             "days":"12 days"
            }

    Sentiment().crew().kickoff(inputs=inputs)
run()




