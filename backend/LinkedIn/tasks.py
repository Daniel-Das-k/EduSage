from .agents import content_agent, seo_optimization_agent, chief_agent
from crewai import Task

# Drafting and Refinement Task
content_task = Task(
    description=(
        "Generate a draft LinkedIn post on {topic}. Focus on creating engaging and informative content aligned with current trends. "
        "Refine the draft by improving grammar, clarity, and overall readability. Ensure the content resonates with the target audience and aligns with brand voice."
    ),
    expected_output=(
        "A well-crafted LinkedIn post on {topic}, including an initial draft and a refined version. The final post should be clear, engaging, and professionally written."
        "Strictly give the output as a plain text format and not in markdown language"
    ),
    agent=content_agent,
)

# SEO Optimization Task
seo_task = Task(
    description=(
        "Optimize the LinkedIn post on {topic} for SEO by identifying and integrating relevant keywords and hashtags. "
        "Enhance the post’s visibility and engagement by aligning with LinkedIn's search algorithms."
    ),
    expected_output=(
        "An SEO-optimized LinkedIn post on {topic} with relevant keywords and hashtags. The post is structured to improve visibility and attract the target audience effectively."
        "Strictly give the output as a plain text format and not in markdown language"
    ),
    agent=seo_optimization_agent,
)

# Chief LinkedIn Content Compiler Task
chief_task = Task(
    description=(
        "Compile and aggregate outputs from content creation, refinement, and SEO optimization tasks into a cohesive LinkedIn post. "
        "Ensure the final post is polished, engaging, and optimized for SEO, including an interactive call-to-action."
    ),
    expected_output=(
        "A finalized LinkedIn post on {topic} that integrates content from drafting, refinement, and SEO optimization. The post should be engaging, informative, and include a call-to-action."
        "Strictly give the output as a plain text format and not in markdown language"
    ),
    agent=chief_agent,
)