# TLK – Music Studio Booking Web Application  
### (Java, JSP, Servlets, AI Chatbot Integration)

TLK is a **Java-based web application** developed as part of a **group academic project**.  
It allows users to book music lessons, rehearsal sessions, and studio services through a web interface deployed on **Apache Tomcat**.

In addition to the standard booking workflow, the application integrates an **AI-powered chatbot** that assists users with navigation, booking decisions, availability checks, and appointment management.

---

## Project Context

- **Type:** Academic group project  
- **Backend:** Java, JSP, Servlets, JDBC  
- **Frontend:** HTML, CSS, JavaScript  
- **Server:** Apache Tomcat  
- **Database:** MySQL  

> While this was a group project, the **AI chatbot feature, its backend integration, and prompt design were fully implemented by me**.

---

## Core Application Features

### Booking System
- User registration and authentication
- Secure session management
- Booking of rehearsal and music sessions
- Date and time validation
- Prevention of double booking
- Appointment cancellation and management

### AI Chatbot (Key Contribution)
The chatbot is embedded directly into the TLK platform and acts as an **intelligent booking assistant**, not a standalone chat application.

It improves usability by allowing users to interact with the system using **natural language**, instead of navigating multiple pages manually.

---

##  Chatbot Architecture & AI Integration

### API Integration (OpenRouter)

The chatbot is integrated using the **OpenRouter API**, which provides access to multiple Large Language Models (LLMs) through a unified interface.

- API communication is handled server-side
- The API key is stored securely (not exposed in frontend code)
- Requests are dynamically built using real application context (services, schedules, user state)

This approach allows flexibility and avoids tight coupling to a single AI provider.

---

### Model Selection Strategy

The selected model was:

**`deepseek/deepseek-chat-v3-0324`**

**Reasons for choosing this model:**
- Strong natural language understanding
- Good performance on structured, task-oriented conversations
- Lower cost compared to larger models
- Fast response time suitable for real-time web applications
- Consistent behavior when constrained by contextual prompts

The model is used **as an assistant**, not as a source of truth.  
All factual responses are driven by **backend logic and database queries**, not by the model alone.

---

### Prompt Engineering & Context Control

To prevent hallucinations and ensure accuracy:

- The chatbot receives a **strictly controlled context**
- Business rules (opening hours, booking logic, authentication rules) are enforced server-side
- The model is instructed to answer **only using the provided context**
- User-specific data is included only when the user is authenticated

This ensures:
- Reliable answers
- Data privacy
- Predictable behavior

---

##  Stateless Chatbot Design (Intentional)

The chatbot is intentionally implemented as a **stateless conversational component**.

- No conversation history is stored
- Each request is processed independently
- Responses depend on real-time backend and database state

**Why this design was chosen:**
- Simpler architecture
- Easier debugging and maintenance
- No risk of leaking previous user context
- Suitable for academic and production-style environments

Any perceived continuity comes from consistent backend data, not stored memory.

---

##  Chatbot Demonstration (Extracted from Screenshots)

The following screenshots were captured directly from the running TLK application.  
They demonstrate **real chatbot interactions** and highlight the backend-driven logic behind each response.

### 1 Platform onboarding and explanation
**User question:**
> “I’m new here, how does TLK work?”

![Chatbot onboarding explanation](./screenshots/chatbot-01-onboarding.png)

**Demonstrates:**
- Natural language understanding
- Platform explanation
- User guidance

---

### 2 Booking guidance
**User question:**
> “How can I book a music lesson?”

![Chatbot booking assistance](./screenshots/chatbot-02-booking-help.png)

**Demonstrates:**
- Booking workflow awareness
- Business logic explanation
- Studio opening rules

---

### 3 Next appointment retrieval (authenticated user)
**User question:**
> “When is my next appointment?”

![Chatbot next appointment](./screenshots/chatbot-03-next-appointment.png)

**Demonstrates:**
- Database-backed responses
- User-specific data access
- Authentication-aware logic

---

### 4 Availability and conflict validation
**User question:**
> “Is it possible to schedule an appointment next Wednesday at 1 pm?”

![Chatbot availability check](./screenshots/chatbot-04-availability-check.png)

**Demonstrates:**
- Real-time availability checking
- Conflict detection
- Intelligent rejection with explanation

---

## Architecture Overview

- **Backend:** Java Servlets (MVC-style architecture)
- **Persistence:** JDBC with DAO pattern
- **Frontend:** JSP, HTML, CSS, JavaScript
- **AI Integration:** OpenRouter API (LLM-based assistant)
- **Deployment:** Apache Tomcat (WAR-based at runtime)

---

## Demo Video

 **TLK Project – AI Chatbot Design & Live Demonstration (Group Project)** 
https://youtu.be/9v_N2A6udBo

Throughout the video, I provide a detailed explanation of:
- the chatbot architecture and its integration within the TLK platform,
- the use of the OpenRouter API and the rationale behind the chosen language model,
- how the chatbot assists users with booking guidance, availability checks, and appointment-related questions.

---

## Author Contribution

- Chatbot architecture and AI integration
- OpenRouter API usage and configuration
- Model selection and evaluation
- Prompt engineering and context control
- Backend logic for booking, availability, and appointments
- Security-aware design (authentication-based responses)

---

## Why This Project Matters

TLK demonstrates:
- Real-world Java web development
- Backend-driven business logic
- Secure and structured AI integration
- Thoughtful architectural trade-offs
- Practical use of AI to enhance user experience (not replace logic)

---

## Technologies Used

Java • JSP • Servlets • JDBC • MySQL • Apache Tomcat  
HTML • CSS • JavaScript • OpenRouter API • LLM Integration