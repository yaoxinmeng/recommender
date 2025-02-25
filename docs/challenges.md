# Challenges
## Technical Challenges
1. Builtin API from LangChain does not work great out of the box - 

## Non-technical challenges
1. Allowed LLM invocation rate is very low for personal AWS account. 
This makes development work slower than expected, since each run of the pipeline takes a few minutes to process (multiple retries using the customised backoff function).
2. Large models with better performance are prohibitively expensive and not feasible for experimentation with an agentic system that will be making iterative LLM calls. As such, the system could only be tested with smaller models, and performance had to be boosted through other means such as prompt engineering.