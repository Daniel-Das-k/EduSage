from crewai import Task
from agents import (
    discord_content_creation_specialist,
    discord_content_compiler_formatter
)

# Task for Discord Content Creation Specialist
content_creation_task_discord = Task(
    description=(
        "Generate and optimize a Discord post on {topic}. Create engaging, clear, and well-structured content with relevant keywords. "
        "Include ideas for multimedia elements to boost engagement."
    ),
    expected_output=(
        "An engaging and optimized Discord post on {topic}, improved in grammar and clarity, and structured for maximum impact."
    ),
    agent=discord_content_creation_specialist,
)

# Task for Discord Content Compiler and Formatter
compile_and_format_task_discord = Task(
    description=(
        "Compile and format the final Discord post using content from previous tasks. Ensure it is well-structured, engaging, and optimized for readability. "
        "Include a call-to-action and format it as a neat, concise paragraph."
    ),
    expected_output=(
        "A finalized Discord post on {topic}, incorporating drafts and optimizations, formatted as a concise paragraph (4-5 lines) with a call-to-action."
        "don't give any multimedia ideas "
    ),
    agent=discord_content_compiler_formatter,
    async_execution=False,
    output_file="outputs/post.md"
)
