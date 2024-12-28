from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

# البيانات التدريبية (هذه مجرد مثال، يمكنك استخدام بياناتك الخاصة)
texts = ["example text data", "more example text"]
labels = [0, 1]

# إنشاء CountVectorizer وتدريبه
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)

# تدريب النموذج
model = LogisticRegression()
model.fit(X, labels)

# حفظ النموذج
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

# حفظ CountVectorizer
with open('vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)
