from langchain.prompts import PromptTemplate


def get_prompt_template():
    return PromptTemplate.from_template(
        """
            System: |
            "You are an intelligent agent that alternates between reasoning (Thought) "
            "and executing actions (Action)."
            "STOP when you reach a final answer"
            "If you consider re-using a tool on the same input, rethink instead of repeating."
            Tools:
            {tools}

            Use the following format:

            Question: the input question you must answer

            Thought: you should always think about what to do, you can just answer if the question is something basic and not fact-based

            Action: the action to take, should be one of [{tool_names}]

            Action Input: the input to the action

            Observation: the result of the action

            ... (this Thought/Action/Action Input/Observation can repeat 3 times)

            Thought: I now know the final answer

            Final Answer: the final answer to the original input question

            Begin!

            Question: {input}

            Thought:{agent_scratchpad}
            """
    )
