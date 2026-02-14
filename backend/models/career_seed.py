"""
Seed data for the Career Counselor feature — 20 professions with transition edges.
"""

from backend.models.schemas import Profession, CareerTransitionEdge

PROFESSIONS: list[Profession] = [
    # ── Technology & Engineering ──────────────────────────────────────────────
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
        id="cybersecurity-analyst",
        title="Cybersecurity Analyst",
        short_description="Protect organizations from cyber threats by monitoring systems, investigating breaches, and implementing security protocols.",
        icon_emoji="\U0001F510",
        tags=["Security", "Technology", "Risk Management", "Networking"],
    ),
    Profession(
        id="devops-engineer",
        title="DevOps / Cloud Engineer",
        short_description="Bridge development and operations by automating deployments, managing cloud infrastructure, and ensuring system reliability.",
        icon_emoji="\U00002601",
        tags=["Cloud", "Automation", "Infrastructure", "CI/CD"],
    ),
    Profession(
        id="mechanical-engineer",
        title="Mechanical Engineer",
        short_description="Design, analyze, and manufacture mechanical systems — from engines and robotics to renewable energy devices.",
        icon_emoji="\U00002699",
        tags=["Engineering", "Manufacturing", "CAD", "Physics"],
    ),

    # ── Business & Finance ────────────────────────────────────────────────────
    Profession(
        id="product-manager",
        title="Product Manager",
        short_description="Define product vision, prioritize features, and coordinate cross-functional teams to deliver solutions that users love.",
        icon_emoji="\U0001F680",
        tags=["Product", "Strategy", "Leadership", "User-Centric"],
    ),
    Profession(
        id="financial-analyst",
        title="Financial Analyst",
        short_description="Evaluate financial data, market trends, and investment opportunities to guide organizations in making sound fiscal decisions.",
        icon_emoji="\U0001F4B9",
        tags=["Finance", "Analysis", "Investment", "Economics"],
    ),
    Profession(
        id="management-consultant",
        title="Management Consultant",
        short_description="Help organizations solve complex business problems, improve performance, and implement strategic change initiatives.",
        icon_emoji="\U0001F4BC",
        tags=["Strategy", "Consulting", "Business", "Problem-Solving"],
    ),
    Profession(
        id="entrepreneur",
        title="Entrepreneur / Founder",
        short_description="Build and scale new businesses by identifying market opportunities, securing funding, and leading teams through uncertainty.",
        icon_emoji="\U0001F4A1",
        tags=["Startup", "Leadership", "Innovation", "Risk-Taking"],
    ),

    # ── Creative & Design ─────────────────────────────────────────────────────
    Profession(
        id="ux-designer",
        title="UX / Graphic Designer",
        short_description="Craft intuitive user experiences and compelling visual designs that bridge the gap between people and technology.",
        icon_emoji="\U0001F3A8",
        tags=["Design", "Creativity", "User Research", "Visual Arts"],
    ),
    Profession(
        id="marketing-manager",
        title="Marketing Manager",
        short_description="Develop and execute marketing strategies that build brand awareness, engage audiences, and drive revenue growth.",
        icon_emoji="\U0001F4E3",
        tags=["Marketing", "Strategy", "Branding", "Digital Media"],
    ),
    Profession(
        id="content-creator",
        title="Content Creator / Writer",
        short_description="Produce engaging written, visual, or multimedia content for digital platforms, brands, and media organizations.",
        icon_emoji="\U0000270D",
        tags=["Writing", "Creativity", "Social Media", "Storytelling"],
    ),

    # ── Healthcare & Science ──────────────────────────────────────────────────
    Profession(
        id="doctor-physician",
        title="Doctor / Physician",
        short_description="Diagnose and treat illnesses, promote preventive care, and improve patient health outcomes across medical specialties.",
        icon_emoji="\U0001FA7A",
        tags=["Healthcare", "Medicine", "Patient Care", "Science"],
    ),
    Profession(
        id="pharmacist",
        title="Pharmacist",
        short_description="Dispense medications, advise patients on drug interactions, and collaborate with healthcare teams to ensure safe treatments.",
        icon_emoji="\U0001F48A",
        tags=["Healthcare", "Pharmacy", "Chemistry", "Patient Safety"],
    ),
    Profession(
        id="research-scientist",
        title="Research Scientist",
        short_description="Conduct experiments, analyze data, and publish findings that advance human knowledge in fields from biology to physics.",
        icon_emoji="\U0001F52C",
        tags=["Research", "Science", "Academia", "Innovation"],
    ),

    # ── Law & Public Service ──────────────────────────────────────────────────
    Profession(
        id="lawyer",
        title="Lawyer",
        short_description="Advise clients on legal matters, represent them in court, and navigate complex regulatory frameworks to protect rights.",
        icon_emoji="\U00002696",
        tags=["Law", "Advocacy", "Critical Thinking", "Negotiation"],
    ),

    # ── Education ─────────────────────────────────────────────────────────────
    Profession(
        id="teacher-educator",
        title="Teacher / Educator",
        short_description="Inspire and empower learners of all ages by creating engaging curricula, fostering critical thinking, and shaping future generations.",
        icon_emoji="\U0001F4DA",
        tags=["Education", "Mentoring", "Curriculum Design", "Leadership"],
    ),

    # ── Trades & Emerging ─────────────────────────────────────────────────────
    Profession(
        id="architect",
        title="Architect",
        short_description="Design buildings and spaces that are functional, sustainable, and aesthetically striking — from homes to skyscrapers.",
        icon_emoji="\U0001F3D7",
        tags=["Architecture", "Design", "Engineering", "Sustainability"],
    ),
    Profession(
        id="hr-manager",
        title="HR Manager",
        short_description="Recruit talent, shape company culture, manage employee relations, and drive organizational development strategies.",
        icon_emoji="\U0001F465",
        tags=["Human Resources", "People", "Culture", "Recruitment"],
    ),
    Profession(
        id="project-manager",
        title="Project Manager",
        short_description="Plan, execute, and deliver projects on time and on budget by coordinating teams, managing risks, and tracking milestones.",
        icon_emoji="\U0001F4CB",
        tags=["Management", "Planning", "Agile", "Coordination"],
    ),
]

# Quick lookup dicts
PROFESSIONS_BY_ID: dict[str, Profession] = {p.id: p for p in PROFESSIONS}
ALL_PROFESSION_IDS: list[str] = [p.id for p in PROFESSIONS]


# ---------------------------------------------------------------------------
# Career Transition Edges — realistic cross-profession switches
# ---------------------------------------------------------------------------

CAREER_TRANSITIONS: list[CareerTransitionEdge] = [
    # Software Engineer
    CareerTransitionEdge(id="se-ds", source="software-engineer", target="data-scientist", label="ML & analytics skills", stage="Mid-Career", difficulty="moderate"),
    CareerTransitionEdge(id="se-pm", source="software-engineer", target="product-manager", label="Tech leadership path", stage="Senior", difficulty="easy"),
    CareerTransitionEdge(id="se-ux", source="software-engineer", target="ux-designer", label="Frontend to UX pivot", stage="Mid-Career", difficulty="moderate"),
    CareerTransitionEdge(id="se-dv", source="software-engineer", target="devops-engineer", label="Infrastructure focus", stage="Mid-Career", difficulty="easy"),
    CareerTransitionEdge(id="se-cy", source="software-engineer", target="cybersecurity-analyst", label="AppSec specialization", stage="Mid-Career", difficulty="moderate"),
    CareerTransitionEdge(id="se-en", source="software-engineer", target="entrepreneur", label="Tech founder path", stage="Senior", difficulty="moderate"),
    CareerTransitionEdge(id="se-pj", source="software-engineer", target="project-manager", label="Tech lead to PM", stage="Senior", difficulty="easy"),

    # Data Scientist
    CareerTransitionEdge(id="ds-se", source="data-scientist", target="software-engineer", label="ML engineering focus", stage="Mid-Career", difficulty="easy"),
    CareerTransitionEdge(id="ds-fa", source="data-scientist", target="financial-analyst", label="Quantitative finance", stage="Mid-Career", difficulty="moderate"),
    CareerTransitionEdge(id="ds-pm", source="data-scientist", target="product-manager", label="Data-driven product", stage="Senior", difficulty="moderate"),
    CareerTransitionEdge(id="ds-mm", source="data-scientist", target="marketing-manager", label="Growth analytics", stage="Mid-Career", difficulty="moderate"),
    CareerTransitionEdge(id="ds-rs", source="data-scientist", target="research-scientist", label="Research focus", stage="Mid-Career", difficulty="moderate"),
    CareerTransitionEdge(id="ds-mc", source="data-scientist", target="management-consultant", label="Analytics consulting", stage="Senior", difficulty="moderate"),

    # Cybersecurity Analyst
    CareerTransitionEdge(id="cy-se", source="cybersecurity-analyst", target="software-engineer", label="Secure development", stage="Mid-Career", difficulty="moderate"),
    CareerTransitionEdge(id="cy-dv", source="cybersecurity-analyst", target="devops-engineer", label="SecOps pipeline", stage="Mid-Career", difficulty="easy"),
    CareerTransitionEdge(id="cy-mc", source="cybersecurity-analyst", target="management-consultant", label="Security consulting", stage="Senior", difficulty="moderate"),
    CareerTransitionEdge(id="cy-pj", source="cybersecurity-analyst", target="project-manager", label="Security program lead", stage="Senior", difficulty="easy"),

    # DevOps / Cloud Engineer
    CareerTransitionEdge(id="dv-se", source="devops-engineer", target="software-engineer", label="Platform engineering", stage="Mid-Career", difficulty="easy"),
    CareerTransitionEdge(id="dv-cy", source="devops-engineer", target="cybersecurity-analyst", label="Cloud security", stage="Mid-Career", difficulty="moderate"),
    CareerTransitionEdge(id="dv-pj", source="devops-engineer", target="project-manager", label="Infra project lead", stage="Senior", difficulty="easy"),
    CareerTransitionEdge(id="dv-mc", source="devops-engineer", target="management-consultant", label="Cloud consulting", stage="Senior", difficulty="moderate"),

    # Mechanical Engineer
    CareerTransitionEdge(id="me-se", source="mechanical-engineer", target="software-engineer", label="CAD / simulation code", stage="Early-Career", difficulty="moderate"),
    CareerTransitionEdge(id="me-pm", source="mechanical-engineer", target="product-manager", label="Hardware product lead", stage="Senior", difficulty="moderate"),
    CareerTransitionEdge(id="me-ds", source="mechanical-engineer", target="data-scientist", label="Sensor / IoT data", stage="Mid-Career", difficulty="hard"),
    CareerTransitionEdge(id="me-ar", source="mechanical-engineer", target="architect", label="Structural engineering", stage="Mid-Career", difficulty="moderate"),
    CareerTransitionEdge(id="me-pj", source="mechanical-engineer", target="project-manager", label="Engineering PM", stage="Senior", difficulty="easy"),

    # Product Manager
    CareerTransitionEdge(id="pm-se", source="product-manager", target="software-engineer", label="Technical PM return", stage="Mid-Career", difficulty="moderate"),
    CareerTransitionEdge(id="pm-mm", source="product-manager", target="marketing-manager", label="Go-to-market focus", stage="Senior", difficulty="easy"),
    CareerTransitionEdge(id="pm-ux", source="product-manager", target="ux-designer", label="Product design", stage="Mid-Career", difficulty="moderate"),
    CareerTransitionEdge(id="pm-en", source="product-manager", target="entrepreneur", label="Startup founder", stage="Senior", difficulty="moderate"),
    CareerTransitionEdge(id="pm-mc", source="product-manager", target="management-consultant", label="Strategy consulting", stage="Senior", difficulty="easy"),
    CareerTransitionEdge(id="pm-fa", source="product-manager", target="financial-analyst", label="Business analytics", stage="Senior", difficulty="moderate"),

    # Financial Analyst
    CareerTransitionEdge(id="fa-ds", source="financial-analyst", target="data-scientist", label="Quantitative modeling", stage="Mid-Career", difficulty="moderate"),
    CareerTransitionEdge(id="fa-pm", source="financial-analyst", target="product-manager", label="FinTech product", stage="Senior", difficulty="moderate"),
    CareerTransitionEdge(id="fa-mm", source="financial-analyst", target="marketing-manager", label="Market strategy", stage="Mid-Career", difficulty="easy"),
    CareerTransitionEdge(id="fa-mc", source="financial-analyst", target="management-consultant", label="Financial consulting", stage="Senior", difficulty="easy"),
    CareerTransitionEdge(id="fa-en", source="financial-analyst", target="entrepreneur", label="FinTech founder", stage="Senior", difficulty="hard"),

    # Management Consultant
    CareerTransitionEdge(id="mc-pm", source="management-consultant", target="product-manager", label="Product strategy", stage="Mid-Career", difficulty="easy"),
    CareerTransitionEdge(id="mc-en", source="management-consultant", target="entrepreneur", label="Startup advisory", stage="Senior", difficulty="moderate"),
    CareerTransitionEdge(id="mc-fa", source="management-consultant", target="financial-analyst", label="Corporate finance", stage="Mid-Career", difficulty="easy"),
    CareerTransitionEdge(id="mc-hr", source="management-consultant", target="hr-manager", label="Org development", stage="Senior", difficulty="moderate"),

    # Entrepreneur
    CareerTransitionEdge(id="en-pm", source="entrepreneur", target="product-manager", label="Product leadership", stage="Mid-Career", difficulty="easy"),
    CareerTransitionEdge(id="en-mc", source="entrepreneur", target="management-consultant", label="Advisory role", stage="Senior", difficulty="easy"),
    CareerTransitionEdge(id="en-mm", source="entrepreneur", target="marketing-manager", label="Growth marketing", stage="Mid-Career", difficulty="moderate"),
    CareerTransitionEdge(id="en-te", source="entrepreneur", target="teacher-educator", label="Startup mentoring", stage="Senior", difficulty="easy"),

    # UX / Graphic Designer
    CareerTransitionEdge(id="ux-se", source="ux-designer", target="software-engineer", label="Design engineering", stage="Mid-Career", difficulty="moderate"),
    CareerTransitionEdge(id="ux-pm", source="ux-designer", target="product-manager", label="Design-led product", stage="Senior", difficulty="easy"),
    CareerTransitionEdge(id="ux-mm", source="ux-designer", target="marketing-manager", label="Brand & creative", stage="Mid-Career", difficulty="easy"),
    CareerTransitionEdge(id="ux-cc", source="ux-designer", target="content-creator", label="Visual storytelling", stage="Mid-Career", difficulty="easy"),
    CareerTransitionEdge(id="ux-ar", source="ux-designer", target="architect", label="Spatial design", stage="Mid-Career", difficulty="hard"),

    # Marketing Manager
    CareerTransitionEdge(id="mm-pm", source="marketing-manager", target="product-manager", label="Product marketing", stage="Senior", difficulty="easy"),
    CareerTransitionEdge(id="mm-ux", source="marketing-manager", target="ux-designer", label="User research pivot", stage="Mid-Career", difficulty="moderate"),
    CareerTransitionEdge(id="mm-cc", source="marketing-manager", target="content-creator", label="Content strategy", stage="Mid-Career", difficulty="easy"),
    CareerTransitionEdge(id="mm-en", source="marketing-manager", target="entrepreneur", label="DTC brand founder", stage="Senior", difficulty="moderate"),
    CareerTransitionEdge(id="mm-hr", source="marketing-manager", target="hr-manager", label="Employer branding", stage="Senior", difficulty="moderate"),

    # Content Creator
    CareerTransitionEdge(id="cc-mm", source="content-creator", target="marketing-manager", label="Content marketing", stage="Mid-Career", difficulty="easy"),
    CareerTransitionEdge(id="cc-ux", source="content-creator", target="ux-designer", label="UX writing", stage="Mid-Career", difficulty="moderate"),
    CareerTransitionEdge(id="cc-te", source="content-creator", target="teacher-educator", label="Educational content", stage="Mid-Career", difficulty="easy"),
    CareerTransitionEdge(id="cc-en", source="content-creator", target="entrepreneur", label="Media business", stage="Senior", difficulty="moderate"),

    # Doctor / Physician
    CareerTransitionEdge(id="dr-te", source="doctor-physician", target="teacher-educator", label="Medical education", stage="Senior", difficulty="easy"),
    CareerTransitionEdge(id="dr-rs", source="doctor-physician", target="research-scientist", label="Clinical research", stage="Mid-Career", difficulty="easy"),
    CareerTransitionEdge(id="dr-pm", source="doctor-physician", target="product-manager", label="HealthTech product", stage="Senior", difficulty="moderate"),
    CareerTransitionEdge(id="dr-ph", source="doctor-physician", target="pharmacist", label="Pharma advisory", stage="Senior", difficulty="moderate"),
    CareerTransitionEdge(id="dr-mc", source="doctor-physician", target="management-consultant", label="Healthcare consulting", stage="Senior", difficulty="moderate"),

    # Pharmacist
    CareerTransitionEdge(id="ph-rs", source="pharmacist", target="research-scientist", label="Drug development", stage="Mid-Career", difficulty="moderate"),
    CareerTransitionEdge(id="ph-ds", source="pharmacist", target="data-scientist", label="Pharma analytics", stage="Mid-Career", difficulty="hard"),
    CareerTransitionEdge(id="ph-pm", source="pharmacist", target="product-manager", label="Pharma product", stage="Senior", difficulty="moderate"),
    CareerTransitionEdge(id="ph-te", source="pharmacist", target="teacher-educator", label="Pharmacy professor", stage="Senior", difficulty="easy"),

    # Research Scientist
    CareerTransitionEdge(id="rs-ds", source="research-scientist", target="data-scientist", label="Applied ML research", stage="Mid-Career", difficulty="easy"),
    CareerTransitionEdge(id="rs-te", source="research-scientist", target="teacher-educator", label="Academic teaching", stage="Senior", difficulty="easy"),
    CareerTransitionEdge(id="rs-pm", source="research-scientist", target="product-manager", label="R&D product lead", stage="Senior", difficulty="moderate"),
    CareerTransitionEdge(id="rs-en", source="research-scientist", target="entrepreneur", label="DeepTech startup", stage="Senior", difficulty="hard"),

    # Lawyer
    CareerTransitionEdge(id="lw-pm", source="lawyer", target="product-manager", label="Legal-tech leadership", stage="Senior", difficulty="moderate"),
    CareerTransitionEdge(id="lw-fa", source="lawyer", target="financial-analyst", label="Corporate finance", stage="Mid-Career", difficulty="moderate"),
    CareerTransitionEdge(id="lw-mc", source="lawyer", target="management-consultant", label="Legal consulting", stage="Senior", difficulty="easy"),
    CareerTransitionEdge(id="lw-te", source="lawyer", target="teacher-educator", label="Law professor", stage="Senior", difficulty="easy"),
    CareerTransitionEdge(id="lw-hr", source="lawyer", target="hr-manager", label="Employment law to HR", stage="Mid-Career", difficulty="moderate"),
    CareerTransitionEdge(id="lw-en", source="lawyer", target="entrepreneur", label="Legal-tech founder", stage="Senior", difficulty="hard"),

    # Teacher / Educator
    CareerTransitionEdge(id="te-ux", source="teacher-educator", target="ux-designer", label="Instructional design", stage="Mid-Career", difficulty="moderate"),
    CareerTransitionEdge(id="te-pm", source="teacher-educator", target="product-manager", label="EdTech product", stage="Mid-Career", difficulty="moderate"),
    CareerTransitionEdge(id="te-cc", source="teacher-educator", target="content-creator", label="Educational media", stage="Mid-Career", difficulty="easy"),
    CareerTransitionEdge(id="te-hr", source="teacher-educator", target="hr-manager", label="L&D specialist", stage="Mid-Career", difficulty="moderate"),

    # Architect
    CareerTransitionEdge(id="ar-ux", source="architect", target="ux-designer", label="Spatial UX design", stage="Mid-Career", difficulty="moderate"),
    CareerTransitionEdge(id="ar-pm", source="architect", target="project-manager", label="Construction PM", stage="Senior", difficulty="easy"),
    CareerTransitionEdge(id="ar-me", source="architect", target="mechanical-engineer", label="Building systems", stage="Mid-Career", difficulty="moderate"),
    CareerTransitionEdge(id="ar-en", source="architect", target="entrepreneur", label="Design studio founder", stage="Senior", difficulty="moderate"),

    # HR Manager
    CareerTransitionEdge(id="hr-mc", source="hr-manager", target="management-consultant", label="People consulting", stage="Senior", difficulty="easy"),
    CareerTransitionEdge(id="hr-pm", source="hr-manager", target="product-manager", label="HR-tech product", stage="Senior", difficulty="moderate"),
    CareerTransitionEdge(id="hr-te", source="hr-manager", target="teacher-educator", label="Corporate training", stage="Mid-Career", difficulty="easy"),
    CareerTransitionEdge(id="hr-en", source="hr-manager", target="entrepreneur", label="HR-tech startup", stage="Senior", difficulty="hard"),

    # Project Manager
    CareerTransitionEdge(id="pj-pm", source="project-manager", target="product-manager", label="Product ownership", stage="Mid-Career", difficulty="easy"),
    CareerTransitionEdge(id="pj-mc", source="project-manager", target="management-consultant", label="Delivery consulting", stage="Senior", difficulty="easy"),
    CareerTransitionEdge(id="pj-hr", source="project-manager", target="hr-manager", label="People operations", stage="Senior", difficulty="moderate"),
    CareerTransitionEdge(id="pj-en", source="project-manager", target="entrepreneur", label="Agency founder", stage="Senior", difficulty="moderate"),
]
