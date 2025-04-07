import pandas as pd
from openai import OpenAI
import argparse
import matplotlib.pyplot as plt

# Initialize Groq OpenAI 
client = OpenAI(
    api_key="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",  # Replace with your actual key
    base_url="https://api.groq.com/openai/v1"
)

# Load comments from comments.csv 
def load_comments(file_path):
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith('.json'):
        df = pd.read_json(file_path)
    else:
        raise ValueError("Unsupported file format.")
    print(f"Loaded {len(df)} comments.")
    print("Sample preview:")
    print(df.head())
    return df


def analyze_comment(comment_text):
    try:
        prompt = (
            f"Analyze the following comment for offensive content:\n"
            f"Comment: \"{comment_text}\"\n"
            f"Determine:\n"
            f"1. Is it offensive? (yes or no)\n"
            f"2. Type of offense (e.g., hate speech, toxicity, profanity, harassment, none)\n"
            f"3. Short explanation.\n"
            f"Reply in this format:\n"
            f"Offensive: <yes/no>\n"
            f"Type: <offense_type>\n"
            f"Explanation: <short explanation>"
        )

        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
        )

        output = response.choices[0].message.content.strip()
        lines = output.split('\n')

        is_offensive = "yes" in lines[0].lower()
        offense_type = lines[1].split(":", 1)[1].strip() if len(lines) > 1 else "unknown"
        explanation = lines[2].split(":", 1)[1].strip() if len(lines) > 2 else "No explanation provided."

        return is_offensive, offense_type, explanation
    except Exception as e:
        print(f"Error analyzing comment: {e}")
        return False, "error", str(e)


def analyze_comments(df):
    df['is_offensive'] = False
    df['offense_type'] = ""
    df['explanation'] = ""

    for i, row in df.iterrows():
        text = row['comment_text']
        is_offensive, offense_type, explanation = analyze_comment(text)
        df.at[i, 'is_offensive'] = is_offensive
        df.at[i, 'offense_type'] = offense_type
        df.at[i, 'explanation'] = explanation
        print(f"[{i+1}/{len(df)}] Done")  
    return df


def print_summary(df):
    offensive_df = df[df['is_offensive'] == True]
    print(f"\nTotal offensive comments: {len(offensive_df)}")

    breakdown = offensive_df['offense_type'].value_counts()
    print("\nOffense Type Breakdown:")
    print(breakdown)

    print("\nTop 5 Offensive Comments:")
    print(offensive_df[['comment_text', 'offense_type', 'explanation']].head(5))

# Plot chart
def plot_offense_distribution(df):
    offensive_df = df[df['is_offensive']]
    breakdown = offensive_df['offense_type'].value_counts()
    if not breakdown.empty:
        breakdown.plot(kind='pie', autopct='%1.1f%%', figsize=(6, 6), title="Offense Type Distribution")
        plt.ylabel("")
        plt.tight_layout()
        plt.show()
    else:
        print("No offensive comments to plot.")

# Main Function
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Input file path (CSV or JSON)")
    parser.add_argument("--output", default="analyzed_comments.csv", help="Output file path")
    args = parser.parse_args()

    df = load_comments(args.input)
    analyzed_df = analyze_comments(df)
    analyzed_df.to_csv(args.output, index=False)

    print_summary(analyzed_df)
    plot_offense_distribution(analyzed_df)

if __name__ == "__main__":
    main()

