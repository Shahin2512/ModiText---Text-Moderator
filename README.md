# ModiText---Text-Moderator
ModiText is a project built to help quickly find and understand if a comment or piece of text is offensive. It uses AI (LLaMA3 model from Groq API) to scan each comment  and tells you three things:

1. Whether the comment is offensive or not

2. What type of offense it is (like hate speech, toxicity, profanity, etc.)

3. A short explanation in simple words

Upload a .csv or .json file containing comments, and ModiText will analyze each one, add new columns to show the results, and give a clean output file with everything marked clearly.

It also gives a quick summary and even shows a pie chart to help visualize the types of offensive content found in the data.
