import os
from openai import OpenAI

def seperate_text(user_message, 
                           seperator="sentence",
                           model="mistral-nemo-instruct-2407", 
                           temperature=0.7,
                         ):
    # Start lm-studio server
    print("Starting lm-studio server...")
    os.system("lms server start")
    os.system(f"lms load {model} --identifier \"{model}\"")

    # Connect to the local server
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

    try:
        # Interact with the model
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": f"""Take the input text and separate each {seperator} with three vertical bars (|||). 
                 Do not change the content of the text;  simply insert ||| between each {seperator}. 
                 Return the modified text exactly as described."""},
                {"role": "user", "content": user_message}
            ],
            temperature=temperature,
        )
        response = completion.choices[0].message.content

        # Unload the model after use
        os.system(f"lms unload {model}")
        return split_text(response)
    except Exception as e:
        print("An error occurred:", e)
        os.system(f"lms unload {model}")
        return None



def represent_text(user_messages: list[str], 
                    seperator="|||",
                    system_message="",
                    model="mistral-nemo-instruct-2407", 
                    temperature=0.7):
    # Start lm-studio server
    is_system_message = True
    if not system_message:
        is_system_message = False
        system_message="""For the paragraph in the input text perform the following tasks: 
        1.	Identify a physical aspect of the paragraph. This should be a tangible object, action, or concept described in real life. 
        Avoid abstract terms. For example: If the paragraph discusses climate change, a suitable example might be 
        solar panels rather than global warming, as solar panels represent a physical object.	
        2.	Return a string of up to five words, representing this physical aspect.
        3. Return nothing else, do not return your explanation for your decision
        4. Do not use any of the following words or a plural version of these words, unless you add an additional word: """
    print("Starting lm-studio server...")
    os.system("lms server start")
    os.system(f"lms load {model} --identifier \"{model}\"")

    # Connect to the local server
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

    try:
        responses = []
        # user_messages = split_text(user_message)
        for user_message in user_messages:
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                temperature=temperature,
            )
            responses.append(completion.choices[0].message.content)
            if not is_system_message:
                system_message += completion.choices[0].message.content + ", "

        # Unload the model after use
        os.system(f"lms unload {model}")
        # print(system_message)
        return responses
    except Exception as e:
        print("An error occurred:", e)
        os.system(f"lms unload {model}")
        return None

def split_text(text):
    return text.split("|||")