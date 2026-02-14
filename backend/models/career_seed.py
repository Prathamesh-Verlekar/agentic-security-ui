"""
Seed data for the Career Counselor feature — top 10 professions.
"""

from backend.models.schemas import Profession

PROFESSIONS: list[Profession] = [
    Profession(
        id="software-engineer",
        title="Software Engineer",
        short_description="Design, build, and maintain software systems that power the modern world — from mobile apps to cloud infrastructure.",
        icon_emoji="\U0001F4BB",
        tags=["Technology", "Engineering", "Problem-Solving", "Remote-Friendly"],
    ),
    Profession(
        id="data-scientist",
        title="Data Scientist",
        short_description="Extract insights from complex datasets using statistics, machine learning, and domain expertise to drive business decisions.",
        icon_emoji="\U0001F4CA",
        tags=["Analytics", "Machine Learning", "Statistics", "Research"],
    ),
    Profession(
        id="doctor-physician",
        title="Doctor / Physician",
        short_description="Diagnose and treat illnesses, promote preventive care, and improve patient health outcomes across medical specialties.",
        icon_emoji="\U0001FA7A",
        tags=["Healthcare", "Medicine", "Patient Care", "Science"],
    ),
    Profession(
        id="lawyer",
        title="Lawyer",
        short_description="Advise clients on legal matters, represent them in court, and navigate complex regulatory frameworks to protect rights.",
        icon_emoji="\U00002696",
        tags=["Law", "Advocacy", "Critical Thinking", "Negotiation"],
    ),
    Profession(
        id="financial-analyst",
        title="Financial Analyst",
        short_description="Evaluate financial data, market trends, and investment opportunities to guide organizations in making sound fiscal decisions.",
        icon_emoji="\U0001F4B9",
        tags=["Finance", "Analysis", "Investment", "Economics"],
    ),
    Profession(
        id="ux-designer",
        title="UX / Graphic Designer",
        short_description="Craft intuitive user experiences and compelling visual designs that bridge the gap between people and technology.",
        icon_emoji="\U0001F3A8",
        tags=["Design", "Creativity", "User Research", "Visual Arts"],
    ),
    Profession(
        id="mechanical-engineer",
        title="Mechanical Engineer",
        short_description="Design, analyze, and manufacture mechanical systems — from engines and robotics to renewable energy devices.",
        icon_emoji="\U00002699",
        tags=["Engineering", "Manufacturing", "CAD", "Physics"],
    ),
    Profession(
        id="marketing-manager",
        title="Marketing Manager",
        short_description="Develop and execute marketing strategies that build brand awareness, engage audiences, and drive revenue growth.",
        icon_emoji="\U0001F4E3",
        tags=["Marketing", "Strategy", "Branding", "Digital Media"],
    ),
    Profession(
        id="teacher-educator",
        title="Teacher / Educator",
        short_description="Inspire and empower learners of all ages by creating engaging curricula, fostering critical thinking, and shaping future generations.",
        icon_emoji="\U0001F4DA",
        tags=["Education", "Mentoring", "Curriculum Design", "Leadership"],
    ),
    Profession(
        id="product-manager",
        title="Product Manager",
        short_description="Define product vision, prioritize features, and coordinate cross-functional teams to deliver solutions that users love.",
        icon_emoji="\U0001F680",
        tags=["Product", "Strategy", "Leadership", "User-Centric"],
    ),
]

# Quick lookup dicts
PROFESSIONS_BY_ID: dict[str, Profession] = {p.id: p for p in PROFESSIONS}
ALL_PROFESSION_IDS: list[str] = [p.id for p in PROFESSIONS]


# ---------------------------------------------------------------------------
# Career Transition Edges — realistic cross-profession switches
# ---------------------------------------------------------------------------
from backend.models.schemas import CareerTransitionEdge  # noqa: E402

CAREER_TRANSITIONS: list[CareerTransitionEdge] = [
    # Software Engineer transitions
    CareerTransitionEdge(id="se-ds", source="software-engineer", target="data-scientist", label="ML & analytics skills", stage="Mid-Career", difficulty="moderate"),
    CareerTransitionEdge(id="se-pm", source="software-engineer", target="product-manager", label="Tech leadership path", stage="Senior", difficulty="easy"),
    CareerTransitionEdge(id="se-ux", source="software-engineer", target="ux-designer", label="Frontend to UX pivot", stage="Mid-Career", difficulty="moderate"),
    CareerTransitionEdge(id="se-me", source="software-engineer", target="mechanical-engineer", label="IoT / embedded systems", stage="Early-Career", difficulty="hard"),

    # Data Scientist transitions
    CareerTransitionEdge(id="ds-se", source="data-scientist", target="software-engineer", label="ML engineering focus", stage="Mid-Career", difficulty="easy"),
    CareerTransitionEdge(id="ds-fa", source="data-scientist", target="financial-analyst", label="Quantitative finance", stage="Mid-Career", difficulty="moderate"),
    CareerTransitionEdge(id="ds-pm", source="data-scientist", target="product-manager", label="Data-driven product", stage="Senior", difficulty="moderate"),
    CareerTransitionEdge(id="ds-mm", source="data-scientist", target="marketing-manager", label="Growth analytics", stage="Mid-Career", difficulty="moderate"),

    # Doctor / Physician transitions
    CareerTransitionEdge(id="dr-te", source="doctor-physician", target="teacher-educator", label="Medical education", stage="Senior", difficulty="easy"),
    CareerTransitionEdge(id="dr-ds", source="doctor-physician", target="data-scientist", label="Health informatics", stage="Mid-Career", difficulty="hard"),
    CareerTransitionEdge(id="dr-pm", source="doctor-physician", target="product-manager", label="HealthTech product", stage="Senior", difficulty="moderate"),

    # Lawyer transitions
    CareerTransitionEdge(id="lw-pm", source="lawyer", target="product-manager", label="Legal-tech leadership", stage="Senior", difficulty="moderate"),
    CareerTransitionEdge(id="lw-fa", source="lawyer", target="financial-analyst", label="Corporate finance", stage="Mid-Career", difficulty="moderate"),
    CareerTransitionEdge(id="lw-mm", source="lawyer", target="marketing-manager", label="Brand & compliance", stage="Mid-Career", difficulty="moderate"),
    CareerTransitionEdge(id="lw-te", source="lawyer", target="teacher-educator", label="Law professor", stage="Senior", difficulty="easy"),

    # Financial Analyst transitions
    CareerTransitionEdge(id="fa-ds", source="financial-analyst", target="data-scientist", label="Quantitative modeling", stage="Mid-Career", difficulty="moderate"),
    CareerTransitionEdge(id="fa-pm", source="financial-analyst", target="product-manager", label="FinTech product", stage="Senior", difficulty="moderate"),
    CareerTransitionEdge(id="fa-mm", source="financial-analyst", target="marketing-manager", label="Market strategy", stage="Mid-Career", difficulty="easy"),

    # UX / Graphic Designer transitions
    CareerTransitionEdge(id="ux-se", source="ux-designer", target="software-engineer", label="Design engineering", stage="Mid-Career", difficulty="moderate"),
    CareerTransitionEdge(id="ux-pm", source="ux-designer", target="product-manager", label="Design-led product", stage="Senior", difficulty="easy"),
    CareerTransitionEdge(id="ux-mm", source="ux-designer", target="marketing-manager", label="Brand & creative", stage="Mid-Career", difficulty="easy"),

    # Mechanical Engineer transitions
    CareerTransitionEdge(id="me-se", source="mechanical-engineer", target="software-engineer", label="CAD / simulation code", stage="Early-Career", difficulty="moderate"),
    CareerTransitionEdge(id="me-pm", source="mechanical-engineer", target="product-manager", label="Hardware product lead", stage="Senior", difficulty="moderate"),
    CareerTransitionEdge(id="me-ds", source="mechanical-engineer", target="data-scientist", label="Sensor / IoT data", stage="Mid-Career", difficulty="hard"),

    # Marketing Manager transitions
    CareerTransitionEdge(id="mm-pm", source="marketing-manager", target="product-manager", label="Product marketing", stage="Senior", difficulty="easy"),
    CareerTransitionEdge(id="mm-ux", source="marketing-manager", target="ux-designer", label="User research pivot", stage="Mid-Career", difficulty="moderate"),
    CareerTransitionEdge(id="mm-ds", source="marketing-manager", target="data-scientist", label="MarTech analytics", stage="Mid-Career", difficulty="hard"),

    # Teacher / Educator transitions
    CareerTransitionEdge(id="te-ux", source="teacher-educator", target="ux-designer", label="Instructional design", stage="Mid-Career", difficulty="moderate"),
    CareerTransitionEdge(id="te-pm", source="teacher-educator", target="product-manager", label="EdTech product", stage="Mid-Career", difficulty="moderate"),
    CareerTransitionEdge(id="te-mm", source="teacher-educator", target="marketing-manager", label="Content & community", stage="Mid-Career", difficulty="moderate"),

    # Product Manager transitions
    CareerTransitionEdge(id="pm-se", source="product-manager", target="software-engineer", label="Technical PM return", stage="Mid-Career", difficulty="moderate"),
    CareerTransitionEdge(id="pm-mm", source="product-manager", target="marketing-manager", label="Go-to-market focus", stage="Senior", difficulty="easy"),
    CareerTransitionEdge(id="pm-ux", source="product-manager", target="ux-designer", label="Product design", stage="Mid-Career", difficulty="moderate"),
    CareerTransitionEdge(id="pm-fa", source="product-manager", target="financial-analyst", label="Business analytics", stage="Senior", difficulty="moderate"),
]
