import re
import json
import os
from datetime import datetime

# File to store evaluations
EVALUATIONS_FILE = "evaluations.json"

# Load evaluations from file
def load_evaluations():
    if os.path.exists(EVALUATIONS_FILE):
        with open(EVALUATIONS_FILE, 'r') as f:
            return json.load(f)
    return {}

# Save evaluations to file
def save_evaluations(evaluations):
    with open(EVALUATIONS_FILE, 'w') as f:
        json.dump(evaluations, f, indent=4)

# Evaluate performance based on rules
def evaluate_performance(productivity, punctuality, teamwork, completion_rate):
    # Calculate average score
    avg_score = (productivity + punctuality + teamwork + completion_rate) / 4

    # Rule-based evaluation
    if avg_score >= 90:
        rating = "Excellent"
        feedback = "Outstanding performance across all metrics!"
    elif avg_score >= 75:
        rating = "Good"
        feedback = "Solid performance, keep up the great work!"
    elif avg_score >= 60:
        rating = "Average"
        feedback = "Performance is satisfactory but could improve in some areas."
    else:
        rating = "Needs Improvement"
        feedback = "Consider focusing on key areas like productivity or teamwork."

    return {
        "average_score": round(avg_score, 2),
        "rating": rating,
        "feedback": feedback,
        "metrics": {
            "productivity": productivity,
            "punctuality": punctuality,
            "teamwork": teamwork,
            "completion_rate": completion_rate
        },
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

# Process user input
def respond(message):
    message = message.lower()

    # Evaluate command
    if re.search(r'\bevaluate\b', message):
        match = re.match(r'evaluate\s+(\w+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)', message)
        if match:
            name = match.group(1)
            try:
                productivity = int(match.group(2))
                punctuality = int(match.group(3))
                teamwork = int(match.group(4))
                completion_rate = int(match.group(5))
                
                # Validate inputs
                if all(0 <= x <= 100 for x in [productivity, punctuality, teamwork, completion_rate]):
                    result = evaluate_performance(productivity, punctuality, teamwork, completion_rate)
                    
                    # Save evaluation
                    evaluations = load_evaluations()
                    if name not in evaluations:
                        evaluations[name] = []
                    evaluations[name].append(result)
                    save_evaluations(evaluations)
                    
                    return (f"Evaluation for {name}:\n"
                            f"Rating: {result['rating']}\n"
                            f"Average Score: {result['average_score']}\n"
                            f"Feedback: {result['feedback']}\n"
                            f"Metrics: Productivity={productivity}, Punctuality={punctuality}, "
                            f"Teamwork={teamwork}, Completion Rate={completion_rate}")
                else:
                    return "Please provide metrics between 0 and 100."
            except ValueError:
                return "Invalid numbers. Use format: evaluate <name> <productivity> <punctuality> <teamwork> <completion_rate>"
        return "Use format: evaluate <name> <productivity> <punctuality> <teamwork> <completion_rate> (all 0-100)"

    # View evaluations
    elif re.search(r'\bview\b', message):
        match = re.match(r'view\s+(\w+)', message)
        if match:
            name = match.group(1)
            evaluations = load_evaluations()
            if name in evaluations and evaluations[name]:
                response = f"Evaluations for {name}:\n"
                for i, eval in enumerate(evaluations[name], 1):
                    response += (f"\nEvaluation {i} ({eval['timestamp']}):\n"
                                 f"Rating: {eval['rating']}\n"
                                 f"Average Score: {eval['average_score']}\n"
                                 f"Feedback: {eval['feedback']}\n"
                                 f"Metrics: Productivity={eval['metrics']['productivity']}, "
                                 f"Punctuality={eval['metrics']['punctuality']}, "
                                 f"Teamwork={eval['metrics']['teamwork']}, "
                                 f"Completion Rate={eval['metrics']['completion_rate']}\n")
                return response
            return f"No evaluations found for {name}."
        return "Use format: view <name>"

    # Exit
    elif re.search(r'\b(exit|bye|quit)\b', message):
        return "Thank you for using the Performance Evaluation System! Goodbye."

    # Default
    else:
        return "Commands: 'evaluate <name> <productivity> <punctuality> <teamwork> <completion_rate>' or 'view <name>' or 'exit'"

# Main execution
def main():
    print("Employee Performance Evaluation System: Type 'exit' to quit.")
    print("Commands: 'evaluate <name> <productivity> <punctuality> <teamwork> <completion_rate>' or 'view <name>'")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'bye', 'quit']:
            print("System: Goodbye!")
            break
        response = respond(user_input)
        print(f"System: {response}")

if __name__ == "__main__":
    main()