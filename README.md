<h1 align="center">
XAgents: A Unified Framework for Multi-Agent Cooperation viaIF-THEN Rules and Multi-Polar Task Processing Graph
</h1>
<p align="center">
<img src="https://img.shields.io/badge/OS-Ubuntu22.4-blue" />
<img src="https://img.shields.io/badge/Python-3.8-red" />
<img src="https://img.shields.io/badge/Build-Success-green" />
<img src="https://img.shields.io/badge/License-BSD-blue" />
<img src="https://img.shields.io/badge/Release-0.1-blue" />
</p>

<p align="center">
<img src="doc/png/fig.xagents.png" width=80%/> <br>
<b>Figure 1</b>. Structure of XAgents.
</p>


## Email Reply Case Study
<p align="center">
<img src="doc/png/fig.xemail.png" width=80%/> <br>
<b>Figure 2</b>. Case study: XAgents applied to a real-world email processing task.
</p>

To further analyze the capabilities of XAgents, we applied it to real-world email processing tasks, as shown in Fig. 2. This case involves replying an email from the editor-in-chief of a film review magazine. The detailed processing flow is as follow:
- Step 1. PA initializes an MTPG. MTPG includes a original task node, four subtask node, and a Fusion Node, as illustrated in Fig. 2.a.
- Step 2. For each subtask, ITRDM uses DAA to initialize three domain rules. As shown in Fig. 2.b, DAA analyses the domains of the $T_1$ subtask.
- Step 3. Based on the domain rules, the subtasks are processed from different domain perspectives, and all the results are fused by FEA in an adversarial manner to generate a unified output. This output is then matched with the global objective under the global rule.  As shown in Fig. 2.d, ITRDM conduct rule-based reasoning and decision-making for the subtask $T_1$.
- Step 4. If it does not match, the process returns to Step 2. If a subtask fails to execute, a task path reconstruction is triggered. As shown in Fig. 2.e, the subtask $T_3$ failed, ITRDM reconstructs the task path through add new subtasks {$T_{3a}, T_{3b}, T_{3c}$}.
- Step 5. After all subtasks are finalized, all outputs are fused at the fusion node of the MTPG to form a complete email as shown in Fig 2.f.

## Conda Enviroment Setup

``` shell
conda create --name XAgents --file ./requirements.txt
conda activate XAgents
```

## Datasets

**Task1.Trivia Creative Writing.** The task tests LLMs' ability to retrieve and integrate diverse
information from their internal knowledge. In this task, a model must craft a coherent story around a
given topic while incorporating answers to 𝑁 trivia questions. We evaluate the models with 𝑁 set to 5
and 10, where a higher 𝑁 requires more extensive domain knowledge. Our benchmark includes 100
instances for each 𝑁, totaling 1,000 trivia questions.

**Task2. Logic Grid Puzzle.** The task is from the Bigbench dataset, which comprises 200 instances.
Each instance describes a logic puzzle involving 2 to 5 houses, each occupied by a person with specific
characteristics, such as playing the piano. The goal is to answer questions about house numbers based
on given clues, requiring multi-step reasoning and the selection of relevant information. For evaluation,
we measure the accuracy of the predicted house numbers by comparing them to the ground truth targets
provided by the dataset.

**Task3. Codenames Collaborative.** The task is an extension of the Codenames task from the BigBench.
Codenames Collaborative is a collaborative task that examines a model’s knowledge, reasoning, and
theory of mind abilities by assigning two player roles: the Spymaster and the Guesser. The Spymaster’s
role is to provide a hint word related to the target words, excluding some other distractor words, while
the Guesser’s role is to identify the target words based on the given hint and the full list of words.

The three datasets are publicly accessible in https://github.com/MikeWangWZHL/Solo-PerformancePrompting/tree/main/data (SPP project). These data does not contain any information that names or
uniquely identifies individual people or offensive content. The datasets are only for test. Trivia
Creative Writing has 100 samples (N=5) and 100 samples (N=10). Logic Grid Puzzle has 200
samples. Codenames Collaborative has 50 samples.

## Installation and Usage

### Installation

```bash
cd XAgents
python setup.py install
```

### Configuration

- Configure your `OPENAI_API_KEY` in  `config/config.yaml`

| Variable Name                              | Explain                                   | Sample                                          |
| ------------------------------------------ | ----------------------------------------- | ----------------------------------------------- |
| OPENAI_API_KEY                             | Replace with your own key                 | OPENAI_API_KEY: "sk-..."                        |
| OPENAI_API_BASE                            | Optional, access OpenAI API through a third-party proxy. | OPENAI_API_BASE: "https://<YOUR_SITE>/v1"       |
| OPENAI_API_MODEL                           | The specific version of the model used    | OPENAI_API_MODEL: "<PROVIDER>/<MODEL_NAME>"     |
| MAX_TOKENS                                 | The maximum number of tokens allowed in API requests and responses | MAX_TOKENS: 3000       |

### Usage
```python
python startup.py --question_or_task "Write an article about American culture."
```

## Examples

### Question or Task: Write an article about American culture.

[XAgents-Case.md](XAgents-Case.md)
