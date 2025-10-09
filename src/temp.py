# Training data
training_data = [
    ("A great game", "Sports"),
    ("The election was over", "Not sports"),
    ("Very clean match", "Sports"),
    ("A close but forgettable game", "Sports"),
    ("There was election", "Not sports")
]

# Basic tokenizer: lowercase and split by space
def tokenize(text):
    return text.lower().split()

# Training function
def train_naive_bayes(data):
    class_word_counts = {}
    class_counts = {}
    vocabulary = set()

    for text, label in data:
        words = tokenize(text)
        if label not in class_word_counts:
            class_word_counts[label] = {}
            class_counts[label] = 0
        class_counts[label] += 1
        for word in words:
            vocabulary.add(word)
            if word not in class_word_counts[label]:
                class_word_counts[label][word] = 0
            class_word_counts[label][word] += 1

    return class_word_counts, class_counts, list(vocabulary)

# Prediction function
def predict(text, class_word_counts, class_counts, vocabulary):
    words = tokenize(text)
    total_docs = sum(class_counts.values())
    results = {}

    for label in class_counts:
        prob = class_counts[label] / total_docs
        total_words = sum(class_word_counts[label].values())
        for word in words:
            word_freq = class_word_counts[label].get(word, 0) + 1  # Laplace smoothing
            prob *= word_freq / (total_words + len(vocabulary))
        results[label] = prob

    # Return label with highest probability
    return max(results, key=results.get)

# Train model
class_word_counts, class_counts, vocabulary = train_naive_bayes(training_data)

# Test data
test_sentences = [
    "A very close game"
]

# Predict and print results
for sentence in test_sentences:
    label = predict(sentence, class_word_counts, class_counts, vocabulary)
    print(f"'{sentence}' => {label}")
