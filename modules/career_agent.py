
import json
import os
from modules.memory import save_preference, get_preferences
from openai import OpenAI
from dotenv import load_dotenv

from modules.job_search import search_jobs
from modules.recommender import recommend_jobs

load_dotenv()


# --------------------------------
# TOOL 1: Search jobs
# --------------------------------

def search_jobs_tool(query, location="Any"):

    results = search_jobs(query)

    if location != "Any":
        results = results[
            results["location"].str.lower() == location.lower()
        ]

    return results.head(5).to_dict(orient="records")


# --------------------------------
# TOOL 2: Recommend jobs
# --------------------------------

def recommend_jobs_tool(candidate_skills, location="Any"):

    if not candidate_skills:
        return {"message": "Please upload your resume first."}

    results = recommend_jobs(
        candidate_skills,
        location
    )

    return results.to_dict(orient="records")


# --------------------------------
# TOOL DEFINITIONS
# --------------------------------

tools = [
    {
        "type": "function",
        "function": {
            "name": "search_jobs_tool",
            "description": "Search jobs based on a natural language query and optional location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The job search query"
                    },
                    "location": {
                        "type": "string",
                        "description": "Preferred location or Any"
                    }
                },
                "required": ["query", "location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "recommend_jobs_tool",
            "description": "Recommend jobs based on the candidate's actual resume skills.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Preferred location or Any"
                    }
                },
                "required": ["location"]
            }
        }
    }
]


# --------------------------------
# EXECUTE TOOLS
# --------------------------------

def execute_tool(name, arguments, candidate_skills):

    if name == "search_jobs_tool":

        return search_jobs_tool(
            arguments["query"],
            arguments["location"]
        )

    elif name == "recommend_jobs_tool":

        return recommend_jobs_tool(
            candidate_skills,
            arguments["location"]
        )

    return {"error": "Unknown tool"}


# --------------------------------
# LOCAL FALLBACK AGENT
# --------------------------------

def detect_preferences(message):

    text = message.lower()
    preferences = {}

    # Detect preferred job role
    roles = [
        "Python Developer",
        "Java Developer",
        "Data Analyst",
        "Data Scientist",
        "Machine Learning Engineer",
        "AI Engineer",
        "Cloud Engineer",
        "DevOps Engineer",
        "NLP Engineer",
        "Full Stack Developer"
    ]

    for role in roles:
        if role.lower() in text:
            preferences["preferred_role"] = role
            break

    # Detect preferred location
    locations = [
        "Chennai",
        "Bengaluru",
        "Gurugram",
        "Hyderabad",
        "Remote"
    ]

    for location in locations:
        if location.lower() in text:
            preferences["preferred_location"] = location
            break

    # Detect preferred job type
    if "internship" in text or "intern" in text:
        preferences["preferred_job_type"] = "Internship"

    elif "full-time" in text or "full time" in text:
        preferences["preferred_job_type"] = "Full-time"

    elif "part-time" in text or "part time" in text:
        preferences["preferred_job_type"] = "Part-time"

    return preferences


def local_agent(message, candidate_skills):

    # Detect new preferences
    detected = detect_preferences(message)

    # Save detected preferences in SQLite
    for key, value in detected.items():
        save_preference(key, value)

    # Retrieve saved preferences
    preferences = get_preferences()

    # Check whether the user wants to view preferences
    if any(word in message.lower() for word in
           ["my preferences", "what do you remember", "my saved preferences"]):

        if preferences:
            return "Your saved preferences:\n\n" + json.dumps(
                preferences, indent=2
            )

        return "You have not saved any preferences yet."

    # If new preferences were detected, confirm saving
    if detected:
        return (
            "Your preferences have been saved successfully!\n\n"
            + json.dumps(preferences, indent=2)
            + "\n\nI will use these preferences for future job searches."
        )

    # Use saved location if no new location is mentioned
    location = preferences.get("preferred_location", "Any")

    # Use saved role if available
    preferred_role = preferences.get("preferred_role", "")

    # Use saved job type if available
    job_type = preferences.get("preferred_job_type", "")

    text = message.lower()

    # Personalized job recommendations
    if any(word in text for word in
           ["recommend", "based on my resume", "my skills"]):

        results = recommend_jobs_tool(candidate_skills, location)

        return (
            "Here are your personalized job recommendations:\n\n"
            + json.dumps(results, indent=2)
        )

    # Search jobs using saved preferences
    if any(word in text for word in
           ["find", "search", "job", "internship", "developer"]):

        query = message

        if preferred_role and preferred_role.lower() not in text:
            query = preferred_role + " " + query

        results = search_jobs_tool(query, location)

        if isinstance(results, list) and job_type:
            results = [
                job for job in results
                if job_type.lower() in job.get("job_type", "").lower()
            ]

        return (
            "Here are the jobs based on your preferences:\n\n"
            + json.dumps(results, indent=2)
        )

    return (
        "Hello! I am your AI Career Agent. "
        "I can search jobs and recommend opportunities "
        "based on your resume and saved preferences."
    )


# --------------------------------
# MAIN AI AGENT
# --------------------------------

def run_agent(message, history, candidate_skills):

    api_key = os.getenv("OPENAI_API_KEY")

    # Use local agent if no API key exists
    if not api_key:

        reply = local_agent(message, candidate_skills)

        history.append({
            "role": "user",
            "content": message
        })

        history.append({
            "role": "assistant",
            "content": reply
        })

        return reply, history

    try:

        client = OpenAI(api_key=api_key)

        messages = [
            {
                "role": "system",
                "content": (
                    "You are an AI Career Agent. "
                    "Help users find jobs and improve their careers. "
                    "Use search_jobs_tool for job searches. "
                    "Use recommend_jobs_tool for resume-based recommendations. "
                    "Never invent job listings. "
                    "Only claim to remember preferences when they are present "
                    "in the conversation history."
                )
            }
        ]

        messages.extend(history[-10:])

        messages.append({
            "role": "user",
            "content": message
        })

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        assistant_message = response.choices[0].message

        # Execute requested tools
        if assistant_message.tool_calls:

            messages.append(
                assistant_message.model_dump(exclude_none=True)
            )

            for tool_call in assistant_message.tool_calls:

                name = tool_call.function.name

                arguments = json.loads(
                    tool_call.function.arguments
                )

                result = execute_tool(
                    name,
                    arguments,
                    candidate_skills
                )

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })

            # Get final AI response
            final_response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=messages
            )

            reply = final_response.choices[0].message.content

        else:

            reply = assistant_message.content

        history.append({
            "role": "user",
            "content": message
        })

        history.append({
            "role": "assistant",
            "content": reply
        })

        return reply, history

    except Exception as error:

        reply = (
            "The AI service encountered an error: "
            + str(error)
            + ". Please check your API configuration."
        )

        return reply, history
