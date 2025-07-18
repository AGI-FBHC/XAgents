#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
@Time    : 2024/4/18 13:26          
@Author  : Mingxian Gu
@File    : manager
"""
from xagents.roles import Role
from xagents.system.logs import logger
from xagents.system.schema import Message
from xagents.actions import Requirement, MakePlans, CreateGraph, OptimizeGraph, CreateRoles
import json
import re


class Manager(Role):
    def __init__(self, name="Manager", profile="Manager", goal="Efficiently to develop plans", constraints="",
                 serpapi_key=None, **kwargs):
        super().__init__(name, profile, goal, constraints, **kwargs)

        self._init_actions([MakePlans, CreateGraph, OptimizeGraph, CreateRoles])
        self._watch([Requirement])

    async def _act(self) -> Message:
        self._set_state(0)
        logger.info(f"{self._setting}: ready to {self._rc.todo}")
        plans = await self._rc.todo.run(question_or_task=self._rc.important_memory[0].content)

        self._set_state(1)
        logger.info(f"{self._setting}: ready to {self._rc.todo}")
        graph = await self._rc.todo.run(question_or_task=self._rc.important_memory[0].content,
                                        plans=plans.instruct_content.Subtasks.strip())

        self._set_state(2)
        logger.info(f"{self._setting}: ready to {self._rc.todo}")
        graph = await self._rc.todo.run(question_or_task=self._rc.important_memory[0].content,
                                        plans=graph.content)
        result = extract_tasks_from_graph_content(graph.content)

        self._set_state(3)
        logger.info(f"{self._setting}: ready to {self._rc.todo}")
        roles = await self._rc.todo.run(question_or_task=self._rc.important_memory[0].content,
                                        plans=result)

        response = plans.content + graph.content + roles.content

        msg = Message(content=response, role=self.profile, cause_by=type(self._rc.todo))
        self._rc.memory.add(msg)

        return msg

    async def run(self, message=None):
        await self._observe()
        rsp = await self._act()
        await self._publish_message(rsp)
        return rsp


def extract_tasks_from_graph_content(graph_content):
    json_blocks = re.findall(r'\{.*?\}', graph_content, re.DOTALL)
    tasks = []
    for block in json_blocks:
        try:
            data = json.loads(block.strip())
            tasks.append(f"{data['number']}.{data['task']}")
        except json.JSONDecodeError:
            continue
    return "\n".join(tasks)
