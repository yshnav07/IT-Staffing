def store_feedback(candidate_id, ai_output, human_output):
    feedback_data = {
        "candidate_id": candidate_id,
        "ai_output": ai_output,
        "human_corrected": human_output
    }
    collection.insert_one(feedback_data)