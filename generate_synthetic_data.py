"""
Synthetic Data Generator for the ARC Clinical Browser Demo
===========================================================

Generates a fully synthetic dashboard_data.json suitable for public demos.
NO real patient data is used. All names, dates, MRNs, and patient IDs are
randomly generated. Clinical codes (LOINC, ICD-10, RxNorm) are real public
codes used in realistic ALS-flavored patterns.

OUTPUT: demo_dashboard_data.json — drop this into a folder with
        dashboard_demo.html and open in a browser.

This file is safe to publish publicly (e.g. on GitHub Pages).

USAGE:
    python generate_synthetic_data.py

CONFIGURATION: edit the constants at the top of the file.
"""

import json
import random
import uuid
from datetime import datetime, timedelta

# ============================================================
# CONFIGURATION
# ============================================================
N_PATIENTS = 50
SEED = 42                              # change for different patient sets
OUTPUT_FILE = "demo_dashboard_data.json"
NAME_SUFFIX = " [DEMO]"                # appended to every patient last name
START_YEAR = 2018                      # earliest synthetic encounter year
END_YEAR = 2026

random.seed(SEED)

# ============================================================
# SYNTHETIC NAMES (no real-person resemblance intended)
# ============================================================
FIRST_NAMES = [
    "Alex", "Bailey", "Cameron", "Dakota", "Ellis", "Finley", "Gray", "Harper",
    "Indigo", "Jordan", "Kai", "Logan", "Morgan", "Nova", "Oakley", "Parker",
    "Quinn", "Rowan", "Sage", "Taylor", "Umber", "Vale", "Wren", "Xen", "Yara",
    "Avery", "Blair", "Casey", "Devon", "Emery", "Frankie", "Glenn", "Hollis",
    "Iris", "Jules", "Kendall", "Lane", "Mason", "Niko", "Onyx", "Phoenix",
    "Reese", "Skyler", "Tatum", "Uriah", "Vesper", "Wyatt", "Yael", "Zion",
    "Sloane", "Marlowe"
]

LAST_NAMES = [
    "Aldridge", "Brookwood", "Castellan", "Drummond", "Everwood", "Fairchild",
    "Glendower", "Hartwell", "Ivers", "Jordane", "Kentish", "Lachlan",
    "Marrowby", "Northgate", "Oakhaven", "Pemberton", "Quincey", "Ravenwood",
    "Stoneford", "Tideswell", "Underwood", "Vaughn", "Westmore", "Yardley", "Zell",
    "Ashworth", "Briarcliff", "Coldwater", "Dunmore", "Elderwick", "Foxglove",
    "Greenleaf", "Holloway", "Inglewood", "Jasperson", "Kingsley", "Linwood",
    "Merriweather", "Nightingale", "Ostlund", "Pennington", "Quartermaine",
    "Rosenfield", "Silvermoor", "Thornbury", "Underhill", "Veridian", "Whitlock",
    "Yorkshire", "Zerwick", "Ashbury"
]

# ============================================================
# CLINICAL VOCABULARIES (real public codes)
# ============================================================
# Real LOINC codes (LOINC is publicly available)
LOINC_VITALS = [
    ("8480-6", "Systolic blood pressure", "mm[Hg]", (110, 145)),
    ("8462-4", "Diastolic blood pressure", "mm[Hg]", (65, 95)),
    ("8867-4", "Heart rate", "/min", (58, 95)),
    ("9279-1", "Respiratory rate", "/min", (12, 20)),
    ("8310-5", "Body temperature", "Cel", (36.4, 37.4)),
    ("29463-7", "Body weight", "kg", (55, 95)),
    ("8302-2", "Body height", "cm", (155, 190)),
    ("39156-5", "Body mass index (BMI)", "kg/m2", (19.5, 31.0)),
    ("59408-5", "Oxygen saturation", "%", (94, 99)),
]

LOINC_LABS = [
    ("2160-0", "Creatinine [Mass/volume] in Serum", "mg/dL", (0.6, 1.4)),
    ("2345-7", "Glucose [Mass/volume] in Serum", "mg/dL", (75, 130)),
    ("2823-3", "Potassium [Moles/volume] in Serum", "mmol/L", (3.5, 5.1)),
    ("2951-2", "Sodium [Moles/volume] in Serum", "mmol/L", (135, 145)),
    ("718-7",  "Hemoglobin [Mass/volume] in Blood", "g/dL", (11.5, 16.5)),
    ("4544-3", "Hematocrit [Volume Fraction]", "%", (35, 50)),
    ("6690-2", "White blood cell count", "10*3/uL", (4.0, 11.0)),
    ("777-3",  "Platelets [#/volume] in Blood", "10*3/uL", (150, 400)),
    ("1742-6", "Alanine aminotransferase (ALT)", "U/L", (7, 55)),
    ("1920-8", "Aspartate aminotransferase (AST)", "U/L", (8, 48)),
    ("2093-3", "Cholesterol [Mass/volume] in Serum", "mg/dL", (140, 240)),
    ("3094-0", "Urea nitrogen [Mass/volume] in Serum", "mg/dL", (8, 24)),
]

# ALS-specific
LOINC_ALS = [
    ("67131-4", "Total ALSFRS-R score", "{score}", (12, 48)),
]

# ICD-10 conditions: ALS + common comorbidities
CONDITIONS = [
    ("G12.21", "Amyotrophic lateral sclerosis", "ICD-10-CM", True),  # primary
    ("G47.33", "Obstructive sleep apnea (adult) (pediatric)", "ICD-10-CM", False),
    ("J96.20", "Acute and chronic respiratory failure", "ICD-10-CM", False),
    ("R63.4",  "Abnormal weight loss", "ICD-10-CM", False),
    ("R13.10", "Dysphagia, unspecified", "ICD-10-CM", False),
    ("M62.81", "Muscle weakness (generalized)", "ICD-10-CM", False),
    ("F32.9",  "Major depressive disorder, single episode, unspecified", "ICD-10-CM", False),
    ("R47.81", "Slurred speech", "ICD-10-CM", False),
    ("R29.890","Other symptoms involving nervous and musculoskeletal systems", "ICD-10-CM", False),
    ("E11.9",  "Type 2 diabetes mellitus without complications", "ICD-10-CM", False),
    ("I10",    "Essential (primary) hypertension", "ICD-10-CM", False),
    ("E78.5",  "Hyperlipidemia, unspecified", "ICD-10-CM", False),
]

# RxNorm codes for ALS and supportive medications
MEDICATIONS = [
    ("83366",   "Riluzole 50 MG Oral Tablet", "RxNorm", "ALS"),
    ("1922474", "Edaravone 30 MG/100 ML Injection", "RxNorm", "ALS"),
    ("2371759", "Sodium phenylbutyrate / Taurursodiol oral suspension", "RxNorm", "ALS"),
    ("8163",    "Baclofen 10 MG Oral Tablet", "RxNorm", "Spasticity"),
    ("4337",    "Glycopyrrolate 1 MG Oral Tablet", "RxNorm", "Sialorrhea"),
    ("283742",  "Quinine sulfate 324 MG Oral Tablet", "RxNorm", "Cramps"),
    ("89013",   "Dextromethorphan / Quinidine", "RxNorm", "Pseudobulbar affect"),
    ("314076",  "Lisinopril 10 MG Oral Tablet", "RxNorm", "Hypertension"),
    ("617314",  "Atorvastatin 20 MG Oral Tablet", "RxNorm", "Hyperlipidemia"),
    ("860975",  "Metformin 500 MG Oral Tablet", "RxNorm", "Diabetes"),
    ("596926",  "Sertraline 50 MG Oral Tablet", "RxNorm", "Depression"),
    ("104894",  "Pantoprazole 40 MG Oral Tablet", "RxNorm", "GERD"),
]

# CPT/SNOMED procedures
PROCEDURES = [
    ("95860", "Needle electromyography (EMG), 1 extremity", "CPT"),
    ("95900", "Nerve conduction study, motor, without F-wave", "CPT"),
    ("94010", "Spirometry; complete pulmonary function", "CPT"),
    ("94014", "Patient-initiated spirometric recording", "CPT"),
    ("43246", "Esophagogastroduodenoscopy, with PEG tube placement", "CPT"),
    ("31600", "Tracheostomy, planned (separate procedure)", "CPT"),
    ("99213", "Office or other outpatient visit, established patient (15 min)", "CPT"),
    ("99214", "Office or other outpatient visit, established patient (25 min)", "CPT"),
    ("99215", "Office or other outpatient visit, established patient (40 min)", "CPT"),
]

# FHIR encounter classes
ENCOUNTER_CLASSES = [
    ("AMB", "Ambulatory"),
    ("AMB", "Outpatient ALS clinic visit"),
    ("AMB", "Multidisciplinary ALS clinic"),
    ("AMB", "Pulmonology consultation"),
    ("AMB", "Speech therapy evaluation"),
    ("AMB", "Physical therapy evaluation"),
    ("EMER", "Emergency department visit"),
    ("IMP", "Inpatient admission for respiratory complication"),
]

ALLERGIES = [
    ("387207008", "Penicillin", "high"),
    ("82670002",  "Codeine", "moderate"),
    ("373270004", "Latex", "moderate"),
    ("256277009", "Shellfish", "low"),
    ("256302005", "Tree nuts", "moderate"),
]

IMMUNIZATIONS = [
    ("207", "COVID-19 mRNA vaccine"),
    ("141", "Influenza, seasonal, injectable"),
    ("133", "Pneumococcal conjugate PCV13"),
    ("115", "Tdap, adolescent/adult use"),
]

CARE_PLANS = [
    "ALS multidisciplinary care plan",
    "Respiratory monitoring and BiPAP titration",
    "Nutritional support and PEG tube planning",
    "Speech therapy and AAC device evaluation",
    "Home health aide coordination",
]

GOALS = [
    "Maintain forced vital capacity above 50% predicted",
    "Maintain stable body weight (within 5% of baseline)",
    "Continue independent ambulation as long as feasible",
    "Optimize communication strategies as speech declines",
    "Establish advance directives and goals of care",
]

# ============================================================
# HELPERS
# ============================================================
def fake_uuid():
    return str(uuid.uuid4())

def fake_mrn():
    return ''.join(random.choices('0123456789', k=10))

def fake_dob():
    """ALS most often diagnosed 55-75; generate plausible DOBs."""
    age = random.randint(45, 80)
    year = 2026 - age
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f"{year:04d}-{month:02d}-{day:02d}"

def fake_date(start_year=START_YEAR, end_year=END_YEAR):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 1, 1)
    delta = end - start
    rand_days = random.randint(0, delta.days)
    return (start + timedelta(days=rand_days))

def date_str(dt):
    return dt.strftime("%Y-%m-%d")

def datetime_str(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%S")

def random_value(low, high, decimals=1):
    return round(random.uniform(low, high), decimals)

def pick_source():
    """Mostly FHIR, some CCDA-sourced."""
    return random.choices(['fhir', 'ccda'], weights=[3, 2])[0]


# ============================================================
# PATIENT GENERATION
# ============================================================
def make_patient(idx):
    first = FIRST_NAMES[idx % len(FIRST_NAMES)]
    last = LAST_NAMES[idx % len(LAST_NAMES)] + NAME_SUFFIX

    # ALS onset characteristics
    # ~70% limb-onset, ~25% bulbar-onset, ~5% respiratory-onset
    onset_type = random.choices(
        ['limb', 'bulbar', 'respiratory'],
        weights=[70, 25, 5]
    )[0]

    # Diagnosis age: most often 55-75, but can range 35-85
    age = random.choices(
        [random.randint(35, 54), random.randint(55, 75), random.randint(76, 85)],
        weights=[10, 75, 15]
    )[0]
    year = 2026 - age
    month = random.randint(1, 12)
    day = random.randint(1, 28)

    # Disease progression rate: slow / typical / fast
    # ALSFRS-R declines ~1 pt/month on average; spread is wide
    progression_rate = random.choices(
        ['slow', 'typical', 'fast'],
        weights=[20, 60, 20]
    )[0]

    return {
        'patient_id': fake_uuid(),
        'mrn': fake_mrn(),
        'first_name': first,
        'last_name': last,
        'dob': f"{year:04d}-{month:02d}-{day:02d}",
        'gender': random.choice(['male', 'female']),
        'race': '',
        'ethnicity': '',
        'document_date': '',
        'num_documents': 0,
        # Internal-only attributes used during generation (stripped before output)
        '_onset_type': onset_type,
        '_progression': progression_rate,
        '_diagnosis_year': random.randint(START_YEAR, END_YEAR - 1),
    }


def make_observations(patient, n_visits=8):
    """Generate ~150-300 observations per patient across multiple visits."""
    obs = []
    diag_year = patient.get('_diagnosis_year', START_YEAR)
    base_date = datetime(diag_year, random.randint(1, 12), random.randint(1, 28))

    # Disease progression rate determines ALSFRS-R decline (points/month)
    progression = patient.get('_progression', 'typical')
    decline_per_month = {
        'slow': 0.5,      # slow progressors: ~0.5 pt/month
        'typical': 1.0,   # typical: ~1 pt/month
        'fast': 1.7,      # fast progressors: ~1.5-2 pt/month
    }[progression]

    # Starting ALSFRS-R near diagnosis: typically high 30s to mid-40s out of 48
    starting_alsfrs = random.randint(38, 47)

    for visit in range(n_visits):
        visit_date = base_date + timedelta(days=visit * random.randint(60, 120))
        if visit_date.year > END_YEAR:
            break
        date_s = date_str(visit_date)
        dt_s = datetime_str(visit_date)
        months_since_dx = visit * random.randint(2, 4)

        # Vitals at every visit
        for code, name, unit, (lo, hi) in LOINC_VITALS:
            obs.append({
                'patient_id': patient['patient_id'],
                'observation_date': date_s,
                'effective_datetime': dt_s,
                'display_name': name,
                'code': code,
                'code_system_name': 'LOINC',
                'value': str(random_value(lo, hi)),
                'unit': unit,
                'status': 'final',
                'source': pick_source(),
                'category': 'vital-signs',
            })

        # Labs at ~half of visits
        if visit % 2 == 0:
            for code, name, unit, (lo, hi) in random.sample(LOINC_LABS, k=random.randint(6, 10)):
                val = random_value(lo, hi, 2 if 'mmol' in unit else 1)
                obs.append({
                    'patient_id': patient['patient_id'],
                    'observation_date': date_s,
                    'effective_datetime': dt_s,
                    'display_name': name,
                    'code': code,
                    'code_system_name': 'LOINC',
                    'value': str(val),
                    'unit': unit,
                    'status': 'final',
                    'source': pick_source(),
                    'category': 'laboratory',
                })

        # ALSFRS-R at every visit: realistic monotonic decline with small noise
        alsfrs = max(8, int(starting_alsfrs - (decline_per_month * months_since_dx) + random.gauss(0, 1.2)))
        obs.append({
            'patient_id': patient['patient_id'],
            'observation_date': date_s,
            'effective_datetime': dt_s,
            'display_name': 'Total ALSFRS-R score',
            'code': '67131-4',
            'code_system_name': 'LOINC',
            'value': str(alsfrs),
            'unit': '{score}',
            'status': 'final',
            'source': 'fhir',
            'category': 'survey',
        })

        # Forced vital capacity (FVC) at most visits — also declining
        if visit % 2 == 0 or random.random() < 0.6:
            fvc_pct = max(25, int(95 - (decline_per_month * months_since_dx * 1.5) + random.gauss(0, 4)))
            obs.append({
                'patient_id': patient['patient_id'],
                'observation_date': date_s,
                'effective_datetime': dt_s,
                'display_name': 'Forced vital capacity (% predicted)',
                'code': '19868-9',
                'code_system_name': 'LOINC',
                'value': str(fvc_pct),
                'unit': '%',
                'status': 'final',
                'source': 'fhir',
                'category': 'pulmonary',
            })

    return obs


def make_conditions(patient):
    conds = []
    diag_year = patient.get('_diagnosis_year', START_YEAR)
    onset_date = datetime(diag_year, random.randint(1, 12), random.randint(1, 28))

    # Always primary ALS diagnosis
    conds.append({
        'patient_id': patient['patient_id'],
        'onset_date': date_str(onset_date),
        'onset_datetime': datetime_str(onset_date),
        'display_name': 'Amyotrophic lateral sclerosis',
        'code': 'G12.21',
        'code_system_name': 'ICD-10-CM',
        'clinical_status': 'active',
        'status': 'confirmed',
        'severity': random.choice(['moderate', 'severe']),
        'source': pick_source(),
    })

    # Onset-type-specific early symptoms
    onset_type = patient.get('_onset_type', 'limb')
    early_codes = []
    if onset_type == 'bulbar':
        # Bulbar-onset: dysphagia + slurred speech come early
        early_codes = ['R13.10', 'R47.81']
    elif onset_type == 'limb':
        # Limb-onset: muscle weakness early
        early_codes = ['M62.81']
    elif onset_type == 'respiratory':
        # Respiratory-onset (rare): respiratory failure
        early_codes = ['J96.20', 'M62.81']

    for code in early_codes:
        for c, n, s, _ in CONDITIONS:
            if c == code:
                cdate = onset_date + timedelta(days=random.randint(-90, 60))
                conds.append({
                    'patient_id': patient['patient_id'],
                    'onset_date': date_str(cdate),
                    'onset_datetime': datetime_str(cdate),
                    'display_name': n,
                    'code': c,
                    'code_system_name': s,
                    'clinical_status': 'active',
                    'status': 'confirmed',
                    'severity': 'moderate',
                    'source': pick_source(),
                })
                break

    # Add 2-4 other comorbidities
    other_pool = [c for c in CONDITIONS if not c[3] and c[0] not in early_codes]
    n_comorbid = random.randint(2, 4)
    for code, name, system, _ in random.sample(other_pool, k=min(n_comorbid, len(other_pool))):
        cdate = onset_date + timedelta(days=random.randint(-365, 730))
        conds.append({
            'patient_id': patient['patient_id'],
            'onset_date': date_str(cdate),
            'onset_datetime': datetime_str(cdate),
            'display_name': name,
            'code': code,
            'code_system_name': system,
            'clinical_status': random.choice(['active', 'resolved', 'active']),
            'status': 'confirmed',
            'severity': random.choice(['mild', 'moderate']),
            'source': pick_source(),
        })
    return conds


def make_medications(patient):
    meds = []
    base = fake_date(START_YEAR, START_YEAR + 1)
    # Most ALS patients on riluzole
    if random.random() < 0.85:
        meds.append({
            'patient_id': patient['patient_id'],
            'authored_on': datetime_str(base),
            'start_date': date_str(base),
            'display_name': 'Riluzole 50 MG Oral Tablet',
            'code': '83366',
            'code_system': 'http://www.nlm.nih.gov/research/umls/rxnorm',
            'status': 'active',
            'dose_quantity': '50', 'dose_unit': 'mg',
            'route': 'Oral',
            'source': pick_source(),
        })
    # Some on edaravone
    if random.random() < 0.35:
        meds.append({
            'patient_id': patient['patient_id'],
            'authored_on': datetime_str(base + timedelta(days=random.randint(30, 365))),
            'start_date': date_str(base + timedelta(days=random.randint(30, 365))),
            'display_name': 'Edaravone 30 MG/100 ML Injection',
            'code': '1922474',
            'code_system': 'http://www.nlm.nih.gov/research/umls/rxnorm',
            'status': 'active',
            'dose_quantity': '30', 'dose_unit': 'mg',
            'route': 'Intravenous',
            'source': pick_source(),
        })
    # Other supportive meds
    n_other = random.randint(2, 6)
    for code, name, system, _ in random.sample(MEDICATIONS[3:], k=n_other):
        mdate = base + timedelta(days=random.randint(-180, 720))
        meds.append({
            'patient_id': patient['patient_id'],
            'authored_on': datetime_str(mdate),
            'start_date': date_str(mdate),
            'display_name': name,
            'code': code,
            'code_system': 'http://www.nlm.nih.gov/research/umls/rxnorm',
            'status': random.choice(['active', 'completed', 'active']),
            'dose_quantity': str(random.choice([5, 10, 20, 40, 50, 100])), 'dose_unit': 'mg',
            'route': 'Oral',
            'source': pick_source(),
        })
    return meds


def make_procedures(patient):
    procs = []
    diag_year = patient.get('_diagnosis_year', START_YEAR)
    onset_type = patient.get('_onset_type', 'limb')
    progression = patient.get('_progression', 'typical')

    base = datetime(diag_year, random.randint(1, 12), random.randint(1, 28))

    # EMG and nerve conduction studies are universal at/near diagnosis
    for code, name in [('95860', 'Needle electromyography (EMG), 1 extremity'),
                       ('95900', 'Nerve conduction study, motor, without F-wave')]:
        pdate = base + timedelta(days=random.randint(-60, 30))
        procs.append({
            'patient_id': patient['patient_id'],
            'procedure_date': date_str(pdate),
            'performed_datetime': datetime_str(pdate),
            'display_name': name,
            'code': code,
            'code_system_name': 'CPT',
            'status': 'completed',
            'category': 'diagnostic',
            'source': pick_source(),
        })

    # Spirometry: every 3-6 months throughout disease course
    n_spiro = random.randint(3, 8)
    for j in range(n_spiro):
        pdate = base + timedelta(days=j * random.randint(90, 180))
        if pdate.year > END_YEAR:
            break
        procs.append({
            'patient_id': patient['patient_id'],
            'procedure_date': date_str(pdate),
            'performed_datetime': datetime_str(pdate),
            'display_name': 'Spirometry; complete pulmonary function',
            'code': '94010',
            'code_system_name': 'CPT',
            'status': 'completed',
            'category': 'pulmonary',
            'source': pick_source(),
        })

    # PEG tube: more likely for bulbar-onset patients or fast progressors
    peg_probability = 0.7 if onset_type == 'bulbar' else (0.5 if progression == 'fast' else 0.25)
    if random.random() < peg_probability:
        # PEG typically placed 12-24 months after diagnosis
        peg_date = base + timedelta(days=random.randint(365, 730))
        if peg_date.year <= END_YEAR:
            procs.append({
                'patient_id': patient['patient_id'],
                'procedure_date': date_str(peg_date),
                'performed_datetime': datetime_str(peg_date),
                'display_name': 'Esophagogastroduodenoscopy, with PEG tube placement',
                'code': '43246',
                'code_system_name': 'CPT',
                'status': 'completed',
                'category': 'gastrointestinal',
                'source': pick_source(),
            })

    # Tracheostomy: rare, only for late-stage / respiratory-onset / fast progressors
    trach_probability = 0.4 if (onset_type == 'respiratory' or progression == 'fast') else 0.05
    if random.random() < trach_probability:
        trach_date = base + timedelta(days=random.randint(540, 1095))
        if trach_date.year <= END_YEAR:
            procs.append({
                'patient_id': patient['patient_id'],
                'procedure_date': date_str(trach_date),
                'performed_datetime': datetime_str(trach_date),
                'display_name': 'Tracheostomy, planned (separate procedure)',
                'code': '31600',
                'code_system_name': 'CPT',
                'status': 'completed',
                'category': 'respiratory',
                'source': pick_source(),
            })

    # Office visits — multiple over the course of care
    n_visits = random.randint(8, 20)
    for j in range(n_visits):
        pdate = base + timedelta(days=j * random.randint(45, 90))
        if pdate.year > END_YEAR:
            break
        visit_code = random.choice(['99213', '99214', '99215'])
        visit_name = next(p[1] for p in PROCEDURES if p[0] == visit_code)
        procs.append({
            'patient_id': patient['patient_id'],
            'procedure_date': date_str(pdate),
            'performed_datetime': datetime_str(pdate),
            'display_name': visit_name,
            'code': visit_code,
            'code_system_name': 'CPT',
            'status': 'completed',
            'category': 'office-visit',
            'source': pick_source(),
        })

    return procs


def make_encounters(patient):
    encs = []
    n = random.randint(8, 18)
    base = fake_date(START_YEAR, START_YEAR + 1)
    for j in range(n):
        edate = base + timedelta(days=j * random.randint(45, 100))
        if edate.year > END_YEAR:
            break
        cls, desc = random.choice(ENCOUNTER_CLASSES)
        encs.append({
            'patient_id': patient['patient_id'],
            'start_date': date_str(edate),
            'end_date': date_str(edate),
            'visit_type': desc,
            'class': cls,
            'reason': 'ALS follow-up' if 'ALS' in desc else 'Routine care',
            'location_or_provider': 'Demo Health System Clinic',
            'source': pick_source(),
        })
    return encs


def make_allergies(patient):
    if random.random() < 0.5:
        return []
    n = random.randint(1, 2)
    out = []
    for code, allergen, severity in random.sample(ALLERGIES, k=n):
        out.append({
            'patient_id': patient['patient_id'],
            'recorded_date': date_str(fake_date()),
            'allergen': allergen,
            'allergen_code': code,
            'category': 'medication' if allergen in ('Penicillin', 'Codeine') else 'food',
            'criticality': severity,
            'clinical_status': 'active',
            'reactions': random.choice(['rash', 'hives', 'itching', 'swelling']),
            'source': 'fhir',
        })
    return out


def make_immunizations(patient):
    n = random.randint(2, 5)
    out = []
    base = fake_date(START_YEAR, START_YEAR + 2)
    for k, (code, name) in enumerate(random.sample(IMMUNIZATIONS, k=min(n, len(IMMUNIZATIONS)))):
        idate = base + timedelta(days=k * random.randint(180, 400))
        if idate.year > END_YEAR:
            break
        out.append({
            'patient_id': patient['patient_id'],
            'occurrence_datetime': datetime_str(idate),
            'vaccine': name,
            'vaccine_code': code,
            'status': 'completed',
            'site': 'left deltoid',
            'route': 'IM',
            'dose_quantity': '0.5', 'dose_unit': 'mL',
            'source': 'fhir',
        })
    return out


def make_careplans(patient):
    n = random.randint(1, 3)
    out = []
    for title in random.sample(CARE_PLANS, k=n):
        start = fake_date(START_YEAR + 1, END_YEAR - 1)
        out.append({
            'patient_id': patient['patient_id'],
            'period_start': date_str(start),
            'period_end': date_str(start + timedelta(days=365)),
            'status': 'active',
            'title': title,
            'categories': 'comprehensive care',
            'description': f"Coordinated care plan: {title}",
            'activities': 'multidisciplinary team coordination',
            'note': '',
            'source': 'fhir',
        })
    return out


def make_diagnostic_reports(patient):
    n = random.randint(2, 8)
    out = []
    report_types = [
        ('11506-3', 'Provider-unspecified progress note'),
        ('51848-0', 'Evaluation note'),
        ('18746-5', 'Comprehensive history and physical note'),
        ('57133-1', 'Referral note'),
        ('11488-4', 'Consultation note'),
    ]
    base = fake_date(START_YEAR, START_YEAR + 1)
    for j in range(n):
        rdate = base + timedelta(days=j * random.randint(60, 200))
        if rdate.year > END_YEAR:
            break
        code, name = random.choice(report_types)
        out.append({
            'patient_id': patient['patient_id'],
            'effective_datetime': datetime_str(rdate),
            'issued': datetime_str(rdate),
            'display_name': name,
            'code': code,
            'status': 'final',
            'categories': 'clinical-note',
            'conclusion': 'Synthetic demonstration record. Not real clinical content.',
            'source': 'fhir',
        })
    return out


def make_goals(patient):
    n = random.randint(1, 3)
    out = []
    for desc in random.sample(GOALS, k=n):
        sdate = fake_date(START_YEAR + 1, END_YEAR - 1)
        out.append({
            'patient_id': patient['patient_id'],
            'start_date': date_str(sdate),
            'target_due_date': date_str(sdate + timedelta(days=365)),
            'description': desc,
            'lifecycle_status': 'active',
            'priority': 'high-priority',
            'note': '',
            'source': 'fhir',
        })
    return out


def make_documents(patient, n_docs):
    docs = []
    for j in range(n_docs):
        ddate = fake_date()
        doc_type = random.choices(
            ['ccda_xml', 'html_fragment', 'rtf_note', 'pdf'],
            weights=[15, 48, 34, 3]
        )[0]
        docs.append({
            'patient_id': patient['patient_id'],
            'document_uuid': fake_uuid(),
            'source_type': doc_type,
            'document_date': date_str(ddate),
            'word_count': str(random.randint(50, 2500)),
            'file': fake_uuid() + '.xml',
            'plain_text': (
                "[SYNTHETIC DEMO RECORD — not real clinical content]\n\n"
                "This is a placeholder narrative for demonstration purposes only.\n"
                "Patient seen in multidisciplinary ALS clinic for routine follow-up.\n"
                "Reviewed medications, current ALSFRS-R score, respiratory function,\n"
                "swallowing status, and home care needs. No acute concerns at this visit.\n"
                "Plan: continue current regimen, follow up in 3 months.\n\n"
                "(Generated by demo synthetic data tool. No real PHI.)"
            ),
        })
    return docs


# ============================================================
# MAIN
# ============================================================
def main():
    print("=" * 70)
    print("SYNTHETIC DATA GENERATOR — ARC Clinical Browser Demo")
    print("=" * 70)
    print(f"  Patients:      {N_PATIENTS}")
    print(f"  Random seed:   {SEED}")
    print(f"  Output:        {OUTPUT_FILE}")
    print()

    bundle = {
        'patients': [], 'documents': [],
        'encounters': [], 'problems': [], 'medications': [], 'procedures': [],
        'labs_vitals': [], 'notes': [],
        'allergies': [], 'immunizations': [], 'careplans': [],
        'diagnostic_reports': [], 'goals': [], 'care_teams': [], 'devices': [],
    }

    for i in range(N_PATIENTS):
        p = make_patient(i)
        n_docs = random.randint(40, 350)
        p['num_documents'] = n_docs

        bundle['patients'].append(p)
        bundle['documents'].extend(make_documents(p, n_docs))
        bundle['encounters'].extend(make_encounters(p))
        bundle['problems'].extend(make_conditions(p))
        bundle['medications'].extend(make_medications(p))
        bundle['procedures'].extend(make_procedures(p))
        bundle['labs_vitals'].extend(make_observations(p))
        bundle['allergies'].extend(make_allergies(p))
        bundle['immunizations'].extend(make_immunizations(p))
        bundle['careplans'].extend(make_careplans(p))
        bundle['diagnostic_reports'].extend(make_diagnostic_reports(p))
        bundle['goals'].extend(make_goals(p))

    # Set last document date for each patient
    docs_by_pid = {}
    for d in bundle['documents']:
        pid = d['patient_id']
        if pid not in docs_by_pid or d['document_date'] > docs_by_pid[pid]:
            docs_by_pid[pid] = d['document_date']
    for p in bundle['patients']:
        p['document_date'] = docs_by_pid.get(p['patient_id'], '')

    # Strip internal-only fields (those starting with _) before writing
    for p in bundle['patients']:
        for k in list(p.keys()):
            if k.startswith('_'):
                del p[k]

    # Write
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(bundle, f, ensure_ascii=False)

    print(f"  ✓ Wrote {OUTPUT_FILE}")
    print()
    print("  Bundle contents:")
    for k, v in bundle.items():
        print(f"    {k:25}: {len(v):>6,} records")

    print()
    print("=" * 70)
    print("DONE.")
    print()
    print("To view: open dashboard_demo.html in a browser, click")
    print(f"   '▲ Load demo data' and select {OUTPUT_FILE}")
    print("=" * 70)


if __name__ == "__main__":
    main()
