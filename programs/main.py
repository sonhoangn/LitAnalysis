import datetime
import json
import os
import PyPDF2
import requests
import time
import webbrowser
from pathlib import Path

import google.generativeai as genai
import pandas as pd

# Defining paths
PARENT_DIR = Path(__file__).parent
RESULT_DIR = PARENT_DIR / "results"
os.makedirs(RESULT_DIR, exist_ok=True)

# Defining current timestamp
def ct():
    return datetime.datetime.now()

# Extract text from pdf
def pdf_text_extraction(filepath):
    try:
        with open(filepath, "rb") as file:
            reader=PyPDF2.PdfReader(file)
            text=""
            for page  in reader.pages:
                text += page.extract_text()
            return text
    except FileNotFoundError:
        return f"{ct()} - Error: PDF file not found."
    except Exception as e:
        return f"{ct()} - Error extracting text: {e}"

# Set up instruction
def genai_config():
    s_instructions="""
    You are an expert researcher and educator, who is well versed in the field of circular economy, sustainable manufacturing and various digital learning and teaching methodologies, also known as e-learning tools. Your primary goal is to assess whether a research paper does indeed provided relevant data and information to help with the effort to design an e-learning platform for circular economy competencies that aims at the development of a tailored concept for the Berlin industrial SME sector.
    
    Instructions:
    
    1. Analyze Research Paper Content and determine if the provided paper could provide relevant and useful data for the aforementioned goals. If the Content of Research Paper does not show any relevance to the aforementioned goals, categorize the Relevance as N/A. 
    2. Explain the goal of the Research Paper based on its content in a concise manner.
    3. Thoroughly analyze the Research Paper Content and provide an accurate summary of the content including the goals, methodologies used, results, discussions and conclusions from the author(s).
    4. Provide suggestion on whether the Research Paper Content is reliable whose data could then be utilized to help with the aforementioned goals.
    5. Decide whether the Research Paper is a Qualitative or a Quantitative one based on its content.
    6. Focus on Key Areas of Interest to decide if the Research Paper is relevant enough for its data to be extracted and used for further analysis and consolidation.
    7. Based on the content decide whether the Research Paper belongs to any of most common types of research papers as listed below.
    8. Provide an APA Citation for the Research Paper following the style of the APA 7th Edition. 
    
    Key Areas of Interest:
    
    1. Circular Economy Concept.
    2. E-learning:
        - E-learning concepts.
        - E-learning platform and tools.
    3. Berlin Industrial SME Sector.
    4. Applications of E-learning within the context of Circular Economy.
    5. Others (Please specify, no more than 5 words).
    
    Common types of research papers:
    
    1. Analytical Research Paper.
    2. Argumentative Research Paper.
    3. Case Study.
    4. Comparative Research Paper.
    5. Experimental Research Paper.
    6. Literature Review.
    7. Review Paper.
    8. Survey Research Paper.
    
    Response format: (Strictly adhere to this format)
    
    - Relevance: N/A or Yes. If Relevance is N/A then the other sections in the response must also be N/A.
    - Relevance level: Low, Medium or High.
    - Key Areas of Interest: select from the list of key areas of interest.
    - Research goal: Goal.
    - Research category: Qualitative or Quantitative.
    - Research type: Select from the list of common types of research papers.
    - Research summary: Summary of the research (no more than 2 sentences).
    - Research methodology: Methodology.
    - Research Purpose: Theoretical or Applied.
    - Research discussion: key discussions (no more than 2 sentences).
    _ Research reliability: Low or High.
    - Reference: APA 7th Edition style.
    
    """

    api_key = input(f"{ct()} - Input API Key: ")
    if api_key:
        llm  = input(f"{ct()} - Choose LLM (gemini-1.5-flash, gemini-1.5-flash-8b, gemini-1.5-pro, gemini-2.0-flash, gemini-2.0-flash-lite-preview-02-05): ")
        if llm=="gemini-1.5-flash" or llm=="gemini-1.5-flash-8b" or llm=="gemini-1.5-pro" or llm=="gemini-2.0-flash" or llm=="gemini-2.0-flash-lite-preview-02-05":
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(
                model_name=llm,
                system_instruction=s_instructions
            )
            return model
        else:
            return f"{ct()} - Invalid LLM selection. Exiting..."
    else:
        return f"{ct()} - No API Key found. Exiting..."

# Define method to extract data from response
def response_data_extraction(data, model):

    prompt=f"Research Paper Content: {data}"

    response = model.generate_content(prompt)

    print(f"{ct()} - Response is provided. Analyzing and extracting relevant information...\n")

    # print(f"{ct()} - Response for paper no. {index} is provided. Analyzing and extracting relevant information...\n")

    # print(f"{ct()} - Response:"
    #       f"\n {response}")


    line0=[line for line in response.text.split("\n") if line.startswith("- Relevance: ")]
    if line0:
        relevance = line0[0].split(": ")[1].strip()
    else:
        relevance = "N/A"

    if relevance != "N/A":
        line1=[line for line in response.text.split("\n") if line.startswith("- Relevance level: ")]
        if line1:
            rel_level = line1[0].split(": ")[1].strip()
        else:
            rel_level = "N/A"

        line1=[line for line in response.text.split("\n") if line.startswith("- Research goal: ")]
        if line1:
            goal = line1[0].split(": ")[1].strip()
        else:
            goal = "N/A"

        line1=[line for line in response.text.split("\n") if line.startswith("- Key Areas of Interest: ")]
        if line1:
            area = line1[0].split(": ")[1].strip()
        else:
            area = "N/A"

        line1=[line for line in response.text.split("\n") if line.startswith("- Research category: ")]
        if line1:
            category = line1[0].split(": ")[1].strip()
        else:
            category = "N/A"

        line1 = [line for line in response.text.split("\n") if line.startswith("- Research type: ")]
        if line1:
            rtype = line1[0].split(": ")[1].strip()
        else:
            rtype = "N/A"

        line1 = [line for line in response.text.split("\n") if line.startswith("- Research summary: ")]
        if line1:
            summary = line1[0].split(": ")[1].strip()
        else:
            summary = "N/A"

        line1 = [line for line in response.text.split("\n") if line.startswith("- Research methodology: ")]
        if line1:
            methodology = line1[0].split(": ")[1].strip()
        else:
            methodology = "N/A"

        line1 = [line for line in response.text.split("\n") if line.startswith("- Research Purpose: ")]
        if line1:
            purpose = line1[0].split(": ")[1].strip()
        else:
            purpose = "N/A"

        line1 = [line for line in response.text.split("\n") if line.startswith("- Research discussion: ")]
        if line1:
            discussion = line1[0].split(": ")[1].strip()
        else:
            discussion = "N/A"

        line1 = [line for line in response.text.split("\n") if line.startswith("- Research reliability: ")]
        if line1:
            reliability = line1[0].split(": ")[1].strip()
        else:
            reliability = "N/A"

        line1 = [line for line in response.text.split("\n") if line.startswith("- Reference: ")]
        if line1:
            reference = line1[0].split(": ")[1].strip()
        else:
            reference = "N/A"

    else:
        rel_level = "N/A"
        area = "N/A"
        goal = "N/A"
        category = "N/A"
        rtype = "N/A"
        summary = "N/A"
        methodology = "N/A"
        purpose = "N/A"
        discussion = "N/A"
        reliability = "N/A"
        reference = "N/A"

    print(f"{ct()} - Relevance: {relevance}."
          f"\n - Relevance level: {rel_level}."
          f"\n - Key Areas of Interest: {area}."
          f"\n - Research Goal: {goal}."
          f"\n - Research Category: {category}."
          f"\n - Research Type: {rtype}."
          f"\n - Summary: {summary}."
          f"\n - Methodology: {methodology}."
          f"\n - Purpose: {purpose}."
          f"\n - Discussion: {discussion}."
          f"\n - Reliability: {reliability}."
          f"\n - Reference: {reference}")
    return relevance, rel_level, area, goal, category, rtype, summary, methodology, purpose, discussion, reliability, reference

# Process Loop
def process_loop(dir, model):
    if not os.path.isdir(dir):
        print(f"{ct()} - Incorrect file path.")
        return
    for filename in os.listdir(dir):
        if filename.endswith(".pdf"):
            filepath=os.path.join(dir,filename)
            print(f"{ct()} - Processing document: {filename}")
            content=pdf_text_extraction(filepath)
            if "Error:" in content:
                print(content)
                continue

            response_data_extraction(content, model)
            
    return

# Main function
def main():
    file_path=input(f"{ct()} - Input documents dir: ")
    if file_path:
        # content=pdf_text_extraction(file_path)
        model=genai_config()
        process_loop(file_path,model)
        # response_data_extraction(content,model)
    else:
        return f"{ct()} - File not found. Exiting..."

if __name__ == "__main__":
    main()
