from flask import Flask, render_template, jsonify, request
from load_corpus import load_from_tsv

app = Flask(__name__)
corpus = load_from_tsv("data/corpus_annotated.tsv")

#página raiz
@app.route("/")
def index():
    #Lista dos dados do template
    sentences_data = []

    #Percorre cada item do dicionário de frases; sentence_id é o key do Dicionário, sentence_obj é o conteúdo
    for sentence_id, sentence_obj in corpus.sentences.items():
        
        #Gera o HTML formatado da frase atual a partir do objeto Sentence
        html_content = sentence_obj.render_html()
        
        #Cria uma tupla com os IDs e o HTML resultante
        data_tuple = (sentence_id, html_content)
        
        # Adiciona a tupla na lista de dados
        sentences_data.append(data_tuple)

    #Retorna a lista de dados para o Flask renderizar a partir do template
    return render_template("index.html", sentences=sentences_data)

@app.route("/sentence/<sid>")
def sentence_view(sid):
    #busca a frase pela ID no dicionário
    s = corpus.sentences.get(sid)
    #caso não encontrado, emite erro
    if not s:
        return "Frase não encontrada.", 404
    #senão, retorna a instância de Sentence
    return render_template("sentence.html", sid=sid, sentence=s)

@app.route("/api/word/<word_id>")
def api_word(word_id):
    w = corpus.words.get(word_id)
    if not w:
        return jsonify({"Erro":"Palavra não encontrada."}), 404
    return jsonify({
        "id": w.id,
        "form": w.form,
        "lemma": w.lemma,
        "pos": w.pos,
        "morph_class": w.morph_class,
        "gloss_pt": w.glosa_ptbr,
        "propriedades": w.propriedades,
        "sentence_id": w.sentence_id,
        "token_index": w.word_index
    })

@app.route("/word/<word_id>")
def word_details(word_id):
    #Busca a palavra no dicionário global do corpus
    w = corpus.words.get(word_id)
    
    #Se não achar, retorna erro
    if not w:
        return "Palavra não encontrada.", 404
    
    #Renderiza o novo template passando o objeto word
    return render_template("word.html", word=w)

@app.route("/search")
def word_search():
    q = request.args.get("q","").strip()
    results = []
    if q:
        for sid,s in corpus.sentences.items():
            for w in s.words:
                if q.lower() in (w.form or "").lower() or q.lower() in (w.lemma or "").lower():
                    results.append({"sid": sid, "snippet": s.render_html()})
                    break
    return render_template("search.html", q=q, results=results)

if __name__ == "__main__":
    app.run(debug=True)
