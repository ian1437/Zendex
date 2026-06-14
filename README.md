# Zendex

Zendex is a desktop ticket management application built with Python and SQLite for organizing customer onboarding, installation, scheduling, and completion workflows.

The application provides a centralized interface for tracking customer information, work orders, shipping status, installation tickets, and ticket progression through multiple stages.

## Features

- Create and manage customer tickets
- Track onboarding and installation workflows
- Generate install tickets from existing handoff tickets
- Manage work order numbers and tracking information
- Update ticket status throughout the installation lifecycle
- Store ticket information locally using SQLite
- Simple desktop interface built with Tkinter

## Workflow

Tickets move through several stages:

1. Open Tickets
2. Onboarding
3. Install
4. Scheduled
5. Complete

Users can:

- Create new tickets
- Edit ticket information
- Track shipping status
- Assign customer service actions
- Create installation tickets
- Add notes and updates
- Delete completed or unnecessary tickets

---

## Technologies Used

- Python
- Tkinter
- Tkcalendar
- SQLite
- SQL

## Database

The application uses a local SQLite database: 

PR_Tickets.db

This database stores:

- Customer information
- Ticket details
- Order information
- Shipping status
- Installation records
- Notes and updates

---

## Installation

### Clone the repository

```bash
git clone https://github.com/ian1437/Zendex.git
cd Zendex