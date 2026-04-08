"""
Modern styling configuration for the GUI
"""
from .config import COLORS, FONT_FAMILY, FONT_SIZES


def get_primary_button_style():
    """Style for primary action buttons"""
    return {
        'bg': COLORS['primary'],
        'fg': 'white',
        'font': (FONT_FAMILY, FONT_SIZES['normal'], 'bold'),
        'padx': 25,
        'pady': 10,
        'cursor': 'hand2',
        'relief': 'flat',
        'bd': 0,
        'activebackground': COLORS['primary_dark'],
        'activeforeground': 'white'
    }


def get_secondary_button_style():
    """Style for secondary buttons"""
    return {
        'bg': COLORS['secondary'],
        'fg': 'white',
        'font': (FONT_FAMILY, FONT_SIZES['normal'], 'bold'),
        'padx': 20,
        'pady': 8,
        'cursor': 'hand2',
        'relief': 'flat',
        'bd': 0
    }


def get_danger_button_style():
    """Style for danger/clear buttons"""
    return {
        'bg': COLORS['danger'],
        'fg': 'white',
        'font': (FONT_FAMILY, FONT_SIZES['normal'], 'bold'),
        'padx': 20,
        'pady': 8,
        'cursor': 'hand2',
        'relief': 'flat',
        'bd': 0
    }


def get_success_button_style():
    """Style for success/export buttons"""
    return {
        'bg': COLORS['success'],
        'fg': 'white',
        'font': (FONT_FAMILY, FONT_SIZES['normal'], 'bold'),
        'padx': 20,
        'pady': 8,
        'cursor': 'hand2',
        'relief': 'flat',
        'bd': 0
    }


def get_card_style():
    """Style for card frames - returns a dictionary without bg"""
    return {
        'relief': 'flat',
        'bd': 1,
        'highlightbackground': COLORS['border'],
        'highlightthickness': 1
    }


def get_entry_style():
    """Style for entry fields"""
    return {
        'font': (FONT_FAMILY, FONT_SIZES['normal']),
        'bg': COLORS['light'],
        'relief': 'flat',
        'bd': 1,
        'highlightthickness': 0
    }


def get_label_style():
    """Style for labels"""
    return {
        'font': (FONT_FAMILY, FONT_SIZES['normal']),
        'bg': 'white',
        'anchor': 'w'
    }


def get_title_style():
    """Style for main title"""
    return {
        'font': (FONT_FAMILY, FONT_SIZES['title'], 'bold'),
        'fg': COLORS['primary'],
        'bg': 'white',
        'pady': 15
    }


def get_heading_style():
    """Style for section headings"""
    return {
        'font': (FONT_FAMILY, FONT_SIZES['heading'], 'bold'),
        'fg': COLORS['dark'],
        'bg': 'white'
    }


def get_result_card_style(prediction):
    """Style for result card based on prediction"""
    if prediction == 1:
        return {
            'bg': '#ffebee',
            'fg': COLORS['danger'],
            'border_color': COLORS['danger']
        }
    else:
        return {
            'bg': '#e8f5e9',
            'fg': COLORS['success'],
            'border_color': COLORS['success']
        }