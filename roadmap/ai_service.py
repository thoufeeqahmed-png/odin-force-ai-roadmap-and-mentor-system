"""
ai_service.py - Modular AI Engine for ODIN TA Junior

Provides intelligent roadmap synthesis for ANY domain (Tech, Creative, Business, Sciences, Arts, Lifestyle),
personalizing stages, rationale, practice tasks, real-world projects, daily guidance, and supportive advice.
Supports optional external LLM APIs (Gemini/OpenAI) with an intelligent built-in heuristic generator as default.
"""

import os
import json
import re
from typing import Dict, Any, List


class TAJuniorAIService:
    """
    Core AI Service for ODIN TA Junior.
    Designed with a kind, friendly, supportive junior assistant personality.
    """

    SUPPORTIVE_QUOTES = [
        "Don't worry about learning everything at once. Let's start with the foundation and take it one step at a time.",
        "Consistency always beats intensity. Even 30 focused minutes today creates massive momentum over time.",
        "It's completely normal to feel confused in the beginning! That's just your brain making new connections.",
        "Focus on understanding today's concept deeply. You don't need to master the entire field in one afternoon.",
        "The best way to learn is by building small, messy things. Never be afraid to experiment and make mistakes!",
        "Every master was once a beginner who refused to quit. You've got this, and I'm cheering you on every step of the way!"
    ]

    # Pre-crafted domain blueprints for popular fields (to ensure exceptional detail out of the box)
    DOMAIN_BLUEPRINTS = {
        "artificial intelligence": {
            "stages": [
                {
                    "title": "Stage 1 — Mathematical Foundations & Python for AI",
                    "estimated_duration": "Weeks 1-4",
                    "description": "Build comfortable intuition with Python, NumPy data structures, linear algebra essentials (matrices, vectors), and probability fundamentals.",
                    "why_it_matters": "AI models are essentially mathematical machines expressed in code. Having solid footing with matrices, calculus gradients, and data arrays prevents confusion later.",
                    "what_to_practice": "Write vectorized matrix multiplications in NumPy; plot gradient descent curves using Matplotlib; implement basic statistics algorithms from scratch.",
                    "suggested_projects": "1. Matrix Math & Vector Visualization Tool in Python.\n2. Interactive gradient descent visualizer.",
                    "tasks": [
                        {"title": "Python Data Structures & OOP refresher", "type": "topic", "desc": "Master list comprehensions, generator functions, and clean class designs."},
                        {"title": "NumPy & Vectorized Math", "type": "topic", "desc": "Explore array broadcasting, dot products, slicing, and reshaping."},
                        {"title": "Linear Algebra & Calculus Intuition", "type": "topic", "desc": "Understand vectors, eigenvalues, partial derivatives, and the chain rule simply."},
                        {"title": "Build a Vector Calculation Drill", "type": "practice", "desc": "Code 5 vector transformation functions without external math libraries."},
                        {"title": "Project: Vector & Gradient Exploration Notebook", "type": "project", "desc": "Create a documented notebook illustrating 2D loss surfaces and convergence."}
                    ]
                },
                {
                    "title": "Stage 2 — Core Machine Learning & Data Pipeline",
                    "estimated_duration": "Weeks 5-10",
                    "description": "Learn classical supervised and unsupervised ML algorithms: linear/logistic regression, decision trees, random forests, and k-means clustering with Scikit-Learn.",
                    "why_it_matters": "Real-world AI starts with tabular data and classical ML. Understanding bias-variance tradeoffs, feature engineering, and cross-validation is essential before touching neural networks.",
                    "what_to_practice": "Clean messy datasets with Pandas; build regression models to predict housing prices; evaluate models with Precision, Recall, ROC-AUC curves.",
                    "suggested_projects": "1. Customer Churn Prediction System with automated feature importance.\n2. Medical Diagnostic Classifier with explainability reports.",
                    "tasks": [
                        {"title": "Data Preprocessing & Feature Engineering", "type": "topic", "desc": "Handle missing values, categorical encoding, scaling, and outlier detection with Pandas."},
                        {"title": "Supervised Learning (Regression & Trees)", "type": "topic", "desc": "Study decision trees, ensemble methods, and regularization techniques (L1/L2)."},
                        {"title": "Model Evaluation & Cross-Validation", "type": "topic", "desc": "Master confusion matrices, F1-scores, K-fold validation, and avoiding data leakage."},
                        {"title": "Implement Linear Regression from Scratch", "type": "practice", "desc": "Code gradient descent optimization for a single feature predictor."},
                        {"title": "Project: End-to-End Tabular ML Classifier", "type": "project", "desc": "Train, tune hyperparameters, and benchmark 3 algorithms on a real-world dataset."}
                    ]
                },
                {
                    "title": "Stage 3 — Deep Learning & Neural Network Architectures",
                    "estimated_duration": "Weeks 11-16",
                    "description": "Dive into deep neural networks using PyTorch. Understand forward passes, backpropagation, activation functions, CNNs for vision, and RNNs/LSTMs for sequences.",
                    "why_it_matters": "Deep learning unlocks unstructured data (images, audio, text). PyTorch is the industry-standard framework for modern AI research and engineering.",
                    "what_to_practice": "Build a multi-layer perceptron (MLP) from scratch; train a convolutional neural network (CNN) on image classification; experiment with learning rate schedulers.",
                    "suggested_projects": "1. Real-time Image Classifier with Transfer Learning (ResNet/EfficientNet).\n2. Handwritten Digit & Symbol Recognition Web App.",
                    "tasks": [
                        {"title": "PyTorch Tensors, Autograd & Training Loops", "type": "topic", "desc": "Understand computational graphs, zero_grad(), backward(), and optimizers."},
                        {"title": "Convolutional Neural Networks (CNNs) & Vision", "type": "topic", "desc": "Explore convolution filters, pooling, feature maps, and transfer learning."},
                        {"title": "Regularization & Optimization in Deep Networks", "type": "topic", "desc": "Master Dropout, Batch Normalization, AdamW optimizer, and learning rate warmups."},
                        {"title": "Build a Custom PyTorch Dataset & DataLoader", "type": "practice", "desc": "Create a pipeline for custom images with augmentation transformations."},
                        {"title": "Project: Transfer Learning Image Classification App", "type": "project", "desc": "Fine-tune a pretrained vision backbone to classify domain-specific items with >90% accuracy."}
                    ]
                },
                {
                    "title": "Stage 4 — Large Language Models (LLMs) & Generative AI",
                    "estimated_duration": "Weeks 17-20",
                    "description": "Master Transformer architectures (Self-Attention, Encoders/Decoders), HuggingFace ecosystem, Retrieval-Augmented Generation (RAG), and Prompt Engineering techniques.",
                    "why_it_matters": "LLMs and Transformers represent the cutting edge of modern AI. Learning how to build RAG pipelines, manage embeddings, and evaluate LLM agents is in high industry demand.",
                    "what_to_practice": "Implement self-attention mechanism in PyTorch; build a vector search index using ChromaDB/FAISS; craft multi-stage RAG pipelines with LangChain or LlamaIndex.",
                    "suggested_projects": "1. Document Q&A RAG Assistant with citation highlighting.\n2. Autonomous Research Agent that fetches and synthesizes web articles.",
                    "tasks": [
                        {"title": "The Transformer Architecture & Attention Mechanism", "type": "topic", "desc": "Understand query-key-value projections, multi-head attention, and positional encodings."},
                        {"title": "Vector Databases, Embeddings & Semantic Search", "type": "topic", "desc": "Learn how embeddings represent meaning in multi-dimensional space and how cosine similarity works."},
                        {"title": "Retrieval-Augmented Generation (RAG) Architecture", "type": "topic", "desc": "Build chunking strategies, top-k retrieval, re-ranking, and context injection."},
                        {"title": "Fine-Tuning Techniques (LoRA / QLoRA)", "type": "practice", "desc": "Understand parameter-efficient fine-tuning on open weights (e.g. Llama/Mistral)."},
                        {"title": "Project: Custom Knowledge Base RAG Assistant", "type": "project", "desc": "Develop an interactive chatbot that answers domain questions from uploaded PDF manuals."}
                    ]
                },
                {
                    "title": "Stage 5 — Real-World Projects & AI System Deployment (MLOps)",
                    "estimated_duration": "Weeks 21-24",
                    "description": "Package, serve, and monitor AI models in production with FastAPI, Docker, ONNX/TensorRT inference optimization, and cloud deployment.",
                    "why_it_matters": "A model running only in a Jupyter notebook provides zero business value. Production AI engineers need to serve models with low latency, reliability, and automated tests.",
                    "what_to_practice": "Wrap a PyTorch model in an asynchronous FastAPI service; containerize with Docker; benchmark latency and throughput under load.",
                    "suggested_projects": "1. Production-ready AI Microservice API deployed on Cloud with CI/CD.\n2. Complete Capstone: End-to-End AI SaaS Product with user auth and billing.",
                    "tasks": [
                        {"title": "Model Serving with FastAPI & Async Python", "type": "topic", "desc": "Design REST endpoints, request validation with Pydantic, and batch inference queues."},
                        {"title": "Model Optimization & Quantization (ONNX/GGUF)", "type": "topic", "desc": "Convert models to ONNX and 4-bit/8-bit formats for 3x faster inference."},
                        {"title": "Dockerization & Cloud Deployment", "type": "topic", "desc": "Build multi-stage Docker images and deploy to AWS, GCP, or Render."},
                        {"title": "Implement API Rate Limiting & Monitoring", "type": "practice", "desc": "Add Prometheus metrics and logging for token usage and latency tracking."},
                        {"title": "Project: Production Capstone AI Application", "type": "project", "desc": "Deploy an AI web application with frontend, database, API, and cloud-hosted inference."}
                    ]
                }
            ]
        },
        "web development": {
            "stages": [
                {
                    "title": "Stage 1 — Web Fundamentals (HTML5, Modern CSS & Responsive Layouts)",
                    "estimated_duration": "Weeks 1-4",
                    "description": "Master semantic HTML5, modern CSS layout techniques (Flexbox, Grid, Custom Properties), and responsive design principles across mobile and desktop.",
                    "why_it_matters": "Every web app on the internet relies on solid HTML and CSS structure. Writing accessible, clean markup makes your sites fast, SEO-friendly, and easy to maintain.",
                    "what_to_practice": "Code multi-column responsive landing pages without frameworks; build accessible interactive navbars with pure CSS; design fluid typography systems.",
                    "suggested_projects": "1. Responsive Personal Portfolio & Case Study Showcase.\n2. Interactive Product Landing Page with micro-animations.",
                    "tasks": [
                        {"title": "Semantic HTML5 & Web Accessibility (a11y)", "type": "topic", "desc": "Use proper semantic tags, ARIA attributes, and accessible heading structures."},
                        {"title": "CSS Flexbox & CSS Grid Mastery", "type": "topic", "desc": "Master container layouts, fractional units, auto-fit/auto-fill, and alignment."},
                        {"title": "Responsive Design & Media Queries", "type": "topic", "desc": "Build mobile-first layouts that adapt smoothly to smartphones, tablets, and wide monitors."},
                        {"title": "Build a Responsive Component Library", "type": "practice", "desc": "Create reusable cards, buttons, modals, and navigation bars with pure CSS."},
                        {"title": "Project: Modern High-Converting Landing Page", "type": "project", "desc": "Build and publish a responsive landing page scored 95+ on Google Lighthouse."}
                    ]
                },
                {
                    "title": "Stage 2 — Modern JavaScript & DOM Programming",
                    "estimated_duration": "Weeks 5-8",
                    "description": "Deep dive into ES6+ JavaScript, asynchronous programming (Promises, async/await), DOM manipulation, Fetch API, and local storage management.",
                    "why_it_matters": "JavaScript brings web pages to life with user interactivity, real-time client-side updates, and external API communication.",
                    "what_to_practice": "Write event-driven components; fetch live data from public REST APIs; handle error states and loading spinners cleanly.",
                    "suggested_projects": "1. Real-time Weather & City Forecast App using public APIs.\n2. Interactive Kanban Task Board with drag-and-drop and persistence.",
                    "tasks": [
                        {"title": "ES6+ Fundamentals (Destructuring, Arrow Functions, Modules)", "type": "topic", "desc": "Write modern, concise, and modular JavaScript code."},
                        {"title": "Asynchronous JS, Promises & Fetch API", "type": "topic", "desc": "Handle asynchronous network requests, status codes, and JSON parsing gracefully."},
                        {"title": "DOM Traversal, Events & State Management", "type": "topic", "desc": "Update UI dynamically based on user clicks, inputs, and custom events."},
                        {"title": "Build an API Data Fetcher Drill", "type": "practice", "desc": "Fetch, filter, sort, and display a list of 50 items with search debounce."},
                        {"title": "Project: Interactive Personal Finance Tracker", "type": "project", "desc": "Create an expense manager with charts, categories, and local storage backup."}
                    ]
                },
                {
                    "title": "Stage 3 — Backend Development & Databases (Python/Django or Node.js)",
                    "estimated_duration": "Weeks 9-14",
                    "description": "Learn server-side architecture, relational database design (PostgreSQL/SQLite), ORM queries, authentication, session security, and RESTful API endpoints.",
                    "why_it_matters": "Backend servers handle user accounts, secure data storage, business logic, and payments that make applications valuable and trustworthy.",
                    "what_to_practice": "Define relational models with foreign keys; write secure login/registration workflows; build CRUD endpoints with validation.",
                    "suggested_projects": "1. Multi-user Blog or Community Forum with markdown editing and comments.\n2. E-commerce Marketplace with shopping cart and order history.",
                    "tasks": [
                        {"title": "HTTP Protocol, Request/Response Lifecycle & Routing", "type": "topic", "desc": "Understand GET/POST methods, headers, status codes, and URL parameters."},
                        {"title": "Database Schema Design & ORM Queries", "type": "topic", "desc": "Design normalized tables, foreign keys, many-to-many relationships, and efficient queries."},
                        {"title": "User Authentication & Authorization", "type": "topic", "desc": "Implement password hashing, session cookies, permissions, and CSRF protection."},
                        {"title": "Build a Secure REST API Endpoint", "type": "practice", "desc": "Create an API with token authentication, pagination, and error handling."},
                        {"title": "Project: Full-Stack Web Application with Auth", "type": "project", "desc": "Build a full-stack CRUD application with role-based access control and database storage."}
                    ]
                },
                {
                    "title": "Stage 4 — Full-Stack Integration, Testing & Cloud Deployment",
                    "estimated_duration": "Weeks 15-18",
                    "description": "Connect frontend and backend seamlessly, implement automated unit and integration tests, configure CI/CD pipelines, and deploy with custom domains and SSL.",
                    "why_it_matters": "A professional developer knows how to take an application from local code to a live, secure, production-grade URL accessible worldwide.",
                    "what_to_practice": "Write unit test suites; configure automated deployment workflows via GitHub Actions; set up production environment variables and SSL certificates.",
                    "suggested_projects": "1. Live SaaS Capstone Application with automated deployment.\n2. Portfolio Website showcasing 3 live, hosted web applications.",
                    "tasks": [
                        {"title": "Automated Testing (Unit & Integration Tests)", "type": "topic", "desc": "Write unit tests for views, models, and business logic to prevent regressions."},
                        {"title": "Security Hardening & Production Best Practices", "type": "topic", "desc": "Configure HTTPS, secure headers, environment secrets, and CORS policies."},
                        {"title": "Cloud Hosting & CI/CD Pipelines", "type": "topic", "desc": "Deploy to platforms like Render, Railway, or AWS with automated push-to-deploy."},
                        {"title": "Performance Optimization & Asset Caching", "type": "practice", "desc": "Minify assets, configure Gzip/Brotli compression, and optimize database indexing."},
                        {"title": "Project: Live Deployed SaaS Capstone", "type": "project", "desc": "Launch a fully functional web app with live custom domain, SSL, and analytics."}
                    ]
                }
            ]
        },
        "digital photography": {
            "stages": [
                {
                    "title": "Stage 1 — Camera Anatomy & The Exposure Triangle",
                    "estimated_duration": "Weeks 1-3",
                    "description": "Understand your camera controls, sensor mechanics, and master manual mode using Aperture (f-stop), Shutter Speed, and ISO balance.",
                    "why_it_matters": "Moving away from Auto mode gives you total creative control over depth of field, motion blur, and clean low-light imagery.",
                    "what_to_practice": "Shoot 50 photos in full Manual mode varying shutter speed for motion freeze vs motion blur; practice shallow depth of field portraits.",
                    "suggested_projects": "1. 'Motion & Stillness' Photo Series (10 curated images).\n2. Natural Light Portrait Exploration.",
                    "tasks": [
                        {"title": "The Exposure Triangle (Aperture, Shutter Speed, ISO)", "type": "topic", "desc": "Understand stops of light and how each element influences image look and exposure."},
                        {"title": "Camera Modes, Focus Points & Metering Modes", "type": "topic", "desc": "Learn single-point vs continuous autofocus and spot vs evaluative metering."},
                        {"title": "RAW vs JPEG & White Balance", "type": "topic", "desc": "Master color temperature, Kelvin scale, and maximizing dynamic range with RAW."},
                        {"title": "Manual Exposure Drill", "type": "practice", "desc": "Photograph stationary and moving subjects in varying sunlight using Manual mode."},
                        {"title": "Project: Exposure Triangle Study Booklet", "type": "project", "desc": "Assemble a PDF comparison of 12 images demonstrating varied apertures and shutter speeds."}
                    ]
                },
                {
                    "title": "Stage 2 — Composition, Framing & Visual Storytelling",
                    "estimated_duration": "Weeks 4-6",
                    "description": "Learn classic and modern visual composition: Rule of Thirds, leading lines, framing within frames, negative space, color harmony, and perspective.",
                    "why_it_matters": "Technical proficiency means nothing without strong composition. Great framing turns ordinary scenes into captivating, emotionally resonant stories.",
                    "what_to_practice": "Walk a 1-mile route and take 30 photos focusing solely on finding leading lines and geometric patterns in everyday architecture and nature.",
                    "suggested_projects": "1. Street & Architecture Visual Symphony Essay.\n2. Storytelling Photo Essay (A Day in the Life of a Local Artisan).",
                    "tasks": [
                        {"title": "Leading Lines, Symmetry & Golden Ratio", "type": "topic", "desc": "Direct the viewer's eye through the frame using natural and architectural lines."},
                        {"title": "Framing, Foreground Layers & Depth", "type": "topic", "desc": "Use foreground elements to create a 3D sense of depth in 2D photographs."},
                        {"title": "Color Theory & Emotional Atmosphere", "type": "topic", "desc": "Use complementary, monochromatic, and analogous color schemes intentionally."},
                        {"title": "One Lens 100 Shots Challenge", "type": "practice", "desc": "Shoot an entire afternoon using only a single prime focal length (e.g. 50mm or 35mm)."},
                        {"title": "Project: 10-Photo Visual Narrative", "type": "project", "desc": "Produce a cohesive photo story documenting a subject from establishing shot to intimate detail."}
                    ]
                },
                {
                    "title": "Stage 3 — Mastering Natural & Artificial Lighting",
                    "estimated_duration": "Weeks 7-9",
                    "description": "Work with Golden Hour, Blue Hour, harsh midday shadows, reflectors, off-camera speedlights, softboxes, and light modifiers.",
                    "why_it_matters": "Photography literally means 'drawing with light'. Mastering direction, quality (hard vs soft), and color of light is the hallmark of a professional.",
                    "what_to_practice": "Practice 5 portrait lighting patterns: Rembrandt, Loop, Split, Butterfly, and Rim lighting using a single light and reflector.",
                    "suggested_projects": "1. Golden Hour vs Twilight Comparative Portrait Album.\n2. Studio-style Product & Still Life Series with controlled lighting.",
                    "tasks": [
                        {"title": "Qualities of Light: Direction, Hardness & Falloff", "type": "topic", "desc": "Understand the Inverse Square Law, diffusion, and light bounce."},
                        {"title": "Golden Hour & Natural Light Modifiers", "type": "topic", "desc": "Use 5-in-1 reflectors, diffusers, and environmental shade effectively."},
                        {"title": "Introduction to Flash & Speedlights", "type": "topic", "desc": "Learn flash sync speed, TTL vs manual flash, and off-camera triggers."},
                        {"title": "Rembrandt Lighting Drill", "type": "practice", "desc": "Set up a 45-degree key light to achieve the signature triangle under the subject's eye."},
                        {"title": "Project: 5-Style Lighting Showcase", "type": "project", "desc": "Shoot and present 5 distinct lighting styles on the same subject with lighting diagrams."}
                    ]
                },
                {
                    "title": "Stage 4 — Digital Post-Processing & Workflow (Lightroom / Photoshop)",
                    "estimated_duration": "Weeks 10-12",
                    "description": "Develop a professional RAW cataloging, color grading, tone curve adjustments, selective masking, skin retouching, and printing workflow.",
                    "why_it_matters": "Post-processing is the modern digital darkroom. It elevates your raw capture into your distinctive, signature artistic style.",
                    "what_to_practice": "Grade 20 photos with consistent color palettes; practice frequency separation for clean, natural portrait skin retouching.",
                    "suggested_projects": "1. Curated Online Portfolio Website.\n2. Self-published Printed Photo Book or Zine.",
                    "tasks": [
                        {"title": "RAW Catalog Management & Culling Workflow", "type": "topic", "desc": "Establish star ratings, color labels, collections, and automated backup strategies."},
                        {"title": "Tone Curve & Color Grading Mastery", "type": "topic", "desc": "Use HSL sliders, calibration, and color wheels for cohesive artistic tones."},
                        {"title": "Advanced Masking & Non-Destructive Editing", "type": "topic", "desc": "Master AI subject/sky selection, luminance masks, and radial gradients."},
                        {"title": "Speed Grading Drill", "type": "practice", "desc": "Edit a 30-image batch in under 20 minutes maintaining color uniformity."},
                        {"title": "Project: Professional Online Portfolio & Print Collection", "type": "project", "desc": "Curate and launch a high-resolution online portfolio highlighting your top 20 images."}
                    ]
                }
            ]
        },
        "financial investing": {
            "stages": [
                {
                    "title": "Stage 1 — Financial Literacy & Personal Cash Flow Foundation",
                    "estimated_duration": "Weeks 1-4",
                    "description": "Understand emergency funds, debt management, compound interest mathematics, budgeting frameworks (50/30/20), and inflation dynamics.",
                    "why_it_matters": "You cannot build a sustainable investment portfolio on a shaky financial foundation. Eliminating high-interest debt and establishing safety buffers comes first.",
                    "what_to_practice": "Audit the past 6 months of expenses; calculate your personal net worth; model 20-year compound interest curves with varied return rates.",
                    "suggested_projects": "1. Comprehensive Personal Financial Blueprint & Cash Flow Model.\n2. Debt Payoff & Savings Optimization Plan.",
                    "tasks": [
                        {"title": "Compound Interest, Inflation & Time Horizon", "type": "topic", "desc": "Learn how the Rule of 72 works and why time in the market beats timing the market."},
                        {"title": "Budgeting Systems & Emergency Fund Architecture", "type": "topic", "desc": "Design a 3-6 month liquid safety reserve in high-yield instruments."},
                        {"title": "Debt Prioritization: Avalanche vs Snowball", "type": "topic", "desc": "Strategize high-interest elimination before deploying capital to volatile assets."},
                        {"title": "Build a Compound Growth Calculator", "type": "practice", "desc": "Model monthly contributions across 10, 20, and 30 years with dividend reinvestment."},
                        {"title": "Project: Personal Financial Audit & 1-Year Budget Plan", "type": "project", "desc": "Create a structured spreadsheet tracking income, fixed costs, savings rate, and goals."}
                    ]
                },
                {
                    "title": "Stage 2 — Asset Classes, Market Mechanics & Index Funds",
                    "estimated_duration": "Weeks 5-8",
                    "description": "Learn the mechanics of Equities (Stocks), Fixed Income (Bonds), Real Estate (REITs), Commodities, and low-cost Broad-Market Index Funds/ETFs.",
                    "why_it_matters": "Broad-market index funds allow passive investors to capture market returns with low expense ratios and minimal stress.",
                    "what_to_practice": "Compare expense ratios and historical drawdowns of total stock market ETFs (e.g. S&P 500, Total World) vs actively managed funds.",
                    "suggested_projects": "1. Core 3-Fund Lazy Portfolio Allocation Model.\n2. Tax-Advantaged Account Strategy Map (401k/IRA/ISA).",
                    "tasks": [
                        {"title": "Stock Market Fundamentals & How Exchanges Work", "type": "topic", "desc": "Understand market caps, dividends, IPOs, market orders, and limit orders."},
                        {"title": "Bonds, Yields & Interest Rate Relationships", "type": "topic", "desc": "Learn how bond prices fluctuate inversely with central bank interest rates."},
                        {"title": "ETFs vs Mutual Funds vs Individual Stocks", "type": "topic", "desc": "Analyze expense ratios, liquidity, tracking errors, and tax efficiency."},
                        {"title": "Analyze 3 Major Index Funds", "type": "practice", "desc": "Examine top holdings, sector weighting, and historical risk-adjusted returns."},
                        {"title": "Project: Customized Asset Allocation Strategy", "type": "project", "desc": "Design a personalized diversified portfolio aligned with your specific risk tolerance."}
                    ]
                },
                {
                    "title": "Stage 3 — Fundamental Analysis & Valuation Principles",
                    "estimated_duration": "Weeks 9-14",
                    "description": "Learn how to read financial statements: Income Statement, Balance Sheet, and Cash Flow Statement. Understand P/E, P/B, ROE, Free Cash Flow, and Moats.",
                    "why_it_matters": "If you invest in individual businesses, understanding how to read financial statements is the only way to distinguish quality companies from speculative traps.",
                    "what_to_practice": "Read 2 annual reports (10-K filings); calculate free cash flow and debt-to-equity for a chosen enterprise.",
                    "suggested_projects": "1. In-depth Equity Valuation Report on a publicly traded company.\n2. Competitive Moat Analysis comparing two industry leaders.",
                    "tasks": [
                        {"title": "Reading the Three Financial Statements", "type": "topic", "desc": "Learn how revenue turns into net income and flows into cash balance."},
                        {"title": "Key Valuation Multiples & Financial Ratios", "type": "topic", "desc": "Understand P/E, EV/EBITDA, Free Cash Flow yield, and Return on Invested Capital (ROIC)."},
                        {"title": "Economic Moats & Competitive Advantages", "type": "topic", "desc": "Identify network effects, cost advantages, switching costs, and brand power."},
                        {"title": "Financial Statement Extraction Drill", "type": "practice", "desc": "Extract 5 years of revenue and free cash flow for an enterprise to assess trends."},
                        {"title": "Project: 10-Page Company Investment Memo", "type": "project", "desc": "Write a structured investment thesis detailing risks, valuation, and growth drivers."}
                    ]
                },
                {
                    "title": "Stage 4 — Risk Management, Portfolio Rebalancing & Psychology",
                    "estimated_duration": "Weeks 15-18",
                    "description": "Master behavioral finance, avoiding emotional panic selling, Dollar-Cost Averaging (DCA), periodic portfolio rebalancing, and tax harvesting.",
                    "why_it_matters": "The investor's chief enemy is almost always their own psychology during market corrections. Systematizing your process protects long-term wealth.",
                    "what_to_practice": "Establish an automated monthly investment schedule; create a strict Rebalancing Checklist for quarterly reviews.",
                    "suggested_projects": "1. Comprehensive Personal Investment Policy Statement (IPS).\n2. Long-term Wealth Dashboard with retirement projection scenarios.",
                    "tasks": [
                        {"title": "Behavioral Finance & Cognitive Biases", "type": "topic", "desc": "Overcome loss aversion, recency bias, FOMO, and herd mentality."},
                        {"title": "Dollar Cost Averaging vs Lump Sum Investing", "type": "topic", "desc": "Understand the statistical advantages and psychological benefits of automated contributions."},
                        {"title": "Portfolio Rebalancing & Risk Drift Management", "type": "topic", "desc": "Learn threshold-based vs calendar-based rebalancing strategies."},
                        {"title": "Draft a Personal 'Market Crash Action Protocol'", "type": "practice", "desc": "Write clear written rules for what actions to take when markets drop 20% or more."},
                        {"title": "Project: Written Investment Policy Statement (IPS)", "type": "project", "desc": "Finalize your personal rulebook defining asset limits, buying cadence, and withdrawal criteria."}
                    ]
                }
            ]
        }
    }

    @classmethod
    def generate_roadmap(
        cls,
        domain: str,
        current_level: str,
        goal: str,
        available_time: str,
        duration: str,
        existing_skills: str = "",
        user_name: str = "Learner",
        mentor: str = "auto"
    ) -> Dict[str, Any]:
        """
        Main entry point for roadmap synthesis.
        Attempts LLM generation if configured, otherwise uses the intelligent domain synthesis engine.
        """
        domain_clean = domain.strip().lower()

        # Auto-select mentor based on domain if "auto" is chosen
        selected_mentor = mentor
        if mentor == "auto":
            selected_mentor = cls._select_mentor_for_domain(domain)

        # Check if an API key is available in environment
        gemini_api_key = os.environ.get("GEMINI_API_KEY")
        openai_api_key = os.environ.get("OPENAI_API_KEY")

        if gemini_api_key:
            try:
                llm_result = cls._call_gemini_api(
                    gemini_api_key, domain, current_level, goal, available_time, duration, existing_skills, user_name
                )
                if llm_result:
                    llm_result["selected_mentor"] = selected_mentor
                    llm_result["mentor_greeting"] = cls._generate_mentor_greeting(selected_mentor, user_name, domain, goal)
                    return llm_result
            except Exception as e:
                print(f"[TA Junior AI] Gemini API failed, falling back to heuristic engine: {e}")

        # Intelligent Built-in Universal Synthesis Engine
        result = cls._synthesize_universal_roadmap(
            domain, current_level, goal, available_time, duration, existing_skills, user_name
        )
        result["selected_mentor"] = selected_mentor
        result["mentor_greeting"] = cls._generate_mentor_greeting(selected_mentor, user_name, domain, goal)
        return result

    @classmethod
    def _synthesize_universal_roadmap(
        cls,
        domain: str,
        current_level: str,
        goal: str,
        available_time: str,
        duration: str,
        existing_skills: str,
        user_name: str
    ) -> Dict[str, Any]:
        """
        Synthesizes a rich, personalized roadmap for ANY domain with TA Junior's friendly persona.
        """
        domain_key = domain.strip().lower()
        
        # Friendly personalized greeting & advice
        greeting = cls._generate_friendly_greeting(user_name, domain, goal, current_level)
        advice = cls._generate_supportive_advice(current_level, available_time, duration, existing_skills)

        # Check if we have a deep blueprint for this exact or matching domain
        blueprint_match = None
        for key, bp in cls.DOMAIN_BLUEPRINTS.items():
            if key in domain_key or domain_key in key:
                blueprint_match = bp
                break

        if blueprint_match:
            stages_data = cls._adapt_blueprint_to_user(
                blueprint_match["stages"], current_level, duration, available_time, goal
            )
        else:
            stages_data = cls._generate_dynamic_domain_stages(
                domain, current_level, goal, available_time, duration, existing_skills
            )

        return {
            "greeting_message": greeting,
            "junior_advice": advice,
            "stages": stages_data,
            "total_estimated_stages": len(stages_data),
        }

    @classmethod
    def _generate_friendly_greeting(cls, name: str, domain: str, goal: str, level: str) -> str:
        name_display = name if name and name.lower() != 'learner' else 'Friend'
        return (
            f"Hello {name_display}! 👋 I'm **TA Junior**, your personal learning companion. "
            f"I'm super excited to help you conquer **{domain}** and reach your goal of *'{goal}'*! "
            f"Starting at the **{level}** level is fantastic—we'll break everything down step-by-step so you never feel overwhelmed."
        )

    @classmethod
    def _generate_supportive_advice(cls, level: str, available_time: str, duration: str, existing_skills: str) -> str:
        skills_note = f" Since you already have some background with *{existing_skills}*, we'll leverage that strength to help you move faster!" if existing_skills.strip() else ""
        
        advice_text = (
            f"🌟 **TA Junior's Golden Advice:**\n\n"
            f"With **{available_time}** over **{duration}**, consistency will be your greatest superpower.{skills_note}\n\n"
            f"• **Don't rush to master everything on day one.** Learning is like building muscle—it grows with steady, daily practice.\n"
            f"• **Celebrate small wins.** Every completed topic and mini-exercise gets you closer to your goal.\n"
            f"• **Build as you learn.** Don't just read or watch tutorials; get your hands dirty with the suggested practice drills and projects.\n\n"
            f"Whenever you feel stuck, take a deep breath. I'm right here with you on this journey!"
        )
        return advice_text

    @classmethod
    def _adapt_blueprint_to_user(
        cls,
        blueprint_stages: List[Dict[str, Any]],
        level: str,
        duration: str,
        time_per_day: str,
        goal: str
    ) -> List[Dict[str, Any]]:
        """
        Adapts pre-crafted stages according to user level (skipping basics if advanced) and timeframe.
        """
        stages = [dict(s) for s in blueprint_stages]
        
        # If user is Intermediate or Advanced, adjust first stage note
        if "Intermediate" in level or "Advanced" in level:
            if len(stages) > 0:
                stages[0]["title"] += " (Rapid Review & Knowledge Calibration)"
                stages[0]["description"] = f"A quick calibration stage to ensure zero gaps in fundamentals before diving into advanced topics for your goal: {goal}."

        return stages

    @classmethod
    def _generate_dynamic_domain_stages(
        cls,
        domain: str,
        level: str,
        goal: str,
        available_time: str,
        duration: str,
        existing_skills: str
    ) -> List[Dict[str, Any]]:
        """
        Universal dynamic curriculum engine for ANY custom or novel domain (Music, Cooking, Game Dev, Biology, Marketing, etc.).
        Produces 5 coherent, progressive stages tailored to the domain and goal.
        """
        d_clean = domain.strip().title()
        
        stages = [
            {
                "title": f"Stage 1 — {d_clean} Foundations & Core Principles",
                "estimated_duration": "Weeks 1-4",
                "description": f"Master the fundamental vocabulary, tools, core theories, and essential mental models of {d_clean}.",
                "why_it_matters": f"Without strong foundations in {d_clean}, advanced concepts will feel confusing and frustrating. A solid base gives you confidence to solve real problems.",
                "what_to_practice": f"Daily 20-minute drill practicing fundamental {d_clean} exercises; document your key takeaways in a personal learning journal.",
                "suggested_projects": f"1. 'Foundations Primer' — A structured breakdown of top 10 core concepts in {d_clean}.\n2. Mini starter exercise putting initial principles to test.",
                "tasks": [
                    {"title": f"Core Terminology & Mental Models of {d_clean}", "type": "topic", "desc": f"Understand the language, primary concepts, and rules that govern {d_clean}."},
                    {"title": f"Essential Tools & Environment Setup for {d_clean}", "type": "topic", "desc": f"Configure your workspace, tools, and software/materials needed for daily practice."},
                    {"title": "Foundational Principles & Best Practices", "type": "topic", "desc": f"Learn the time-tested rules and standard standards used by experienced practitioners."},
                    {"title": "Hands-on Starter Drill", "type": "practice", "desc": f"Complete your very first hands-on exercise applying Stage 1 principles."},
                    {"title": f"Project: {d_clean} Fundamentals Milestone", "type": "project", "desc": f"Create a tangible initial artifact demonstrating mastery of basics in {d_clean}."}
                ]
            },
            {
                "title": f"Stage 2 — Essential Techniques & Practical Workflows in {d_clean}",
                "estimated_duration": "Weeks 5-8",
                "description": f"Transition from theory into practical execution. Learn the standard workflows, methods, and routines used by practitioners in {d_clean}.",
                "why_it_matters": f"Understanding how different techniques combine in {d_clean} allows you to work independently without constantly relying on step-by-step guides.",
                "what_to_practice": f"Build 3 small practical exercises applying standard {d_clean} workflows; critique and refine your own work.",
                "suggested_projects": f"1. Practical Case Study / Applied Exercise in {d_clean}.\n2. Component / Asset Library for future use.",
                "tasks": [
                    {"title": f"Core Techniques & Execution Methods in {d_clean}", "type": "topic", "desc": f"Deep dive into the primary techniques that drive results in {d_clean}."},
                    {"title": "Quality Standards & Common Pitfalls to Avoid", "type": "topic", "desc": f"Study the most common beginner mistakes in {d_clean} and learn how to identify them early."},
                    {"title": "Workflow Optimization & Productivity Habits", "type": "topic", "desc": f"Structure your working process so you can iterate quickly and cleanly."},
                    {"title": "Intermediate Technique Drill", "type": "practice", "desc": f"Practice executing the core technique under timed conditions."},
                    {"title": f"Project: Applied {d_clean} Case Study", "type": "project", "desc": f"Execute an end-to-end task from initial plan to polished deliverable."}
                ]
            },
            {
                "title": f"Stage 3 — Advanced Strategies & Specialized Problem Solving",
                "estimated_duration": "Weeks 9-14",
                "description": f"Tackle complex scenarios, advanced nuances, edge cases, and specialized sub-disciplines within {d_clean}.",
                "why_it_matters": f"To reach your goal of '{goal}', you must be able to solve ambiguous, non-standard challenges where simple tutorials are not enough.",
                "what_to_practice": f"Analyze complex real-world examples in {d_clean}; deconstruct and reverse-engineer work done by top industry leaders.",
                "suggested_projects": f"1. Complex Multi-Stage Problem Solver in {d_clean}.\n2. Deep-dive Analytical Report or Custom Creation.",
                "tasks": [
                    {"title": f"Advanced Problem Decomposition in {d_clean}", "type": "topic", "desc": f"Break down multifaceted, high-difficulty challenges into manageable components."},
                    {"title": "Specialized Tools, Systems & Advanced Nuances", "type": "topic", "desc": f"Explore advanced tools and specialized techniques tailored for '{goal}'."},
                    {"title": "Performance, Optimization & Critical Analysis", "type": "topic", "desc": f"Evaluate outcomes rigorously using metrics and feedback loops."},
                    {"title": "Advanced Problem Drill", "type": "practice", "desc": "Solve a challenging, simulated real-world prompt without external hints."},
                    {"title": f"Project: Advanced Solution Prototype", "type": "project", "desc": f"Design and execute a high-level project showcasing deep competence in {d_clean}."}
                ]
            },
            {
                "title": f"Stage 4 — Real-World Capstone & Portfolio Development",
                "estimated_duration": "Weeks 15-20",
                "description": f"Synthesize everything learned into a substantial, publication-ready capstone project directly aligned with: '{goal}'.",
                "why_it_matters": f"A comprehensive capstone project serves as indisputable proof of your skills to employers, clients, collaborators, or peers.",
                "what_to_practice": f"Polish your work to industry standards; seek constructive feedback from communities or mentors; refine based on reviews.",
                "suggested_projects": f"1. Complete Comprehensive Capstone for '{goal}'.\n2. Public Portfolio / Case Study Presentation.",
                "tasks": [
                    {"title": "Capstone Scoping, Planning & Milestone Design", "type": "topic", "desc": f"Plan every phase of your final showcase project aligned with '{goal}'."},
                    {"title": "End-to-End Execution & Integration", "type": "topic", "desc": f"Build out the complete system/deliverable with attention to detail and polish."},
                    {"title": "Review, Polish & Feedback Iteration", "type": "topic", "desc": "Run through checklists and refine edges based on feedback."},
                    {"title": "Documentation & Case Study Writing", "type": "practice", "desc": f"Write an engaging summary explaining your process, challenges overcome, and results."},
                    {"title": f"Project: Major Capstone Showcase for '{goal}'", "type": "project", "desc": f"A flagship, high-impact project demonstrating readiness for '{goal}'."}
                ]
            },
            {
                "title": f"Stage 5 — Professional Growth, Networking & Next Horizons",
                "estimated_duration": "Weeks 21-24",
                "description": f"Take your expertise into the world: build your network, share your knowledge, stay updated on trends, and establish long-term mastery.",
                "why_it_matters": f"Learning never stops. Knowing how to maintain momentum, connect with other enthusiasts, and stay current ensures lasting success.",
                "what_to_practice": f"Share one piece of learning publicly each week; participate actively in {d_clean} discussions and community forums.",
                "suggested_projects": f"1. Public Resource Guide or Tutorial for Beginners.\n2. Personal Career / Growth Roadmap for the next 2 years.",
                "tasks": [
                    {"title": f"Community Engagement & Industry Networking in {d_clean}", "type": "topic", "desc": f"Discover where practitioners hang out, join discussions, and find mentors."},
                    {"title": "Continuous Learning Habits & Trend Tracking", "type": "topic", "desc": f"Curate newsletters, journals, and sources to keep your {d_clean} knowledge fresh."},
                    {"title": "Sharing Knowledge & Teaching Others", "type": "topic", "desc": "Solidify your mastery by explaining complex concepts to newcomers."},
                    {"title": "Professional Pitch / Bio Drill", "type": "practice", "desc": f"Draft your elevator pitch and portfolio presentation for '{goal}'."},
                    {"title": f"Project: Final Launch & Roadmap Graduation", "type": "project", "desc": f"Celebrate your completed journey and publish your roadmap portfolio!"}
                ]
            }
        ]
        return stages

    @classmethod
    def _call_gemini_api(
        cls,
        api_key: str,
        domain: str,
        level: str,
        goal: str,
        available_time: str,
        duration: str,
        existing_skills: str,
        user_name: str
    ) -> Dict[str, Any]:
        """
        Optional connector to Google Gemini API when GEMINI_API_KEY is provided in environment.
        """
        import urllib.request
        
        prompt = f"""
You are TA Junior, a kind, friendly, supportive AI assistant helping a learner create a personalized roadmap.
Domain: {domain}
Current Level: {level}
Goal: {goal}
Available Time: {available_time}
Duration: {duration}
Existing Skills: {existing_skills}
User Name: {user_name}

Personality:
- Kind, encouraging, speaks naturally.
- Breaks down large goals into small steps.
- Gives practical advice.
- Never judges.

Return ONLY a valid JSON object matching this schema:
{{
  "greeting_message": "Friendly greeting mentioning user and their goal warmly.",
  "junior_advice": "Supportive practical advice tailored to their time and level.",
  "stages": [
    {{
      "title": "Stage 1 — ...",
      "estimated_duration": "Weeks 1-4",
      "description": "Overview of stage",
      "why_it_matters": "Why this stage is important",
      "what_to_practice": "Practical drills",
      "suggested_projects": "Suggested project ideas",
      "tasks": [
        {{"title": "Topic title", "type": "topic", "desc": "Short description"}},
        {{"title": "Practice drill", "type": "practice", "desc": "Short description"}},
        {{"title": "Project title", "type": "project", "desc": "Short description"}}
      ]
    }}
  ]
}}
"""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        payload = json.dumps({
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"response_mime_type": "application/json"}
        }).encode('utf-8')

        req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=12) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            text_content = res_data['candidates'][0]['content']['parts'][0]['text']
            parsed_json = json.loads(text_content)
            return parsed_json

    @classmethod
    def ask_ta_junior_for_stage_help(cls, stage_title: str, question: str, domain: str) -> str:
        """
        Interactive Q&A support from TA Junior for a specific stage or question.
        """
        supportive_intro = "I'm right here to help you understand this! 😊"
        
        q_lower = question.lower()
        if "stuck" in q_lower or "hard" in q_lower or "difficult" in q_lower or "confused" in q_lower:
            return (
                f"{supportive_intro}\n\n"
                f"When working on **{stage_title}** in **{domain}**, it's completely natural to hit a roadblock. "
                f"Here is how I recommend breaking it down:\n\n"
                f"1. **Isolate the smallest step:** Try tackling just 1 single sub-concept or 10 lines of practice rather than the whole stage.\n"
                f"2. **Explain it out loud:** Try explaining what you're trying to do as if you're explaining it to a friend.\n"
                f"3. **Take a 15-minute break:** Stepping away gives your brain time to synthesize new information.\n\n"
                f"You're doing great—keep going one step at a time! — TA Junior 🌱"
            )
        elif "project" in q_lower or "idea" in q_lower:
            return (
                f"{supportive_intro}\n\n"
                f"For **{stage_title}**, the best project is something you genuinely find fun or useful! "
                f"Try creating a mini-tool that solves a tiny annoyance in your daily routine, or a showcase piece you can proudly show friends. "
                f"Remember, a finished simple project is 10x better than an unfinished complex one! — TA Junior 🌱"
            )
        else:
            return (
                f"{supportive_intro}\n\n"
                f"Regarding **'{question}'** in **{stage_title}**:\n\n"
                f"The key concept here is to connect this directly back to your overall {domain} goal. "
                f"Focus on the practical 'Why it matters' section of this stage and try applying it to a tiny 15-minute practice drill today. "
                f"Consistency and small experiments will make it click! — TA Junior 🌱"
            )

    @classmethod
    def get_odin_wisdom(cls, domain: str, goal: str, level: str = "Beginner") -> str:
        """
        Odin's strategic, long-term Allfather wisdom for the learner.
        """
        return (
            f"👁️ **Allfather Odin's Strategic Vision for {domain}:**\n\n"
            f"True mastery is forged not through haste, but through seeing the whole battlefield before striking. "
            f"To achieve *'{goal}'*, your mind must perceive the interconnected runes of {domain} from the highest vantage point of Hlidskjalf.\n\n"
            f"• **The First Sacrifice:** Sacrifice the illusion that you can learn everything overnight. Focus deeply on foundational principles.\n"
            f"• **The Ravens' Counsel:** Let Huginn (Thought) analyze theory, but let Muninn (Memory) anchor it through repetitive application.\n"
            f"• **The Long Horizon:** Keep your eye fixed on the overarching vision. Temporary setbacks are merely the fog before dawn."
        )

    @classmethod
    def get_thor_challenge(cls, stage_title: str, domain: str) -> str:
        """
        Thor's thunderous daily practice challenge & battle-tested grit.
        """
        return (
            f"⚡ **Thor's Thunder Drill for {stage_title}:**\n\n"
            f"By Mjolnir! Reading scrolls alone will not build your strength in {domain}! You must strike the anvil and forge real muscle!\n\n"
            f"• **The Heavy Lift Drill:** Dedicate 25 uninterrupted minutes right now with zero distractions. No switching tabs, no idle scrolling.\n"
            f"• **Break the Obstacle:** When an exercise feels too difficult, don't retreat—break it into 3 smaller strikes until the wall shatters.\n"
            f"• **Warrior Discipline:** Consistency is your lightning strike. Strike daily, and no barrier in {domain} will withstand you!"
        )

    @classmethod
    def get_loki_hack(cls, stage_title: str, domain: str) -> str:
        """
        Loki's clever shortcuts, mental models, and creative debugging hacks.
        """
        return (
            f"🐍 **Loki's Clever Hack for {stage_title}:**\n\n"
            f"Why march through the front gates in heavy armor when there's a side door wide open? Let's be smart about {domain}.\n\n"
            f"• **The Inversion Trick:** Instead of asking *'How do I master this perfectly?'*, ask *'What are the 3 dumbest mistakes beginners make here?'* Avoid those 3, and you're already in the top 20%.\n"
            f"• **The 80/20 Shifter:** 80% of real-world results in {domain} come from just 20% of core patterns. Find those 20% first and automate or look up the rest.\n"
            f"• **Playful Mischief:** Build something ridiculous or funny with today's concept. Curiosity and fun will teach your brain faster than any dry textbook!"
        )

    @classmethod
    def get_pantheon_council(cls, domain: str, goal: str) -> Dict[str, str]:
        """
        Returns full council perspectives from Odin, Thor, Loki, and TA Junior.
        """
        return {
            "odin": cls.get_odin_wisdom(domain, goal),
            "thor": cls.get_thor_challenge("Foundations & Active Practice", domain),
            "loki": cls.get_loki_hack("Smart Learning & Creative Hacks", domain),
            "ta_junior": (
                f"🌱 **TA Junior's Cheerful Note:**\n\n"
                f"The gods offer incredible power and wisdom, but remember: I'm always right here beside you to break every single day into gentle, friendly steps. You've got this!"
            )
        }

    @classmethod
    def _select_mentor_for_domain(cls, domain: str) -> str:
        """
        Intelligently select a mentor based on the domain type.
        """
        domain_lower = domain.strip().lower()
        
        # Career, long-term planning, leadership, strategy -> ODIN
        career_keywords = ['career', 'business', 'entrepreneurship', 'finance', 'investing', 'leadership', 'management', 'strategy', 'planning']
        if any(kw in domain_lower for kw in career_keywords):
            return 'odin'
        
        # Practical skills, projects, coding, execution -> THOR
        practical_keywords = ['programming', 'coding', 'python', 'web', 'development', 'data', 'engineering', 'django', 'project', 'build', 'execution']
        if any(kw in domain_lower for kw in practical_keywords):
            return 'thor'
        
        # Creative subjects, arts, innovation -> LOKI
        creative_keywords = ['photography', 'art', 'music', 'design', 'creative', 'writing', 'innovation', 'ui/ux', 'design']
        if any(kw in domain_lower for kw in creative_keywords):
            return 'loki'
        
        # Default to THOR for action-oriented topics
        return 'thor'

    @classmethod
    def _generate_mentor_greeting(cls, mentor: str, user_name: str, domain: str, goal: str) -> str:
        """
        Generate a personalized mentor greeting based on selected mentor.
        """
        name_display = user_name if user_name and user_name.lower() != 'learner' else 'Traveler'
        
        if mentor == 'odin':
            return (
                f"👁️ **Allfather Odin speaks:**\n\n"
                f"Welcome, {name_display}. I have gazed from Hlidskjalf and seen your path toward **{goal}** in the realm of **{domain}**. "
                f"A worthy ambition. Let us forge a strategic vision—one that requires sacrifice of hasty impulses, yet yields lasting mastery. "
                f"Trust in patience. Trust in consistency. And the victory shall be yours."
            )
        elif mentor == 'loki':
            return (
                f"🐍 **Loki grins mischievously:**\n\n"
                f"Ah, {name_display}! So you wish to master **{domain}** and achieve *'{goal}'*, yes? How delightfully ambitious! "
                f"I have a secret for you: most learners trudge the long boring path. But not you—I'll show you the clever shortcuts, the hidden side doors, "
                f"and the mental tricks that make experts look effortless. Ready to break the mold?"
            )
        else:  # thor
            return (
                f"⚡ **Thor booms with enthusiasm:**\n\n"
                f"By Mjolnir, {name_display}! Your quest to conquer **{domain}** and achieve *'{goal}'* is exactly what I love—ACTION! "
                f"Forget the endless philosophizing. We'll strike hard, build real skills, complete projects that matter, and celebrate each victory! "
                f"Ready to get to work? Let's forge your destiny together!"
            )

