import os
import streamlit as st
from dotenv import load_dotenv
from pipeline import (
    run_agent_1_discover,
    run_agent_idea_evaluator,
    run_agent_2_strategy,
    run_agent_3_critic,
    run_agent_4_visual_and_launch,
    run_agent_5_execution_path
)

load_dotenv()

st.set_page_config(page_title="Brand Intelligence Engine",page_icon="📈",layout="wide")
st.title("Brand Intelligence Engine")
st.markdown("Turn a raw startup idea into a structured, launch-ready brand system and execution plan.")
st.markdown("---")

if "step" not in st.session_state:
    st.session_state.step = 1
if "agent1_data" not in st.session_state:
    st.session_state.agent1_data = None
if "eval_data" not in st.session_state:
    st.session_state.eval_data = None
if "strategy_data" not in st.session_state:
    st.session_state.strategy_data = None
if "critic_data" not in st.session_state:
    st.session_state.critic_data = None
if "launch_data" not in st.session_state:
    st.session_state.launch_data = None
if "execution_data" not in st.session_state:
    st.session_state.execution_data = None
if "user_idea" not in st.session_state:
    st.session_state.user_idea = ""
if "user_answers_str" not in st.session_state:
    st.session_state.user_answers_str = ""

if st.session_state.step == 1:
    st.subheader("Step 1: The Raw Idea (Discovery)")
    user_idea = st.text_area("Tell us about your business or startup idea:", height=150)
    if st.button("Start AI Interview"):
        if user_idea.strip():
            with st.spinner("Agent 1 is analyzing your idea..."):
                st.session_state.user_idea = user_idea
                st.session_state.agent1_data = run_agent_1_discover(user_idea)
                if "error" in st.session_state.agent1_data:
                    st.error(f"API Error: {st.session_state.agent1_data['error']}")
                else:
                    st.session_state.step = 2
                    st.rerun()
        else:
            st.warning("Please enter your startup idea.")

elif st.session_state.step == 2:
    st.subheader("Step 2: Deep Dive Interview")
    st.info("Answer these questions to build context.")
    with st.form("interview_form", enter_to_submit=False):
        answers = {}
        # Dynamic loop handles however many questions AI generates
        for key, val in st.session_state.agent1_data.items():
            if key.lower().startswith("question"):
                answers[key] = st.text_area(f"{val}", height=100)
        submitted = st.form_submit_button("Analyze Answers")
        if submitted:
            with st.spinner("Agent 1.5 is evaluating strengths and risks..."):
                answers_str = "\n".join([f"Q: {st.session_state.agent1_data[k]}\nA: {v}" for k, v in answers.items()])
                st.session_state.user_answers_str = answers_str
                st.session_state.eval_data = run_agent_idea_evaluator(st.session_state.user_idea, answers_str)
                st.session_state.step = 3
                st.rerun()

elif st.session_state.step == 3:
    st.subheader("Step 3: AI Reality Check (Positives & Risks)")
    col1, col2 = st.columns(2)
    with col1:
        st.success("Green Flags (Positives)")
        for p in st.session_state.eval_data.get("positives", []):
            st.markdown(f"- {p}")
    with col2:
        st.warning("Red Flags (Risks)")
        for n in st.session_state.eval_data.get("negatives", []):
            st.markdown(f"- {n}")
    st.markdown("---")
    if st.button("Proceed to Complete Brand Kit & Execution Plan"):
        with st.spinner("Generating strategy, names, visual direction, and execution path. This will take time please be patient...."):
            strategy = run_agent_2_strategy(st.session_state.user_idea, st.session_state.agent1_data, st.session_state.user_answers_str)
            st.session_state.strategy_data = strategy
            
            critic = run_agent_3_critic(strategy)
            st.session_state.critic_data = critic
            
            launch = run_agent_4_visual_and_launch(strategy)
            st.session_state.launch_data = launch
            
            execution = run_agent_5_execution_path(strategy)
            st.session_state.execution_data = execution
            
            st.session_state.step = 4
            st.rerun()

elif st.session_state.step == 4:
    st.subheader("Step 4: Final Brand System & Launch Kit")
    st.success("Complete brand intelligence pipeline executed successfully.")
    
    st.markdown("### Brand Positioning")
    cat = st.session_state.strategy_data.get('Category', 'N/A')
    vp = st.session_state.strategy_data.get('Value Proposition', 'N/A')
    st.markdown(f"**Category:** {cat}")
    st.markdown(f"**Value Proposition:** {vp}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Personality Traits:**")
        for t in st.session_state.strategy_data.get('Personality Traits', []):
            st.markdown(f"- {t}")
    with col2:
        st.markdown("**Traits to AVOID:**")
        for a in st.session_state.strategy_data.get('Traits to AVOID', []):
            st.markdown(f"- {a}")
            
    st.markdown("---")
    st.markdown("### Brand Names & Critic Review")
    for b in st.session_state.critic_data.get('brand_names', []):
        with st.expander(f"Name: **{b.get('name', 'N/A')}**", expanded=True):
            st.markdown(f"**Concept:** {b.get('concept_rationale', 'N/A')}")
            st.markdown(f"**Critic Verdict:** {b.get('critic_review', 'N/A')}")
            
    st.markdown("---")
    st.markdown("### Visual Direction & Launch Content")
    ld = st.session_state.launch_data
    st.markdown(f"**Typography Style:** {ld.get('typography', 'N/A')}")
    st.markdown(f"**Color Mood:** {ld.get('color_mood', 'N/A')}")
    st.markdown(f"**Imagery Style:** {ld.get('imagery_style', 'N/A')}")
    st.markdown(f"**Landing Page Headline:** {ld.get('landing_headline', 'N/A')}")
    st.markdown(f"**One-Line Pitch:** {ld.get('one_line_pitch', 'N/A')}")
    st.markdown(f"**Social Launch Post:** {ld.get('social_launch_post', 'N/A')}")
    
    st.markdown("---")
    st.markdown("### The Execution Path (How to Start Building)")
    ex = st.session_state.execution_data
    
    st.markdown("**Immediate Next Steps:**")
    # Using your exact requested Title Case keys with multiple fallbacks just in case
    next_steps = ex.get('Immediate Next Steps', ex.get('immediate_next_steps', []))
    if isinstance(next_steps, list):
        for step_item in next_steps:
            st.markdown(f"- {step_item}")
    else:
        st.markdown(f"- {next_steps}")
        
    mvp = ex.get('MVP Approach', ex.get('mvp_approach', 'N/A'))
    customers = ex.get('First Customers', ex.get('first_customers', 'N/A'))
    
    st.markdown(f"**MVP Approach:** {mvp}")
    st.markdown(f"**Acquiring First Customers:** {customers}")
    
    st.markdown("---")
    if st.button("Start New Project"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()