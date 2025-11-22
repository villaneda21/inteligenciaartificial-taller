from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

frases_motivadoras = [
    "El éxito es la suma de pequeños esfuerzos repetidos día tras día.",
    "No cuentes los días, haz que los días cuenten.",
    "La única forma de hacer un gran trabajo es amar lo que haces.",
    "Cree en ti mismo y todo será posible.",
    "El fracaso es solo la oportunidad de comenzar de nuevo de forma más inteligente.",
    "Tu única limitación eres tú mismo.",
    "Los sueños no funcionan a menos que tú lo hagas.",
    "No esperes la oportunidad, créala.",
    "La motivación es lo que te pone en marcha, el hábito es lo que te mantiene.",
    "Cada día es una nueva oportunidad para cambiar tu vida.",
    "El éxito no es el final, el fracaso no es fatal: es el coraje para continuar lo que cuenta.",
    "Haz hoy lo que otros no quieren, haz mañana lo que otros no pueden.",
    "La diferencia entre lo imposible y lo posible está en tu determinación.",
    "No te rindas, el comienzo es siempre lo más difícil.",
    "La disciplina es el puente entre metas y logros.",
    "El mejor momento para plantar un árbol fue hace 20 años. El segundo mejor momento es ahora.",
    "No dejes que lo que no puedes hacer interfiera con lo que puedes hacer.",
    "El único lugar donde el éxito viene antes que el trabajo es en el diccionario.",
    "Si puedes soñarlo, puedes lograrlo.",
    "La vida es 10% lo que te sucede y 90% cómo reaccionas ante ello."
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/frase')
def obtener_frase():
    frase_aleatoria = random.choice(frases_motivadoras)
    return jsonify({'frase': frase_aleatoria})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
