# Team-specific configuration (overrides from environment variables or default values)
TEAM_CONFIG = {
    # Basic Team Info
    "team_name": "Connect ATX Elite",
    "about_heading": "About Connect ATX Elite",
    "about_text": "Family-run AAU program turning East Austin students into honor-roll athletes and leaders.",
    "about_poster": "connect-atx-team.jpg",  # Default team image
    "cta_label": "Join Our Champion Circle",
    "cta_url": "mailto:connectatxelite@gmail.com",
    # Impact Stats
    "impact_stats": [
        {"label": "Players Enrolled", "value": 16},
        {"label": "Honor Roll Scholars", "value": 11},
    ],
    # Challenge Info
    "challenge_heading": "The Challenge We Face",
    "challenge_text": "Despite our passion, we struggle with gym space. Sponsorships make it possible for our youth to train, grow, and succeed.",
    "funding_label": "Gym Rental Funding",
    "challenge_cta_label": "Sponsor a Practice",
    "challenge_testimonial_text": "Without enough court time, our team can't develop their potential.",
    "challenge_testimonial_author": "Team Parent, Class of 2030",
    "challenge_testimonial_detail": "We missed practices last season due to lack of funding for gym rentals. Sponsors make all the difference!",
    # Mission Info
    "mission_heading": "Our Mission",
    "mission_text": "Empowering the next generation through basketball, academics, and leadership.",
    "mission_poster": "connect-atx-team-poster.jpg",
    "mission_bg_video": "mission-bg.mp4",
    "mission_story_btn_label": "Read Our Story",
    "mission_share_label": "Share Mission",
    "mission_stories": [
        {
            "text": "“Basketball taught my son confidence and leadership.”",
            "meta": "Maria R.",
            "title": "Parent",
        },
        {
            "text": "“The team helped me stay on track in school.”",
            "meta": "David L.",
            "title": "Class of 2026",
        },
    ],
    # Fundraising
    "fundraising_goal": 10000,
    "amount_raised": 0,  # This could be dynamically populated by your fundraising system
    "stripe_key": "your-stripe-api-key-here",
    # Example Sponsors
    "sponsors": [
        {"name": "Company A", "amount": 500, "status": "approved"},
        {"name": "Company B", "amount": 1000, "status": "approved"},
        {"name": "Company C", "amount": 250, "status": "pending"},
    ],
    # Featured Sponsors (as logos or images)
    "featured_logos": [
        {"src": "images/sponsor_a_logo.png", "alt": "Company A"},
        {"src": "images/sponsor_b_logo.png", "alt": "Company B"},
        {"src": "images/sponsor_c_logo.png", "alt": "Company C"},
    ],
    # Additional Configurable Information (optional)
    "nav_links": [
        ("about", "About"),
        ("challenge", "Challenge"),
        ("sponsor-wall-wrapper", "Sponsors"),
        ("testimonials", "Testimonials"),
        ("contact", "Contact"),
    ],
}
