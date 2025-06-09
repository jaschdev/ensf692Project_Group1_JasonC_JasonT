"""
main.py

Entry point of the ENSF 692 Spring 2025 final project.

This script coordinates the overall program execution, including loading data,
getting user input, performing analysis, and exporting results.

Responsibilities:
- Call all main functions in proper order
- Ensure no global variables are used
- Document structure clearly with inline comments

Note:
This file must be executable from the terminal and should orchestrate the full program.
"""

from .data_loader import load_data
from .user_interface import get_user_input
from .analysis import perform_analysis
from .visualization import create_plot


def main():
    dr = load_data()
    perform_analysis(df)

if __name__ == "__main__":
    main()