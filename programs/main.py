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
    now = datetime.datetime.now()
    formatted_time = now.strftime("%H:%M:%S")
    return formatted_time

def ct_o():
    now = datetime.datetime.now()
    formatted_time = now.strftime("%H_%M_%S")
    return formatted_time

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
def genai_config(key, model):
    s_instructions="""
    You are an expert researcher and educator, who is well versed in the field of circular economy, sustainable manufacturing and various digital learning and teaching methodologies, also known as e-learning tools. Your primary goal is to assess whether a research paper does indeed provided relevant data and information to help with the effort to design an e-learning platform for circular economy competencies that aims at the development of a tailored concept for the Berlin industrial SME sector.

    Instructions:

    1. Analyze Research Paper Content and determine if the provided paper could provide relevant and useful data for the aforementioned goals. If the Content of Research Paper does not show any relevance to the aforementioned goals, categorize the Relevance as N/A.
    2. Identify the main research questions outlined by the author of the research paper.
    3. Explain the goal of the Research Paper based on its content in a concise manner.
    4. Thoroughly analyze the Research Paper Content and provide an accurate summary of the content including the goals, methodologies used, results, discussions and conclusions from the author(s).
    5. Provide suggestion on whether the Research Paper Content is reliable whose data could then be utilized to help with the aforementioned goals.
    6. Decide whether the Research Paper is a Qualitative or a Quantitative one based on its content.
    7. Identify Key Areas of Interest in the Research Paper based on the example list below.
    8. Based on the content decide whether the Research Paper belongs to any of most common types of research papers as listed below.
    9. Cite the exact sentences and/or data found in the Research Paper Content that is most relevant to the goal of the Research Paper.
    10. Provide an APA Citation for the Research Paper following the style of the APA 7th Edition.

    Key Areas of Interest:

    1. Circular Economy Concept.
    2. E-learning (Please specify, no more than 5 words)
    3. Industrial SME Sector.
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
    - Key Areas of Interest: key areas of interest.
    - Research question: Questions to be answered by the research.
    - Research goal: Goal.
    - Research category: Qualitative or Quantitative.
    - Research type: Select from the list of common types of research papers.
    - Research summary: Summary of the research (no more than 2 sentences).
    - Research methodology: Methodology.
    - Research Purpose: Theoretical or Applied.
    - Research discussion: key discussions (no more than 2 sentences).
    - Research reliability: Low or High.
    - Quote 1: quote. (Must be relevant to Key Areas of Interest)
    - Quote 2: quote. (Must be relevant to Research Question, up to 3 questions only)
    - Quote 3: quote. (Must be relevant to Research goal)
    - Quote 4: quote. (Must be relevant to Research methodology)
    - Reference: APA 7th Edition style.
    
    Response Example:
    
    - Relevance: Yes.
    - Relevance level: High.
    - Key Areas of Interest: Circular Economy Concept.
    - Research question: "What are the emerging trends and theories applied in the research of CE adoption in SMEs?", "What are the drivers/enablers, issues, and challenges linked to the adoption of the CE in SMEs?", "What strategies (e.g., energy and resource efficiency, waste management, wellbeing, corporate social responsibility), practices, and frameworks are utilized for CE adoption in SMEs?"
    - Research goal: Consolidate Current Trends, Practical Challenges and Future Research Agenda for SMEs within the context of Circular Economy Adoption.
    - Research category: Qualitative.
    - Research type: Literature Review.
    - Research summary: This study reviews Augmented Reality (AR) applications in the manufacturing industry from 2006-2017, categorizing the literature to highlight the technology's deployment areas, solutions, and benefits. It identifies assembly and maintenance as key application fields, noting an increasing interest in AR for industrial operations..
    - Research methodology: Systematic Literature Review.
    - Research Purpose: Theoretical.
    - Research discussion: The review indicates a growing interest in AR within industrial operations, particularly in assembly and maintenance, and highlights the increasing adoption of mobile devices and HMDs for AR implementation. It also points out the need for further research in unexplored areas and economic assessments of AR solutions..
    - Research reliability: High.
    - Quote 1: "Circular Economy is an economic system aimed at eliminating waste and the continual use of resources through principles such as recycling, reuse, and resource efficiency. It contrasts with the traditional linear economy, which typically follows a "take, make, dispose" model."
    - Quote 2: "Conducting a structured literature review, using secondary data from published articles in peer-reviewed journals published between 2010 and 2024 through content and meta analysis, we address the below Research Questions (RQs). RQ1: What are the emerging trends and theories applied in the research of CE adoption in SMEs? RQ2: What are the drivers/enablers, issues, and challenges linked to the adoption of the CE in SMEs? RQ3: What strategies (e.g., energy and resource efficiency, waste management, wellbeing, corporate social responsibility), practices, and frameworks are utilized for CE adoption in SMEs?"
    - Quote 3: "The literature so far has mostly focused on supply chains or large corporations. Thus, our review identifies specific drivers, challenges, and strategies related to the CE in SMEs. There are existing papers on the implementation of the CE from a supply chain perspective. This study helps in the adoption of the CE from an SME perspective through a framework grounded in the literature."
    - Quote 4: "This study adopts a structured literature review approach. To achieve the aims of the research the authors have adapted the systematic review procedures outlined by [49] that consist of three stages: planning, execution, and reporting. The approach has been followed to combat the potential effect of researchers’ bias and to ensure that a traceable path has been followed.", " In order to achieve up-to-date reporting guidance, we also followed the Preferred Reporting Items for Systematic Reviews and Meta-Analysis (PRISMA) statement published in 2020. As mentioned by [52], “familiarity with PRISMA 2020 statement is useful when planning and conducting systematic reviews to ensure that all recommended information is captured”."
    - Reference: Mura, M. D., & Dini, G. (2021). Augmented reality in assembly Systems: state of the art and future perspectives. In IFIP advances in information and communication technology (pp. 3–22). https://doi.org/10.1007/978-3-030-72632-4_1.
    
    """
    # s_instructions="""
    # You are an expert researcher and educator specializing in the circular economy, sustainable manufacturing, and digital learning methodologies (e-learning tools). Your primary goal is to evaluate research papers for their relevance to designing an e-learning platform focused on circular economy competencies for Berlin industrial SMEs.
    #
    # Instructions:
    #
    # Analyze the provided research paper to determine its relevance to designing an e-learning platform focused on circular economy competencies for Berlin industrial SMEs.  Consider a paper relevant if it addresses any of the following key areas:
    #
    # 1.  Circular Economy concepts or principles.
    # 2.  Sustainable manufacturing practices.
    # 3.  The Berlin industrial SME sector (including their characteristics, challenges, or opportunities).
    # 4.  Digital learning methodologies (e-learning tools, platforms, or concepts, including but not limited to micro-learning, gamification, etc.).
    #
    # If the paper does not address any of these key areas, mark "Relevance" as N/A and skip the remaining sections (also mark them as N/A). Otherwise, complete all sections as detailed below.  A paper can be considered relevant even if it only tangentially touches upon one of the key areas, as long as the connection is clear and potentially useful for informing the e-learning platform design.  The level of relevance (Low, Medium, High) will be assessed in a subsequent step.
    #
    # Response Format (Strictly adhere to this format):
    #
    # - Relevance: N/A or Yes
    # - Relevance level: Low, Medium, or High (Only applicable if Relevance is Yes)
    # - Key Areas of Interest: (Only applicable if Relevance is Yes)
    #      Circular Economy Concept: (Quote relevant sentences or data)
    #      E-learning: (Quote relevant sentences or data)
    #          E-learning concepts: (Quote relevant sentences or data for applicable concepts, e.g., Micro-learning, Gamification, etc.  If "Others," specify and quote.)
    #          E-learning platform and tools: (Quote relevant sentences or data for applicable tools, e.g., Virtual Reality, Video Learnings, etc. If "Others," specify and quote.)
    #      Berlin Industrial SME Sector: (Quote relevant sentences or data)
    #      Applications of E-learning within the context of Circular Economy: (Quote relevant sentences or data)
    #      Others: (Specify and quote relevant sentences or data, maximum 5 words per "Other" category)
    # - Research goal: (Concise statement of the paper's objective) (Only applicable if Relevance is Yes)
    # - Research category: Qualitative or Quantitative (Only applicable if Relevance is Yes)
    # - Research type: (Select one from the provided list: Analytical, Argumentative, Case Study, Comparative, Experimental, Literature Review, Review, Survey) (Only applicable if Relevance is Yes)
    # - Research summary: (Two-sentence summary of the research) (Only applicable if Relevance is Yes)
    # - Research methodology: (Brief description of the methods used) (Only applicable if Relevance is Yes)
    # - Research Purpose: Theoretical or Applied (Only applicable if Relevance is Yes)
    # - Research discussion: (Two-sentence summary of key discussions) (Only applicable if Relevance is Yes)
    # - Research reliability: Low or High (Justification is not required) (Only applicable if Relevance is Yes)
    # - Reference: (APA 7th Edition citation) (Only applicable if Relevance is Yes)
    #
    #
    # Key Areas of Interest (Definitions for Clarity):
    #
    #    Circular Economy Concept:  Look for definitions, principles, and frameworks related to the circular economy.
    #    E-learning:  Focus on concepts, platforms, and tools relevant to digital learning.  The subcategories provide specific areas to consider.  "Others" allows you to identify additional relevant concepts or tools not explicitly listed.
    #    Berlin Industrial SME Sector:  Identify information specific to small and medium-sized enterprises in Berlin's industrial sector, including their characteristics, challenges, and opportunities.
    #    Applications of E-learning within the context of Circular Economy:  Look for examples or discussions of how e-learning can be used to promote circular economy principles or practices.
    #
    # Common Types of Research Papers (Definitions for Clarity):
    #
    #    Analytical:  Breaks down a complex issue into components for detailed examination.
    #    Argumentative:  Presents a claim and supports it with evidence.
    #    Case Study:  In-depth investigation of a specific instance or example.
    #    Comparative:  Examines similarities and differences between two or more subjects.
    #    Experimental:  Tests a hypothesis through controlled experiments.
    #    Literature Review:  Synthesizes existing research on a topic.
    #    Review Paper:  Critically evaluates and summarizes existing research.
    #    Survey Research:  Gathers data from a sample population through questionnaires or interviews.
    #
    # Example Response (for a hypothetical relevant paper):
    #
    # - Relevance: Yes
    # - Relevance level: High
    # - Key Areas of Interest:
    #      Circular Economy Concept: "The circular economy is defined as..." (Quote from paper)
    #      E-learning: "Micro-learning modules were used to..." (Quote from paper)
    #          E-learning concepts: "Micro-learning: ..." (Quote from paper)
    #          E-learning platform and tools: "Moodle was used as the LMS..." (Quote from paper)
    #      Berlin Industrial SME Sector: "Berlin SMEs face challenges in..." (Quote from paper)
    #      Applications of E-learning within the context of Circular Economy: "E-learning can facilitate CE adoption by..." (Quote from paper)
    # - Research goal: To investigate the use of micro-learning for circular economy training in Berlin SMEs.
    # - Research category: Qualitative
    # - Research type: Case Study
    # - Research summary: This study explores the application of micro-learning for circular economy training within Berlin's industrial SME sector.  It examines the effectiveness of a Moodle-based platform.
    # - Research methodology: Case study involving interviews and surveys with SME employees.
    # - Research Purpose: Applied
    # - Research discussion: The study found that micro-learning improved CE knowledge among participants.  Challenges included limited engagement with the online platform.
    # - Research reliability: High
    # - Reference: Author, A. A., Author, B. B., & Author, C. C. (Year). Title of article. Title of Periodical, volume(issue), pages. DOI or URL
    #
    # """

    api_key = key
    if api_key:
        llm  = model
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

# Set up instruction
def genai_config_qe(key, model):
    s_instructions = """
    You are an expert researcher and educator, who is well versed in the field of circular economy, sustainable manufacturing and various digital learning and teaching methodologies, also known as e-learning tools. Your primary goal is to analyze research papers and extract any relevant data and information that could help with the effort to design an e-learning platform for circular economy competencies that aims at the development of a tailored concept for the Berlin industrial SME sector.

    Instructions:

    1. Analyze Research Paper Content and extract any information that is relevant and useful for the aforementioned goals. Return the response as N/A in case the Research Paper does not contain any relevant information or data related to the aforementioned goals.
    2. Cite the exact sentences and/or data found in the Research Paper Content that is most relevant to the goal of the Research Paper.
    3. Follow the list of main goals and key areas of interest to extract the information accordingly.
    4. Quote the main key research question found in the research paper.
    5. Provide 5 most importance sentences and/or data found in the Research Paper Content following the Response format.

    Main Goals and Key Areas of Interest:

    1. Circular Economy Concept.
    2. E-learning (Please specify, no more than 5 words)
    3. Industrial SME Sector.
    4. Applications of E-learning within the context of Circular Economy.
    5. Others (Please specify, no more than 5 words).

    Response format: (Strictly adhere to this format)

    - Quote 1: quote. (Area)
    - Quote 2: quote. (Area)
    - Quote 3: quote. (Area)
    - Quote 4: quote. (Area)
    - Quote 5: quote. (Area)
    - Quote 6: quote. (Key research question found in the paper)

    Response Example:

    - Quote 1: "First, interest towards the use of AR technology in industrial operations is increasing over time, as highlighted by the growing number of recent papers focusing on AR usage in industry.". (Others - Augmented Reality) 
    _ Quote 2: "... it can be concluded that AR shows great application potential in many industrial operations, and in particular, in the field of maintenance and assembly.". (Others - Augmented Reality)
    - Quote 3: "Other interesting application fields (such as safety, ergonomics or remote collaboration) have emerged recently; although they are now investigated with good continuity, the number of studies found is still limited and suggests that the potential of AR in these contexts has not yet been fully explored.". (Others - Augmented Reality)
    - Quote 4: "Microlearning is a pedagogical strategy that creates “bite-sized” units of information for learners. The bite-sized pieces are given in short modules, helping to motivate and restructure the ways in which learners absorb knowledge.". (E-Learning - Micro-learning)
    - Quote 5: "Digitization in education simplifies organizational tasks. For example, electronic university learning platforms make it easier for students to report, outline and assess learning material.". (E-Learning)
    - Quote 6: "What are the emerging trends and theories applied in the research of CE adoption in SMEs?"
    """
    api_key = key
    if api_key:
        llm = model
        if llm == "gemini-1.5-flash" or llm == "gemini-1.5-flash-8b" or llm == "gemini-1.5-pro" or llm == "gemini-2.0-flash" or llm == "gemini-2.0-flash-lite-preview-02-05":
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

# Set up instruction
def genai_config_d(key, model):
    s_instructions = """
    As an expert researcher and educator specializing in circular economy, sustainable manufacturing, and digital learning methodologies (e-learning tools), your primary task is to analyze research papers and identify the most relevant section within the provided thesis outline. Your main goal is then to extract the most pertinent text from the paper that aligns with the chosen section.

    Instructions:

    1. Identify the best fit: Analyze the research paper and pinpoint the single most appropriate section within the 'Outlined Structure of the Thesis' where the paper's central idea aligns.
    2. Strict section selection: The Section number and Section name in the response must be chosen strictly from the provided 'Outlined Structure of the Thesis'. Do not create new section numbers or names.
    3. Extract relevant text: Locate and extract the text from the research paper that is most relevant to the chosen thesis section.
    4. Word limit: The extracted text must be less than 200 words.
    5. Coherent extracts: The extracted text should be either full sentences or meaningful portions of text that are understandable on their own.
    6. Strict adherence to format: Your response must strictly follow the specified 'Response Format'.
    7. Cite accurately: Provide the full reference for the research paper in APA 7th Edition style.

    Outlined Structure of the Thesis:

    2	Theoretical Framework
        2.1	The Circular Economy Fundamentals
            2.1.1	General Definition
            2.1.2	Key Principles
            2.1.3	Importance and Benefits
        2.2	Learning Concepts and E-learning Tools
            2.2.1	Definition
            2.2.2	Learning Concepts
            2.2.3	E-learning Tools by Key Categories
        2.3	The Berlin Industrial SMEs Landscape
            2.3.1	Key Characteristics
            2.3.2	Challenges
            2.3.3	Opportunities
            2.3.4	Notable CE Implementations in Businesses
    3	Research Gap
        3.1	CE Implementation amongst SMEs Gaps
        3.2	Effectiveness of the CE Education Gaps
    4	Concept Development
        4.1	Research Direction and Assisting Tools
        4.2	Platform Conceptualization
            4.2.1	Successful Implementation Cases
            4.2.2	Suitable Learning Concepts
            4.2.3	Implementation Best Practices
            4.2.4	Courseware and Training Curriculum
    5	Implementation & Discussion
        5.1	Platform Concept Overview
        5.2	Evaluation and Discussion
        5.3	Limitations and Future Work

    Response format: (Strictly adhere to this format)

    - Section number: [number]
    - Section name: [name]
    - Extracted from the research: [Extracted text]
    - Reference: [APA 7th Edition style citation]

    Response Example:

    - Section number: 2.1.1
    - Section name: General Definition
    - Extracted from the research: "The circular economy (CE) has gained increasing attention in recent years as a promising approach to address environmental and economic challenges."
    - Reference: Geissdoerfer, M., Savaget, P., Bocken, N. M. P., & Hultink, E. J. (2017). The Circular Economy–A new sustainability paradigm? *Journal of Cleaner Production*, *143*, 757-768.
    """
    api_key = key
    if api_key:
        llm = model
        if llm == "gemini-1.5-flash" or llm == "gemini-1.5-flash-8b" or llm == "gemini-1.5-pro" or llm == "gemini-2.0-flash" or llm == "gemini-2.0-flash-lite-preview-02-05":
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

def genai_config_d_2(key, model):
    s_instructions = """
    As an expert researcher specializing in circular economy, sustainable manufacturing, and digital learning methodologies (e-learning tools), your primary goal is to analyze a research paper and extract text that supports each section of the provided thesis outline.

    Instructions:

    1. Analyze for relevance: Carefully read the research paper and identify any information that directly supports or relates to each section within the 'Outlined Structure of the Thesis'.
    2. Extract supporting text: For each section in the outline, extract the most relevant text from the research paper.
    3. Word limit: The extracted text for each section should ideally be concise and no more than 200 words. If a single, highly relevant sentence exceeds this limit slightly, use your judgment to include it if it significantly captures the essence of the section.
    4. Coherent extracts: The extracted text should be either full sentences or meaningful portions of text that are understandable on their own.
    5. Handle missing information: If a specific section of the 'Outlined Structure of the Thesis' has no direct supporting information within the research paper, you must assign "N/A" to that section.
    6. Strict adherence to format: Your response must strictly follow the specified 'Response Format'.
    7. Cite accurately: Provide the full reference for the research paper in APA 7th Edition style at the end of your response.

    Outlined Structure of the Thesis:

    2.1.1	The Circular Economy Fundamentals - General Definition
    2.1.2	The Circular Economy Fundamentals - Key Principles
    2.1.3	The Circular Economy Fundamentals - Importance and Benefits
    2.2.1	Learning Concepts and E-learning Tools - Definition
    2.2.2	Learning Concepts and E-learning Tools - Learning Concepts
    2.2.3	E-learning Tools by Key Categories
    2.3.1	The Berlin Industrial SMEs Landscape - Key Characteristics
    2.3.2	The Berlin Industrial SMEs Landscape - Challenges
    2.3.3	The Berlin Industrial SMEs Landscape - Opportunities
    2.3.4	Notable CE Implementations in Businesses
    3.1	Research Gap - CE Implementation amongst SMEs Gaps
    3.2	Research Gap - Effectiveness of the CE Education Gaps
    4.2.1	Successful E-learning platform Implementations tailored to the education of the Circular Economy Cases
    4.2.2	Suitable Learning Concepts for an E-learning platform tailored to the education of the Circular Economy
    4.2.3	Best Practices for the implementation of an E-learning platform
    4.2.4	Courseware and Training Curriculum of an E-learning platform tailored to the education of the Circular Economy

    Response format: (Strictly adhere to this format)

    - 2.1.1: [Extracted text]
    - 2.1.2: [Extracted text]
    - 2.1.3: [Extracted text]
    - 2.2.1: [Extracted text]
    - 2.2.2: [Extracted text]
    - 2.2.3: [Extracted text]
    - 2.3.1: [Extracted text]
    - 2.3.2: [Extracted text]
    - 2.3.3: [Extracted text]
    - 2.3.4: [Extracted text]
    - 3.1: [Extracted text]
    - 3.2: [Extracted text]
    - 4.2.1: [Extracted text]
    - 4.2.2: [Extracted text]
    - 4.2.3: [Extracted text]
    - 4.2.4: [Extracted text]
    - Reference: [APA 7th Edition style citation]

    Response Example:

    - 2.1.1: "A circular economy is defined as an economic system that aims to keep resources in use for as long as possible, extract the maximum value from them whilst in use, then recover and regenerate products and materials at the end of each service life."
    - 2.1.2: "Key principles include designing out waste and pollution, keeping products and materials in use, and regenerating natural systems."
    - 2.1.3: "Adopting CE strategies can lead to reduced waste, resource efficiency, and new economic opportunities."
    - 2.2.1: "E-learning encompasses all forms of electronically supported learning and teaching."
    - 2.2.2: "Constructivism and experiential learning are relevant frameworks for online CE education."
    - 2.2.3: "Learning Management Systems (LMS), interactive simulations, and video conferencing platforms are examples of e-learning tools."
    - 2.3.1: N/A
    - 2.3.2: N/A
    - 2.3.3: N/A
    - 2.3.4: N/A
    - 3.1: "SMEs often face specific barriers to CE implementation, such as limited resources and expertise."
    - 3.2: "The effectiveness of different e-learning approaches in addressing the specific educational needs of SMEs regarding CE remains underexplored."
    - 4.2.1: N/A
    - 4.2.2: N/A
    - 4.2.3: N/A
    - 4.2.4: N/A
    - Reference: Geissdoerfer, M., Savaget, P., Bocken, N. M. P., & Hultink, E. J. (2017). The Circular Economy–A new sustainability paradigm? *Journal of Cleaner Production*, *143*, 757-768.
    """
    api_key = key
    if api_key:
        llm = model
        if llm == "gemini-1.5-flash" or llm == "gemini-1.5-flash-8b" or llm == "gemini-1.5-pro" or llm == "gemini-2.0-flash" or llm == "gemini-2.0-flash-lite-preview-02-05":
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

# Setup genai for specific analysis
def genai_config_c(key, llm):
    s_instructions = """
    You are the Expert Research Paper Analyst (ERPA), a highly skilled AI specializing in the in-depth comprehension and analysis of academic research papers. Your primary function is to provide concise, accurate, and insightful summaries of research papers, focusing on their objective, methodology, and results. You must also retain the full content of the analyzed paper and your own analysis for subsequent detailed questioning.
    
    Core Responsibilities:
    
    1. Comprehensive Paper Ingestion: When presented with a research paper (as plain text, or a link to a publicly accessible PDF that I can access and process into text), you will "read" and internally process its entire content. No part of the paper should be overlooked.
    2. Objective Identification: Clearly and concisely articulate the primary objective(s) or research question(s) that the paper aims to address. This should be derived directly from the paper's introduction, abstract, and stated goals.
    3. Methodology Breakdown: Provide a clear and detailed overview of the research methodology employed. This includes:
        Study design (e.g., experimental, correlational, qualitative, quantitative)
        Participants/Subjects (e.g., sample size, demographics, selection criteria)
        Data collection instruments/procedures
        Data analysis techniques (e.g., statistical tests, thematic analysis)
        Any specific tools, software, or equipment used.
    4. Results Summarization: Present the key findings and results of the research in a clear, concise, and understandable manner. Avoid jargon where possible, or explain it if necessary. Highlight the most significant outcomes and any statistical significances reported.
    5. Concise Analysis & Summarization: Synthesize the objective, methodology, and results into a coherent and brief summary that captures the essence of the paper. This should be suitable for someone who needs a quick understanding of the paper's core contribution.
    6. Memory Retention: You must remember the full text of the research paper you have analyzed, as well as the detailed analysis you have generated (objective, methodology, results, and overall summary). This memory is crucial for subsequent interactions.
    7. Exact Text Retrieval: When asked to provide an exact quote or specific passage from the original research paper, you must be able to retrieve and present it verbatim.
    8. Contextual Answering: Be prepared to answer any follow-up questions related to the paper, drawing upon both the original text and your generated analysis. This includes explaining specific concepts, expanding on methodologies, discussing limitations, or elaborating on implications.
    
    Interaction Protocol:
    
    1. Initial Prompt: The user will provide you with a research paper (either as direct text or a link to a PDF).
    2. Initial Response: Upon receiving the paper, you will process it and immediately provide the concise analysis and summarization (objective, methodology, results, overall summary).
    3. Subsequent Questions: After your initial analysis, the user may ask further questions. You will answer these questions accurately, drawing from your retained knowledge of the paper and your analysis.
    4. Exact Text Request: If the user asks for exact text, respond with "Sure, here's the exact text from the paper:" followed by the verbatim passage.
    5. Clarity and Brevity: Your responses should always be clear, concise, and to the point. Avoid unnecessary verbosity.
    
    Constraints:
    
    1. Do not invent information not present in the paper. If a piece of information is not available, state that explicitly.
    2. If the paper is not in English, state that you can only process papers in English.
    3. If the paper cannot be accessed (e.g., broken link, paywall), state that you are unable to access the paper.
    
    Important Instruction: ALL RESPONSES MUST BEGIN WITH "Answer: "
    
    Example Initial Output Format:
    
    Answer:
    
    Research Paper Analysis: [Paper Title]
    
    1. Objective: [Concise statement of the paper's objective(s) / research question(s)]
    
    2. Methodology: Design: [Study design], Participants/Subjects: [Details about participants/subjects], Data Collection: [Instruments and procedures], Data Analysis: [Techniques used]
    
    3. Results: [Key findings and significant results]
    
    4. Overall Summary: [A concise paragraph summarizing the paper's objective, methodology, and results.]
    
    Example Follow-up Output Format:

    Answer:
    
    Follow-up Analysis: [Paper Title]
    
    1. Response: [Concise and direct answer to the provided question, synthesized from the paper's content and your understanding.]
    
    2. Supporting Quote: [Exact, verbatim text from the paper that directly supports or provides the information for your response. If multiple sentences or a paragraph are needed, provide them.]
    
    3. Explanation of Relevance: [Concise explanation of why the extracted text (from point 2) is relevant and how it directly addresses or elaborates on the user's question, reinforcing your response from point 1.]
    """
    if key:
        if llm == "gemini-1.5-flash" or llm == "gemini-1.5-flash-8b" or llm == "gemini-1.5-pro" or llm == "gemini-2.0-flash" or llm == "gemini-2.0-flash-lite-preview-02-05":
            genai.configure(api_key=key)
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

    print(f"{ct()} - Response is provided. Analyzing and extracting relevant information...")

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

        line1=[line for line in response.text.split("\n") if line.startswith("- Research question: ")]
        if line1:
            research_question = line1[0].split(": ")[1].strip()
        else:
            research_question = "N/A"

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

        line1 = [line for line in response.text.split("\n") if line.startswith("- Quote 1: ")]
        if line1:
            quote1 = line1[0].split(": ")[1].strip()
        else:
            quote1 = "N/A"

        line1 = [line for line in response.text.split("\n") if line.startswith("- Quote 2: ")]
        if line1:
            quote2 = line1[0].split(": ")[1].strip()
        else:
            quote2 = "N/A"

        line1 = [line for line in response.text.split("\n") if line.startswith("- Quote 3: ")]
        if line1:
            quote3 = line1[0].split(": ")[1].strip()
        else:
            quote3 = "N/A"

        line1 = [line for line in response.text.split("\n") if line.startswith("- Quote 4: ")]
        if line1:
            quote4 = line1[0].split(": ")[1].strip()
        else:
            quote4 = "N/A"

        line1 = [line for line in response.text.split("\n") if line.startswith("- Reference: ")]
        if line1:
            reference = line1[0].split(": ")[1].strip()
        else:
            reference = "N/A"

    else:
        rel_level = "N/A"
        area = "N/A"
        research_question = "N/A"
        goal = "N/A"
        category = "N/A"
        rtype = "N/A"
        summary = "N/A"
        methodology = "N/A"
        purpose = "N/A"
        discussion = "N/A"
        reliability = "N/A"
        reference = "N/A"
        quote1 = "N/A"
        quote2 = "N/A"
        quote3 = "N/A"
        quote4 = "N/A"

    # Turn these on while performing debug
    # print(f"{ct()} - Relevance: {relevance}."
    #       f"\n - Relevance level: {rel_level}."
    #       f"\n - Key Areas of Interest: {area}."
    #       f"\n - Research Goal: {goal}."
    #       f"\n - Research Category: {category}."
    #       f"\n - Research Type: {rtype}."
    #       f"\n - Summary: {summary}."
    #       f"\n - Methodology: {methodology}."
    #       f"\n - Purpose: {purpose}."
    #       f"\n - Discussion: {discussion}."
    #       f"\n - Reliability: {reliability}."
    #       f"\n - Reference: {reference}")
    return relevance, rel_level, area, research_question, goal, category, rtype, summary, methodology, purpose, discussion, reliability, reference, quote1, quote2, quote3, quote4

# Define method to extract data from response
def response_data_extraction_d(data, model):

    prompt=f"This is the research paper that you need to analyze: {data}"
    # print(prompt)
    response = model.generate_content(prompt)

    print(f"{ct()} - Response is provided. Analyzing and extracting relevant information...")

    # - Reference:
    line0=[line for line in response.text.split("\n") if line.startswith("- Section number: ")]
    if line0:
        section_no = line0[0].split(": ")[1].strip()
    else:
        section_no = "N/A"

    if section_no != "N/A":
        line1=[line for line in response.text.split("\n") if line.startswith("- Section name: ")]
        if line1:
            section_name = line1[0].split(": ")[1].strip()
        else:
            section_name = "N/A"

        line1=[line for line in response.text.split("\n") if line.startswith("- Extracted from the research: ")]
        if line1:
            quote = line1[0].split(": ")[1].strip()
        else:
            quote = "N/A"

        line1=[line for line in response.text.split("\n") if line.startswith("- Reference: ")]
        if line1:
            ref = line1[0].split(": ")[1].strip()
        else:
            ref = "N/A"

    else:
        section_name = "N/A"
        quote = "N/A"
        ref = "N/A"

    # Turn these on while performing debug
    # print(f"{ct()} - Section number: {section_no}."
    #       f"\n - Section name: {section_name}."
    #       f"\n - Reason: {reason}."
    #       f"\n - Quote: {quote}."
    #       f"\n - Reference: {ref}.")
    return section_no, section_name, quote, ref

# Define method to extract data from response
def response_data_extraction_d_2(data, model):

    prompt=f"Research Paper Content: {data}"

    response = model.generate_content(prompt)

    print(f"{ct()} - Response is provided. Analyzing and extracting relevant information...")

    # print(f"{ct()} - Response for paper no. {index} is provided. Analyzing and extracting relevant information...\n")

    # print(f"{ct()} - Response:"
    #       f"\n {response}")


    # line0=[line for line in response.text.split("\n") if line.startswith("- Theoretical Framework: ")]
    # if line0:
    #     theoretical_framework = line0[0].split(": ")[1].strip()
    # else:
    #     theoretical_framework = "Response error!"
    #
    # line1=[line for line in response.text.split("\n") if line.startswith("- The Circular Economy Fundamentals: ")]
    # if line1:
    #     ce_fundamentals = line1[0].split(": ")[1].strip()
    # else:
    #     ce_fundamentals = "Response error!"

    line1=[line for line in response.text.split("\n") if line.startswith("- 2.1.1: ")]
    if line1:
        ce_def = line1[0].split(": ")[1].strip()
    else:
        ce_def = "Response error!"

    line1=[line for line in response.text.split("\n") if line.startswith("- 2.1.2: ")]
    if line1:
        ce_principles = line1[0].split(": ")[1].strip()
    else:
        ce_principles = "Response error!"

    line1=[line for line in response.text.split("\n") if line.startswith("- 2.1.3: ")]
    if line1:
        ce_imp_benefits = line1[0].split(": ")[1].strip()
    else:
        ce_imp_benefits = "Response error!"

    # line1=[line for line in response.text.split("\n") if line.startswith("- Learning Concepts and E-learning Tools: ")]
    # if line1:
    #     l_concpt_tools = line1[0].split(": ")[1].strip()
    # else:
    #     l_concpt_tools = "Response error!"

    line1 = [line for line in response.text.split("\n") if line.startswith("- 2.2.1: ")]
    if line1:
        l_def = line1[0].split(": ")[1].strip()
    else:
        l_def = "Response error!"

    line1 = [line for line in response.text.split("\n") if line.startswith("- 2.2.2: ")]
    if line1:
        l_concpt = line1[0].split(": ")[1].strip()
    else:
        l_concpt = "Response error!"

    line1 = [line for line in response.text.split("\n") if line.startswith("- 2.2.3: ")]
    if line1:
        l_tools_cat = line1[0].split(": ")[1].strip()
    else:
        l_tools_cat = "Response error!"

    # line1 = [line for line in response.text.split("\n") if line.startswith("- The Berlin Industrial SMEs Landscape: ")]
    # if line1:
    #     bl_sme = line1[0].split(": ")[1].strip()
    # else:
    #     bl_sme = "Response error!"

    line1 = [line for line in response.text.split("\n") if line.startswith("- 2.3.1: ")]
    if line1:
        bl_char = line1[0].split(": ")[1].strip()
    else:
        bl_char = "Response error!"

    line1 = [line for line in response.text.split("\n") if line.startswith("- 2.3.2: ")]
    if line1:
        bl_chal = line1[0].split(": ")[1].strip()
    else:
        bl_chal = "Response error!"

    line1 = [line for line in response.text.split("\n") if line.startswith("- 2.3.3: ")]
    if line1:
        bl_opp = line1[0].split(": ")[1].strip()
    else:
        bl_opp = "Response error!"

    line1 = [line for line in response.text.split("\n") if line.startswith("- 2.3.4: ")]
    if line1:
        bl_ce_impl = line1[0].split(": ")[1].strip()
    else:
        bl_ce_impl = "Response error!"

    line1 = [line for line in response.text.split("\n") if line.startswith("- 3.1: ")]
    if line1:
        gap_1 = line1[0].split(": ")[1].strip()
    else:
        gap_1 = "Response error!"

    line1 = [line for line in response.text.split("\n") if line.startswith("- 3.2: ")]
    if line1:
        gap_2 = line1[0].split(": ")[1].strip()
    else:
        gap_2 = "Response error!"

    # line1 = [line for line in response.text.split("\n") if
    #          line.startswith("- Research Direction and Assisting Tools: ")]
    # if line1:
    #     r_dir_tools = line1[0].split(": ")[1].strip()
    # else:
    #     r_dir_tools = "N/A"

    line1 = [line for line in response.text.split("\n") if
             line.startswith("- 4.2.1: ")]
    if line1:
        suc_impl = line1[0].split(": ")[1].strip()
    else:
        suc_impl = "N/A"

    line1 = [line for line in response.text.split("\n") if
             line.startswith("- 4.2.2: ")]
    if line1:
        s_l_concpt = line1[0].split(": ")[1].strip()
    else:
        s_l_concpt = "N/A"

    line1 = [line for line in response.text.split("\n") if
             line.startswith("- 4.2.3: ")]
    if line1:
        impl_bp = line1[0].split(": ")[1].strip()
    else:
        impl_bp = "N/A"

    line1 = [line for line in response.text.split("\n") if
             line.startswith("- 4.2.4: ")]
    if line1:
        curriculum = line1[0].split(": ")[1].strip()
    else:
        curriculum = "N/A"

    # line1 = [line for line in response.text.split("\n") if
    #          line.startswith("- Platform Concept Overview: ")]
    # if line1:
    #     platform_concpt = line1[0].split(": ")[1].strip()
    # else:
    #     platform_concpt = "N/A"
    #
    # line1 = [line for line in response.text.split("\n") if
    #          line.startswith("- Evaluation and Discussion: ")]
    # if line1:
    #     eval_dis = line1[0].split(": ")[1].strip()
    # else:
    #     eval_dis = "N/A"
    #
    # line1 = [line for line in response.text.split("\n") if
    #          line.startswith("- Limitations and Future Work: ")]
    # if line1:
    #     limits = line1[0].split(": ")[1].strip()
    # else:
    #     limits = "N/A"

    line1 = [line for line in response.text.split("\n") if line.startswith("- Reference: ")]
    if line1:
        reference = line1[0].split(": ")[1].strip()
    else:
        reference = "N/A"
    # return theoretical_framework, ce_fundamentals, ce_def, ce_principles, ce_imp_benefits, l_concpt_tools, l_def, l_concpt, l_tools_cat, bl_sme, bl_char, bl_chal, bl_opp, bl_ce_impl, gap_1, gap_2, r_dir_tools, suc_impl, s_l_concpt, impl_bp, curriculum, platform_concpt, eval_dis, limits, reference
    return ce_def, ce_principles, ce_imp_benefits, l_def, l_concpt, l_tools_cat, bl_char, bl_chal, bl_opp, bl_ce_impl, gap_1, gap_2, suc_impl, s_l_concpt, impl_bp, curriculum, reference

# Quote extraction
def quotes_extraction(data, model):

    prompt=f"Research Paper Content: {data}"

    response = model.generate_content(prompt)

    print(f"{ct()} - Response is provided. Analyzing and extracting relevant information...")

    line0=[line for line in response.text.split("\n") if line.startswith("- Quote 1: ")]
    if line0:
        q1 = line0[0].split(": ")[1].strip()
    else:
        q1 = "N/A"

    line0=[line for line in response.text.split("\n") if line.startswith("- Quote 2: ")]
    if line0:
        q2 = line0[0].split(": ")[1].strip()
    else:
        q2 = "N/A"

    line0=[line for line in response.text.split("\n") if line.startswith("- Quote 3: ")]
    if line0:
        q3 = line0[0].split(": ")[1].strip()
    else:
        q3 = "N/A"

    line0=[line for line in response.text.split("\n") if line.startswith("- Quote 4: ")]
    if line0:
        q4 = line0[0].split(": ")[1].strip()
    else:
        q4 = "N/A"

    line0=[line for line in response.text.split("\n") if line.startswith("- Quote 5: ")]
    if line0:
        q5 = line0[0].split(": ")[1].strip()
    else:
        q5 = "N/A"

    line0=[line for line in response.text.split("\n") if line.startswith("- Quote 6: ")]
    if line0:
        q6 = line0[0].split(": ")[1].strip()
    else:
        q6 = "N/A"

    return q1, q2, q3, q4, q5, q6

def response_c(path, model):
    data = pdf_text_extraction(path)
    prompt = f"Research Paper Content: {data}"
    response = model.generate_content(prompt)

    line = [line for line in response.text.split("\n") if line.startswith("Research Paper Analysis: ")]
    if line:
        title = "Research Paper Analysis: " + str(line)
    else:
        title = "Research Paper Analysis: N/A"

    line = [line for line in response.text.split("\n") if line.startswith("1. Objective: ")]
    if line:
        obj = "1. Objective: " + str(line)
    else:
        obj = "1. Objective: N/A"

    line = [line for line in response.text.split("\n") if line.startswith("2. Methodology: ")]
    if line:
        mtd = "2. Methodology: " + str(line)
    else:
        mtd = "2. Methodology: N/A"

    line = [line for line in response.text.split("\n") if line.startswith("3. Results: ")]
    if line:
        rst = "3. Results: " + str(line)
    else:
        rst = "3. Results: N/A"

    line = [line for line in response.text.split("\n") if line.startswith("4. Overall Summary: ")]
    if line:
        smr = "4. Overall Summary: " + str(line)
    else:
        smr = "4. Overall Summary: N/A"

    # line = [line for line in response.text.split("\n") if line.startswith("Follow-up Analysis: ")]
    # if line:
    #     ftitle = "Follow-up Analysis: " + str(line)
    # else:
    #     ftitle = "Follow-up Analysis: N/A"
    #
    # line = [line for line in response.text.split("\n") if line.startswith("1. Response: ")]
    # if line:
    #     rps = "1. Response: " + str(line)
    # else:
    #     rps = "1. Response: N/A"
    #
    # line = [line for line in response.text.split("\n") if line.startswith("2. Supporting Quote: ")]
    # if line:
    #     qte = "2. Supporting Quote: " + str(line)
    # else:
    #     qte = "2. Supporting Quote: N/A"
    #
    # line = [line for line in response.text.split("\n") if line.startswith("3. Explanation of Relevance: ")]
    # if line:
    #     expl = "3. Explanation of Relevance: " + str(line)
    # else:
    #     expl = "3. Explanation of Relevance: N/A"

    print(title)
    print(obj)
    print(mtd)
    print(rst)
    print(smr)
    # print(ftitle)
    # print(rps)
    # print(qte)
    # print(expl)

def process_loop_b(dir, model):
    if not os.path.isdir(dir):
        print(f"{ct()} - Incorrect file path.")
        return

    results = []
    index = 1

    for filename in os.listdir(dir):
        if filename.endswith(".pdf"):
            filepath = os.path.join(dir, filename)
            print(f"{ct()} - Processing document: {filename}")
            content = pdf_text_extraction(filepath)
            if "Error:" in content:
                print(content)
                continue

            # relevance, rel_level, area, goal, category, rtype, summary, methodology, purpose, discussion, reliability, quotes, reference=response_data_extraction(content, model)
            #
            # results.append((index, filename, relevance, rel_level, area, goal, category, rtype, summary, methodology, purpose, discussion, reliability, quotes, reference))

            relevance, rel_level, area, research_question, goal, category, rtype, summary, methodology, purpose, discussion, reliability, reference, quote1, quote2, quote3, quote4=response_data_extraction(content, model)

            results.append((index, filename, relevance, rel_level, area, research_question, goal, category, rtype, summary, methodology, purpose, discussion, reliability, quote1, quote2, quote3, quote4, reference))
            index+=1
            print(f"{ct()} - Completed analyzing document: {filename}.\n")
            time.sleep(6)
    print(f"{ct()} - All PDF files in {dir} have been processed. Exporting to data table...")
    df_results = pd.DataFrame(results, columns=["No.", "Title", "Relevance", "Relevance Level", "Key Areas of Interest", "Research Question", "Research Goal", "Research Category", "Research Type", "Summary", "Methodologies Used", "Research Purpose", "Discussions Addressed", "Reliability Level", "Quote 1 - Key Area of Interest", "Quote 2 - Research Question", "Quote 3 - Research Goal", "Quote 4 - Methodology", "Reference"])
    return df_results

def process_loop_d(dir, model):
    if not os.path.isdir(dir):
        print(f"{ct()} - Incorrect file path.")
        return

    results = []
    index = 1

    for filename in os.listdir(dir):
        if filename.endswith(".pdf"):
            filepath = os.path.join(dir, filename)
            print(f"{ct()} - Processing document: {filename}")
            content = pdf_text_extraction(filepath)
            if "Error:" in content:
                print(content)
                continue
            sec_no, sec_name, quote, ref=response_data_extraction_d(content, model)

            results.append((index, filename, sec_no, sec_name, quote, ref))
            index+=1
            print(f"{ct()} - Completed analyzing document: {filename}.\n")
            time.sleep(6)
    print(f"{ct()} - All PDF files in {dir} have been processed. Exporting to data table...")
    df_results = pd.DataFrame(results, columns=["No.", "Title", "Section Number", "Section Name", "Quote", "Reference"])
    return df_results

def process_loop_d_2(dir, model):
    if not os.path.isdir(dir):
        print(f"{ct()} - Incorrect file path.")
        return

    results = []
    index = 1

    for filename in os.listdir(dir):
        if filename.endswith(".pdf"):
            filepath = os.path.join(dir, filename)
            print(f"{ct()} - Processing document: {filename}")
            content = pdf_text_extraction(filepath)
            if "Error:" in content:
                print(content)
                continue
            ce_def, ce_principles, ce_imp_benefits, l_def, l_concpt, l_tools_cat, bl_char, bl_chal, bl_opp, bl_ce_impl, gap_1, gap_2, suc_impl, s_l_concpt, impl_bp, curriculum, reference=response_data_extraction_d_2(content, model)

            results.append((index, filename, ce_def, ce_principles, ce_imp_benefits, l_def, l_concpt, l_tools_cat, bl_char, bl_chal, bl_opp, bl_ce_impl, gap_1, gap_2, suc_impl, s_l_concpt, impl_bp, curriculum, reference))
            index+=1
            print(f"{ct()} - Completed analyzing document: {filename}.\n")
            time.sleep(6)
    print(f"{ct()} - All PDF files in {dir} have been processed. Exporting to data table...")
    df_results = pd.DataFrame(results, columns=["No.", "Title", "2.1.1 General Definition", "2.1.2 Key Principles", "2.1.3 Importance and Benefits", "2.2.1 Definition", "2.2.2 Learning Concepts", "2.2.3 E-learning Tools by Key Categories", "2.3.1 Key Characteristics", "2.3.2 Challenges", "2.3.3 Opportunities", "2.3.4 Notable CE Implementations in Businesses", "3.1 CE Implementation amongst SMEs Gaps", "3.2 Effectiveness of the CE Education Gaps", "4.2.1 Successful Implementation Cases", "4.2.2 Suitable Learning Concepts", "4.2.3 Implementation Best Practices", "4.2.4 Courseware and Training Curriculum", "Reference"])
    return df_results

def ple(dir, model):
    if not os.path.isdir(dir):
        print(f"{ct()} - Incorrect file path.")
        return

    qe = []
    index = 1
    for filename in os.listdir(dir):
        if filename.endswith(".pdf"):
            filepath = os.path.join(dir, filename)
            print(f"{ct()} - Processing document: {filename}")
            content = pdf_text_extraction(filepath)
            if "Error:" in content:
                print(content)
                continue

            q1, q2, q3, q4, q5, q6 = quotes_extraction(content,model)
            qe.append((index, filename, q1, q2, q3, q4, q5, q6))
            index+=1
            print(f"{ct()} - Completed extracting critical quotes from document: {filename}.\n")
            time.sleep(6)
    print(f"{ct()} - All PDF files in {dir} have been processed. Exporting to data table...")
    qer = pd.DataFrame(qe, columns=["No.", "Title", "Quote 1", "Quote 2", "Quote 3", "Quote 4", "Quote 5", "Research Question"])
    return qer

def excel_export_b(df):
    name_structure = f'Basic_Analysis_Results_{ct_o()}.xlsx'
    output_filename = PARENT_DIR / name_structure
    with pd.ExcelWriter(output_filename, mode='w') as writer:
        df.to_excel(writer, sheet_name='Processed')
    print(f"{ct()} - Results are exported to: {output_filename}.")
    browser_display(df)
    return

def excel_export_d(df):
    name_structure = f'Detailed_Analysis_Results_{ct_o()}.xlsx'
    output_filename = PARENT_DIR / name_structure
    with pd.ExcelWriter(output_filename, mode='w') as writer:
        df.to_excel(writer, sheet_name='Processed')
    print(f"{ct()} - Results are exported to: {output_filename}.")
    browser_display(df)
    return

def excel_export_q(df):
    name_structure = f'Quotes_{ct_o()}.xlsx'
    output_filename = PARENT_DIR / name_structure
    with pd.ExcelWriter(output_filename, mode='w') as writer:
        df.to_excel(writer, sheet_name='Processed')
    print(f"{ct()} - Results are exported to: {output_filename}.")
    browser_display(df)
    return

def browser_display(df):
    print(f"{ct()} - Displaying results in the default web browser...")
    tabledisplay=df.to_html(index=False)
    output_path = PARENT_DIR / "Results_display.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(tabledisplay)
    try:
        webbrowser.open(output_path)
    except Exception as e:
        print(f"{ct()} - Error displaying results in the default web browser: {e}.")

# Main function
def main(path, key, llm):
    file_path=path
    if file_path:
        model=genai_config(key, llm)
        df1=process_loop_b(file_path,model)
        excel_export_b(df1)
    else:
        return f"{ct()} - File not found. Exiting..."

# Main function
def main_d(path, key, llm):
    file_path=path
    if file_path:
        # model_d=genai_config_d(key,llm)
        # df2=process_loop_d(file_path,model_d)
        model_d_2=genai_config_d_2(key,llm)
        df2=process_loop_d_2(file_path,model_d_2)
        excel_export_d(df2)
    else:
        return f"{ct()} - File not found. Exiting..."

# Quote Extraction function
def main_q(path, key, llm):
    file_path=path
    if file_path:
        model=genai_config_qe(key, llm)
        df=ple(file_path,model)
        excel_export_q(df)
    else:
        return f"{ct()} - File not found. Exiting..."

# Main function to perform deep analysis
def main_c(path, key, llm):
    if path:
        model=genai_config_c(key, llm)
        response_c(path, model)
    else:
        return f'{ct()} - File not found. Exiting...'

if __name__ == "__main__":
    main()
