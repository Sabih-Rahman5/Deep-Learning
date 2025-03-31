

def loadModel():
    model_name = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
    model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Pipeline for text generation
    text_generation_pipeline = pipeline(
        model=model,
        tokenizer=tokenizer,
        task="text-generation",
        temperature=0.2,
        do_sample=True,
        repetition_penalty=1.1,
        return_full_text=False,
        max_new_tokens=500,
    )

    llm_pipeline = HuggingFacePipeline(pipeline=text_generation_pipeline)

    # Prompt template to match desired output format
    prompt_template = """
    You are a professional AI researcher, give an help in study. Use the following context to answer the question using information provided by the paper:

    {context}

    Question: {question}
    """
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=prompt_template,
    )

    llm_chain = prompt | llm_pipeline | StrOutputParser()


    pipeline = (
        {"context": retriever, "question": RunnablePassthrough()}
        | llm_chain
    )

    return pipeline
