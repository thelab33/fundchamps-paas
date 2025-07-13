# starforge-saas/app/config/team_config.py

TEAM_CONFIG = {
    "team_name": "Connect ATX Elite",
    "location": "Austin, TX",
    "logo": "images/logo.webp",
    "contact_email": "info@connectatxelite.org",
    "instagram": "https://instagram.com/connectatxelite",
    "is_trial": True,
    "fundraising_goal": 10000,
    "amount_raised": 7850,
    "brand_color": "amber-400",
    "about": [
        "Connect ATX Elite is a community-powered, non-profit 12U AAU basketball program based in Austin, TX.",
        "We develop skilled athletes, but also confident, disciplined, and academically driven young leaders.",
    ],
    "players": [
        {"name": "Andre", "role": "Guard"},
        {"name": "Jordan", "role": "Forward"},
        {"name": "Malik", "role": "Center"},
        {"name": "CJ", "role": "Guard"},
        {"name": "Terrance", "role": "Forward"},
    ],
    "impact_stats": [
        {"label": "Players Enrolled", "value": 16},
        {"label": "Honor Roll Scholars", "value": 11},
        {"label": "Tournaments Played", "value": 12},
        {"label": "Years Running", "value": 3},
    ],
    # 💡 Add more dynamic fields as needed to power your templates and dashboard widgets
}
