import sys
import os
sys.path.append(os.path.abspath("../services")) 
from llama_service import generate_counterargument, summarize_debate

# Test counterargument
text = "AI will eventually outperform humans in all cognitive tasks."
counter = generate_counterargument(text, stance="for")
print("Counterargument:\n", counter)

# Test summary
arguments = [
    "AI will eventually outperform humans in all cognitive tasks.",
    "Humans will always have unique creativity and empathy."
]
summary = summarize_debate(arguments)
print("\nSummary:\n", summary)
