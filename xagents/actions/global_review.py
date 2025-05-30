#!/usr/bin/env python
# -*- coding: utf-8 -*

import re
from xagents.actions import Action
# from xagents.system.rules import RULES

PROMPT_TEMPLATE = '''
-----
You are a manager and also a professional analyst with expertise in multiple fields. Your goal is to evaluate whether the provided knowledge can sufficiently answer the given question.

# Question
{question}

# Answer
{knowledge}

# Steps
You will determine if the provided knowledge sufficiently addresses the question by following these steps:
1. Understand and analyze the question.
2. Evaluate the provided knowledge to determine if it fully resolves the question.
3. If the knowledge sufficiently resolves the question, output "accept".
4. If the knowledge does not resolve the question, output "reject".

# Format example
Your final output should ALWAYS be in the following format:
## Result: <accept/reject>

# Attention
1. You MUST only output "accept" or "reject" based on the evaluation.
2. DO NOT include any additional explanation or reasoning in the output.
3. Use '## Result:' as the prefix for the output.
-----
'''

OUTPUT_MAPPING = {
    "Global Review": (str, ...)
}


class GlobalReview(Action):

    def __init__(self, name="GlobalReview", context=None, llm=None):
        super().__init__(name, context, llm)

    async def run(self, question, knowledge):

        prompt = PROMPT_TEMPLATE.format(question=question, knowledge=knowledge)
        rsp = await self._aask_v1(prompt, "task", OUTPUT_MAPPING)

        return rsp
