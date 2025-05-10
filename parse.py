from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st
import time

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

model = OllamaLLM(model="deepseek-r1:latest", timeout=30)


def parse_with_ollama(dom_chunks, parse_description):
    try:
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | model

        parsed_results = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, chunk in enumerate(dom_chunks, start=1):
            status_text.text(f"Processing chunk {i} of {len(dom_chunks)}...")
            try:
                start_time = time.time()
                response = chain.invoke(
                    {"dom_content": chunk, "parse_description": parse_description}
                )
                end_time = time.time()
                st.write(f"Chunk {i} processed in {end_time - start_time:.2f} seconds")
                parsed_results.append(response)
            except Exception as e:
                st.error(f"Error processing chunk {i}: {str(e)}")
                parsed_results.append("")  # Add empty string for failed chunks
            
            # Update progress
            progress = i / len(dom_chunks)
            progress_bar.progress(progress)
            
        return "\n".join(parsed_results)
    except Exception as e:
        st.error(f"Error during parsing: {str(e)}")
        return None