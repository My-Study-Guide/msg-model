from transformers import AutoTokenizer, AutoModelForCausalLM
import google.generativeai as genai
import os
import logging
import time
import re

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MSG:
    def __init__(self, summarizing_model_name, scoring_model_name, device):
        logger.info("Initializing MSG class")
        start_time = time.time()

        self.summarizing_model_name = summarizing_model_name
        self.scoring_model_name = scoring_model_name
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

        try:
            # Load model and tokenizer
            logger.info(f"Loading model and tokenizer for {self.summarizing_model_name}, on {device}")
            self.tokenizer = AutoTokenizer.from_pretrained(self.summarizing_model_name)
            logger.debug(f"Tokenizer loaded: {self.tokenizer.__class__.__name__}")

            self.model = AutoModelForCausalLM.from_pretrained(self.summarizing_model_name).to(device)
            logger.debug(f"Model loaded: {self.model.__class__.__name__}")            

        except Exception as e:
            logger.exception(f"An error occurred: {str(e)}")

        finally:
            total_time = time.time() - start_time
            logger.info(f"ModelHandler initialized in {total_time:.2f} seconds")
    
    def summarize(self, text_input):
        logger.info("Starting summarizing function")
        start_time = time.time()

        try:            
            # Prepare chat and prompt
            logger.debug("Preparing chat and prompt")
            chat = [
                { "role": "user", "content": f"Please summarize the following html source in three lines or less.:{text_input}" },
            ]
            prompt = self.tokenizer.apply_chat_template(chat, tokenize=False, add_generation_prompt=True)
            logger.debug(f"Prompt created.")

            # Tokenize input
            logger.debug("Tokenizing input")
            input_ids = self.tokenizer(prompt, return_tensors="pt")
            logger.debug(f"Input tokenized. Shape: {input_ids.input_ids.shape}")

            # Generate output
            logger.info("Generating summary")
            generation_start_time = time.time()
            outputs = self.model.generate(
                **input_ids,
                max_length=2000,
                do_sample=True,
                top_p=0.95,
                temperature=0.7,
                repetition_penalty=1.1,
            )
            generation_time = time.time() - generation_start_time
            logger.info(f"Summary generated in {generation_time:.2f} seconds")

            # Decode output
            logger.debug("Decoding output")
            raw_summary = self.tokenizer.decode(outputs[0])
            logger.debug(f"Raw summary length: {len(raw_summary)} characters")

            # Extract summary using regex
            logger.debug("Extracting summary")
            pattern = r'<start_of_turn>model\s*(.*?)\s*<end_of_turn>'

            match = re.search(pattern, raw_summary, re.DOTALL)

            if match:
                self.summary = match.group(1).strip()
                logger.info("Summary successfully extracted")
                logger.info(f"Summary:\n{self.summary}")
            else:
                logger.error("Failed to extract summary from model output")
                print("Error!")

        except Exception as e:
            logger.exception(f"An error occurred: {str(e)}")

        finally:
            total_time = time.time() - start_time
            logger.info(f"Summary function completed in {total_time:.2f} seconds")
            
    def scoring(self, topics):
        logger.info("Start scoring function")
        start_time = time.time()
        try:
            generation_start_time = time.time()
            self.scoring_model = genai.GenerativeModel(self.scoring_model_name) 
            prompt = """Compare given sentences and topics and score the sentences between 1~100. 
                The criteria are as following:
                - Is the sentence relevant to at least 1 topic among the given topics?
                - Is there any topic well-representing the sentence?
                - Is the sentence properly matches at least 1 topic?
                Answer in this format: <score>put_score_in_integer</score><reason>put_reason_in_2_or_3_sentences</reason>"

                Sentences: """ + self.summary + '\nTopics: ' + topics

            response = self.scoring_model.generate_content(prompt)     

            generation_time = time.time() - generation_start_time
            logger.info(f"Score and reason generated in {generation_time:.2f} seconds")

            # Extract score & reason using regex
            logger.debug("Processing..")

            score_pattern = r'<score>(.*?)</score>'
            reason_pattern = r'<reason>(.*?)</reason>'

            score_match = re.search(score_pattern, response.text)
            reason_match = re.search(reason_pattern, response.text, re.DOTALL)

            if score_match:
                self.score = score_match.group(1)
                logger.info("Score successfully extracted")
                logger.info(f"Score: {self.score}")
            else:
                self.score = None
                logger.error("Failed to extract score from model output")

            if reason_match:
                self.reason = reason_match.group(1)
                logger.info("Reason successfully extracted")
                logger.info(f"Reason: {self.reason}")
            else:
                self.reason = None
                logger.error("Failed to extract reason from model output")

        except Exception as e:
            logger.exception(f"An error occurred: {str(e)}")

        finally:
            total_time = time.time() - start_time
            logger.info(f"Scoring function completed in {total_time:.2f} seconds")

        return self.score, self.reason
    