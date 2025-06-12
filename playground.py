from agno.agent import Agent
from agno.playground import Playground, serve_playground_app
from tools.transcript_agent import get_transcripts
from agno.models.openai import OpenAIChat
from agno.storage.sqlite import SqliteStorage

# Define the agent storage
agent_storage: str = "tmp/agents.db"

# Create the Transcript agent
transcript_agent = Agent(
    name="Transcript Agent",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[get_transcripts],
    instructions=[
        "You are my intelligent assistant for analyzing customer call transcripts and finding specific information.",
        "IMPORTANT: You MUST follow this EXACT sequence for EVERY question:",
        "",
        "1. For questions about specific terms or phrases (e.g., 'Who mentioned X?' or 'Find mentions of Y'):",
        "   - Use exact_search with the term or phrase",
        "   - The tool will return matches with context",
        "   - For each match, use get_call_by_id to get the full transcript",
        "   - Format the response with:",
        "     * Company name and POC",
        "     * Date of the mention",
        "     * Context of the mention",
        "     * Full transcript reference",
        "",
        "2. For questions about specific companies:",
        "   - First call get_transcript_ids with the company name",
        "   - For each transcript ID:",
        "     * Call get_call_by_id with the ID",
        "     * If split into parts, process each part",
        "     * Analyze for relevant information",
        "     * Track quotes and dates",
        "",
        "Your response MUST follow this format:",
        "SUMMARY: Brief 1-2 sentence summary",
        "",
        "DETAILS:",
        "- [Date] (Company: X, POC: Y): 'Relevant quote or context'",
        "- [Date] (Company: X, POC: Y): 'Another relevant quote'",
        "",
        "CONCLUSION: Brief wrap-up of key points",
        "",
        "IMPORTANT RULES:",
        "- For term searches, ALWAYS use exact_search first",
        "- Keep responses concise and focused",
        "- Only include directly relevant information",
        "- Format all responses exactly as shown above",
        "- If no relevant information is found, say so clearly",
        "- If there are many matches, focus on the most relevant ones",
        "- Process transcripts in chronological order (newest first)",
        "",
        "DEBUGGING TIPS:",
        "- If no matches found, try alternative terms",
        "- Make sure to process every transcript returned",
        "- Keep track of which transcript each piece of information came from",
        "- If you get an error on one transcript, continue with the others",
        "- If a transcript is split into parts, make sure to analyze all parts"
    ],
    storage=SqliteStorage(table_name="transcript_agent", db_file=agent_storage),
    add_datetime_to_instructions=True,
    add_history_to_messages=True,
    num_history_responses=5,
    markdown=True,
    show_tool_calls=True
)

app = Playground(agents=[transcript_agent]).get_app()

if __name__ == "__main__":
    serve_playground_app("playground:app", reload=True)