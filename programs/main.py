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
    6. Identify Key Areas of Interest in the Research Paper based on the example list below.
    7. Based on the content decide whether the Research Paper belongs to any of most common types of research papers as listed below.
    8. Cite the exact sentences and/or data found in the Research Paper Content that is most relevant to the goal of the Research Paper.
    9. Provide an APA Citation for the Research Paper following the style of the APA 7th Edition.

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
    - Research goal: Goal.
    - Research category: Qualitative or Quantitative.
    - Research type: Select from the list of common types of research papers.
    - Research summary: Summary of the research (no more than 2 sentences).
    - Research methodology: Methodology.
    - Research Purpose: Theoretical or Applied.
    - Research discussion: key discussions (no more than 2 sentences).
    - Research reliability: Low or High.
    - Quotes: quotes.
    - Reference: APA 7th Edition style.
    
    Response Example:
    
    - Relevance: Yes.
    - Relevance level: High.
    - Key Areas of Interest: Circular Economy Concept.
    - Research goal: Classification of all researches on Augmented Reality (AR) technology applications in the manufacturing industry from 2006 to early 2017.
    - Research category: Qualitative.
    - Research type: Literature Review.
    - Research summary: This study reviews Augmented Reality (AR) applications in the manufacturing industry from 2006-2017, categorizing the literature to highlight the technology's deployment areas, solutions, and benefits. It identifies assembly and maintenance as key application fields, noting an increasing interest in AR for industrial operations..
    - Research methodology: Systematic Literature Review.
    - Research Purpose: Theoretical.
    - Research discussion: The review indicates a growing interest in AR within industrial operations, particularly in assembly and maintenance, and highlights the increasing adoption of mobile devices and HMDs for AR implementation. It also points out the need for further research in unexplored areas and economic assessments of AR solutions..
    - Research reliability: High.
    - Quotes: "First, interest towards the use of AR technology in industrial operations is increasing over time, as highlighted by the growing number of recent papers focusing on AR usage in industry.", "... it can be concluded that AR shows great application potential in many industrial operations, and in particular, in the field of maintenance and assembly.", "Other interesting application fields (such as safety, ergonomics or remote collaboration) have emerged recently; although they are now investigated with good continuity, the number of studies found is still limited and suggests that the potential of AR in these contexts has not yet been fully explored.", etc.
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

    api_key = input(f"{ct()} - Input API Key: ")
    if api_key:
        llm  = input(f"{ct()} - Choose LLM (gemini-1.5-flash, gemini-1.5-flash-8b, gemini-1.5-pro, gemini-2.0-flash, gemini-2.0-flash-lite-preview-02-05): \n")
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

        line1 = [line for line in response.text.split("\n") if line.startswith("- Quotes: ")]
        if line1:
            quotes = line1[0].split(": ")[1].strip()
        else:
            quotes = "N/A"

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
        quotes = "N/A"
        reference = "N/A"

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
    return relevance, rel_level, area, goal, category, rtype, summary, methodology, purpose, discussion, reliability, quotes, reference

# Process Loop
# def process_loop(dir, model):
#     if not os.path.isdir(dir):
#         print(f"{ct()} - Incorrect file path.")
#         return
#     for filename in os.listdir(dir):
#         if filename.endswith(".pdf"):
#             filepath=os.path.join(dir,filename)
#             print(f"{ct()} - Processing document: {filename}")
#             content=pdf_text_extraction(filepath)
#             if "Error:" in content:
#                 print(content)
#                 continue
#
#             response_data_extraction(content, model)
#
#     return

def process_loop(dir, model):
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

            relevance, rel_level, area, goal, category, rtype, summary, methodology, purpose, discussion, reliability, quotes, reference=response_data_extraction(content, model)

            results.append((index, filename, relevance, rel_level, area, goal, category, rtype, summary, methodology, purpose, discussion, reliability, quotes, reference))
            index+=1
            print(f"{ct()} - Completed analyzing document: {filename}.\n")
    print(f"{ct()} - All PDF files in {dir} have been processed. Exporting to data table...")
    df_results = pd.DataFrame(results, columns=["No.", "Title", "Relevance", "Relevance Level", "Key Areas of Interest", "Research Goal", "Research Category", "Research Type", "Summary", "Methodologies Used", "Research Purpose", "Discussions Addressed", "Reliability Level", "Quotes", "Reference"])
    return df_results

def excel_export(df):
    output_filename = PARENT_DIR / "Results.xlsx"
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
def main():
    file_path=input(f"{ct()} - Input documents dir: ")
    if file_path:
        # content=pdf_text_extraction(file_path)
        model=genai_config()
        df=process_loop(file_path,model)
        excel_export(df)
        # response_data_extraction(content,model)
    else:
        return f"{ct()} - File not found. Exiting..."

if __name__ == "__main__":
    main()
