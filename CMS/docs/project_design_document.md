# CMS Project Design Document

## 1. Project Overview
The CMS project is a simple content management system for managing articles. It allows users to create, view, and manage article content through a web application. The system uses Django for backend logic and React for the frontend experience.

## 2. Problem Statement
The current system provides a basic article listing and detail view, but it needs a more modern and scalable frontend architecture. The goal is to separate concerns by using Django as the backend API provider and React as the interactive frontend, while preserving the existing CMS functionality.

## 3. Functional Requirements
- Users can view a list of articles.
- Users can open an article to read its full content.
- Articles should display their title, content, and creation date.
- Admin users can access the Django admin panel.
- The frontend should communicate with the backend through API endpoints.
- The application should support navigation between the article list and article details.

## 4. Non-functional Requirements
- The system should be easy to maintain and extend.
- The application should respond quickly for basic article operations.
- The frontend should be responsive and user-friendly.
- The system should support future growth with additional CMS features.
- The application should follow a clean separation between backend and frontend layers.

## 5. User Roles
- Admin: Manages content through Django admin and oversees the CMS.
- Viewer: Reads published articles through the web interface.

## 6. Assumptions
- The project will continue using Django as the backend framework.
- React will be used for the client-side interface.
- Articles are stored in a relational database.
- The system will run in a local development environment initially.

## 7. Scope of the Project
In scope:
- Article listing page
- Article detail page
- Django REST-style JSON API
- React frontend integration
- Basic admin access

Out of scope:
- User authentication and authorization beyond admin access
- Advanced content editor
- Role-based content management workflows
- Multi-language support

---

## 8. High-Level Architecture Diagram
```text
User Browser
   |
   v
React Frontend
   |
   v
Django Views / API Layer
   |
   v
Database (SQLite)
```

## 9. Component Diagram
```text
+-------------------+
| React Frontend    |
| - HomePage        |
| - ArticleDetail   |
| - Navbar          |
+-------------------+
          |
          v
+-------------------+
| Django Backend    |
| - Views           |
| - URL Routes      |
| - API Endpoints   |
+-------------------+
          |
          v
+-------------------+
| Database          |
| - Article Model   |
+-------------------+
```

## 10. Database ER Diagram
```text
Article
---------
| id (PK) |
| title   |
| content |
| created_at |
| updated_at |
```

## 11. Application Flow Diagram
```text
User opens homepage
   |
   v
React requests article list from Django API
   |
   v
Django returns article data
   |
   v
React renders article cards
   |
   v
User clicks an article
   |
   v
React requests article details from Django API
   |
   v
Django returns article details
   |
   v
React displays full article page
```
