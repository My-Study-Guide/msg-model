from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import login
import re

login("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")
# text_input = '' # html관련 api 요청

text_input = """Explore
Show notifications
Menu pop-up Collapsed
J
Home
My Learning
Online Degrees
Find your New Career

Your goal is to explore topics outside of work as a Student

Edit
Recently Viewed Products
D

DeepLearning.AI

Deep Learning

Make progress toward a degree

Specialization

D

DeepLearning.AI

Neural Networks and Deep Learning

Course

D

DeepLearning.AI

Improving Deep Neural Networks: Hyperparameter Tuning, Regularization and Optimization

Course

D

DeepLearning.AI

Convolutional Neural Networks

Course

Show 2 more
Most Popular Certificates
D

DeepLearning.AI

Deep Learning

Make progress toward a degree

Specialization

I

IBM

IBM Full Stack Software Developer

Make progress toward a degree

Professional Certificate

I

IBM

IBM Cybersecurity Analyst

Make progress toward a degree

Professional Certificate

I

IBM

IBM Data Science

Make progress toward a degree

Professional Certificate

Show 8 more
Personalized Specializations for You
D

DeepLearning.AI

Natural Language Processing

Specialization

D

DeepLearning.AI

DeepLearning.AI TensorFlow Developer

Professional Certificate

D

DeepLearning.AI

Machine Learning

Make progress toward a degree

Specialization

D

DeepLearning.AI

Generative Adversarial Networks (GANs)

Specialization

Show 8 more
Build In-Demand Artificial Neural Networks Skills
D

DeepLearning.AI

Convolutional Neural Networks

Course

D

DeepLearning.AI

Sequence Models

Course

D

DeepLearning.AI

Structuring Machine Learning Projects

Course

D

DeepLearning.AI

TensorFlow: Data and Deployment

Specialization

Show 8 more
Explore with a Coursera Plus Subscription
I

IBM

IBM AI Engineering

Make progress toward a degree

Professional Certificate

I

IBM

IBM Machine Learning

Make progress toward a degree

Professional Certificate

I

Imperial College London

Mathematics for Machine Learning

Specialization

I

IBM

Applied Data Science Capstone

Course

Show 8 more
Based on Your Recent Views
D

DeepLearning.AI

Deep Learning

Make progress toward a degree

Specialization

D

DeepLearning.AI

Improving Deep Neural Networks: Hyperparameter Tuning, Regularization and Optimization

Course

D

DeepLearning.AI

Convolutional Neural Networks

Course

D

DeepLearning.AI

Structuring Machine Learning Projects

Course

Show 8 more
Earn credit towards one of these degrees
Your enrollment in Deep Learning is eligible for college credit towards any of these degrees. If you complete the certificate and are admitted into the program, you can transfer your credit.¹

¹Each university determines the number of pre-approved prior learning credits that may count towards the degree requirements according to institutional policies.

B

Ball State University

Master of Science in Computer Science

Degree

I

Illinois Tech

Master of Data Science

Degree

B

Ball State University

Master of Science in Data Science

Degree

I

Illinois Tech

Bachelor of Information Technology

Degree

Show 1 more
Earn Your Degree
I

Indian Statistical Institute

Postgraduate Diploma in Applied Statistics

Earn a degree

Degree

O

O.P. Jindal Global University

MBA in Business Analytics

Earn a degree

Degree

O

O.P. Jindal Global University

M.A. in International Relations, Security, and Strategy

Earn a degree

Degree

O

O.P. Jindal Global University

M.A. in Public Policy

Earn a degree

Degree

Show 8 more

Get Started with These Free Courses
Status: Free
Free
D

DeepLearning.AI

Finetuning Large Language Models

Project

Status: Free
Free
D

DeepLearning.AI

How Diffusion Models Work

Project

Status: Free
Free
D

DeepLearning.AI

LangChain Chat with Your Data

Project

Status: Free
Free
D

DeepLearning.AI

ChatGPT Prompt Engineering for Developers

Project

Show 8 more
New on Coursera
G

Google

Google AI Essentials

Course

M

Microsoft

Microsoft Project Management

Professional Certificate

M

Microsoft

Microsoft Cybersecurity Analyst

Professional Certificate

Status: Free
Free
U

University of Leeds

Fundamental Skills in Engineering Design

Course

Show 8 more
Popular in Data Science
Status: [object Object]
New AI skills
G

Google

Google Data Analytics

Make progress toward a degree

Professional Certificate

G

Google

Foundations: Data, Data, Everywhere

Course

G

Google

Ask Questions to Make Data-Driven Decisions

Course

G

Google

Prepare Data for Exploration

Course

Show 8 more
Personalized Courses for You
D

DeepLearning.AI

Machine Learning in Production

Course

D

DeepLearning.AI

Generative AI with Large Language Models

Course

D

DeepLearning.AI

Natural Language Processing with Classification and Vector Spaces

Course

D

DeepLearning.AI

Sequences, Time Series and Prediction

Course

Show 8 more
Guided Projects for You
C

Coursera Project Network

Deep Learning with PyTorch : Image Segmentation

Guided Project

C

Coursera Project Network

Fine Tune BERT for Text Classification with TensorFlow

Guided Project

C

Coursera Project Network

Introduction to Microsoft Excel

Guided Project

C

Coursera Project Network

Deep Learning with PyTorch : Generative Adversarial Network

Guided Project

Show 8 more
Learn a New Skill in 2 Hours
D

Deprecated Guided Projects

Build Random Forests in R with Azure ML Studio

Guided Project

C

Coursera Project Network

AWS S3 Basics

Guided Project

Status: Free
Free
M

Microsoft

Build a computer vision app with Azure Cognitive Services

Guided Project

C

Coursera Project Network

Introduction to Basic Game Development using Scratch

Guided Project

Show 7 more
Grow Your Skill Set
Status: Free
Free
D

DeepLearning.AI

ChatGPT Prompt Engineering for Developers

Project

Status: Free
Free
U

University of California, Davis

The Strategy of Content Marketing

Course

Status: Free
Free
U

University of Toronto

Learn to Program: The Fundamentals

Course

G

Google Cloud

Google Cloud Fundamentals: Core Infrastructure

Course

Show 8 more
Coursera
Community
More
Mobile App
© 2024 Coursera Inc. All rights reserved."""

model_name = "google/gemma-2-2b-it"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    # device_map="auto",
)

chat = [
    { "role": "user", "content": f"Please summarize the following text in three lines or less.:{text_input}" },
]
prompt = tokenizer.apply_chat_template(chat, tokenize=False, add_generation_prompt=True)

input_ids = tokenizer(prompt, return_tensors="pt")

outputs = model.generate(
    **input_ids,
    max_length=2000,
    do_sample=True,
    top_p=0.95,
    temperature=0.7,
    repetition_penalty=1.1,
)

raw_summary = tokenizer.decode(outputs[0])

pattern = r'<start_of_turn>model\s*(.*?)\s*<end_of_turn>'

match = re.search(pattern, raw_summary, re.DOTALL)

if match:
    # 그룹에서 매칭된 내용 추출
    summary = match.group(1).strip()
    print("summary:")
    print(summary)
else:
    print("Error!")

# summary -> 최종본