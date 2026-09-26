import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def call_ai_agent(model_id: str, system_prompt: str, user_prompt: str) -> dict:
    try:
        response = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )
        raw_text = response.choices[0].message.content.strip()
        start = raw_text.find('{')
        end = raw_text.rfind('}') + 1
        if start != -1 and end != 0:
            return json.loads(raw_text[start:end])
        return {"error": "Invalid JSON response", "raw_output": raw_text}
    except Exception as e:
        return {"error": str(e)}

DEFAULT_MODEL = "nvidia/nemotron-3-ultra-550b-a55b:free"

def run_agent_1_discover(user_idea: str) -> dict:
    """Stage 1: Discover & Interview"""
    system_prompt = """You are an expert startup interviewer. Analyze the user's idea and ask maximum 5 critical missing context questions. Do not be constrained to 5 questions it can be more or less depending how well it satisfies the context.
    Return output in clean JSON with keys: 'Your Core Idea', 'Question 1', 'Question 2', 'Question 3' (and so on)."""
    return call_ai_agent(DEFAULT_MODEL, system_prompt, user_idea)

def run_agent_idea_evaluator(user_idea: str, user_answers_str: str) -> dict:
    """Stage 1.5: Evaluation & Positives/Negatives Analysis"""
    combined_context = f"Idea: {user_idea}\nAnswers: {user_answers_str}"
    system_prompt = """You are a startup advisor. Identify 2 strong Positives and 2 critical Negatives or risks based on the interview.
    Return EXACTLY this JSON structure:
    {"positives": ["Point 1", "Point 2"], "negatives": ["Risk 1", "Risk 2"]}"""
    return call_ai_agent(DEFAULT_MODEL, system_prompt, combined_context)

def run_agent_2_strategy(user_idea: str, questions: dict, answers_str: str) -> dict:
    """Stage 2 & 3: Position & Shape (Strategy & Personality)"""
    combined_context = f"Idea: {user_idea}\nQuestions: {json.dumps(questions)}\nAnswers: {answers_str}"
    system_prompt = """You are an expert Brand Strategist. Define category, value proposition, personality traits, and traits to avoid.
    Return EXACTLY this JSON structure:
    {"Category": "Market category", "Value Proposition": "Value prop", "Personality Traits": ["Trait 1", "Trait 2"], "Traits to AVOID": ["Avoid 1"]}"""
    return call_ai_agent(DEFAULT_MODEL, system_prompt, combined_context)

def run_agent_3_critic(strategy_dict: dict) -> dict:
    """Stage 5: Challenge (Naming & Cliche Check)"""
    system_prompt = """You are a Ruthless Brand Critic and Naming Expert. Generate 5 distinctive brand names and a 1-sentence critic review for each. Avoid generic cliches.
    Return EXACTLY this JSON structure:
    {"brand_names": [{"name": "Name 1", "concept_rationale": "Rationale", "critic_review": "Review"}]}"""
    return call_ai_agent(DEFAULT_MODEL, system_prompt, json.dumps(strategy_dict))

def run_agent_4_visual_and_launch(strategy_dict: dict) -> dict:
    """Stage 4 & 6: Visualize & Deliver (Design Brief & Launch Kit)"""
    system_prompt = """You are a Creative Director and Growth Marketer. Create visual direction (typography, color mood, imagery style) and launch assets (landing page headline, one-line pitch, social launch post).
    Return EXACTLY this JSON structure:
    {"typography": "Font style", "color_mood": "Color mood description", "imagery_style": "Image style", "landing_headline": "Headline", "one_line_pitch": "Pitch", "social_launch_post": "Post content"}"""
    return call_ai_agent(DEFAULT_MODEL, system_prompt, json.dumps(strategy_dict))

def run_agent_5_execution_path(strategy_dict: dict) -> dict:
    """Stage 7: Execution (How to start building)"""
    system_prompt = """You are a seasoned Startup Operator. Based on the brand strategy, give a pragmatic, step-by-step execution path on how to actually start building this product or business.
    Return EXACTLY this JSON structure without any underscores in keys:
    {"Immediate Next Steps": ["Step 1", "Step 2", "Step 3"], "MVP Approach": "How to build the MVP minimally", "First Customers": "How to get the first 10 users"}"""
    return call_ai_agent(DEFAULT_MODEL, system_prompt, json.dumps(strategy_dict))