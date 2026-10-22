"""Hospital patient records and admission manager."""

import ast
import hashlib
import operator
import os
import secrets

patient_records = {
    "P101": {
        "name": "John Doe", "ward": "ICU", "is_admitted": True, "bill": 2400.0
    },
    "P102": {
        "name": "Jane Smith", "ward": "General", "is_admitted": False,
        "bill": 450.0
    },
    "P103": {
        "name": "Robert Brown", "ward": "Private", "is_admitted": True,
        "bill": 1200.0
    },
}

_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def _safe_eval(node, base_bill):
    """Evaluate a parsed arithmetic expression using only + - * / ,
    numbers and the name ``base_bill``. Anything else is rejected."""
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body, base_bill)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.Name) and node.id == "base_bill":
        return base_bill
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](
            _safe_eval(node.left, base_bill),
            _safe_eval(node.right, base_bill),
        )
    raise ValueError("Unsupported expression")


def admit_patient(p_id, name, ward, intake_log=None):
    """Admit a new patient. Return False if the ID already exists."""
    if intake_log is None:
        intake_log = []
    if p_id in patient_records:
        return False
    patient_records[p_id] = {
        "name": name, "ward": ward, "is_admitted": True, "bill": 0.0
    }
    intake_log.append(f"Admitted patient {p_id} into ward {ward}")
    return True


def discharge_patient(p_id):
    """Mark a patient as discharged. Return False if the ID is unknown."""
    if p_id not in patient_records:
        print("Unknown patient:", p_id)
        return False
    patient_records[p_id]["is_admitted"] = False
    return True


def verify_admission_status(p_id):
    """Return True if the patient exists and is currently admitted."""
    record = patient_records.get(p_id)
    return record is not None and record["is_admitted"]


def calculate_treatment_cost(p_id, formula_expr):
    """Apply a simple arithmetic formula to the patient's base bill."""
    base_bill = patient_records[p_id]["bill"]
    total = _safe_eval(ast.parse(formula_expr, mode="eval"), base_bill)
    return round(total, 2)


def generate_patient_hash(p_id):
    """Return the SHA-256 hex digest of a patient ID."""
    return hashlib.sha256(p_id.encode()).hexdigest()


def generate_ward_token():
    """Return a random 4-digit ward token (1000-9999)."""
    return secrets.randbelow(9000) + 1000


def export_patient_ledger(filename="patient_records.txt"):
    """Write all patient records to a text file."""
    with open(filename, "w", encoding="utf-8") as ledger_file:
        ledger_file.write(str(patient_records))
    print("Patient ledger exported to: " + filename)


def get_ward_summary(records):
    """Return the number of currently admitted patients."""
    return sum(1 for details in records.values() if details["is_admitted"])


def main():
    """Run a short demonstration of the system."""
    nurse_access_key = os.environ.get("NURSE_ACCESS_KEY")
    admit_patient("P104", "Alice Walker", "General")
    discharge_patient("P101")
    print("Is P103 admitted:", verify_admission_status("P103"))
    print("Cost calculated:",
          calculate_treatment_cost("P103", "base_bill * 1.12"))
    print("Patient Hash:", generate_patient_hash("P103"))
    print("Ward Token:", generate_ward_token())
    export_patient_ledger()
    print("Active admits:", get_ward_summary(patient_records))
    print("Access key loaded:", nurse_access_key is not None)


if __name__ == "__main__":
    main()