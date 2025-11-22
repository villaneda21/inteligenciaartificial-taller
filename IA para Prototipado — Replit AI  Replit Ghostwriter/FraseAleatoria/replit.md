# Overview

This is a motivational quotes web application built with Flask. It displays random Spanish motivational phrases to users through a simple, elegant web interface. The application serves a single-page frontend that fetches random quotes from a REST API endpoint.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Technology**: Vanilla HTML/CSS/JavaScript (no framework)
- **Design Pattern**: Single-page application with client-side rendering
- **Styling**: Custom CSS with gradient backgrounds and responsive design
- **UI Components**: Simple container-based layout with centered content display

## Backend Architecture
- **Framework**: Flask (Python web framework)
- **Pattern**: RESTful API with template rendering
- **Routes**:
  - `/` - Serves the main HTML page
  - `/api/frase` - JSON API endpoint for retrieving random quotes
- **Data Storage**: In-memory list of Spanish motivational quotes (no database)
- **Response Format**: JSON for API endpoints

## Design Decisions

### Why Flask?
- Lightweight and simple for small applications
- Built-in template rendering with Jinja2
- Easy to set up RESTful API endpoints
- No overhead from larger frameworks like Django

### Why In-Memory Storage?
- Dataset is static (20 motivational quotes)
- No need for persistence or user-generated content
- Simplifies deployment and eliminates database dependencies
- Fast access times for small datasets

### Why Client-Side Fetching?
- Reduces server load (client fetches quotes on demand)
- Enables smooth user interactions without page reloads
- Separates concerns between presentation and data retrieval

# External Dependencies

## Python Packages
- **Flask**: Web framework for routing and template rendering
- **random**: Standard library module for selecting random quotes

## Frontend Dependencies
- None - uses vanilla JavaScript and CSS without external libraries

## Development Environment
- **Host**: 0.0.0.0 (accessible from any network interface)
- **Port**: 5000
- **Debug Mode**: Enabled for development

## Notes
- No database required
- No authentication or user management
- No external API integrations
- Fully self-contained application