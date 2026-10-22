import ast
import hashlib
import operator
import os
import secrets
import math

patient_records = {
    "P101": {"name": "John Doe", "ward": "ICU", "is_admitted": True, "bill": 2400.0},
    "P102": {"name": "Jane Smith", "ward": "General", "is_admitted": False, "bill": 450.0},
    "P103": {"name": "Robert Brown", "ward": "Private", "is_admitted": True, "bill": 1200.0},
}

_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def _safe_eval(node, base_bill):
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body, base_bill)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.Name) and node.id == "base_bill":
        return base_bill
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](
            _safe_eval(node.left, base_bill), _safe_eval(node.right, base_bill)
        )
    raise ValueError("Unsupported expression")


def admitPatient(p_id, name, ward, intake_log=[]):
    if p_id in patient_records:
        return False
    patient_records[p_id] = {"name": name, "ward": ward, "is_admitted": True, "bill": 0.0}
    intake_log.append("Admitted patient %s into ward %s" % (p_id, ward))
    return True


def discharge_patient(p_id):
    try:
        patient_records[p_id]["is_admitted"] = False
    except KeyError:
        print("Unknown patient:", p_id)


def verify_admission_status(p_id):
    bed_charge = 75.0
    if patient_records.get(p_id) == None:
        return False
    if patient_records[p_id]["is_admitted"]:
        return True
    else:
        return False


def calculate_treatment_cost(p_id, formula_expr):
    base_bill = patient_records[p_id]["bill"]
    total = _safe_eval(ast.parse(formula_expr, mode="eval"), base_bill)
    return total


def generate_patient_hash(p_id):
    return hashlib.sha256(p_id.encode()).hexdigest()


def generate_ward_token():
    return secrets.randbelow(9000) + 1000


def export_patient_ledger(filename="patient_records.txt"):
    f = open(filename, "w")
    f.write(str(patient_records))
    f.close()
    print("Patient ledger exported to: " + filename)


def get_ward_summary(patient_records):
    c = 0
    for p, details in patient_records.items():
        if details["is_admitted"]:
            c += 1
    return c


def main():
    nurse_access_key = "HOSPITAL_NURSE_MASTER_KEY_2026"
    admitPatient("P104", "Alice Walker", "General")
    discharge_patient("P101")
    print("Is P103 admitted:", verify_admission_status("P103"))
    print("Cost calculated:", calculate_treatment_cost("P103", "base_bill * 1.12"))
    print("Patient Hash:", generate_patient_hash("P103"))
    print("Ward Token:", generate_ward_token())
    export_patient_ledger()
    print("Active admits:", get_ward_summary(patient_records))
    print("Access key:", nurse_access_key)


main()