"""Generate synthetic seed SQL for the ACE prototype.

Everything here is invented. Names, IDs, grades and emails are fake.
Dates are written around ANCHOR (the demo's "today"); the app reads
demo_clock.anchor_date as today, so the demo never goes stale.
"""
import random, uuid, datetime as dt, json

random.seed(60010)
ANCHOR = dt.date(2026, 11, 19)          # Thursday, first-pass check-in
TZ = "-05:00"

def d(offset):                          # date relative to anchor
    return ANCHOR + dt.timedelta(days=offset)

def ts(offset, hh=23, mm=59):
    return f"{d(offset).isoformat()} {hh:02d}:{mm:02d}:00{TZ}"

def q(v):
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, list):
        return "array[" + ",".join(q(x) for x in v) + "]::text[]" if v else "'{}'::text[]"
    if isinstance(v, (dict,)) or (isinstance(v, list)):
        return "'" + json.dumps(v).replace("'", "''") + "'::jsonb"
    return "'" + str(v).replace("'", "''") + "'"

def qj(v):
    return "'" + json.dumps(v).replace("'", "''") + "'::jsonb"

out = []
def ins(table, rows):
    if not rows:
        return
    cols = list(rows[0].keys())
    vals = ",\n".join("(" + ",".join(qj(r[c]) if c in ("items",) else q(r[c]) for c in cols) + ")" for r in rows)
    out.append(f"insert into {table} ({','.join(cols)}) values\n{vals};")

# ------------------------------------------------------------------ reference
out.append(f"insert into demo_clock (anchor_date, note) values ('{ANCHOR}', 'Synthetic data. App treats anchor_date as today.');")

ins("terms", [
    dict(code="202680", name="Fall 2026", starts_on="2026-08-24", ends_on="2026-12-12"),
    dict(code="202710", name="Spring 2027", starts_on="2027-01-19", ends_on="2027-05-15"),
])

COURSES = [
    # subject, number, title, credits, kent core area
    ("COMM", "15000", "Introduction to Human Communication", 3, "Humanities"),
    ("COMM", "20000", "Research Methods in Communication", 3, None),
    ("COMM", "26000", "Public Speaking", 3, None),
    ("COMM", "35852", "Intercultural Communication", 3, None),
    ("STAT", "11008", "Introduction to Statistics", 3, "Mathematics"),
    ("STAT", "21300", "Statistics for Social Sciences", 3, None),
    ("ENG", "11011", "College Writing I", 3, "Composition"),
    ("ENG", "21011", "College Writing II", 3, "Composition"),
    ("HIST", "12070", "History of the United States", 3, "Humanities"),
    ("PHIL", "21001", "Introduction to Ethics", 3, "Humanities"),
    ("ART", "22006", "Art History: Renaissance to Modern", 3, "Humanities"),
    ("MUS", "22111", "The Understanding of Music", 3, "Humanities"),
    ("PSYC", "11762", "General Psychology", 3, "Social Sciences"),
    ("SOC", "12050", "Introduction to Sociology", 3, "Social Sciences"),
    ("BSCI", "10001", "Human Biology", 3, "Basic Sciences"),
    ("GEOL", "11040", "Earth Dynamics", 3, "Basic Sciences"),
    ("MATH", "11010", "Algebra for Calculus", 3, "Mathematics"),
    ("MATH", "12002", "Analytic Geometry and Calculus I", 5, "Mathematics"),
    ("CS", "13001", "Computer Science I: Programming and Problem Solving", 4, None),
    ("CS", "23001", "Computer Science II: Data Structures", 4, None),
    ("CS", "33101", "Structure of Programming Languages", 3, None),
    ("CS", "33211", "Operating Systems", 3, None),
    ("EMAT", "20100", "Digital Media Tools", 3, None),
    ("EMAT", "36000", "Motion Graphics", 3, None),
    ("EMAT", "45000", "Emerging Media Capstone", 3, None),
    ("EMAT", "41092", "Internship in Emerging Media", 3, None),
    ("JMC", "20004", "Media Writing", 3, None),
    ("UC", "10001", "Flashes 101", 1, None),
    ("NURS", "20020", "Foundations of Nursing Practice", 4, None),
    ("BUS", "10123", "Introduction to Business", 3, None),
]
ins("courses", [dict(subject=s, number=n, title=t, credits=c, kent_core_area=k) for s, n, t, c, k in COURSES])
CID = {f"{s} {n}": i + 1 for i, (s, n, *_rest) in enumerate(COURSES)}
CREDITS = {f"{s} {n}": c for s, n, t, c, k in COURSES}

# Spring 2027 sections in Visual Schedule Builder
sections = []
crn = 21000
for key in CID:
    for _ in range(random.choice([1, 2, 3])):
        crn += random.randint(3, 40)
        pattern = random.choice([("MWF", "09:15", "10:05"), ("MWF", "11:00", "11:50"), ("TR", "12:30", "13:45"),
                                 ("TR", "15:45", "17:00"), ("MW", "17:30", "18:45"), ("Online", None, None)])
        sections.append(dict(course_id=CID[key], term_code="202710", crn=str(crn), days=pattern[0],
                             start_time=pattern[1], end_time=pattern[2],
                             instructor=random.choice(["Okafor", "Lindqvist", "Ramirez", "Huang", "Patel", "Brennan", "Kowalski", "Adeyemi", "Moretti", "Sato"]),
                             seats_open=random.choice([0, 2, 5, 8, 12, 19, 24]),
                             modality="Online" if pattern[0] == "Online" else "In person"))
# make sure the humanities sections Jordan needs are open and fit TR afternoons free
for s in sections:
    if s["course_id"] in (CID["PHIL 21001"], CID["ART 22006"]):
        s["seats_open"] = max(s["seats_open"], 6)
ins("schedule_sections", sections)

SERVICES = [
    dict(name="Academic Success Center Tutoring", kind="tutoring", subjects=["STAT", "MATH", "CS", "BSCI"], location="University Library, 2nd floor", hours="Mon-Thu 10 am-8 pm", booking_url="navigate360/tutoring"),
    dict(name="Writing Commons", kind="writing", subjects=["ENG", "COMM", "JMC", "HIST"], location="University Library, 1st floor", hours="Mon-Fri 9 am-6 pm", booking_url="navigate360/writing"),
    dict(name="Academic Advising", kind="advising", subjects=[], location="Your college advising office", hours="Mon-Fri 8 am-5 pm", booking_url="navigate360/advising"),
    dict(name="Career Exploration and Development", kind="career", subjects=[], location="Schwartz Center, Suite 261", hours="Mon-Fri 8 am-5 pm", booking_url="navigate360/career"),
    dict(name="Math Emporium Drop-in", kind="tutoring", subjects=["MATH", "STAT"], location="Math Emporium, Library 1st floor", hours="Daily 9 am-9 pm", booking_url="navigate360/math"),
    dict(name="Bursar Payment Plans", kind="financial", subjects=[], location="Schwartz Center, 1st floor", hours="Mon-Fri 8 am-5 pm", booking_url="flashline/bursar"),
]
ins("navigate_services", SERVICES)

EVENTS = [
    dict(title="Fall Internship and Career Fair", host="Career Exploration and Development", kind="career fair", starts_at=ts(12, 11, 0), location="Kent Student Center Ballroom", majors=[]),
    dict(title="Creative Industries Networking Night", host="School of Emerging Media and Technology", kind="networking", starts_at=ts(6, 18, 0), location="Franklin Hall", majors=["Emerging Media and Technology", "Communication Studies", "Journalism"]),
    dict(title="Resume Lab: Get Your Resume Fair-Ready", host="Career Exploration and Development", kind="workshop", starts_at=ts(5, 15, 0), location="Schwartz Center 261", majors=[]),
    dict(title="Tech Employer Info Session: Progressive", host="Progressive Insurance", kind="info session", starts_at=ts(8, 17, 30), location="Math and Computer Science Building 228", majors=["Computer Science"]),
    dict(title="Graduate School Q&A", host="Division of Graduate Studies", kind="workshop", starts_at=ts(14, 16, 0), location="Library 10th floor", majors=[]),
]
ins("handshake_events", EVENTS)

JOBS = [
    dict(title="Social Media Intern (Spring 2027)", employer="Cleveland Cavaliers", kind="internship", location="Cleveland, OH", apply_by=str(d(9)), majors=["Communication Studies", "Journalism", "Emerging Media and Technology"]),
    dict(title="Junior Motion Designer", employer="Rosetta (Brunner)", kind="full-time", location="Akron, OH", apply_by=str(d(21)), majors=["Emerging Media and Technology"]),
    dict(title="Video Production Assistant", employer="WKSU / Ideastream", kind="full-time", location="Cleveland, OH", apply_by=str(d(16)), majors=["Emerging Media and Technology", "Journalism"]),
    dict(title="Software Engineering Intern (Summer 2027)", employer="Progressive Insurance", kind="internship", location="Mayfield Village, OH", apply_by=str(d(11)), majors=["Computer Science"]),
    dict(title="IT Help Desk Student Assistant", employer="Kent State Information Services", kind="part-time", location="Kent, OH", apply_by=str(d(7)), majors=[]),
    dict(title="Research Assistant, Communication Lab", employer="Kent State School of Communication Studies", kind="part-time", location="Kent, OH", apply_by=str(d(10)), majors=["Communication Studies", "Psychology"]),
    dict(title="Data Analyst Co-op", employer="Goodyear", kind="co-op", location="Akron, OH", apply_by=str(d(24)), majors=["Computer Science", "Business Analytics"]),
]
ins("handshake_jobs", JOBS)
JID = {j["title"]: i + 1 for i, j in enumerate(JOBS)}

ins("key_dates", [
    dict(term_code="202680", label="Last day to withdraw from a Fall 2026 course", date=str(d(3)), audience="all"),
    dict(term_code="202680", label="CCP: last day to withdraw without high school penalty", date=str(d(3)), audience="ccp"),
    dict(term_code="202680", label="Thanksgiving recess (no classes)", date=str(d(6)), audience="all"),
    dict(term_code="202680", label="Final exams begin", date=str(d(18)), audience="all"),
    dict(term_code="202710", label="Spring 2027 tuition due", date=str(d(42)), audience="all"),
    dict(term_code="202710", label="Deadline to apply for May 2027 graduation", date=str(d(8)), audience="graduating"),
    dict(term_code="202710", label="CCP: Spring 2027 intent-to-participate form due", date=str(d(13)), audience="ccp"),
])

ins("ace_sync_log", [
    dict(source=s, synced_at=f"{ANCHOR} 06:0{i}:00{TZ}", records=r, status="ok")
    for i, (s, r) in enumerate([("Canvas", 1842), ("GPS audit", 45), ("Schedule Builder", len(sections)), ("Navigate360", 131), ("Handshake", 212)])
])

# ------------------------------------------------------------------ personas
PERSONAS = [
    dict(
        key="jordan", first="Jordan", last="Rivera", campus="Kent", level="Sophomore", college="College of Communication and Information",
        major="Communication Studies", minor=None, catalog="2025-2026", grad="May 2028", gpa=3.12, earned=78, inprog=15, firstgen=True, ccp=False, transfer=False,
        advisor="Dana Whitfield", label="Jordan · first-gen sophomore",
        story="First-generation sophomore. Research paper due tonight, a shaky stats quiz, and one humanities course left in Kent Core.",
    ),
    dict(
        key="maya", first="Maya", last="Chen", campus="Kent (online)", level="CCP", college="College Credit Plus",
        major="Undeclared (CCP)", minor=None, catalog="2026-2027", grad=None, gpa=3.71, earned=6, inprog=9, firstgen=False, ccp=True, transfer=False,
        advisor="Luis Ortega", label="Maya · College Credit Plus",
        story="High school senior taking college classes through CCP. Strong grades, but CCP-only deadlines she has never heard about.",
    ),
    dict(
        key="marcus", first="Marcus", last="Bell", campus="Kent", level="Senior", college="College of Communication and Information",
        major="Emerging Media and Technology", minor="Marketing", catalog="2023-2024", grad="May 2027", gpa=3.38, earned=108, inprog=12, firstgen=False, ccp=False, transfer=False,
        advisor="Renee Castillo", label="Marcus · graduating senior",
        story="Senior graduating in May. Has not applied to graduate, is missing one experiential requirement, and job deadlines are stacking up.",
    ),
    dict(
        key="priya", first="Priya", last="Nair", campus="Kent", level="Junior", college="College of Arts and Sciences",
        major="Computer Science", minor="Mathematics", catalog="2026-2027", grad="Dec 2028", gpa=3.55, earned=61, inprog=14, firstgen=False, ccp=False, transfer=True,
        advisor="Kenji Watanabe", label="Priya · transfer junior",
        story="Transferred from a community college this fall. Some transfer credit has not posted, and an advising hold blocks spring registration.",
    ),
    dict(
        key="tyler", first="Tyler", last="Brooks", campus="Stark", level="Freshman", college="College of Business Administration",
        major="Business Management", minor=None, catalog="2026-2027", grad="May 2030", gpa=None, earned=0, inprog=13, firstgen=True, ccp=False, transfer=False,
        advisor="Alicia Grant", label="Tyler · freshman at risk",
        story="First-semester freshman at the Stark campus. Two missing assignments, an instructor early alert in math, and a bursar hold.",
    ),
]

students, enrolls, assigns, gps, regw, holds_rows, appts, alerts, apps, briefs, notes = ([] for _ in range(11))
enroll_id = 0
assign_count = 0

def add_student(p, order, persona=True):
    sid = str(uuid.UUID(int=random.getrandbits(128)))
    first, last = p["first"], p["last"]
    students.append(dict(
        id=sid, banner_id=f"81{random.randint(1000000, 9999999)}", first_name=first, last_name=last,
        email=f"{first[0].lower()}{last.lower()}@ace-demo.kent.edu", campus=p["campus"], class_level=p["level"],
        college=p["college"], major=p["major"], minor=p.get("minor"), catalog_year=p["catalog"],
        expected_grad_term=p.get("grad"), gpa=p.get("gpa"), credits_earned=p["earned"], credits_in_progress=p["inprog"],
        credits_required=120, first_generation=p["firstgen"], college_credit_plus=p["ccp"], transfer=p["transfer"],
        advisor_name=p.get("advisor"), advisor_email=(p["advisor"].split()[0][0] + p["advisor"].split()[-1]).lower() + "@ace-demo.kent.edu" if p.get("advisor") else None,
        is_persona=persona, persona_label=p.get("label"), persona_story=p.get("story"), sort_order=order))
    return sid

def enroll(sid, course, score, instructor, section="001", modality="In person"):
    global enroll_id
    enroll_id += 1
    enrolls.append(dict(id=enroll_id, student_id=sid, course_id=CID[course], term_code="202680", section=section,
                        instructor=instructor, modality=modality, current_score=score, status="enrolled"))
    return enroll_id

def assignment(eid, title, kind, due_off, pts, submitted=None, score=None, hh=23, mm=59):
    assigns.append(dict(enrollment_id=eid, title=title, kind=kind, due_at=ts(due_off, hh, mm), points_possible=pts,
                        submitted_at=ts(submitted, 14, 12) if submitted is not None else None, score=score))

def past_work(eid, base_pct, n=5, kinds=("quiz", "discussion", "problem set")):
    for i in range(n):
        off = -7 * (n - i) - random.randint(0, 3)
        pts = random.choice([10, 20, 25, 50])
        pct = max(0, min(1, random.gauss(base_pct / 100, 0.08)))
        assignment(eid, f"{random.choice(kinds).title()} {i + 1}", random.choice(kinds), off, pts, submitted=off - 1, score=round(pts * pct, 1))

def req(sid, block, name, need, done, inprog, order):
    status = "complete" if done >= need else ("in_progress" if done + inprog >= need or inprog else "not_started")
    gps.append(dict(student_id=sid, block=block, requirement=name, credits_required=need, credits_completed=done,
                    credits_in_progress=inprog, status=status, sort_order=order))

SID = {}
for i, p in enumerate(PERSONAS):
    SID[p["key"]] = add_student(p, i + 1)

# ---- Jordan (matches the Slide 6 mockup)
j = SID["jordan"]
e1 = enroll(j, "COMM 20000", 84.5, "Prof. Lindqvist"); past_work(e1, 85, kinds=("discussion", "quiz"))
assignment(e1, "Research paper: Media use survey analysis", "paper", 0, 100)
assignment(e1, "Peer review: methods section", "discussion", 7, 20)
e2 = enroll(j, "STAT 21300", 78.2, "Dr. Huang"); past_work(e2, 82, kinds=("problem set", "quiz"))
assignment(e2, "Quiz 7: Hypothesis testing", "quiz", -1, 50, submitted=-1, score=40)
assignment(e2, "Problem set 6", "problem set", 5, 40)
assignment(e2, "Exam 3", "exam", 13, 100, hh=10, mm=0)
e3 = enroll(j, "COMM 35852", 91.0, "Prof. Adeyemi"); past_work(e3, 91, kinds=("discussion", "reflection"))
assignment(e3, "Cultural interview reflection", "paper", 8, 50)
e4 = enroll(j, "JMC 20004", 88.0, "Prof. Moretti"); past_work(e4, 88, kinds=("story draft", "quiz"))
assignment(e4, "Feature story draft", "paper", 6, 60)
e5 = enroll(j, "GEOL 11040", 86.4, "Dr. Kowalski"); past_work(e5, 86, kinds=("lab", "quiz"))
assignment(e5, "Lab 9: Plate boundaries", "lab", 2, 25)
for o, (b, r, need, done, ip) in enumerate([
        ("Kent Core", "Composition", 6, 6, 0), ("Kent Core", "Mathematics and Critical Reasoning", 3, 3, 0),
        ("Kent Core", "Humanities and Fine Arts", 9, 6, 0), ("Kent Core", "Social Sciences", 6, 6, 0),
        ("Kent Core", "Basic Sciences", 6, 3, 3), ("Kent Core", "Additional Kent Core", 6, 6, 0),
        ("Major", "Communication Studies core", 24, 15, 9), ("Major", "Major electives", 18, 0, 0),
        ("Diversity", "Domestic and global diversity", 6, 3, 3), ("Electives", "General electives", 36, 36, 0)]):
    req(j, b, r, need, done, ip, o)
regw.append(dict(student_id=j, term_code="202710", opens_at=ts(18, 7, 0)))
appts.append(dict(student_id=j, service_id=3, with_name="Dana Whitfield", starts_at=ts(-13, 14, 0), status="completed"))
apps.append(dict(student_id=j, job_id=JID["Research Assistant, Communication Lab"], status="saved", updated_on=str(d(-4))))

# ---- Maya (CCP)
m = SID["maya"]
e = enroll(m, "ENG 11011", 94.2, "Prof. Brennan", modality="Online"); past_work(e, 94, kinds=("discussion", "essay draft"))
assignment(e, "Essay 3 final draft", "paper", 4, 100)
e = enroll(m, "PSYC 11762", 89.5, "Dr. Patel", modality="Online"); past_work(e, 89, kinds=("quiz", "chapter check"))
assignment(e, "Chapter 11 quiz", "quiz", 1, 20)
assignment(e, "Final exam (online, proctored)", "exam", 19, 100, hh=9, mm=0)
e = enroll(m, "HIST 12070", 92.0, "Prof. Sato", modality="Online"); past_work(e, 92, kinds=("discussion", "source analysis"))
assignment(e, "Primary source analysis 4", "paper", 2, 40)
for o, (b, r, need, done, ip) in enumerate([
        ("Kent Core", "Composition", 6, 0, 3), ("Kent Core", "Humanities and Fine Arts", 9, 3, 3),
        ("Kent Core", "Social Sciences", 6, 3, 3), ("Kent Core", "Mathematics and Critical Reasoning", 3, 0, 0)]):
    req(m, b, r, need, done, ip, o)
regw.append(dict(student_id=m, term_code="202710", opens_at=ts(25, 7, 0)))
holds_rows.append(dict(student_id=m, kind="ccp", description="Spring 2027 CCP intent-to-participate form not on file", blocks_registration=True, resolve_at="Your high school counselor and the CCP office", placed_on=str(d(-10))))

# ---- Marcus (graduating senior)
mb = SID["marcus"]
e = enroll(mb, "EMAT 45000", 90.5, "Prof. Okafor"); past_work(e, 90, kinds=("milestone", "critique"))
assignment(e, "Capstone milestone 3: working build", "project", 3, 100)
e = enroll(mb, "EMAT 36000", 87.0, "Prof. Ramirez"); past_work(e, 87, kinds=("exercise", "critique"))
assignment(e, "Kinetic type project", "project", 9, 100)
e = enroll(mb, "COMM 26000", 93.0, "Prof. Lindqvist"); past_work(e, 93, kinds=("speech", "outline"))
e = enroll(mb, "BUS 10123", 81.0, "Dr. Brennan"); past_work(e, 81, kinds=("quiz", "case brief"))
assignment(e, "Case brief 5", "paper", 1, 30)
for o, (b, r, need, done, ip) in enumerate([
        ("Kent Core", "All Kent Core areas", 36, 36, 0), ("Major", "EMAT major core", 30, 27, 3),
        ("Major", "EMAT concentration", 15, 12, 3), ("Minor", "Marketing minor", 18, 15, 0),
        ("Experiential", "Experiential learning requirement (internship or approved course)", 3, 0, 0),
        ("Writing", "Writing-intensive course", 3, 3, 0), ("Electives", "General electives", 15, 15, 0)]):
    req(mb, b, r, need, done, ip, o)
regw.append(dict(student_id=mb, term_code="202710", opens_at=ts(-9, 7, 0)))
apps.append(dict(student_id=mb, job_id=JID["Junior Motion Designer"], status="saved", updated_on=str(d(-2))))
apps.append(dict(student_id=mb, job_id=JID["Video Production Assistant"], status="applied", updated_on=str(d(-6))))

# ---- Priya (transfer)
pn = SID["priya"]
e = enroll(pn, "CS 23001", 88.0, "Dr. Huang"); past_work(e, 88, kinds=("programming assignment", "quiz"))
assignment(e, "Programming assignment 6: hash tables", "project", 2, 100)
e = enroll(pn, "CS 33101", 83.5, "Prof. Kowalski"); past_work(e, 84, kinds=("homework", "quiz"))
assignment(e, "Homework 8: lambda calculus", "problem set", 4, 50)
e = enroll(pn, "MATH 12002", 79.0, "Dr. Sato"); past_work(e, 80, kinds=("webwork", "quiz"))
assignment(e, "Exam 3", "exam", 6, 100, hh=11, mm=0)
e = enroll(pn, "UC 10001", 100.0, "Peer mentor"); past_work(e, 100, n=3, kinds=("reflection",))
for o, (b, r, need, done, ip) in enumerate([
        ("Kent Core", "All Kent Core areas", 36, 30, 0), ("Major", "CS lower division", 16, 8, 4),
        ("Major", "CS upper division", 30, 0, 3), ("Minor", "Mathematics minor", 20, 4, 5),
        ("Transfer", "Transfer credit pending evaluation (Lorain County CC)", 9, 0, 0), ("Electives", "General electives", 18, 15, 0)]):
    req(pn, b, r, need, done, ip, o)
regw.append(dict(student_id=pn, term_code="202710", opens_at=ts(4, 7, 0)))
holds_rows.append(dict(student_id=pn, kind="advising", description="Advising hold: meet with your advisor before Spring 2027 registration", blocks_registration=True, resolve_at="Navigate360: book with Kenji Watanabe", placed_on=str(d(-20))))
apps.append(dict(student_id=pn, job_id=JID["Software Engineering Intern (Summer 2027)"], status="saved", updated_on=str(d(-1))))

# ---- Tyler (at risk)
tb = SID["tyler"]
e = enroll(tb, "MATH 11010", 61.5, "Dr. Adeyemi", section="801"); past_work(e, 64, kinds=("webwork", "quiz"))
assignment(e, "WebWork 9", "problem set", -2, 30)              # missing
assignment(e, "WebWork 10", "problem set", 1, 30)
assignment(e, "Exam 3", "exam", 5, 100, hh=9, mm=30)
e = enroll(tb, "ENG 11011", 74.0, "Prof. Moretti", section="802"); past_work(e, 76, kinds=("discussion", "essay draft"))
assignment(e, "Essay 2 revision", "paper", -4, 100)            # missing
assignment(e, "Essay 3 draft", "paper", 6, 100)
e = enroll(tb, "BUS 10123", 82.0, "Dr. Brennan", section="801"); past_work(e, 82, kinds=("quiz", "case brief"))
assignment(e, "Case brief 5", "paper", 1, 30)
e = enroll(tb, "SOC 12050", 79.0, "Prof. Patel", section="805"); past_work(e, 79, kinds=("quiz", "discussion"))
e = enroll(tb, "UC 10001", 90.0, "Peer mentor", section="810"); past_work(e, 90, n=3, kinds=("reflection",))
for o, (b, r, need, done, ip) in enumerate([
        ("Kent Core", "Composition", 6, 0, 3), ("Kent Core", "Mathematics and Critical Reasoning", 3, 0, 3),
        ("Kent Core", "Social Sciences", 6, 0, 3), ("Major", "Business core", 33, 0, 3)]):
    req(tb, b, r, need, done, ip, o)
regw.append(dict(student_id=tb, term_code="202710", opens_at=ts(30, 7, 0)))
holds_rows.append(dict(student_id=tb, kind="bursar", description="Past-due balance on Fall 2026 account", blocks_registration=True, resolve_at="FlashLine > Bursar, or Bursar Payment Plans", placed_on=str(d(-12))))
alerts.append(dict(student_id=tb, raised_by="Dr. Adeyemi", course_id=CID["MATH 11010"], reason="Missing assignments and exam 2 score below 60%", raised_on=str(d(-3)), status="open"))

# ------------------------------------------------------------------ background students
FIRST = ["Avery", "Noah", "Elena", "Malik", "Sofia", "Ethan", "Grace", "Isaiah", "Hannah", "Diego", "Leah", "Owen", "Zara", "Caleb",
         "Amara", "Lucas", "Nia", "Ryan", "Chloe", "Mateo", "Jasmine", "Liam", "Aaliyah", "Wyatt", "Fatima", "Logan", "Imani",
         "Carter", "Lily", "Jamal", "Ava", "Hunter", "Mia", "Xavier", "Ella", "Andre", "Paige", "Omar", "Brooke", "Devin"]
LAST = ["Kowalczyk", "Thompson", "Okonkwo", "Martinez", "Schaefer", "Hughes", "Nguyen", "Washington", "Petrov", "Morales", "Fischer",
        "Coleman", "Haddad", "Russo", "Jenkins", "Kim", "Abernathy", "Delgado", "Yoder", "Sullivan"]
MAJORS = [("Communication Studies", "College of Communication and Information"), ("Emerging Media and Technology", "College of Communication and Information"),
          ("Computer Science", "College of Arts and Sciences"), ("Psychology", "College of Arts and Sciences"),
          ("Business Management", "College of Business Administration"), ("Nursing", "College of Nursing"),
          ("Journalism", "College of Communication and Information")]
LEVEL_CREDITS = {"Freshman": (0, 29), "Sophomore": (30, 59), "Junior": (60, 89), "Senior": (90, 116)}
core_pool = [k for k in CID if not k.startswith(("CS 3", "EMAT 4", "NURS"))]
for i, fn in enumerate(FIRST):
    major, college = random.choice(MAJORS)
    level = random.choice(list(LEVEL_CREDITS))
    earned = random.randint(*LEVEL_CREDITS[level])
    p = dict(first=fn, last=random.choice(LAST), campus=random.choice(["Kent"] * 6 + ["Stark", "Tuscarawas", "Trumbull"]), level=level,
             college=college, major=major, catalog="2025-2026", grad=None, gpa=round(random.uniform(2.1, 3.95), 2), earned=earned,
             inprog=random.choice([12, 13, 15, 16]), firstgen=random.random() < 0.34, ccp=False, transfer=random.random() < 0.15,
             advisor=random.choice(["Dana Whitfield", "Renee Castillo", "Kenji Watanabe", "Alicia Grant"]))
    sid = add_student(p, 100 + i, persona=False)
    base = random.gauss(84, 8)
    for course in random.sample(core_pool, 4):
        eid = enroll(sid, course, round(max(45, min(100, random.gauss(base, 6))), 1), random.choice(["Prof. Okafor", "Dr. Huang", "Prof. Ramirez", "Dr. Patel"]))
        past_work(eid, base, n=4)
        assignment(eid, random.choice(["Project milestone", "Quiz", "Short paper", "Problem set"]), "assignment", random.randint(0, 14), random.choice([20, 50, 100]))
    need_h = 9
    done_h = random.choice([3, 6, 9])
    req(sid, "Kent Core", "Humanities and Fine Arts", need_h, done_h, 0, 0)
    req(sid, "Major", f"{major} core", 30, min(30, earned // 4), 6, 1)
    regw.append(dict(student_id=sid, term_code="202710", opens_at=ts(random.randint(-10, 30), 7, 0)))
    if random.random() < 0.18:
        holds_rows.append(dict(student_id=sid, kind=random.choice(["bursar", "advising", "immunization"]),
                               description="Hold on account", blocks_registration=True, resolve_at="FlashLine", placed_on=str(d(-random.randint(3, 30)))))

# ------------------------------------------------------------------ fallback briefs + email nudges (personas)
BRIEFS = {
    "jordan": ("Good morning, Jordan. 3 things need you today.", [
        dict(rank=1, label="Due tonight 11:59 pm", title="COMM 20000 research paper", detail="Worth 100 points, about 20% of your grade. Not submitted yet.", source="Canvas", action="Open in Canvas"),
        dict(rank=2, label="Study help", title="40/50 on stats quiz 7: tutoring today 2 to 5 pm", detail="Exam 3 in STAT 21300 is in 13 days. Hypothesis testing will be on it.", source="Canvas + Navigate360", action="Book in Navigate360"),
        dict(rank=3, label="Plan ahead", title="1 humanities course left; 2 Spring sections fit", detail="PHIL 21001 and ART 22006 both have open seats that fit your current schedule.", source="GPS audit + Schedule Builder", action="Open Schedule Builder"),
    ]),
    "maya": ("Good morning, Maya. 2 things need you today.", [
        dict(rank=1, label="CCP deadline", title="Spring CCP intent form is not on file", detail="It is due in 13 days and it blocks Spring registration. Your high school counselor submits it.", source="FlashLine holds", action="See CCP steps"),
        dict(rank=2, label="Due tomorrow", title="PSYC 11762 chapter 11 quiz", detail="20 points, online. Opens tonight.", source="Canvas", action="Open in Canvas"),
        dict(rank=3, label="Heads up", title="Withdraw deadline is Sunday", detail="You are doing well in all three courses. Nothing to do; CCP withdrawals can affect your high school record.", source="Key dates", action="Learn more"),
    ]),
    "marcus": ("Good morning, Marcus. 3 things need you this week.", [
        dict(rank=1, label="Graduation", title="Apply to graduate by Nov 27", detail="You are on track for May 2027, but you have not applied. Missing the deadline pushes your graduation term.", source="GPS audit + key dates", action="Apply in FlashLine"),
        dict(rank=2, label="Degree gap", title="Experiential learning requirement not met", detail="EMAT 41092 (Internship) in Spring would satisfy it. Talk with Renee Castillo first.", source="GPS audit", action="Book with your advisor"),
        dict(rank=3, label="Career", title="Junior Motion Designer, apply by Dec 10", detail="Saved in Handshake. The Creative Industries Networking Night is in 6 days.", source="Handshake", action="Open in Handshake"),
    ]),
    "priya": ("Good morning, Priya. 2 things need you today.", [
        dict(rank=1, label="Registration blocked", title="Advising hold; your window opens Monday", detail="Book with Kenji Watanabe before Monday 7 am so the hold can be lifted.", source="FlashLine holds + Navigate360", action="Book in Navigate360"),
        dict(rank=2, label="Degree audit", title="9 transfer credits still pending", detail="Your Lorain County CC credits are not on your GPS audit yet. Ask your advisor to check the evaluation.", source="GPS audit", action="Open GPS audit"),
        dict(rank=3, label="Due Saturday", title="CS 23001 programming assignment 6", detail="Hash tables, 100 points.", source="Canvas", action="Open in Canvas"),
    ]),
    "tyler": ("Good morning, Tyler. Let's get 3 things back on track.", [
        dict(rank=1, label="Your instructor reached out", title="Dr. Adeyemi flagged MATH 11010", detail="WebWork 9 is missing and Exam 3 is in 5 days. The Math Emporium is open daily 9 am to 9 pm.", source="Navigate360 + Canvas", action="Get math help"),
        dict(rank=2, label="Missing work", title="ENG 11011 essay 2 revision", detail="It was due Sunday. Ask Prof. Moretti if late work is accepted.", source="Canvas", action="Open in Canvas"),
        dict(rank=3, label="Account hold", title="A bursar hold blocks Spring registration", detail="A payment plan can remove it. Your window opens in 30 days.", source="FlashLine holds", action="See payment options"),
    ]),
}
for k, (headline, items) in BRIEFS.items():
    briefs.append(dict(student_id=SID[k], brief_date=str(ANCHOR), headline=headline, items=items, generated_by="scripted"))

NOTES = {
    "jordan": ("ACE: Your COMM 20000 paper is due tonight", "Hi Jordan,\n\nYour research paper for COMM 20000 is due tonight at 11:59 pm and has not been submitted yet.\n\nOpen it in Canvas: canvas.kent.edu\n\nAlso today: tutoring for STAT 21300 runs 2 to 5 pm at the Academic Success Center.\n\nACE, inside FlashLine\nThis summary uses your Canvas, GPS audit, Schedule Builder, Navigate360 and Handshake data. Reply STOP to turn off ACE emails."),
    "maya": ("ACE: Your Spring CCP form is missing", "Hi Maya,\n\nYour Spring 2027 College Credit Plus intent-to-participate form is not on file. It is due in 13 days and you cannot register for Spring without it.\n\nNext step: ask your high school counselor to submit it.\n\nACE, inside FlashLine"),
    "marcus": ("ACE: Apply to graduate by Nov 27", "Hi Marcus,\n\nYou are on track to graduate in May 2027, but your graduation application is not on file. The deadline is Nov 27.\n\nApply in FlashLine > Student > Graduation.\n\nACE, inside FlashLine"),
    "priya": ("ACE: Your registration window opens Monday", "Hi Priya,\n\nYour Spring 2027 registration window opens Monday at 7 am, but an advising hold is on your account.\n\nBook with Kenji Watanabe in Navigate360 before then.\n\nACE, inside FlashLine"),
    "tyler": ("ACE: Your math instructor reached out", "Hi Tyler,\n\nDr. Adeyemi raised a concern about MATH 11010. WebWork 9 is missing and Exam 3 is Tuesday.\n\nThe Math Emporium is open daily, 9 am to 9 pm, no appointment needed.\n\nACE, inside FlashLine"),
}
for k, (subj, body) in NOTES.items():
    notes.append(dict(student_id=SID[k], channel="kent_email", send_at=ts(0, 6, 30), subject=subj, body=body))

ins("students", students)
ins("enrollments", enrolls)
ins("canvas_assignments", assigns)
ins("gps_requirements", gps)
ins("registration_windows", regw)
ins("holds", holds_rows)
ins("navigate_appointments", appts)
ins("navigate_alerts", alerts)
ins("handshake_applications", apps)
ins("ace_briefs", briefs)
ins("ace_notifications", notes)
out.append("select setval('enrollments_id_seq', (select max(id) from enrollments));")

open("/home/claude/ace/seed.sql", "w").write("\n\n".join(out))
print(len(students), "students,", len(enrolls), "enrollments,", len(assigns), "assignments")
