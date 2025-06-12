# Transcript Agent

This repository contains a simple transcript agent that allows users to query and analyze call transcripts stored in a Supabase database.

## Features

- Query transcripts by company name.
- Case-insensitive search for company domains.
- Output formatted transcript information.

## Prerequisites

- Python 3.6 or higher
- Supabase account and API key
- OpenAI API key

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/austin02202016/the_nest_public.git
   cd the_nest_public
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with the following content:
   ```
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_api_key
   OPEN_AI_API_KEY=your_openai_api_key
   ```

## Usage

1. Run the transcript agent:
   ```bash
   python tools/transcript_agent.py
   ```

2. Use the agent to query transcripts by company name:
   ```bash
   python -c "from tools.transcript_agent import get_transcripts; print(get_transcripts('Origami'))"
   ```

3. Go to your UI and ask a question concerning the company domain you entered. For example, if the company domain was "origamiagents.com," you can ask, "What was the summary for the last call with Origami?"

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 