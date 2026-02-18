from uuid import uuid4


def start_training_job(user_id: str, dataset_reference: str) -> dict:
    return {
        "job_id": str(uuid4()),
        "user_id": user_id,
        "dataset_reference": dataset_reference,
        "status": "training_started",
    }
