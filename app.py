import pandas as pd
import numpy as np
from flask import Flask, request, render_template_string
from tensorflow.keras.models import load_model

# Load trained model
model = load_model("eeg_model.h5")

app = Flask(__name__)

html = """
<h1>EEG Detection System</h1>
<form method="POST" enctype="multipart/form-data">
<input type="file" name="file">
<button type="submit">Predict</button>
</form>
{% if result %}
<h2>{{ result }}</h2>
{% endif %}
"""

@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        file = request.files['file']
        data = pd.read_csv(file)

        data = data.select_dtypes(include=[np.number]).fillna(0)
        values = data.iloc[0].values

        REQUIRED = model.input_shape[1]

        if len(values) < REQUIRED:
            values = np.pad(values, (0, REQUIRED - len(values)))
        else:
            values = values[:REQUIRED]

        values = values.reshape(1, REQUIRED, 1)

        prediction = model.predict(values)
        pred = np.argmax(prediction)

        if pred == 0:
            result = "Normal"
        elif pred == 1:
            result = "Stress"
        else:
            result = "Epilepsy"

        return render_template_string(html, result=result)

    return render_template_string(html)
if __name__ == '__main__':
    app.run(debug=True)