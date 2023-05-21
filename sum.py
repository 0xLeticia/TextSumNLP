import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from langdetect import detect
from colorama import Fore, Style

def summarize_text(text, lang='en', summarize_by_language=False, num_sentences=3):
    if summarize_by_language:
        try:
            lang = detect(text)
        except:
            print("Could not detect language automatically.")
            lang = input("Please enter your preferred language (e.g. en, pt): ")
    
    if lang == 'pt':
        sentences = sent_tokenize(text, language='portuguese')
        stop_words = stopwords.words('portuguese')
    else:
        sentences = sent_tokenize(text)
        stop_words = stopwords.words('english')
    
    sentence_scores = []
    for sentence in sentences:
        words = word_tokenize(sentence)
        filtered_words = [word for word in words if word.casefold() not in stop_words]
        word_frequencies = {}
        for word in filtered_words:
            if word not in word_frequencies:
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
        sentence_score = sum(word_frequencies.values())
        sentence_scores.append((sentence, sentence_score))
    
    sorted_sentence_scores = sorted(sentence_scores, key=lambda x: x[1], reverse=True)
    summary_sentences = [sentence for sentence, score in sorted_sentence_scores[:num_sentences]]
    summary = ' '.join(summary_sentences)
    
    num_original_words = len(word_tokenize(text))
    num_summary_words = len(word_tokenize(summary))
    percent_reduction = (num_original_words - num_summary_words) / num_original_words * 100
    
    return summary, num_original_words, num_summary_words, percent_reduction

text = input("Enter text to summarize: ")
summarize_by_language_input = input("Summarize by language? (y/n): ")
if summarize_by_language_input.lower() == 'y':
    summarize_by_language = True
else:
    summarize_by_language = False

if summarize_by_language:
    summary, num_original_words, num_summary_words, percent_reduction = summarize_text(text, summarize_by_language=True)
else:
    lang_pref = input("Enter language preference (en/pt): ")
    num_sentences_input = input("Enter number of sentences for summary (default is 3): ")
    if num_sentences_input.isdigit():
        num_sentences = int(num_sentences_input)
    else:
        num_sentences = 3
    summary, num_original_words, num_summary_words, percent_reduction = summarize_text(text, lang=lang_pref, num_sentences=num_sentences)

print(Fore.GREEN + "Summary:")
print(summary)
print(Style.RESET_ALL)

print(Fore.BLUE + "Statistics of sum:")
print(f"Number of original words: {num_original_words}")
print(f"Number of summary words: {num_summary_words}")
print(f"Percentage reduction: {percent_reduction:.2f}%")
print(Style.RESET_ALL)
