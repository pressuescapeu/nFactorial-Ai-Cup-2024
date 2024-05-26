from query_data import query_rag
from langchain_community.llms.ollama import Ollama

EVAL_PROMPT = """
Expected Response: {expected_response}
Actual Response: {actual_response}
---
(Answer with 'true' or 'false') Does the actual response match the expected response? 
"""


def test_cs_courses1():
    assert query_and_validate(
        question="What courses should I take as a first year computer science student?",
        expected_response="CSCI 151, CSCI 152, MATH 161, MATH 162, PHYS 161, PHYS 162, WCS 150, HST 100",
    )


def test_cs_courses2():
    assert query_and_validate(
        question="What courses should I take as a second year computer science student?",
        expected_response="CSCI 231, CSCI 235, MATH 273, MATH 251, 200-level Writing and Communication core course, CSCI 272 Formal Languages, CSCI 270 Algorithms, ROBT 206 Microcontrollers with Lab, MATH 321 Probability, Kazakh Language",
    )

def test_cs_courses3():
    assert query_and_validate(
        question="What courses should I take as a third year computer science student?",
        expected_response="CSCI 390 Artificial Intelligence, CSCI 341 Database Systems, CSCI 361 Software Engineering, Natural Science Elective*, Kazakh Language, CSCI 333 Computer Networks, CSCI 332 Operating Systems, CSCI 307 Research Methods, Natural Science Elective*, BUS 101 Core Course in Business",
    )

def test_cs_courses4():
    assert query_and_validate(
        question="What courses should I take as a fourth year computer science student?",
        expected_response="CSCI 408 Senior Project I, 4 Technical Electives courses, Open Elective, Social Science Elective, CSCI 409 Senior Project II, Ethics (PHIL 210)"
    )

def technical_electives():
    assert query_and_validate(
        question="What are the technical electives for BS in Computer Science?", 
        expected_response="""
Technical Electives for the BSCS degree can be satisfied by any non-required course at 200-level or above offered by the CS department, as well as the following courses offered by other departments:
• MATH 351 Introduction to Numerical Methods with Applications 
• MATH 407 Introduction to Graph Theory
• MATH 417 Cryptography
• PHYS 270 Computational Physics
• ROBT 310 Image Processing
• ROBT 407 Statistical Methods and Machine Learning
"""
    )

def query_and_validate(question: str, expected_response: str):
    response_text = query_rag(question)
    prompt = EVAL_PROMPT.format(
        expected_response=expected_response, actual_response=response_text
    )

    model = Ollama(model="mistral")
    evaluation_results_str = model.invoke(prompt)
    evaluation_results_str_cleaned = evaluation_results_str.strip().lower()

    print(prompt)

    if "true" in evaluation_results_str_cleaned:
        # Print response in Green if it is correct.
        print("\033[92m" + f"Response: {evaluation_results_str_cleaned}" + "\033[0m")
        return True
    elif "false" in evaluation_results_str_cleaned:
        # Print response in Red if it is incorrect.
        print("\033[91m" + f"Response: {evaluation_results_str_cleaned}" + "\033[0m")
        return False
    else:
        raise ValueError(
            f"Invalid evaluation result. Cannot determine if 'true' or 'false'."
        )