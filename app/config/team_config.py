import os

# Team-specific configuration (overrides from environment variables or default values)
TEAM_CONFIG = {
    # Basic Team Info
    "team_name": os.getenv("TEAM_NAME", "Connect ATX Elite"),
    "about_heading": os.getenv("ABOUT_HEADING", "About Connect ATX Elite"),
    "about_text": os.getenv(
        "ABOUT_TEXT",
        "Family-run AAU program turning East Austin students into honor-roll athletes and leaders.",
    ),
    "about_poster": os.getenv("ABOUT_POSTER", "connect-atx-team.jpg"),  # Default team image
    "cta_label": os.getenv("CTA_LABEL", "Join Our Champion Circle"),
    "cta_url": os.getenv("CTA_URL", "mailto:connectatxelite@gmail.com"),
    
    # Impact Stats
    "impact_stats": [
        {"label": "Players Enrolled", "value": int(os.getenv("IMPACT_PLAYERS", 16))},
        {"label": "Honor Roll Scholars", "value": int(os.getenv("IMPACT_SCHOLARS", 11))},
    ],
    
    # Challenge Info
    "challenge_heading": os.getenv("CHALLENGE_HEADING", "The Challenge We Face"),
    "challenge_text": os.getenv(
        "CHALLENGE_TEXT",
        "Despite our passion, we struggle with gym space. Sponsorships make it possible for our youth to train, grow, and succeed.",
    ),
    "funding_label": os.getenv("FUNDING_LABEL", "Gym Rental Funding"),
    "challenge_cta_label": os.getenv("CHALLENGE_CTA_LABEL", "Sponsor a Practice"),
    "challenge_testimonial_text": os.getenv(
        "CHALLENGE_TESTIMONIAL_TEXT", "Without enough court time, our team can't develop their potential."
    ),
    "challenge_testimonial_author": os.getenv("CHALLENGE_TESTIMONIAL_AUTHOR", "Team Parent, Class of 2030"),
    "challenge_testimonial_detail": os.getenv(
        "CHALLENGE_TESTIMONIAL_DETAIL",
        "We missed practices last season due to lack of funding for gym rentals. Sponsors make all the difference!",
    ),
    
    # Mission Info
    "mission_heading": os.getenv("MISSION_HEADING", "Our Mission"),
    "mission_text": os.getenv("MISSION_TEXT", "Empowering the next generation through basketball, academics, and leadership."),
    "mission_poster": os.getenv("MISSION_POSTER", "connect-atx-team-poster.jpg"),
    "mission_bg_video": os.getenv("MISSION_BG_VIDEO", "mission-bg.mp4"),
    "mission_story_btn_label": os.getenv("MISSION_STORY_BTN_LABEL", "Read Our Story"),
    "mission_share_label": os.getenv("MISSION_SHARE_LABEL", "Share Mission"),
    
    # Mission stories (can be set through environment variables as a fallback)
    "mission_stories": [
        {
            "text": os.getenv("MISSION_STORY_1_TEXT", "“Basketball taught my son confidence and leadership.”"),
            "meta": os.getenv("MISSION_STORY_1_META", "Maria R."),
            "title": os.getenv("MISSION_STORY_1_TITLE", "Parent"),
        },
        {
            "text": os.getenv("MISSION_STORY_2_TEXT", "“The team helped me stay on track in school.”"),
            "meta": os.getenv("MISSION_STORY_2_META", "David L."),
            "title": os.getenv("MISSION_STORY_2_TITLE", "Class of 2026"),
        },
    ],
    
    # Fundraising
    "fundraising_goal": int(os.getenv("FUNDRAISING_GOAL", 10000)),
    "amount_raised": int(os.getenv("AMOUNT_RAISED", 0)),  # Dynamically populate if needed
    "stripe_key": os.getenv("STRIPE_KEY", "your-stripe-api-key-here"),
    
    # Example Sponsors
    "sponsors": [
        {"name": os.getenv("SPONSOR_1_NAME", "Company A"), "amount": int(os.getenv("SPONSOR_1_AMOUNT", 500)), "status": "approved"},
        {"name": os.getenv("SPONSOR_2_NAME", "Company B"), "amount": int(os.getenv("SPONSOR_2_AMOUNT", 1000)), "status": "approved"},
        {"name": os.getenv("SPONSOR_3_NAME", "Company C"), "amount": int(os.getenv("SPONSOR_3_AMOUNT", 250)), "status": "pending"},
    ],
    
    # Featured Sponsors (as logos or images)
    "featured_logos": [
        {"src": os.getenv("SPONSOR_1_LOGO", "images/sponsor_a_logo.png"), "alt": "Company A"},
        {"src": os.getenv("SPONSOR_2_LOGO", "images/sponsor_b_logo.png"), "alt": "Company B"},
        {"src": os.getenv("SPONSOR_3_LOGO", "images/sponsor_c_logo.png"), "alt": "Company C"},
    ],
    
    # Additional Configurable Information (optional)
    "nav_links": [
        ("about", os.getenv("NAV_ABOUT", "About")),
        ("challenge", os.getenv("NAV_CHALLENGE", "Challenge")),
        ("sponsor-wall-wrapper", os.getenv("NAV_SPONSORS", "Sponsors")),
        ("testimonials", os.getenv("NAV_TESTIMONIALS", "Testimonials")),
        ("contact", os.getenv("NAV_CONTACT", "Contact")),
    ],
}

